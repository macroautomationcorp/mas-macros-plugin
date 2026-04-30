# Canvas layout tips

The UIBuilder uses absolute pixel coordinates inside each tab. Widgets don't auto-flow,
so every widget needs sensible `x`, `y`, `width`, `height`. The tips below produce
forms that look right when rendered without manual tweaking.

## Canvas defaults

- `window.width = 980`, `window.height = 640`.
- `window.padding = 24` (inner padding).
- `window.widgetGap = 12` (target gap between stacked widgets).

So usable horizontal space is `980 - 2*24 = 932 px`. Most forms only use the left half.

## Vertical stack pattern (the default)

For most forms, lay widgets out in a single column starting at the canvas padding:

```
y = 24   first widget
y = 24 + h1 + 12   second widget
y = 24 + h1 + 12 + h2 + 12   third
...
```

Use `x = 24` for every widget. Pick `width` based on what the widget holds:

| Widget | Suggested width |
| --- | --- |
| `text-input`, `combobox`, `number-input` | 240 |
| `text-area`, `file-picker`, `directory-picker` | 320 |
| `slider`, `radio-group` | 280 |
| `checkbox` | 200 |
| `date-picker` | 200 |
| `time-picker` | 180 |

Heights match the `argument-widgets.md` defaults. Don't shrink a widget's height
unless the user asks — labels above inputs need ~20 px of headroom.

## Spacing between widgets

The literal canvas gap is `widgetGap` (default 12 px), but each widget already has
~14–20 px of internal label space on top. So the actual visual gap = 12 + label
height. Don't add extra padding manually unless something looks cramped.

## Rough heights for stacking math

| Widget | Approx visual height (incl. label) |
| --- | --- |
| `text-input` | 36 |
| `text-area` (rows=4) | 80 |
| `number-input` | 36 |
| `slider` | 50 |
| `checkbox` | 28 (no label-on-top) |
| `combobox` | 36 |
| `radio-group` (3 vertical options) | 80 |
| `file-picker` | 36 |
| `directory-picker` | 36 |
| `date-picker` | 36 |
| `time-picker` | 36 |

So a form with one text input + slider + checkbox lays out as:

```
y=24  text-input  (height 36)
y=72  slider      (24 + 36 + 12 = 72; height 50)
y=134 checkbox    (72 + 50 + 12 = 134; height 28)
```

## Multi-column

Only do this if asked. Place columns at `x = 24` and `x = 24 + colWidth + 24` (24 px
column gap). Verify total width fits within `window.width - 2*padding`.

## Group boxes

If wrapping a section in a `group-box`:

1. Place the group-box first at the section's top-left, with its full width / height
   covering the children.
2. Set children's `parentId` to the group-box's `id`.
3. Children's `x`, `y` are still in the **tab's** coordinate space, not relative to
   the parent. Position children inside the group-box's rectangle accordingly:
   typically `parent.x + 12`, `parent.y + 36` (room for the title).

## When the user asks for "two columns" or "side by side"

Default layout: two columns of equal width with 24 px gap.

```
left  column:  x=24,  width=440
right column:  x=488, width=440
```

Reduce widget widths to fit (e.g. `text-input` at 240 → 240, but the slider at 280
should drop to 240 or shorter to fit each column).

## When in doubt

Single tab, single column, `x=24`, vertical stack with the heights above. The user
will rearrange in the UIBuilder editor anyway — what matters is producing a file
that opens cleanly with no overlapping widgets.
