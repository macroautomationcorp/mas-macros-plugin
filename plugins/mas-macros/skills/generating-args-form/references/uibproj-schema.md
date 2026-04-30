# `.uibproj` JSON schema

A `.uibproj` is a single JSON document describing a `ScriptRunnerWindow` project. The
UIBuilder loads it via `JSON.parse`; missing optional fields are filled with defaults.
This file documents the canonical shape — match it exactly when generating new files.

## Top-level shape

```json
{
  "version": 1,
  "projectType": "ScriptRunnerWindow",
  "meta": { "name": "My Macro Args", "createdAt": "...", "updatedAt": "..." },
  "window": { /* see below */ }
}
```

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `version` | `1` | yes | Always literal `1`. |
| `projectType` | `"ScriptRunnerWindow"` | yes | Must be this exact string. |
| `meta.name` | string | yes | Display name. Used as the runner dialog title default. |
| `meta.createdAt` | ISO 8601 string | yes | Use `new Date().toISOString()` semantics. |
| `meta.updatedAt` | ISO 8601 string | yes | Same as createdAt on first generate. |

## `window`

```json
{
  "id": "window_1",
  "title": "My Macro Args",
  "width": 980,
  "height": 640,
  "padding": 24,
  "widgetGap": 12,
  "script": {
    "command": "",
    "argumentStyle": "keyValue",
    "keyValueSeparator": "="
  },
  "actionBar": { /* see action-bar.md */ },
  "tabs": [ /* one or more, see below */ ]
}
```

| Field | Type | Default | Notes |
| --- | --- | --- | --- |
| `id` | string | `"window_1"` | Single-window apps don't need to vary this. |
| `title` | string | meta.name | Shown in the runner dialog. |
| `width` | number | `980` | Canvas width in pixels. |
| `height` | number | `640` | Canvas height in pixels. |
| `padding` | number | `24` | Inner padding. |
| `widgetGap` | number | `12` | Vertical gap between auto-stacked widgets. |
| `script.command` | string | `""` | Optional. Often empty — macros use `argparse` directly. |
| `script.argumentStyle` | `"keyValue"` | `"keyValue"` | Only value supported. |
| `script.keyValueSeparator` | `"="` | `"="` | Only value supported. |
| `actionBar` | object | required | See `action-bar.md`. |
| `tabs` | array | required | At least one tab. |

## `tabs[]`

```json
{
  "id": "tab_a1b2c3d4",
  "name": "General",
  "order": 0,
  "widgets": [ /* see argument-widgets.md and layout-widgets.md */ ]
}
```

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `id` | string | yes | Unique tab id. Format `tab_<8 hex chars>`. |
| `name` | string | yes | Display name. Becomes the argparse group name. |
| `order` | number | yes | 0-based; tabs render in ascending order. |
| `widgets` | array | yes | Empty array is fine. |

## `widgets[]` — common envelope

Every widget shares this envelope. Per-kind props go inside `props`.

```json
{
  "id": "textinput_a1b2c3d4",
  "kind": "text-input",
  "name": "input_path",
  "parentId": null,
  "x": 24,
  "y": 24,
  "width": 240,
  "height": 36,
  "padding": 8,
  "props": { /* per-kind, see argument-widgets.md / layout-widgets.md */ }
}
```

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | Format `<kindNoHyphens>_<8 hex chars>`. Must be unique. |
| `kind` | string | One of the widget kinds (see argument-widgets.md / layout-widgets.md). |
| `name` | string | Defaults to `id`. For runtime widgets this is the Python handle, but in args forms it's mostly editor-internal. |
| `parentId` | string \| null | If non-null, must be an existing `group-box` widget's id on the same tab. |
| `x`, `y` | number | Pixel coordinates from tab content origin. |
| `width`, `height` | number | Pixel size. See canvas-layout-tips.md for sane defaults. |
| `padding` | number | Optional. Internal padding. Most kinds default to `8`. |

## ID generation

The UIBuilder uses `crypto.randomUUID().slice(0, 8)` so IDs look like `tab_a1b2c3d4`,
`textinput_e5f67890`, etc. Generate any 8-char hex/alphanumeric slug — uniqueness
within the file is what matters.

## Minimal valid file

```json
{
  "version": 1,
  "projectType": "ScriptRunnerWindow",
  "meta": {
    "name": "Untitled",
    "createdAt": "2026-05-01T00:00:00.000Z",
    "updatedAt": "2026-05-01T00:00:00.000Z"
  },
  "window": {
    "id": "window_1",
    "title": "Untitled",
    "width": 980,
    "height": 640,
    "padding": 24,
    "widgetGap": 12,
    "script": { "command": "", "argumentStyle": "keyValue", "keyValueSeparator": "=" },
    "actionBar": {
      "alignment": "right",
      "buttons": [
        { "id": "action_cancel01", "text": "Cancel", "role": "cancel", "style": "secondary" },
        { "id": "action_run01234", "text": "Run", "role": "run", "style": "primary" }
      ]
    },
    "tabs": [
      { "id": "tab_general0", "name": "General", "order": 0, "widgets": [] }
    ]
  }
}
```
