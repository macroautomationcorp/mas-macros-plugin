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

A `.uibrt` is in **one of two modes**, never both:

- **Flat mode** — the top-level `widgets` array holds every widget; `tabs` is
  absent or empty. Right for single-pane dashboards (the common case).
- **Tabbed mode** — `tabs` is a non-empty array; the top-level `widgets` array
  is empty. The host renders a tab strip and only shows the active tab's
  widgets. Reach for this when the dashboard naturally splits into sections
  (e.g. "Live" vs "Summary", or a per-stage breakdown).

When `tabs` is present, the host app **ignores the top-level `widgets` array**
— anything you leave there is invisible at runtime. Keep flat `widgets: []` in
tabbed files to make this explicit.

Each tab object:

```json
{
  "id": "tab_x",
  "name": "Live",
  "order": 0,
  "widgets": [ /* runtime widgets */ ]
}
```

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | Unique. Format `tab_<8 hex chars>` matches what the editor generates. |
| `name` | string | Shown on the tab strip. Free-form. |
| `order` | number | Render order, left to right. Zero-indexed. |
| `widgets` | array | Same widget envelope as flat mode. |

### Editor parity notes

The UIBuilder editor enforces a few invariants on tabbed runtime files.
Hand-written `.uibrt`s should respect them so they round-trip cleanly:

- **Adding the first tab to an existing flat file** migrates every widget from
  the flat array into a new `Tab 1`, then creates an empty `Tab 2` next to it.
  If you're generating a tabbed file from scratch, just emit two tabs directly.
- **Deleting back down to one tab** collapses to flat mode — the remaining
  tab's widgets are hoisted into the top-level `widgets` array and `tabs` is
  removed. So a "tabbed file with exactly one tab" never persists from the
  editor; treat it as a transient state if you ever observe it.
- Widget `name` fields are still globally unique across all tabs (Python
  addresses widgets by name, not by tab).

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
