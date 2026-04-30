# `script_args.py` generated output

The UIBuilder generates `src/script_args.py` next to the `.uibproj` on save. The
macro's Python code imports it like:

```python
from src.script_args import args

print(args.general.input_path)
print(args.advanced.threads)
```

**Don't generate this file unless the user explicitly asks** — the UIBuilder is the
canonical source. The format below is for when the user wants to see what the
argparse code looks like, or wants Claude to write a Python script that consumes
the args.

## Generated structure

```python
"""
Script Arguments — My Macro Args
================================

Auto-generated from the UI Builder project.
This file is regenerated each time you click 'Generate Args' in the UI Builder.

Usage:
    from src.script_args import args

    # General
    args.general.input_path  (str)
    args.general.threads     (int/float)
    args.general.verbose     (bool)
"""
import argparse
from types import SimpleNamespace


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description='My Macro Args',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    _general = parser.add_argument_group('General')
    _general.add_argument('--input_path', type=str, required=True, help='Path to the source file')
    _general.add_argument('--threads', type=int, default=4, help='Threads')  # min=1, max=64
    _general.add_argument('--verbose', action='store_true')

    return parser


def _organize(flat: argparse.Namespace) -> SimpleNamespace:
    """Organize flat parsed args into tab-based namespaces."""
    return SimpleNamespace(
        general=SimpleNamespace(
            input_path=flat.input_path,
            threads=flat.threads,
            verbose=flat.verbose,
        ),
    )


# Parse and organize arguments when this module is imported
args = _organize(create_parser().parse_args())
```

## Mapping rules

Each tab becomes an argparse argument group. The tab name is slugified to a Python
identifier (`"My Settings"` → `my_settings`). Only argument widgets with a non-empty
`key` are included; layout widgets and runtime widgets are skipped.

### Per-widget argparse mapping

| Widget kind | argparse mapping |
| --- | --- |
| `text-input` | `type=str` |
| `text-area` | `type=str` |
| `number-input` | `type=int` if `step` is integer, else `type=float` |
| `slider` | `type=int` if `step` is integer, else `type=float` |
| `checkbox` | `action='store_true'` (no type, no default) |
| `combobox` | `type=str`, `choices=[...]` from option values |
| `radio-group` | `type=str`, `choices=[...]` from option values |
| `file-picker` | `type=str` |
| `directory-picker` | `type=str` |
| `date-picker` | `type=str` |
| `time-picker` | `type=str` |

### `required` and `default`

- `required=True` is added when the widget's `required` is `true`, except for `checkbox`
  (which always defaults to `False`).
- `default=...` is added when `defaultValue` is set and non-empty, except for `checkbox`.
- For `number-input` / `slider`, the default is emitted unquoted (`default=4`); for
  string-typed widgets it's a Python string literal (`default='json'`).

### `help`

The widget's `helpText` is used as `help=`. If `helpText` is empty, the widget's
`label` (or `text` for checkbox) is used instead.

### `choices` (combobox + radio-group)

Each option's `value` becomes a choice. The option `label` is display-only and
doesn't appear in the generated code.

### Bounds (number-input + slider)

`min` / `max` are emitted as a trailing comment on the same line, e.g.
`# min=1, max=64`. argparse doesn't natively enforce bounds — the comment is
informational; the runner dialog clamps in the UI.

## Tab access pattern

The bottom of the file calls `_organize(...)` which builds a `SimpleNamespace` of
`SimpleNamespace`s, one per tab. So in the macro:

```python
args.<tab_slug>.<arg_key>
```

If a tab has zero argument widgets, it's omitted from the output entirely.

If two tabs slugify to the same name, the second one gets a `_2` suffix
(`my_tab`, `my_tab_2`, …).
