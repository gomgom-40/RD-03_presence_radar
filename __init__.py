from esphome.codegen import esphome_ns
import esphome.config_validation as cv
from esphome.const import CONF_ID, CONF_MIN_RANGE, CONF_MAX_RANGE, CONF_SENSITIVITY


RD03_NS = esphome_ns.namespace('RD_03_presence_radar')
RD03Radar = RD03_NS.class_('RD03Radar', cg.Component)


CONFIG_SCHEMA = cv.All(
cv.Schema({
cv.GenerateID(): cv.declare_id(RD03Radar),
cv.Optional(CONF_MIN_RANGE): cv.float_,
cv.Optional(CONF_MAX_RANGE): cv.float_,
cv.Optional(CONF_SENSITIVITY): cv.int_,
})
)
