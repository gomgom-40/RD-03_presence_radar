# 🎯 RD-03 Smart Presence Radar for ESPHome

[![ESPHome](https://img.shields.io/badge/ESPHome-Compatible-blue.svg)](https://esphome.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Made in Egypt](https://img.shields.io/badge/Made%20in-Egypt%20🇪🇬-green.svg)](https://github.com/gomgom-40)

> Transform a cheap RD-03 radar sensor into an intelligent presence detection system with automated lighting control

## 📖 Overview

This project converts the basic **Ai-Thinker RD-03** (24GHz mmWave radar) from a simple ON/OFF sensor into a **smart presence detection system** with:

- ✅ **Motion-based entry detection** - Triggers on actual movement, not static objects
- ✅ **Intelligent timeout system** - Fast exit (15s no-target) + Safety timeout (configurable)
- ✅ **Multiple control modes** - Auto, Manual, Force ON/OFF
- ✅ **Distance tracking** - Real-time target distance measurement
- ✅ **Watchdog protection** - Auto-recovery from radar hang
- ✅ **Edge case handling** - Manual override reset for false positives

**Perfect for:** Bathrooms, closets, storage rooms, garages - any small space (tested in 2m bathroom)

---

## 🎥 Demo

![RD-03 Smart Presence Radar Demo](https://raw.githubusercontent.com/gomgom-40/RD-03_presence_radar/main/rd03_presence_demo.gif)

Short animated demo showing real-time entry/exit detection in the bathroom.

---

## 🛠️ Hardware Requirements

### Required Components

| Component | Specification | Price (approx) |
|-----------|---------------|----------------|
| **Radar Sensor** | Ai-Thinker RD-03 (24GHz mmWave) | $3-5 |
| **Microcontroller** | ESP32-DevKit or similar | $4-6 |
| **Relay Module** | 1-channel 5V relay | $1-2 |
| **Power Supply** | 5V/2A USB adapter | $2-3 |
| **Optional** | Wall switch (manual override) | $1-2 |

**Total Cost:** ~$15-20 (vs $50+ commercial solutions)

### Wiring Diagram

```
ESP32          RD-03 Radar       Relay          Light
-----          -----------       -----          -----
GPIO17 ────── TX                
GPIO16 ────── RX                
GPIO19 ──────────────────────── IN  ────────── Load
GPIO18 ────── Wall Switch (optional)
GND    ────── GND ──────────────GND
5V     ────── VCC ──────────────VCC
```

---

## 📦 Installation

### Method 1: ESPHome Dashboard (Recommended)

1. **Copy the configuration:**
   ```bash
   # Download the latest config
   wget https://raw.githubusercontent.com/gomgom-40/RD-03_presence_radar/main/bathroom_radar_production.yaml
   ```

2. **Update WiFi credentials:**
   ```yaml
   wifi:
     ssid: "YOUR_WIFI_SSID"
     password: "YOUR_WIFI_PASSWORD"
   ```

3. **Flash to ESP32:**
   - Open ESPHome Dashboard
   - Create new device
   - Paste configuration
   - Click "Install" → "Plug into this computer"

### Method 2: Command Line

```bash
# Install ESPHome
pip3 install esphome

# Compile and upload
esphome run bathroom_radar_production.yaml
```

---

## ⚙️ Configuration

### Adjustable Parameters

All settings are exposed to Home Assistant and can be changed without reflashing:

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| **Minimum Range** | 20 cm | 10-300 cm | Ignore objects closer than this |
| **Maximum Range** | 500 cm | 50-600 cm | Ignore objects farther than this |
| **Activity Level** | 3 | 1-5 | Hold time multiplier (1=sensitive, 5=relaxed) |
| **Max Absence Time** | 5 min | 1-120 min | Safety timeout for auto-off |

### How It Works

#### 1. **Entry Detection** (Motion-based)
```yaml
# Requires actual movement to trigger
Threshold: ≥2cm distance change
Hits required: 1 (immediate response)
Result: Light turns ON
```

#### 2. **Presence Maintenance**
```yaml
# Any valid radar reading extends the timer
Valid range: 20-500 cm (configurable)
Activity timer: Resets on each detection
Hold time: Activity_Level × 10 seconds
```

#### 3. **Exit Detection** (Two-tier system)
```yaml
# Fast Exit (15 seconds)
Trigger: No target detected for 15s
Action: Turn OFF immediately

# Safety Timeout (5 minutes default)
Trigger: No activity for Max_Absence_Time
Action: Force OFF (emergency backup)
```

---

## 🎛️ Control Modes

### 1. **Automatic Mode** (Default)
- Radar controls the light automatically
- Motion triggers ON
- No-target triggers OFF (15s delay)

### 2. **Manual Mode** (Wall Switch)
- Physical switch connected to GPIO18
- Overrides all automation
- Light stays ON until switch is turned OFF

### 3. **Force ON** (Home Assistant)
- Overrides radar and wall switch
- Light stays ON indefinitely
- Useful for cleaning/maintenance

### 4. **Force OFF** (Home Assistant)
- Overrides everything
- Light stays OFF
- Useful for energy saving

---

## 🐛 Troubleshooting

### Light doesn't turn on

**Check:**
1. Is radar receiving power? (Red LED on RD-03)
2. Are UART connections correct? (TX↔RX crossed)
3. Check ESPHome logs: `esphome logs bathroom_radar.yaml`
4. Verify distance readings appear in Home Assistant

### False triggers (ghost presence)

**Solution:**
- This is a rare edge case (2 occurrences in 3 weeks)
- Already handled by `manual_off_recent` reset logic
- If persistent: Reduce `Maximum Range` from 500→250 cm

### Light turns off while occupied

**Fixes:**
1. Increase `Activity Level` from 3→4 or 5
2. Check if person is in Min/Max range (adjust if needed)
3. Verify radar has clear line-of-sight (no obstructions)

### Radar stops responding

**Auto-recovery enabled:**
- Watchdog resets radar after 90s silence
- ESP restarts after 12h complete silence
- Check Diagnostics sensor for status

---

## 📊 Sensors Exposed

### Home Assistant Entities

```yaml
# Binary Sensors
binary_sensor.smart_presence           # Main presence state
binary_sensor.wall_switch_manual       # Physical switch state

# Sensors
sensor.target_distance                 # Real-time distance (cm)

# Text Sensors  
sensor.last_presence_timestamp         # When was last detection
sensor.diagnostics                     # System health status

# Switches
switch.bathroom_light_force_on         # Override to ON
switch.bathroom_light_force_off        # Override to OFF
switch.bathroom_light                  # Main relay (نور الحمام)

# Number Inputs
number.minimum_range                   # Min detection range
number.maximum_range                   # Max detection range  
number.activity_level                  # Sensitivity (1-5)
number.maximum_absence_time            # Safety timeout (min)
```

---

## 🔬 Technical Details

### Algorithm Overview

```cpp
// Entry Detection (presence_active == false)
1. Extract distance from UART "Range XXX" message
2. Validate: within min_range to max_range
3. Detect motion: distance changed ≥2cm from last reading
4. Trigger: 1 motion hit = presence activated

// Maintenance Mode (presence_active == true)  
1. Any valid reading → reset activity timer
2. Invalid/no reading → start no_target_since timer
3. Continue until Fast Exit or Safety timeout

// Exit Detection
Fast Exit: no_target_since > 15 seconds → OFF
Safety: last_activity > max_absence_time → OFF
```

### Edge Cases Handled

1. **Manual Override Reset** - Prevents false re-trigger after manual turn-off
2. **Invalid Jump Protection** - Ignores jumps from >100cm to <10cm
3. **Stale Data Clearing** - UART buffer auto-clears after 30s inactivity
4. **Watchdog Recovery** - Auto-resets radar on communication failure

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Keep changes minimal and focused
- Preserve tested logic (3+ weeks bathroom testing)
- Add comments for complex sections
- Test in real hardware before submitting

---

## 📜 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **ESPHome Team** - For the amazing platform
- **Ai-Thinker** - For the affordable RD-03 radar hardware
- **Home Assistant Community** - For inspiration and support
- **Egyptian Engineering** - For turning cheap hardware into smart solutions 🇪🇬

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/gomgom-40/RD-03_presence_radar/issues)
- **Discussions:** [GitHub Discussions](https://github.com/gomgom-40/RD-03_presence_radar/discussions)
- **Updates:** Watch this repo for new features

---

## 🌟 Show Your Support

If this project helped you, please ⭐ **star this repository** and share it with others!

---

## 📈 Roadmap

- [x] Basic presence detection
- [x] Motion-based entry detection
- [x] Multi-mode control system
- [x] Edge case handling
- [ ] Multi-zone support (future hardware upgrade)
- [ ] Energy consumption tracking
- [ ] Mobile app for configuration
- [ ] Pre-compiled firmware releases

---

**Made with ❤️ in Egypt 🇪🇬**
**By the hands of : Mohamed Eid**

*Transforming budget hardware into premium solutions through software excellence*
