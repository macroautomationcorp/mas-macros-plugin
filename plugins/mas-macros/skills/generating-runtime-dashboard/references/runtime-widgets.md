# Runtime widgets

Seven widget kinds, all addressed by their `name` field from Python.

## Default sizes

| Kind | Default w × h |
| --- | --- |
| runtime-label | 320 × 32 |
| runtime-progress | 360 × 40 |
| runtime-chart | 480 × 280 |
| runtime-textarea | 480 × 200 |
| runtime-table | 480 × 240 |
| runtime-button | 160 × 36 |
| runtime-input | 240 × 36 |

## `runtime-label`

Static or live text. Update from Python via `mas.ui.set_text("name", "...")`.

```json
{
  "id": "runtimelabel_status",
  "kind": "runtime-label",
  "name": "status",
  "parentId": null,
  "x": 24, "y": 24, "width": 320, "height": 32, "padding": 0,
  "props": {
    "text": "Idle",
    "fontSize": 14,
    "color": "",
    "alignment": "left"
  }
}
```

| Prop | Type | Notes |
| --- | --- | --- |
| `text` | string | Initial text shown before the script overrides it. |
| `fontSize` | number | Optional. Default 14. |
| `color` | string | Optional. CSS color (e.g. `"#10b981"`). Empty for default. |
| `alignment` | `"left"` \| `"center"` \| `"right"` | Default `"left"`. |

## `runtime-progress`

Progress bar. Update via `mas.ui.set_progress("name", value)`.

```json
"props": {
  "label": "Overall progress",
  "min": 0,
  "max": 100,
  "value": 0,
  "showPercentage": true
}
```

| Prop | Type | Notes |
| --- | --- | --- |
| `label` | string | Optional. Shown above the bar. |
| `min` | number | Required. Lower bound. |
| `max` | number | Required. Upper bound. |
| `value` | number | Required. Initial value. Updated from Python. |
| `showPercentage` | boolean | Default `true`. Renders `(value / max * 100)%` next to the bar. |

## `runtime-chart`

Line / bar / pie chart. For streaming line charts, the script appends data points
via `mas.ui.add_data_point(...)`. For bar/pie or replaceable line data, use
`mas.ui.set_chart_data(...)`.

```json
"props": {
  "chartType": "line",
  "title": "CPU usage",
  "xAxisLabel": "time",
  "yAxisLabel": "%",
  "showLegend": true,
  "showGrid": true,
  "maxDataPoints": 100
}
```

| Prop | Type | Notes |
| --- | --- | --- |
| `chartType` | `"line"` \| `"bar"` \| `"pie"` | Required. |
| `title` | string | Required. Chart title. |
| `xAxisLabel` | string | Optional. |
| `yAxisLabel` | string | Optional. |
| `showLegend` | boolean | Default `true`. |
| `showGrid` | boolean | Default `true`. |
| `maxDataPoints` | number | Default 50. Older points are dropped past this limit. |

For multi-series line charts, pass a `series` argument when appending data points
in Python — the chart auto-creates a series per unique name.

## `runtime-textarea`

Scrolling text display. Append lines via `mas.ui.append_text("name", "line...")`,
or replace all content via `mas.ui.set_textarea("name", "...")`.

```json
"props": {
  "text": "",
  "fontSize": 12,
  "fontFamily": "mono",
  "scrollable": true,
  "maxLines": 500,
  "showLineNumbers": false
}
```

| Prop | Type | Notes |
| --- | --- | --- |
| `text` | string | Initial content. |
| `fontSize` | number | Default 12. |
| `fontFamily` | `"sans"` \| `"mono"` | Default `"mono"` for log-style use. |
| `scrollable` | boolean | Default `true`. Auto-scrolls on append. |
| `maxLines` | number | Default 100. Older lines are dropped past this limit. |
| `showLineNumbers` | boolean | Default `false`. |

## `runtime-table`

Tabular display. Set the full rows via `mas.ui.set_table_data("name", [...])`, or
append a single row with `mas.ui.append_table_row("name", {...})`.

```json
"props": {
  "columns": ["Name", "Value", "Status"],
  "scrollable": true,
  "striped": true,
  "compact": false,
  "maxRows": 200
}
```

| Prop | Type | Notes |
| --- | --- | --- |
| `columns` | string[] | Required. Header labels and the keys Python rows must use. |
| `scrollable` | boolean | Default `true`. |
| `striped` | boolean | Default `true`. Alternating row backgrounds. |
| `compact` | boolean | Default `false`. Tighter row height. |
| `maxRows` | number | Default 50. Older rows are dropped. |

Each row passed from Python must be a dict whose keys match `columns` exactly:

```python
mas.ui.append_table_row("results", {"Name": "Gold", "Value": "1,250", "Status": "OK"})
```

A cell can also hold a clickable button via `mas.ui.cell_button(...)` — useful
for per-row actions. Click events route through the same channel as standalone
buttons, so `mas.ui.on_click("<cell_id>", fn)` handles them. See
`mas-ui-python-api.md` for the full pattern.

```python
mas.ui.append_table_row("orders", {
    "Name": "Gold",
    "Action": mas.ui.cell_button(id="refund_gold", label="Refund", variant="destructive"),
})
```

## `runtime-button`

User-clickable button. The script reads click events via
`mas.ui.wait_for_event(timeout=...)` or the callback pattern `mas.ui.on_click("name", fn)`.

```json
"props": {
  "text": "Start",
  "variant": "default",
  "disabled": false
}
```

| Prop | Type | Notes |
| --- | --- | --- |
| `text` | string | Required. Button label. |
| `variant` | `"default"` \| `"outline"` \| `"destructive"` | Default `"default"`. |
| `disabled` | boolean | Default `false`. |

## `runtime-input`

User-editable input. The script reads its current value via
`mas.ui.get_input_value("name")` or listens for change events.

```json
"props": {
  "label": "Filter",
  "placeholder": "Type to filter...",
  "defaultValue": ""
}
```

| Prop | Type | Notes |
| --- | --- | --- |
| `label` | string | Optional. Displayed above the input. |
| `placeholder` | string | Optional. |
| `defaultValue` | string | Optional. Initial value. |

## Choosing the right widget

| User wants… | Use |
| --- | --- |
| One-line status text that changes over time | `runtime-label` |
| A progress bar for a known-bounded loop | `runtime-progress` |
| A streaming time-series of one or more metrics | `runtime-chart` (line) |
| A categorical breakdown / final summary chart | `runtime-chart` (bar / pie) |
| A scrolling log of free-form text | `runtime-textarea` |
| A growing tabular view (or final results table) | `runtime-table` |
| A button the user can click during the run | `runtime-button` |
| A text field the user types into during the run | `runtime-input` |
