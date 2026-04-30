# Validation rules

The UIBuilder validates `.uibproj` files on save. Generating files that already pass
all checks avoids round-trips through the validation dialog.

## Arg key

Every argument widget must have `props.key`. The key:

- **Must be non-empty** after trimming whitespace.
- **Must match `^[a-zA-Z_][a-zA-Z0-9_]*$`** — same rule as a Python identifier. The
  key becomes a `--<key>` CLI flag and an attribute on the parsed namespace.
- **Must be unique** across the entire project (across all tabs).

Layout widgets (`label`, `separator`, `group-box`) have no `key` and aren't validated.

## Common invalid keys to avoid

- `Input Path` — has a space. Use `input_path`.
- `2nd-arg` — starts with a digit and has a hyphen. Use `second_arg` or `arg2`.
- `output.dir` — has a dot. Use `output_dir`.
- `class` — Python keyword, technically valid as a CLI flag but the generated
  `script_args.py` will conflict if used inside Python scripts. Avoid Python
  keywords entirely.

## Naming style

Use **snake_case**: `input_path`, `max_retries`, `output_dir`. Match Python convention
since these become attributes on `args.<tab_slug>.<key>`.

## Tab names

Tab names become argparse argument groups and Python attribute names. The UIBuilder
slugifies them (`"My Tab"` → `my_tab`). Avoid characters that produce empty or
clashing slugs:

- ✓ `"General"` → `general`
- ✓ `"Output Settings"` → `output_settings`
- ✗ `"!!!"` → empty slug, falls back to `tab` and conflicts with other empty-slug tabs

## Self-check before emitting

Walk every tab → every widget. For each argument widget:

1. Trim `props.key`. Reject if empty.
2. Test against `/^[a-zA-Z_][a-zA-Z0-9_]*$/`. Reject if it doesn't match.
3. Add to a `Set`. Reject if already present.

If any reject fires, fix the input before emitting the file rather than producing a
broken `.uibproj`.

## Action bar

- `id` must be unique across the action bar's buttons.
- At least one button with `role: "run"` for the dialog to be useful.

## What's *not* validated (but should still be sensible)

- `defaultValue` for `number-input` / `slider` should fall within `[min, max]` when
  bounds are set. The UIBuilder accepts out-of-range defaults but the runner dialog
  will clamp them, surprising the user.
- `combobox` and `radio-group` `defaultValue` should match one of the option `value`s.
- `step` for `number-input` / `slider` should be positive.
