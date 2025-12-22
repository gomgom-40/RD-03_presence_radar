import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import CONF_ID
from . import RD03Radar

CONF_RD03_ID = "rd03_id"

CONFIG_SCHEMA = sensor.sensor_schema(
    unit_of_measurement="cm",
    accuracy_decimals=0,
).extend(
    {
        cv.GenerateID(CONF_RD03_ID): cv.use_id(RD03Radar),
    }
)

async def to_code(config):
    parent = await cg.get_variable(config[CONF_RD03_ID])
    sens = await sensor.new_sensor(config)
    cg.add(parent.set_distance(sens))