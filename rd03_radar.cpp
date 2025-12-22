#include "rd03_radar.h"
#include "esphome/core/log.h"

namespace esphome {
namespace RD_03_presence_radar {

static const char *TAG = "RD-03_presence_radar";

void RD03Radar::setup() {
  buffer_.reserve(128);
  ESP_LOGI(TAG, "RD-03 Radar initialized");
}

void RD03Radar::loop() {
  const uint32_t now = millis();

  while (available()) {
    uint8_t c;
    if (!read_byte(&c)) continue;

    if (now - last_uart_ms_ > 100 && !buffer_.empty()) {
      buffer_.clear();
    }
    last_uart_ms_ = now;

    buffer_.push_back(c);

    if (c == '\n') {
      std::string line(buffer_.begin(), buffer_.end());
      buffer_.clear();

      size_t s = line.find_first_not_of(" \t\r\n");
      if (s == std::string::npos) return;
      size_t e = line.find_last_not_of(" \t\r\n");
      line = line.substr(s, e - s + 1);

      process_line_(line);
    }
  }

  if (presence_ != nullptr) {
    uint32_t elapsed = now - last_activity_ms_;
    uint32_t hold_ms = sensitivity_ * 30000UL;

    bool state = elapsed < hold_ms;
    presence_->publish_state(state);

    if (elapsed > max_absence_ms_) {
      presence_->publish_state(false);
    }
  }
}

void RD03Radar::process_line_(const std::string &line) {
  if (line.rfind("Range ", 0) != 0) return;

  size_t pos = line.find_first_of("0123456789");
  if (pos == std::string::npos) return;

  float dist = atof(line.substr(pos).c_str());

  if (distance_ != nullptr) {
    distance_->publish_state(dist);
  }

  if (dist >= min_range_ && dist <= max_range_) {
    last_activity_ms_ = millis();
  }
}

}  // namespace RD_03_presence_radar
}  // namespace esphome