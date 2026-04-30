# mas-macros

End-to-end macro authoring for Macro Automation Studio. Three skills covering the
three artefacts that make up a macro project:

| Artefact | Skill |
| --- | --- |
| `.uibproj` — argument form (UIBuilder source) | `generating-args-form` |
| `.uibrt` — runtime dashboard (UIBuilder source) | `generating-runtime-dashboard` |
| `src/app.py` — Python script using the `mas` SDK | `writing-macro-script` |

## Skills

### `generating-args-form`

Produces `.uibproj` files — the script-runner argument forms users see before clicking
Run on a macro. Inputs become argparse arguments at runtime via the auto-generated
`script_args.py`.

Triggers on phrases like "design args UI", "create a .uibproj", "I need a form with…".
Knows all 11 argument widget kinds, layout widgets, and the action bar.

### `generating-runtime-dashboard`

Produces `.uibrt` files — live dashboards that update while the macro runs. Widgets are
addressed by `name` from Python via `mas.ui.set_text("widget_name", ...)` etc.

Triggers on phrases like "runtime UI", "live dashboard", "show progress while running".
Knows all 7 runtime widget kinds and which `mas.ui.*` call drives each one.

### `writing-macro-script`

Produces the Python script (typically `src/app.py`) that ties everything together —
reads args from `script_args.py`, drives the runtime dashboard via `mas.ui.*`, and
performs device automation via `mas.click / mas.swipe / mas.find_object / mas.read_text /
mas.open_app / mas.storage.save / …`.

Triggers on phrases like "write a macro that…", "scaffold the Python script", "implement
this macro using the mas SDK", "create app.py for this macro". Knows the standard project
structure, the public mas SDK surface (interaction, vision, storage, app, images, ui),
and common patterns (vision-based loops, retry-and-wait, args-driven control flow).

## Typical session

Most users won't think in terms of three separate skills — they'll just describe a macro
and Claude will reach for whichever skills are appropriate. A request like "build me a
macro that opens an app, finds the Login button, types my username and password, and
reports progress" hits all three skills: an args form for username/password, a runtime
dashboard for progress, and the Python script that drives both.
