import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import CONF_ID

DEPENDENCIES = ["uart"]

RD03_NS = cg.esphome_ns.namespace("RD_03_presence_radar")
RD03Radar = RD03_NS.class_("RD03Radar", cg.Component, uart.UARTDevice)

CONF_MIN_RANGE = "min_range"
CONF_MAX_RANGE = "max_range"
CONF_SENSITIVITY = "sensitivity"
CONF_MAX_ABSENCE = "max_absence"

CONFIG_SCHEMA = uart.UART_DEVICE_SCHEMA.extend(
    {
        cv.GenerateID(): cv.declare_id(RD03Radar),
        cv.Optional(CONF_MIN_RANGE, default=20.0): cv.float_range(min=10, max=300),
        cv.Optional(CONF_MAX_RANGE, default=500.0): cv.float_range(min=50, max=600),
        cv.Optional(CONF_SENSITIVITY, default=3): cv.int_range(min=1, max=5),
        cv.Optional(CONF_MAX_ABSENCE, default=300): cv.positive_int,
    }
).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    cg.add(var.set_min_range(config[CONF_MIN_RANGE]))
    cg.add(var.set_max_range(config[CONF_MAX_RANGE]))
    cg.add(var.set_sensitivity(config[CONF_SENSITIVITY]))
    cg.add(var.set_max_absence(config[CONF_MAX_ABSENCE] * 1000))  # minutes to ms