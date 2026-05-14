---
name: generating-runtime-dashboard
description: Generates Macro Automation Studio runtime UI dashboards (.uibrt files) that display live information from a running Python macro. Use when the user asks to create, design, or edit a UIBuilder runtime dashboard, build a live UI that updates while a macro runs, show progress / charts / logs / tables during script execution, work with .uibrt files, design widgets that update via mas.ui.* Python calls (set_text, set_progress, add_data_point, append_text, set_table_data, cell_button), or add interactive runtime buttons/inputs the script reads via mas.ui.wait_for_event / on_click — including per-row action buttons embedded in table cells. Knows all 7 runtime widgets (runtime-label, runtime-progress, runtime-chart, runtime-textarea, runtime-table, runtime-button, runtime-input) and which mas.ui.* method drives which widget property.
---

# Generating UIBuilder runtime dashboards (.uibrt)

A `.uibrt` file is the editable source for a Macro Automation Studio **runtime UI**.
Unlike `.uibproj` (which describes a pre-run argument form), a `.uibrt` describes a
live dashboard that renders inside the DeviceCard's "Runtime UI" tab while the macro
runs. Widgets update in real time as the Python script calls `mas.ui.*` functions.

There is no separate XML or Python export — the host app reads the `.uibrt` JSON
directly at runtime.

## How widgets update

Each runtime widget is identified by its `name` field (set in the UIBuilder's
inspector). Python addresses the widget by that name:

```python
import mas, time

mas.ui.set_text("status", "Working...")
for i in range(100):
    mas.ui.set_progress("main_bar", i)
    time.sleep(0.1)
mas.ui.set_text("status", "Done")
```

The `name` field for runtime widgets must therefore be a **valid Python identifier**
— same rule as arg keys: `^[a-zA-Z_][a-zA-Z0-9_]*$`, no spaces, no dots. See
`references/widget-naming.md`.

## Workflow

1. **Clarify intent** if it isn't already clear: which signals from the script need
   to be visible? Progress of a long loop? A streaming chart of CPU usage? A scrolling
   log? A summary table at the end?
2. **Pick widgets** for each signal. See `references/runtime-widgets.md` for the full
   set of 7 kinds and what each is for.
3. **Pick widget names** that the user will use from Python — short, meaningful,
   snake_case.
4. **Lay out widgets** in the canvas. See `references/canvas-layout-tips.md`.
5. **Emit the JSON** matching `references/uibrt-schema.md`.
6. **Show the user the matching Python snippet** so they know exactly which
   `mas.ui.*` call drives each widget. See `references/mas-ui-python-api.md`.

## Output

Default to writing the `.uibrt` to the path the user requests, or print the file
contents in a fenced JSON block when no path is specified. After the file, **always
include a short Python snippet** showing the `mas.ui.*` calls that update each
widget — the dashboard is useless without knowing how to drive it.

## References

- [uibrt-schema.md](references/uibrt-schema.md) — the JSON shape, required fields, defaults
- [runtime-widgets.md](references/runtime-widgets.md) — all 7 widget kinds with props
- [mas-ui-python-api.md](references/mas-ui-python-api.md) — Python call → widget property mapping
- [widget-naming.md](references/widget-naming.md) — naming rules and conventions
- [canvas-layout-tips.md](references/canvas-layout-tips.md) — pixel sizes, vertical stacking

## Examples

Real `.uibrt` files in `examples/`. Each one is paired with the Python snippet that
drives it:

- [status-dashboard.uibrt](examples/status-dashboard.uibrt) — status label + progress bar
- [streaming-chart.uibrt](examples/streaming-chart.uibrt) — line chart for streaming metrics
- [log-textarea.uibrt](examples/log-textarea.uibrt) — scrolling mono text-area log
- [data-table.uibrt](examples/data-table.uibrt) — table populated at the end of the run
