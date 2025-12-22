#pragma once
#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/components/binary_sensor/binary_sensor.h"
#include "esphome/components/sensor/sensor.h"


namespace esphome {
namespace RD_03_presence_radar {


class RD03Radar : public Component, public uart::UARTDevice {
public:
void setup() override;
void loop() override;


void set_min_range(float v) { min_range_ = v; }
void set_max_range(float v) { max_range_ = v; }
void set_sensitivity(int v) { sensitivity_ = v; }
void set_max_absence(uint32_t v) { max_absence_ms_ = v; }


void set_presence(binary_sensor::BinarySensor *p) { presence_ = p; }
void set_distance(sensor::Sensor *s) { distance_ = s; }


protected:
void process_line_(const std::string &line);


float min_range_{20.0f};
float max_range_{500.0f};
int sensitivity_{3};


uint32_t last_activity_ms_{0};
uint32_t last_uart_ms_{0};
uint32_t max_absence_ms_{300000};


std::vector<uint8_t> buffer_;


binary_sensor::BinarySensor *presence_{nullptr};
sensor::Sensor *distance_{nullptr};
};


} // namespace RD_03_presence_radar
} // namespace esphome
