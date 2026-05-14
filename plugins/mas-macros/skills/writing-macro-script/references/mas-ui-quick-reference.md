# `mas.ui` quick reference

Updates the runtime dashboard (`.uibrt`) from inside the script. For full coverage
of the runtime widgets and the dashboard JSON, see the
`generating-runtime-dashboard` skill — this file is a one-page summary for use
inside scripts.

Every call addresses a widget by its `name` (the value set in the UIBuilder
inspector — must be a valid Python identifier).

## Display

```python
mas.ui.set_text("status", "Step 3/10")
mas.ui.set_progress("main_bar", 75)

mas.ui.add_data_point("cpu_chart", value=42.5, label="t=12", series="CPU")
mas.ui.set_chart_data("scores", [
    {"label": "Gold", "value": 1250},
    {"label": "XP",   "value": 45000},
])
mas.ui.clear_chart("cpu_chart")

mas.ui.append_text("log", "Step 1 complete")
mas.ui.set_textarea("log", "Full replacement text")
mas.ui.clear_text("log")

mas.ui.set_table_data("results", [
    {"Name": "Gold", "Value": "1,250", "Status": "OK"},
])
mas.ui.append_table_row("results", {"Name": "XP", "Value": "45,000", "Status": "OK"})
mas.ui.clear_table("results")

# Button inside a cell — clicks come back through on_click / wait_for_event
mas.ui.append_table_row("orders", {
    "Name": "Gold",
    "Action": mas.ui.cell_button(id="refund_gold", label="Refund", variant="destructive"),
})
mas.ui.set_cell_button_enabled("orders", "refund_gold", enabled=False)
```

## User interaction

```python
# Blocking
event = mas.ui.wait_for_event(timeout=60)
if event and event.widget_id == "start_btn" and event.event_type == "click":
    do_thing()

# Callback (non-blocking)
def handle_pause():
    pause_flag.set()

mas.ui.on_click("pause_btn", handle_pause)
mas.ui.on_change("filter_input", lambda v: print(f"Filter: {v}"))
mas.ui.start_listener()      # daemon thread

# Read input value at any time
search = mas.ui.get_input_value("search_box")
```

## Batching

Wrap bursts of updates so they share one RPC round-trip:

```python
with mas.ui.batch():
    mas.ui.set_text("status", "Step 3/10")
    mas.ui.set_progress("main_bar", 30)
    mas.ui.add_data_point("cpu_chart", value=42, label="t=3", series="CPU")
```

Especially worth it inside hot loops where multiple widgets update each iteration.

## Widget → call cheat-sheet

| Widget kind | Update | Other |
| --- | --- | --- |
| `runtime-label` | `set_text(name, text)` | — |
| `runtime-progress` | `set_progress(name, value)` | — |
| `runtime-chart` | `add_data_point(name, value=, label=, series=)` | `set_chart_data`, `clear_chart` |
| `runtime-textarea` | `append_text(name, line)` | `set_textarea`, `clear_text` |
| `runtime-table` | `append_table_row(name, dict)` | `set_table_data`, `clear_table`, `cell_button(id=, label=, …)`, `set_cell_button_enabled` |
| `runtime-button` | `on_click(name, fn)` + `start_listener()` | `wait_for_event(timeout=)` |
| `runtime-input` | `on_change(name, fn)` + `start_listener()` | `get_input_value(name)` |
