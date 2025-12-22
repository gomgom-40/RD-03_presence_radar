import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from . import RD03Radar


CONFIG_SCHEMA = binary_sensor.binary_sensor_schema().extend({
cv.GenerateID(): cv.use_id(RD03Radar),
})


async def to_code(config):
var = await cg.get_variable(config[cv.GenerateID()])
sens = await binary_sensor.new_binary_sensor(config)
cg.add(var.set_presence(sens))
