"""The climate template component."""
# CHANGED: was an empty module; now sets up/unloads UI-created config entries.

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_PRECISION, PLATFORMS


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Climate Template from a config entry."""
    # Older versions stored precision as a float. The options selector expects
    # a string, so normalize existing entries before they are opened for edit.
    precision = entry.options.get(CONF_PRECISION)
    if isinstance(precision, (int, float)) and not isinstance(precision, bool):
        options = dict(entry.options)
        options[CONF_PRECISION] = str(precision)
        hass.config_entries.async_update_entry(entry, options=options)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    # Reload the entry whenever it is edited via the UI (options flow)
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    return True


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload the config entry when its options change."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
