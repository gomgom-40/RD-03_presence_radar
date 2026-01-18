# Contributing to RD-03 Smart Presence Radar

First off, thank you for considering contributing to this project! 🙏

## 🎯 Philosophy

This project follows the **"Be Water"** principle:
- **Simple solutions** over complex ones
- **Tested logic** over theoretical perfection
- **Real-world experience** over assumptions
- **Cultural identity** preserved (e.g., "نور الحمام")

## 🚀 How to Contribute

### Reporting Bugs

**Before submitting:**
1. Check [existing issues](https://github.com/gomgom-40/RD-03_presence_radar/issues)
2. Test with latest version
3. Collect ESPHome logs

**Bug report should include:**
```markdown
**Hardware:**
- ESP32 model:
- RD-03 version:
- Power supply:

**Software:**
- ESPHome version:
- Home Assistant version (if applicable):

**Configuration:**
- Min range:
- Max range:
- Activity level:

**Behavior:**
- Expected:
- Actual:
- Frequency: (always/sometimes/rare)

**Logs:**
```esphome logs output here```
```

### Suggesting Features

**Feature requests welcome if:**
- ✅ Based on real use case
- ✅ Compatible with budget hardware
- ✅ Don't break existing functionality
- ✅ Include implementation idea

**Not suitable:**
- ❌ Require expensive hardware upgrade
- ❌ Over-engineering for edge cases
- ❌ Breaking changes without strong justification

### Code Contributions

#### Setup Development Environment

```bash
# Clone repo
git clone https://github.com/gomgom-40/RD-03_presence_radar.git
cd RD-03_presence_radar

# Install ESPHome
pip3 install esphome

# Test compilation
esphome compile bathroom_radar_production.yaml
```

#### Coding Standards

**YAML:**
```yaml
# ✅ Good: Clear comments, organized sections
# Motion detection parameters
const uint8_t MOTION_HITS_REQUIRED = 1;  # Single change triggers

# ❌ Bad: Magic numbers without explanation
if (hits >= 1)
```

**C++ (Lambda):**
```cpp
// ✅ Good: Descriptive names, clear intent
const float MOTION_CHANGE_THRESHOLD = 2.0f;  // cm

// ❌ Bad: Unclear abbreviations
const float MCT = 2.0f;
```

**Comments:**
```cpp
// ✅ Good: Explain WHY
// Reset motion detection on invalid readings to prevent false triggers

// ❌ Bad: Explain WHAT (code already says this)
motion_hits = 0;  // Set motion_hits to zero
```

#### Testing Requirements

**Before submitting PR:**
1. ✅ Code compiles without errors/warnings
2. ✅ Tested on real hardware (minimum 24 hours)
3. ✅ No regression in existing functionality
4. ✅ Edge cases considered (manual override, force modes, etc.)

**Test checklist:**
```markdown
- [ ] Normal entry/exit works
- [ ] Manual wall switch override works
- [ ] Force ON/OFF modes work
- [ ] False positive handling (if changed detection logic)
- [ ] Watchdog recovery (if changed UART/radar code)
- [ ] Configuration changes persist across reboot
```

#### Pull Request Process

1. **Branch naming:**
   ```bash
   feature/add-multi-zone-support
   fix/watchdog-timeout-issue
   docs/improve-installation-guide
   ```

2. **Commit messages:**
   ```bash
   # ✅ Good
   git commit -m "fix: prevent false triggers after manual off"
   
   # ❌ Bad
   git commit -m "fixed bug"
   ```

3. **PR description template:**
   ```markdown
   ## What changed?
   Brief description
   
   ## Why?
   Real-world problem this solves
   
   ## Testing
   How was this tested?
   
   ## Checklist
   - [ ] Code compiles
   - [ ] Tested on hardware
   - [ ] Documentation updated
   - [ ] No breaking changes (or clearly marked)
   ```

## 🎨 Project Structure

```
RD-03_presence_radar/
├── README.md                          # Main documentation
├── CONTRIBUTING.md                    # This file
├── LICENSE                            # MIT License
├── bathroom_radar_production.yaml    # Main ESPHome config (stable)
├── examples/
│   ├── basic_setup.yaml              # Minimal working example
│   ├── advanced_features.yaml        # All features enabled
│   └── debugging.yaml                # Debug logging enabled
├── docs/
│   ├── hardware_guide.md             # Wiring diagrams
│   ├── troubleshooting.md            # Common issues
│   ├── algorithm_explained.md        # Technical deep-dive
│   └── changelog.md                  # Version history
└── .github/
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   └── feature_request.md
    └── workflows/
        └── esphome_compile.yml       # CI/CD
```

## 🐛 Debugging Tips

### Enable Debug Logging

```yaml
logger:
  level: DEBUG
  logs:
    sensor: DEBUG
    text_sensor: DEBUG
```

### Monitor UART Traffic

```yaml
uart:
  debug:
    direction: BOTH
    dummy_receiver: false
    after:
      delimiter: "\n"
    sequence:
      - lambda: UARTDebug::log_hex(direction, bytes, ':');
```

### Common Issues During Development

**Issue:** Changes not taking effect
**Solution:** Full reflash instead of OTA
```bash
esphome run bathroom_radar.yaml --device /dev/ttyUSB0
```

**Issue:** Radar not responding
**Solution:** Check baudrate (115200 for RD-03, not 256000)

**Issue:** False positives during testing
**Solution:** Reduce max_range to room size (e.g., 250cm for 2m bathroom)

## 📚 Resources

- [ESPHome Documentation](https://esphome.io/)
- [RD-03 Datasheet](https://docs.ai-thinker.com/) (Chinese - use translation)
- [Home Assistant Forum](https://community.home-assistant.io/)
- [Similar Projects](https://github.com/Gjorgjevikj/Ai-Thinker-RD-03)

## 🌍 Cultural Note

This project was developed for Egyptian homes and includes Arabic entity names (e.g., "نور الحمام"). This is **intentional** and represents the project's identity.

When contributing:
- ✅ Keep Arabic names in main config
- ✅ Add English equivalents in comments if helpful
- ✅ Respect the cultural fingerprint

Example:
```yaml
switch:
  - platform: gpio
    name: "نور الحمام"  # Bathroom Light
    id: relay_light
```

## 📝 Documentation Standards

- **README.md:** User-facing, non-technical
- **Code comments:** Technical details, algorithm explanations
- **docs/:** Deep-dives, troubleshooting, guides

## ✅ Code Review Checklist

Reviewers will check:
- [ ] Does it solve a real problem?
- [ ] Is it the simplest solution?
- [ ] Are edge cases handled?
- [ ] Is it tested on hardware?
- [ ] Are comments helpful (not redundant)?
- [ ] Does documentation need updating?
- [ ] Backward compatible or migration path provided?

## 🙏 Recognition

Contributors will be:
- Added to README acknowledgments
- Credited in release notes
- Listed in GitHub contributors page

---

**Thank you for helping make budget hardware smart! 🚀🇪🇬**
