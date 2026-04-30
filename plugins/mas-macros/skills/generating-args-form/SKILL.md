---
name: generating-args-form
description: Generates Macro Automation Studio script-runner argument forms (.uibproj files) and the matching ui.xml + script_args.py exports. Use when the user asks to design, create, edit, or scaffold a UIBuilder argument form, build script arguments UI for a macro, lay out input fields for a Python script that will run on an emulator, work with .uibproj files, or describe form fields in natural language ("I need a form with two text inputs, a slider, and a checkbox"). Knows all 11 argument widget kinds (text-input, text-area, number-input, slider, checkbox, combobox, radio-group, file-picker, directory-picker, date-picker, time-picker), layout widgets, action-bar buttons, validation rules (Python-identifier arg keys, no duplicates), and pixel-canvas layout heuristics.
---

# Generating UIBuilder argument forms (.uibproj)

A `.uibproj` file is the editable source for a Macro Automation Studio script-runner
window. The user opens it in the UIBuilder app and clicks Save to produce two artefacts
next to it:

- `ui.xml` — read by the desktop app to render the runner dialog before each run.
- `src/script_args.py` — `argparse`-based parser the macro's Python code imports.

The `.uibproj` is a single JSON document. Every field that ends up as a CLI flag is an
**argument widget** with a `key`. Layout widgets (label, separator, group-box) are
visual-only and don't produce CLI flags.

## Workflow

1. **Clarify intent** if it isn't already clear: how many inputs, what each one is for,
   any required fields, default values, choice options. A concrete example from the user
   is worth ten guesses — ask for one if needed.
2. **Pick widgets** for each input. See `references/argument-widgets.md` for the full set
   and which one fits which kind of value.
3. **Assign arg keys** — each must be a valid Python identifier and unique within the
   project. See `references/validation-rules.md`.
4. **Lay out widgets** vertically in the canvas. See `references/canvas-layout-tips.md`
   for default sizes and stacking.
5. **Emit the JSON** matching the schema in `references/uibproj-schema.md`. Pretty-print
   with 2-space indentation.
6. **Sanity-check** before handing the file back: every arg widget has a non-empty `key`,
   no two widgets share a key, every key matches `^[a-zA-Z_][a-zA-Z0-9_]*$`, and at
   least one tab exists.

The user can save the file directly into a macro project. The UIBuilder also runs full
validation on save and will surface any issue with click-to-jump rows, so anything
slipping through here is caught at the next save.

## Output

Default to writing the `.uibproj` to the path the user requests, or print the file
contents in a fenced JSON block when no path is specified. Don't generate `ui.xml` or
`script_args.py` by default — the UIBuilder produces those on save and they're the
canonical artefact. Only emit them if the user explicitly asks (`references/ui-xml-export.md`
and `references/script-args-py-output.md` describe both formats so you can render them
when needed).

## References

- [uibproj-schema.md](references/uibproj-schema.md) — the JSON shape, required fields, defaults
- [argument-widgets.md](references/argument-widgets.md) — all 11 input widget kinds with props
- [layout-widgets.md](references/layout-widgets.md) — label / separator / group-box
- [action-bar.md](references/action-bar.md) — the bottom Cancel / Run buttons
- [validation-rules.md](references/validation-rules.md) — arg-key regex, duplicate detection
- [canvas-layout-tips.md](references/canvas-layout-tips.md) — pixel sizes, vertical stacking
- [ui-xml-export.md](references/ui-xml-export.md) — generated XML format (only emit on request)
- [script-args-py-output.md](references/script-args-py-output.md) — generated argparse format (only emit on request)

## Examples

Real `.uibproj` files in `examples/`. Each one is a small but complete project the
UIBuilder can open and round-trip:

- [simple-form.uibproj](examples/simple-form.uibproj) — one tab, two text inputs, a checkbox
- [multi-tab-form.uibproj](examples/multi-tab-form.uibproj) — Source / Settings tabs with mixed widgets
- [slider-checkbox.uibproj](examples/slider-checkbox.uibproj) — slider with bounds + boolean toggle
- [file-picker-form.uibproj](examples/file-picker-form.uibproj) — file, directory, and date pickers
