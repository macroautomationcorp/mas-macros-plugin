# Canvas layout tips (runtime dashboards)

Same coordinate system as `.uibproj`: absolute pixels, single canvas per widgets list.
The runtime UI renders inside the DeviceCard, which is narrow — keep dashboards
single-column unless the user asks for more.

## Defaults

- The runtime UI panel inside the DeviceCard is roughly 460 px wide × 480 px tall on
  the default layout.
- Use `x = 24`, `width = 360–440` for widgets to fit comfortably with margin.
- Heights: see runtime-widgets.md.

## Vertical stack pattern

Same as args forms — start at `y = 24`, gap of 12 px between widgets:

```
y = 24
y = 24 + h1 + 12
y = 24 + h1 + 12 + h2 + 12
...
```

## Approx heights for stacking math

| Widget | Approx height |
| --- | --- |
| runtime-label | 32 |
| runtime-progress | 40 (or 60 if `label` is set) |
| runtime-chart | 280 |
| runtime-textarea | 200 |
| runtime-table | 240 |
| runtime-button | 36 |
| runtime-input | 60 (with label) / 36 (without) |

## Common dashboard layouts

### Status + progress (vertical)

```
y=24   status label  (height 32, width 360)
y=68   progress bar  (24+32+12=68; height 40, width 360)
```

### Status + chart

```
y=24   status label
y=68   chart (height 280, width 440)
```

### Log dashboard

```
y=24   status label
y=68   progress
y=120  textarea (height 280, width 440)
```

### Interactive

```
y=24   status label
y=68   input (label "Filter")
y=140  table (height 240, width 440)
y=392  button (height 36, width 160)
```

## Charts

Charts need real estate — at least 240 px tall to be readable. Default width 440
fits the DeviceCard panel; if the user has a wider canvas (rare for runtime UIs)
push to 480.

## Tables

Tables also need height. 240 px shows ~6 compact rows. If the user expects many
rows, set `scrollable: true` (the default) and let it scroll within the widget.

## Don't try to be precise

The DeviceCard's runtime UI panel is itself resizable; widget positions get clipped
or scrolled inside the panel. Aim for a sensible vertical stack with the right
ordering — exact pixel placement matters less than in argument forms because the
user isn't comparing it to a pre-run dialog mockup.
