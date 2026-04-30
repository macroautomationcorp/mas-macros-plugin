# Layout widgets

Three widget kinds are visual-only — they don't produce CLI arguments and aren't
included in the argparse generator output. Useful for grouping and labelling.

## `label`

Static text. Use to add a heading or instructional sentence above a group of inputs.

```json
{
  "id": "label_intro001",
  "kind": "label",
  "name": "label_intro001",
  "parentId": null,
  "x": 24, "y": 24, "width": 320, "height": 24, "padding": 0,
  "props": {
    "text": "Connection settings",
    "fontSize": 14
  }
}
```

| Prop | Type | Notes |
| --- | --- | --- |
| `text` | string | Required. The displayed text. |
| `fontSize` | number | Optional. Default 14 px. |

Default size: 200 × 24 px.

## `separator`

Horizontal or vertical rule, optionally with a label baked into the line.

```json
{
  "id": "separator_a1b2c3d4",
  "kind": "separator",
  "name": "separator_a1b2c3d4",
  "parentId": null,
  "x": 24, "y": 60, "width": 320, "height": 1, "padding": 0,
  "props": {
    "direction": "horizontal",
    "label": "Advanced"
  }
}
```

| Prop | Type | Notes |
| --- | --- | --- |
| `direction` | `"horizontal"` \| `"vertical"` | Required. |
| `label` | string | Optional. Renders inline. |

Default size: 320 × 1 (horizontal) or 1 × 200 (vertical).

## `group-box`

A bordered container. Other widgets can declare it as their `parentId` to render
inside it. The group-box itself is just a frame with a title.

```json
{
  "id": "groupbox_settings",
  "kind": "group-box",
  "name": "groupbox_settings",
  "parentId": null,
  "x": 24, "y": 100, "width": 400, "height": 200, "padding": 12,
  "props": {
    "title": "Output settings"
  }
}
```

| Prop | Type | Notes |
| --- | --- | --- |
| `title` | string | Required. Rendered in the top-left of the border. |

To put a widget inside a group-box, set its `parentId` to the group-box's `id`. The
child's `x`, `y` are still in the tab's coordinate space (not relative to the parent).

Default size: 400 × 200 px.

## When to use these

- A single label above a section of related fields → `label`.
- A horizontal rule between two visually distinct groups of fields → `separator`.
- A bordered box that visually clusters several fields together with its own title → `group-box`.

For most simple forms a single tab with widgets stacked vertically is enough — layout
widgets are purely cosmetic and don't change the runner dialog's behaviour.
