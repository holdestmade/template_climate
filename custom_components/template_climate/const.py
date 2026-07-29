"""Constants for the Climate Template integration."""
# NEW FILE: constants moved out of climate.py so they can be shared
# with config_flow.py without circular imports.

from homeassistant.components.climate.const import (
    FAN_AUTO,
    FAN_HIGH,
    FAN_LOW,
    FAN_MEDIUM,
    PRESET_ACTIVITY,
    PRESET_AWAY,
    PRESET_BOOST,
    PRESET_COMFORT,
    PRESET_ECO,
    PRESET_HOME,
    PRESET_SLEEP,
    HVACMode,
)
from homeassistant.const import STATE_ON, Platform

DOMAIN = "template_climate"  # CHANGED: renamed from climate_template
PLATFORMS = [Platform.CLIMATE]

DEFAULT_NAME = "Template Climate"
DEFAULT_TEMP = 21
DEFAULT_PRECISION = 1.0

# ---- modern entity-level template keys (match core template component) ----
CONF_AVAILABILITY_TEMPLATE_KEY = "availability"
CONF_ICON_KEY = "icon"
CONF_PICTURE_KEY = "picture"

# ---- template config keys (unchanged names, moved from climate.py) ----
CONF_FAN_MODE_LIST = "fan_modes"
CONF_PRESET_MODE_LIST = "preset_modes"
CONF_MODE_LIST = "modes"
CONF_SWING_MODE_LIST = "swing_modes"
CONF_TEMP_MIN_TEMPLATE = "min_temp_template"
CONF_TEMP_MIN = "min_temp"
CONF_TEMP_MAX_TEMPLATE = "max_temp_template"
CONF_TEMP_MAX = "max_temp"
CONF_PRECISION = "precision"
CONF_CURRENT_TEMP_TEMPLATE = "current_temperature_template"
CONF_TEMP_STEP = "temp_step"

CONF_CURRENT_HUMIDITY_TEMPLATE = "current_humidity_template"
CONF_MIN_HUMIDITY_TEMPLATE = "min_humidity_template"
CONF_MAX_HUMIDITY_TEMPLATE = "max_humidity_template"
CONF_TARGET_HUMIDITY_TEMPLATE = "target_humidity_template"
CONF_TARGET_TEMPERATURE_TEMPLATE = "target_temperature_template"
CONF_TARGET_TEMPERATURE_HIGH_TEMPLATE = "target_temperature_high_template"
CONF_TARGET_TEMPERATURE_LOW_TEMPLATE = "target_temperature_low_template"
CONF_HVAC_MODE_TEMPLATE = "hvac_mode_template"
CONF_FAN_MODE_TEMPLATE = "fan_mode_template"
CONF_PRESET_MODE_TEMPLATE = "preset_mode_template"
CONF_SWING_MODE_TEMPLATE = "swing_mode_template"
CONF_HVAC_ACTION_TEMPLATE = "hvac_action_template"

# ---- action (script) config keys ----
CONF_SET_HUMIDITY_ACTION = "set_humidity"
CONF_SET_TEMPERATURE_ACTION = "set_temperature"
CONF_SET_HVAC_MODE_ACTION = "set_hvac_mode"
CONF_SET_FAN_MODE_ACTION = "set_fan_mode"
CONF_SET_PRESET_MODE_ACTION = "set_preset_mode"
CONF_SET_SWING_MODE_ACTION = "set_swing_mode"

CONF_CLIMATES = "climates"

# ---- default lists (moved from inline defaults in climate.py so the
#      config flow and the YAML schema stay consistent) ----
DEFAULT_MODE_LIST = [
    HVACMode.AUTO,
    HVACMode.OFF,
    HVACMode.COOL,
    HVACMode.HEAT,
    HVACMode.DRY,
    HVACMode.FAN_ONLY,
]
DEFAULT_FAN_MODE_LIST = [FAN_AUTO, FAN_LOW, FAN_MEDIUM, FAN_HIGH]
DEFAULT_PRESET_MODE_LIST = [
    PRESET_ECO,
    PRESET_AWAY,
    PRESET_BOOST,
    PRESET_COMFORT,
    PRESET_HOME,
    PRESET_SLEEP,
    PRESET_ACTIVITY,
]
DEFAULT_SWING_MODE_LIST = [STATE_ON, HVACMode.OFF]

# All template-valued options, used to validate config entries in one place.
TEMPLATE_CONF_KEYS = (
    CONF_TEMP_MIN_TEMPLATE,
    CONF_TEMP_MAX_TEMPLATE,
    CONF_CURRENT_TEMP_TEMPLATE,
    CONF_CURRENT_HUMIDITY_TEMPLATE,
    CONF_MIN_HUMIDITY_TEMPLATE,
    CONF_MAX_HUMIDITY_TEMPLATE,
    CONF_TARGET_HUMIDITY_TEMPLATE,
    CONF_TARGET_TEMPERATURE_TEMPLATE,
    CONF_TARGET_TEMPERATURE_HIGH_TEMPLATE,
    CONF_TARGET_TEMPERATURE_LOW_TEMPLATE,
    CONF_HVAC_MODE_TEMPLATE,
    CONF_FAN_MODE_TEMPLATE,
    CONF_PRESET_MODE_TEMPLATE,
    CONF_SWING_MODE_TEMPLATE,
    CONF_HVAC_ACTION_TEMPLATE,
)

# All action-valued options.
ACTION_CONF_KEYS = (
    CONF_SET_HUMIDITY_ACTION,
    CONF_SET_TEMPERATURE_ACTION,
    CONF_SET_HVAC_MODE_ACTION,
    CONF_SET_FAN_MODE_ACTION,
    CONF_SET_PRESET_MODE_ACTION,
    CONF_SET_SWING_MODE_ACTION,
)
