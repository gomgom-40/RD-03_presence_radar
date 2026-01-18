# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-19

### 🎉 Initial Stable Release

Production-ready version tested for 3+ weeks in real bathroom environment (2m²).

### ✨ Features

#### Core Functionality
- **Motion-based entry detection** - Requires 2cm distance change to trigger
- **Intelligent two-tier timeout system**
  - Fast Exit: 15 seconds without target detection
  - Safety Timeout: Configurable max absence time (default 5 minutes)
- **Real-time distance tracking** - Monitors target distance in cm
- **Multiple control modes**
  - Automatic (radar-controlled)
  - Manual (wall switch override)
  - Force ON/OFF (Home Assistant override)

#### Smart Detection Algorithm
- **Entry logic** - Motion-based with 1-hit threshold
- **Maintenance logic** - Any valid reading extends timer
- **Exit logic** - Dual timeout system prevents false positives
- **Range validation** - Configurable min/max range with jump protection

#### Reliability Features
- **Watchdog protection** - Auto-recovers from radar hang
  - Soft reset: 90-180 seconds silence
  - Hard reset: ESP restart after 12 hours
- **Edge case handling**
  - Manual override reset (fixes false positives after manual turn-off)
  - Invalid jump protection (>100cm → <10cm rejected)
  - Stale data clearing (UART buffer auto-clears)

#### User Configuration
All parameters adjustable via Home Assistant:
- Minimum Range: 10-300 cm (default 20cm)
- Maximum Range: 50-600 cm (default 500cm)
- Activity Level: 1-5 sensitivity (default 3)
- Max Absence Time: 1-120 minutes (default 5min)

#### Exposed Entities
- **Binary Sensors:** Smart Presence, Wall Switch
- **Sensors:** Target Distance, Diagnostics
- **Switches:** Bathroom Light (نور الحمام), Force ON/OFF
- **Numbers:** Range controls, Activity level, Timeout

### 📚 Documentation
- Comprehensive README with installation guide
- Wiring diagrams and hardware requirements
- Troubleshooting section
- Algorithm explanation
- Contributing guidelines

### 🐛 Known Issues
- **Rare false positives** (2 occurrences in 3 weeks)
  - Caused by: Radar reflections from mirrors/tiles
  - Mitigation: Manual override reset (`manual_off_recent` flag)
  - Workaround: Reduce max_range from 500→250cm if persistent

### 🔧 Technical Details
- **Platform:** ESPHome + ESP32
- **Sensor:** Ai-Thinker RD-03 (24GHz mmWave)
- **UART:** 115200 baud, 256 byte buffer
- **Update rate:** 45ms distance sensor, 30ms UART parser
- **Framework:** ESP-IDF

### 🎯 Tested Environment
- **Space:** 2m × 2m bathroom
- **Duration:** 3+ weeks continuous operation
- **Scenarios:** 
  - Daily use (multiple entries/exits)
  - Manual overrides (wall switch + Alexa)
  - Edge cases (false positives handled)
- **Reliability:** 99%+ uptime with auto-recovery

---

## [Unreleased]

### 🚧 Planned Features
- [ ] Multi-zone detection (requires hardware upgrade)
- [ ] Energy consumption tracking
- [ ] Pre-compiled firmware releases
- [ ] Mobile app for configuration
- [ ] Advanced statistics (daily patterns, usage analytics)

### 🔍 Under Consideration
- [ ] Machine learning for adaptive timeouts
- [ ] Integration with other sensors (temperature, humidity)
- [ ] Voice feedback support
- [ ] Scheduled presence modes

---

## Version History Summary

| Version | Date | Status | Notes |
|---------|------|--------|-------|
| 1.0.0 | 2025-01-19 | ✅ Stable | Production-ready, 3+ weeks tested |
| 0.x | 2024-2025 | 🧪 Beta | Development and testing phase |

---

## Migration Guide

### From Beta (0.x) to v1.0.0

**Breaking Changes:**
- None - fully backward compatible

**New Features:**
- Enhanced documentation
- Standardized entity names
- Improved code organization (comments, constants)

**Recommended Actions:**
1. Backup current configuration
2. Review new README for best practices
3. Consider adjusting max_range based on room size
4. Test in safe hours (not during peak usage)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to propose changes or report issues.

---

**Format:**
- ✨ Features
- 🐛 Bug Fixes
- 📚 Documentation
- 🔧 Technical/Internal
- 🚨 Breaking Changes
- 🎉 Major Releases
