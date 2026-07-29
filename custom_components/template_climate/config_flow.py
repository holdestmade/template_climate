"""Config flow for the Climate Template integration."""
# NEW FILE: makes the integration creatable and editable from the UI
# (Settings -> Devices & services -> Helpers -> Create helper).
#
# It uses the same SchemaConfigFlowHandler machinery as Home Assistant's own
# template helpers, so creating and later editing (Configure) both work, and
# all values are stored in the config entry's options.

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, cast

import voluptuous as vol

from homeassistant.const import CONF_NAME
from homeassistant.helpers import config_validation as cv, selector
from homeassistant.helpers.schema_config_entry_flow import (
    SchemaCommonFlowHandler,
    SchemaConfigFlowHandler,
    SchemaFlowError,
    SchemaFlowFormStep,
)

from .const import (
    ACTION_CONF_KEYS,
    CONF_AVAILABILITY_TEMPLATE_KEY,
    CONF_FAN_MODE_LIST,
    CONF_ICON_KEY,
    CONF_MODE_LIST,
    CONF_PICTURE_KEY,
    CONF_PRECISION,
    CONF_PRESET_MODE_LIST,
    CONF_SET_FAN_MODE_ACTION,
    CONF_SET_HUMIDITY_ACTION,
    CONF_SET_HVAC_MODE_ACTION,
    CONF_SET_PRESET_MODE_ACTION,
    CONF_SET_SWING_MODE_ACTION,
    CONF_SET_TEMPERATURE_ACTION,
    CONF_SWING_MODE_LIST,
    CONF_TEMP_MAX,
    CONF_TEMP_MIN,
    CONF_TEMP_STEP,
    DEFAULT_FAN_MODE_LIST,
    DEFAULT_MODE_LIST,
    DEFAULT_PRESET_MODE_LIST,
    DEFAULT_SWING_MODE_LIST,
    DEFAULT_PRECISION,
    DOMAIN,
    TEMPLATE_CONF_KEYS,
)

# Selector shorthands
TEMPLATE = selector.TemplateSelector()
ACTION = selector.ActionSelector()

HVAC_MODE_OPTIONS = ["auto", "off", "cool", "heat", "dry", "fan_only", "heat_cool"]
FAN_MODE_OPTIONS = ["auto", "low", "medium", "high", "top", "middle", "focus", "diffuse"]
PRESET_MODE_OPTIONS = [
    "none",
    "eco",
    "away",
    "boost",
    "comfort",
    "home",
    "sleep",
    "activity",
]
SWING_MODE_OPTIONS = ["on", "off", "both", "vertical", "horizontal"]


def _multi_select(options: list[str]) -> selector.SelectSelector:
    """Build a multi-select dropdown that also accepts custom values."""
    return selector.SelectSelector(
        selector.SelectSelectorConfig(
            options=options,
            multiple=True,
            custom_value=True,
            mode=selector.SelectSelectorMode.DROPDOWN,
        )
    )


def _number_box(step: float) -> selector.NumberSelector:
    """Build a plain number input box."""
    return selector.NumberSelector(
        selector.NumberSelectorConfig(
            mode=selector.NumberSelectorMode.BOX, step=step
        )
    )


# All fields shared between the create flow and the edit (options) flow.
OPTIONS_SCHEMA_DICT: dict[Any, Any] = {
    # entity-level templates
    vol.Optional(CONF_AVAILABILITY_TEMPLATE_KEY): TEMPLATE,
    vol.Optional(CONF_ICON_KEY): TEMPLATE,
    vol.Optional(CONF_PICTURE_KEY): TEMPLATE,
    # every templateable entry from the YAML version
    **{vol.Optional(key): TEMPLATE for key in TEMPLATE_CONF_KEYS},
    # actions for each set_* command
    vol.Optional(CONF_SET_HVAC_MODE_ACTION): ACTION,
    vol.Optional(CONF_SET_TEMPERATURE_ACTION): ACTION,
    vol.Optional(CONF_SET_HUMIDITY_ACTION): ACTION,
    vol.Optional(CONF_SET_FAN_MODE_ACTION): ACTION,
    vol.Optional(CONF_SET_PRESET_MODE_ACTION): ACTION,
    vol.Optional(CONF_SET_SWING_MODE_ACTION): ACTION,
    # mode lists
    vol.Optional(CONF_MODE_LIST, default=list(DEFAULT_MODE_LIST)): _multi_select(
        HVAC_MODE_OPTIONS
    ),
    vol.Optional(
        CONF_FAN_MODE_LIST, default=list(DEFAULT_FAN_MODE_LIST)
    ): _multi_select(FAN_MODE_OPTIONS),
    vol.Optional(
        CONF_PRESET_MODE_LIST, default=list(DEFAULT_PRESET_MODE_LIST)
    ): _multi_select(PRESET_MODE_OPTIONS),
    vol.Optional(
        CONF_SWING_MODE_LIST, default=list(DEFAULT_SWING_MODE_LIST)
    ): _multi_select(SWING_MODE_OPTIONS),
    # numeric settings
    vol.Optional(CONF_TEMP_MIN): _number_box(0.5),
    vol.Optional(CONF_TEMP_MAX): _number_box(0.5),
    vol.Optional(CONF_TEMP_STEP, default=DEFAULT_PRECISION): _number_box(0.1),
    vol.Optional(CONF_PRECISION): selector.SelectSelector(
        selector.SelectSelectorConfig(
            options=["0.1", "0.5", "1.0"],
            mode=selector.SelectSelectorMode.DROPDOWN,
        )
    ),
}

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): selector.TextSelector(),
        **OPTIONS_SCHEMA_DICT,
    }
)

OPTIONS_SCHEMA = vol.Schema(OPTIONS_SCHEMA_DICT)


async def _validate_user_input(
    handler: SchemaCommonFlowHandler, user_input: dict[str, Any]
) -> dict[str, Any]:
    """Validate the submitted form.

    Empty values are kept as-is (they overwrite a previously stored value
    when editing, and are filtered out again at setup in climate.py), while
    non-empty templates and actions are validated so a typo fails in the
    form rather than at entity setup.
    """
    for key in TEMPLATE_CONF_KEYS + (
        CONF_AVAILABILITY_TEMPLATE_KEY,
        CONF_ICON_KEY,
        CONF_PICTURE_KEY,
    ):
        if user_input.get(key):
            try:
                cv.template(user_input[key])
            except vol.Invalid as err:
                raise SchemaFlowError("invalid_template") from err

    for key in ACTION_CONF_KEYS:
        if user_input.get(key):
            try:
                cv.SCRIPT_SCHEMA(user_input[key])
            except vol.Invalid as err:
                raise SchemaFlowError("invalid_action") from err

    # precision arrives as a string from the select dropdown
    if user_input.get(CONF_PRECISION) not in (None, ""):
        user_input[CONF_PRECISION] = float(user_input[CONF_PRECISION])

    return user_input


CONFIG_FLOW = {
    "user": SchemaFlowFormStep(
        CONFIG_SCHEMA, validate_user_input=_validate_user_input
    ),
}

OPTIONS_FLOW = {
    "init": SchemaFlowFormStep(
        OPTIONS_SCHEMA, validate_user_input=_validate_user_input
    ),
}


class ClimateTemplateConfigFlowHandler(SchemaConfigFlowHandler, domain=DOMAIN):
    """Handle config and options flows for Climate Template."""

    config_flow = CONFIG_FLOW
    options_flow = OPTIONS_FLOW

    def async_config_entry_title(self, options: Mapping[str, Any]) -> str:
        """Return the config entry title (the entity name)."""
        return cast(str, options[CONF_NAME])
