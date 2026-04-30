# `.uibrt` JSON schema

A `.uibrt` is a single JSON document describing a `RuntimeUI` project. The host
app reads it at runtime to render the DeviceCard's Runtime UI tab.

## Top-level shape

```json
{
  "version": 1,
  "projectType": "RuntimeUI",
  "meta": { "name": "My Dashboard", "createdAt": "...", "updatedAt": "..." },
  "widgets": [ /* flat widget list, see runtime-widgets.md */ ],
  "tabs": [ /* optional, see below */ ]
}
```

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `version` | `1` | yes | Always literal `1`. |
| `projectType` | `"RuntimeUI"` | yes | Must be this exact string. |
| `meta.name` | string | yes | Display name. |
| `meta.createdAt` | ISO 8601 string | yes | |
| `meta.updatedAt` | ISO 8601 string | yes | |
| `widgets` | array | yes | Flat list. Most dashboards use this. |
| `tabs` | array | no | Optional tab structure if the dashboard needs sections. |

## Widget envelope

Same envelope as `.uibproj` argument widgets:

```json
{
  "id": "runtimelabel_status",
  "kind": "runtime-label",
  "name": "status",
  "parentId": null,
  "x": 24, "y": 24, "width": 320, "height": 24, "padding": 0,
  "props": { /* see runtime-widgets.md */ }
}
```

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | Unique within the file. Format `<kindNoHyphens>_<8 hex chars>`. |
| `kind` | string | One of the 7 runtime widget kinds. |
| `name` | string | **Crucial** — this is the Python handle. Must match `^[a-zA-Z_][a-zA-Z0-9_]*$` and be unique. |
| `parentId` | string \| null | Always `null` for runtime widgets — runtime mode doesn't render group-boxes. |
| `x`, `y` | number | Pixel coordinates. |
| `width`, `height` | number | Pixel size. |
| `padding` | number | Optional. |

## `widgets` vs `tabs`

Most dashboards just use the flat `widgets` array. The `tabs` array is supported
for cases where you want section tabs inside the dashboard, but it's rarely needed
in practice — keep dashboards single-pane unless the user explicitly asks for tabs.

When `tabs` is present, the host app renders a tab strip and ignores the top-level
`widgets` array. Each tab object has the same shape as in `.uibproj`:

```json
{
  "id": "tab_x",
  "name": "Live",
  "order": 0,
  "widgets": [ /* runtime widgets */ ]
}
```

## Minimal valid file

```json
{
  "version": 1,
  "projectType": "RuntimeUI",
  "meta": {
    "name": "Untitled",
    "createdAt": "2026-05-01T00:00:00.000Z",
    "updatedAt": "2026-05-01T00:00:00.000Z"
  },
  "widgets": []
}
```
