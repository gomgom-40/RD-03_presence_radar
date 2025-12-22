# RD-03 Presence Radar - ESPHome Component

Custom ESPHome component for the RD-03 mmWave presence radar sensor.

## Features

- UART parsing
- Presence detection
- Distance sensor
- Absence safety
- No lambdas needed — clean YAML

## Installation

Use ESPHome `external_components`:

```yaml
external_components:
  - source: github://gomgom-40/RD-03_presence_radar

uart:
  id: radar_uart
  rx_pin: GPIO16
  tx_pin: GPIO17
  baud_rate: 115200

RD_03_presence_radar:
  id: rd03

binary_sensor:
  - platform: RD_03_presence_radar
    name: "Bathroom Presence"

sensor:
  - platform: RD_03_presence_radar
    name: "Target Distance"

#Config Options
#Option	Description
#min_range	Minimum valid distance (cm)
#max_range	Maximum valid distance (cm)
#sensitivity	Sensitivity level 1–5
#max_absence	Timeout before auto OFF

Author
Mohamed Eid
