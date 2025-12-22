import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from . import RD03Radar


CONFIG_SCHEMA = sensor.sensor_schema(unit_of_measurement="cm").extend({
cv.GenerateID(): cv.use_id(RD03Radar),
})


async def to_code(config):
var = await cg.get_variable(config[cv.GenerateID()])
sens = await sensor.new_sensor(config)
cg.add(var.set_distance(sens))
