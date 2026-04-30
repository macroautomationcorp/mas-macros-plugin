# `mas.ui.*` Python API → widget mapping

The runtime UI is driven from Python via `mas.ui.*`. Every call addresses a widget by
its `name` field (the value set in the UIBuilder's inspector — must be a valid Python
identifier).

## Display widgets

### `runtime-label`

```python
mas.ui.set_text("status", "Working...")
```

Replaces the label's `text` property.

### `runtime-progress`

```python
mas.ui.set_progress("main_bar", 75)
```

Sets the `value` property. The host UI clamps to `[min, max]` defined in the widget.

### `runtime-chart` (line, streaming)

```python
mas.ui.add_data_point("cpu_chart", value=42.5, label="t=12", series="CPU")
```

Appends one point to the chart. `series` lets a single chart hold multiple lines —
each unique series name gets its own line. Older points beyond `maxDataPoints` are
dropped automatically.

### `runtime-chart` (bar / pie / line replace)

```python
mas.ui.set_chart_data("scores", [
    {"label": "Gold",  "value": 1250},
    {"label": "XP",    "value": 45000},
    {"label": "Items", "value": 23},
])
```

Replaces the chart's full dataset. Each entry needs `label` (str) and `value` (number);
`series` (str) is optional for grouped charts.

```python
mas.ui.clear_chart("cpu_chart")
```

Removes all data points.

### `runtime-textarea`

```python
mas.ui.append_text("log", "Step 1 complete")
mas.ui.append_text("log", f"Processed {n} items")
```

Append a line. Auto-scrolls. Older lines beyond `maxLines` drop off.

```python
mas.ui.set_textarea("log", "Full replacement text")
mas.ui.clear_text("log")
```

Replace or clear the entire content.

### `runtime-table`

```python
mas.ui.set_table_data("results", [
    {"Name": "Gold", "Value": "1,250", "Status": "OK"},
    {"Name": "XP",   "Value": "45,000", "Status": "OK"},
])
```

Replace all rows. Each dict's keys **must match `columns`** exactly.

```python
mas.ui.append_table_row("results", {"Name": "Items", "Value": "23", "Status": "OK"})
mas.ui.clear_table("results")
```

## Interactive widgets

### `runtime-button` — wait for event (blocking)

```python
event = mas.ui.wait_for_event(timeout=60)
if event and event.widget_id == "start_btn" and event.event_type == "click":
    print("Start was clicked")
```

`wait_for_event` blocks the current thread. Returns `None` if the timeout elapses.

### `runtime-button` — callback registration (non-blocking)

```python
def handle_pause():
    pause_flag.set()

mas.ui.on_click("pause_btn", handle_pause)
mas.ui.start_listener()  # daemon thread; returns immediately
# ... main script logic continues here ...
```

### `runtime-input` — read current value

```python
search = mas.ui.get_input_value("search_box")
```

Returns the most recent value the user typed, or `None` if never set.

### `runtime-input` — react to changes

```python
def handle_filter(value):
    print(f"Filter changed to: {value}")

mas.ui.on_change("filter_input", handle_filter)
mas.ui.start_listener()
```

## Batching for performance

If many updates fire in close succession, wrap them in a `mas.ui.batch()` to send a
single RPC call instead of many:

```python
with mas.ui.batch():
    mas.ui.set_text("status", "Step 3/10")
    mas.ui.set_progress("main_bar", 30)
    mas.ui.add_data_point("cpu_chart", value=42, label="t=3", series="CPU")
```

## Quick reference

| Widget kind | Update call | Other calls |
| --- | --- | --- |
| `runtime-label` | `set_text(name, text)` | — |
| `runtime-progress` | `set_progress(name, value)` | — |
| `runtime-chart` | `add_data_point(name, value=, label=, series=)` | `set_chart_data(name, list)`, `clear_chart(name)` |
| `runtime-textarea` | `append_text(name, line)` | `set_textarea(name, text)`, `clear_text(name)` |
| `runtime-table` | `append_table_row(name, dict)` | `set_table_data(name, list)`, `clear_table(name)` |
| `runtime-button` | `on_click(name, fn)` + `start_listener()` | `wait_for_event(timeout=)` |
| `runtime-input` | `on_change(name, fn)` + `start_listener()` | `get_input_value(name)` |
