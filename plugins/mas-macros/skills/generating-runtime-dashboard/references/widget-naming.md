# Widget naming rules

Runtime widgets are addressed from Python by their `name` field. Picking the right
name matters more here than in arg forms.

## Hard rules

- **Must match `^[a-zA-Z_][a-zA-Z0-9_]*$`** — Python identifier rule. The Python
  string literal in `mas.ui.set_text("name", ...)` doesn't enforce this, but anything
  else is asking for typos and confusion.
- **Must be unique** within the dashboard. Two widgets with the same `name` will both
  receive every update, which is almost never what you want.
- **No spaces, hyphens, or dots.** `cpu chart` ✗, `cpu-chart` ✗, `cpu.chart` ✗.

## Conventions

- **snake_case**, short, descriptive: `status`, `main_bar`, `cpu_chart`, `log`,
  `results_table`, `start_btn`.
- For buttons, suffix with `_btn`: `start_btn`, `pause_btn`, `cancel_btn`.
- For inputs, suffix with `_input` or use a content noun: `filter_input`, `search`.
- Avoid generic names like `text`, `value`, `chart` — pick something the script
  reader will recognise without context.

## When generating both the .uibrt and a Python snippet

Make the names line up exactly between the two — copy-paste accuracy is what makes
the dashboard usable. After emitting the JSON, immediately show the Python snippet:

```python
import mas, time

mas.ui.set_text("status", "Starting...")
for i in range(100):
    mas.ui.set_progress("main_bar", i)
    time.sleep(0.05)
mas.ui.set_text("status", "Done")
```

Each name in the snippet must appear as a widget `name` in the .uibrt.
