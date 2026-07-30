# Template Climate

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/release/holdestmade/template_climate.svg)](https://github.com/holdestmade/template_climate/releases)
[![License](https://img.shields.io/github/license/holdestmade/template_climate.svg)](LICENSE)

A [Home Assistant](https://www.home-assistant.io/) custom integration that lets you build a fully featured **`climate` entity out of templates**. Use it to expose a thermostat/AC-style UI for any device — an IR blaster, a smart plug + temperature sensor, a REST API, or several helpers combined — by describing how to *read* its state with templates and how to *act* on changes with scripts/actions.

It works like Home Assistant's built-in template helpers but for the climate domain, and can be configured either from the **UI** (Settings → Devices & services → Helpers) or in **YAML**.

## Features

- Current temperature & humidity from templates
- Target temperature, target temperature high/low, and target humidity
- HVAC mode, HVAC action, fan mode, preset mode and swing mode from templates
- Configurable lists of supported HVAC / fan / preset / swing modes
- Min/max temperature and humidity (static values or templates)
- Configurable temperature step and display precision
- Availability, icon and entity-picture templates
- Action (script) hooks for every `set_*` command, with the requested value exposed as a template variable
- **Optimistic mode** — any attribute left without a state template assumes the last value you set
- Configurable from the **UI config flow** *and* in **YAML**

## Requirements

This integration builds on Home Assistant's modern `template` helpers, so a reasonably recent Home Assistant Core release is required. If setup fails after installing, update Home Assistant to the latest stable release and try again.

## Installation

### HACS (recommended)

1. Make sure [HACS](https://hacs.xyz/) is installed.
2. In HACS, open the three-dot menu → **Custom repositories**.
3. Add `https://github.com/holdestmade/template_climate` with category **Integration**.
4. Search for **Template Climate** in HACS and install it.
5. Restart Home Assistant.

### Manual

1. Copy the `custom_components/template_climate` folder into your Home Assistant `config/custom_components` directory.
2. Restart Home Assistant.

## Configuration

### Via the UI

1. Go to **Settings → Devices & services → Helpers**.
2. Click **Create helper** and choose **Template Climate**.
3. Give it a name. Every other field is optional — fill in the templates and actions you need.
4. Optionally pick a **Device** to link the entity to, so it appears under that device instead of as a standalone helper (same as Home Assistant's own template helpers).
5. Edit it later at any time with the **Configure** button (fields you clear are removed).

Any attribute you leave without a state template runs in *optimistic* (assumed-state) mode: Home Assistant remembers the last value you set from the UI.

### Via YAML

Add a `climate` platform entry:

```yaml
climate:
  - platform: template_climate
    name: Living Room AC
    modes:
      - "off"
      - cool
      - heat
      - fan_only
    min_temp: 16
    max_temp: 30
    temp_step: 0.5
    precision: 0.5
    current_temperature_template: "{{ states('sensor.living_room_temperature') }}"
    current_humidity_template: "{{ states('sensor.living_room_humidity') }}"
    hvac_mode_template: "{{ states('input_select.living_room_ac_mode') }}"
    target_temperature_template: "{{ states('input_number.living_room_ac_target') }}"
    set_hvac_mode:
      - service: input_select.select_option
        target:
          entity_id: input_select.living_room_ac_mode
        data:
          option: "{{ hvac_mode }}"
    set_temperature:
      - service: input_number.set_value
        target:
          entity_id: input_number.living_room_ac_target
        data:
          value: "{{ temperature }}"
```

Reload YAML-configured entities from **Developer tools → YAML → Template Climate** (or call the `template_climate.reload` service) without restarting Home Assistant.

### Action variables

Each `set_*` action receives the requested value(s) as template variables:

| Action | Available variables |
| --- | --- |
| `set_hvac_mode` | `hvac_mode` |
| `set_temperature` | `temperature`, `target_temp_high`, `target_temp_low`, `hvac_mode` |
| `set_humidity` | `humidity` |
| `set_fan_mode` | `fan_mode` |
| `set_preset_mode` | `preset_mode` |
| `set_swing_mode` | `swing_mode` |

## Configuration options

| Key | Description |
| --- | --- |
| `name` | Friendly name of the climate entity (required). |
| `device_id` | *(UI only)* Existing device to link the entity to, so it shows up under that device. |
| `availability` / `availability_template` | Template resolving to `true`/`false` for entity availability. |
| `icon` / `icon_template` | Template for the entity icon. |
| `picture` / `entity_picture_template` | Template for the entity picture. |
| `current_temperature_template` | Current temperature. |
| `current_humidity_template` | Current humidity. |
| `target_temperature_template` | Target temperature. |
| `target_temperature_high_template` / `target_temperature_low_template` | Target temperature range. |
| `target_humidity_template` | Target humidity. |
| `min_temp_template` / `max_temp_template` | Min/max temperature (template). |
| `min_humidity_template` / `max_humidity_template` | Min/max humidity (template). |
| `hvac_mode_template` | Current HVAC mode. |
| `hvac_action_template` | Current HVAC action (heating, cooling, idle, …). |
| `fan_mode_template` | Current fan mode. |
| `preset_mode_template` | Current preset mode. |
| `swing_mode_template` | Current swing mode. |
| `set_hvac_mode` / `set_temperature` / `set_humidity` / `set_fan_mode` / `set_preset_mode` / `set_swing_mode` | Actions run when the corresponding value changes. |
| `modes` | List of supported HVAC modes. |
| `fan_modes` | List of supported fan modes. |
| `preset_modes` | List of supported preset modes. |
| `swing_modes` | List of supported swing modes. |
| `min_temp` / `max_temp` | Static min/max temperature. |
| `temp_step` | Target temperature step. |
| `precision` | Display precision (`0.1`, `0.5` or `1.0`). |

## Troubleshooting

- **Entity is unavailable** — check the `availability` template and confirm the templates for current temperature/mode return valid values in **Developer tools → Template**.
- **Setting a value does nothing** — make sure you have configured the matching `set_*` action; without it that attribute is read-only/optimistic.
- **Invalid template/action error in the UI** — the form validates every template and action; fix the flagged field and resubmit.

## Contributing & issues

Bug reports and feature requests are welcome on the [issue tracker](https://github.com/holdestmade/template_climate/issues).

## License

This project is licensed under the terms of the [MIT License](LICENSE).
