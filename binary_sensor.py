import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from esphome.const import CONF_ID
from . import RD03Radar

CONF_RD03_ID = "rd03_id"

CONFIG_SCHEMA = binary_sensor.binary_sensor_schema(
    device_class="occupancy"
).extend(
    {
        cv.GenerateID(CONF_RD03_ID): cv.use_id(RD03Radar),
    }
)

async def to_code(config):
    parent = await cg.get_variable(config[CONF_RD03_ID])
    sens = await binary_sensor.new_binary_sensor(config)
    cg.add(parent.set_presence(sens))