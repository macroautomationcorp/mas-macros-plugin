# Argument widgets

Eleven widget kinds produce CLI arguments. Each one is a `WidgetNode` with `kind` set
to the kind string and `props` set per-kind. Every argument widget's `props` includes
the **shared `ArgMeta`** fields:

| ArgMeta field | Type | Required | Default | Notes |
| --- | --- | --- | --- | --- |
| `key` | string | yes | — | The CLI flag name (`--<key>`). Must match `^[a-zA-Z_][a-zA-Z0-9_]*$` and be unique. |
| `required` | boolean | yes | `false` | argparse `required=True` when true. Ignored for `checkbox`. |
| `helpText` | string | no | — | Shown in tooltip and used as argparse `help`. |
| `showLabel` | boolean | no | `true` | Set `false` to hide the label visually. |
| `labelPosition` | `"top"` \| `"left"` | no | `"top"` | Where the label sits. |
| `labelGap` | number | no | `6` (top) / `12` (left) | Px gap between label and input. |

## Choice option shape (used by combobox + radio-group)

```json
{ "label": "Display Text", "value": "stored_value" }
```

The `value` becomes the actual argparse value.

## Default sizes

These are the UIBuilder palette defaults. Use them unless the user asks for something else.

| Kind | Default w × h |
| --- | --- |
| text-input | 240 × 36 |
| text-area | 320 × 80 |
| number-input | 160 × 36 |
| slider | 280 × 50 |
| checkbox | 200 × 28 |
| combobox | 240 × 36 |
| radio-group | 240 × 80 |
| file-picker | 320 × 36 |
| directory-picker | 320 × 36 |
| date-picker | 200 × 36 |
| time-picker | 180 × 36 |

## `text-input`

Single-line free text. Becomes a `--<key> str` argparse arg.

```json
{
  "id": "textinput_input01",
  "kind": "text-input",
  "name": "input_path",
  "parentId": null,
  "x": 24, "y": 24, "width": 240, "height": 36, "padding": 8,
  "props": {
    "key": "input_path",
    "required": true,
    "helpText": "Path to the source file",
    "label": "Input path",
    "placeholder": "/path/to/file",
    "defaultValue": ""
  }
}
```

Per-kind props: `label` (string, required), `placeholder` (string, optional),
`defaultValue` (string, optional).

## `text-area`

Multi-line free text.

```json
"props": {
  "key": "notes",
  "required": false,
  "label": "Notes",
  "placeholder": "Free-form notes...",
  "defaultValue": "",
  "rows": 4
}
```

Per-kind props: `label` (required), `placeholder`, `defaultValue`, `rows` (int, default 4).

## `number-input`

Numeric input with optional bounds.

```json
"props": {
  "key": "threads",
  "required": false,
  "label": "Threads",
  "min": 1,
  "max": 64,
  "step": 1,
  "precision": 0,
  "defaultValue": 4,
  "suffix": ""
}
```

Per-kind props: `label` (required), `min` (number, optional), `max` (number, optional),
`step` (number, default `1`), `precision` (int, default `0` — number of decimal places),
`defaultValue` (number, required), `suffix` (string, optional — e.g. `"px"`).

argparse type is `int` when `step` is integer, `float` otherwise.

## `slider`

Bounded numeric input via a slider.

```json
"props": {
  "key": "speed",
  "required": false,
  "label": "Speed",
  "min": 0,
  "max": 100,
  "step": 1,
  "defaultValue": 50,
  "showValue": true,
  "suffix": "%"
}
```

Per-kind props: `label` (required), `min` (required), `max` (required), `step`
(default `1`), `defaultValue` (required), `showValue` (default `true` — render the
current value next to the slider), `suffix` (optional).

argparse type is `int` when `step` is integer, `float` otherwise.

## `checkbox`

Boolean flag. argparse `action='store_true'`.

```json
"props": {
  "key": "verbose",
  "required": false,
  "text": "Enable verbose logging",
  "checked": false
}
```

Per-kind props: `text` (required — the label shown next to the checkbox; differs from
other widgets that use `label`), `checked` (default `false` — initial state).

`required` and `defaultValue` are ignored — checkboxes always default to `False` in
argparse and get set to `True` only if the flag is passed.

## `combobox`

Dropdown selector (or editable typeahead).

```json
"props": {
  "key": "format",
  "required": true,
  "label": "Output format",
  "placeholder": "Choose...",
  "editable": false,
  "options": [
    { "label": "JSON",   "value": "json" },
    { "label": "CSV",    "value": "csv" },
    { "label": "YAML",   "value": "yaml" }
  ],
  "defaultValue": "json"
}
```

Per-kind props: `label` (required), `placeholder`, `editable` (default `false` — when
`true`, allows typing arbitrary values), `options` (array of `{label, value}`, required),
`defaultValue` (string — should match one of the option `value`s).

argparse `choices=[...]` is set from the option values.

## `radio-group`

Mutually exclusive radio buttons.

```json
"props": {
  "key": "mode",
  "required": false,
  "label": "Mode",
  "direction": "vertical",
  "options": [
    { "label": "Fast",     "value": "fast" },
    { "label": "Balanced", "value": "balanced" },
    { "label": "Thorough", "value": "thorough" }
  ],
  "defaultValue": "balanced"
}
```

Per-kind props: `label` (required), `direction` (`"horizontal"` | `"vertical"`,
default `"vertical"`), `options`, `defaultValue`.

argparse `choices=[...]` is set from the option values.

## `file-picker`

Native file-selection dialog. The selected absolute path is stored as a string.

```json
"props": {
  "key": "config_file",
  "required": true,
  "label": "Config file",
  "placeholder": "Select a file...",
  "defaultValue": "",
  "filters": "*.json;*.yaml;*.yml"
}
```

Per-kind props: `label` (required), `placeholder`, `defaultValue`, `filters` (string
of semicolon-separated globs filtering the OS file dialog; e.g. `"*.txt;*.csv"`).

## `directory-picker`

Native directory-selection dialog.

```json
"props": {
  "key": "output_dir",
  "required": true,
  "label": "Output directory",
  "placeholder": "Select a folder...",
  "defaultValue": ""
}
```

Per-kind props: `label`, `placeholder`, `defaultValue`.

## `date-picker`

Date input. Stored as a string in the configured format.

```json
"props": {
  "key": "since",
  "required": false,
  "label": "Since",
  "format": "YYYY-MM-DD",
  "defaultValue": ""
}
```

Per-kind props: `label`, `format` (string template — typically `"YYYY-MM-DD"`),
`defaultValue` (string in that format).

## `time-picker`

Time input. Stored as a string.

```json
"props": {
  "key": "deadline",
  "required": false,
  "label": "Deadline",
  "format": "HH:mm",
  "defaultValue": ""
}
```

Per-kind props: `label`, `format` (one of `"HH:mm"`, `"HH:mm:ss"`, `"hh:mm A"`,
`"hh:mm:ss A"`), `defaultValue`.

## Choosing the right widget

| User wants… | Use |
| --- | --- |
| Free-form short text (path, name, URL) | `text-input` |
| Free-form long text (notes, multi-line config) | `text-area` |
| Integer or float with no UI hint | `number-input` |
| Bounded numeric value with visible scrubber | `slider` |
| On/off flag | `checkbox` |
| Pick one from a closed list, dropdown UI | `combobox` |
| Pick one from a closed list, all visible | `radio-group` |
| File path the user picks via OS dialog | `file-picker` |
| Directory path the user picks via OS dialog | `directory-picker` |
| Calendar date | `date-picker` |
| Wall-clock time | `time-picker` |
