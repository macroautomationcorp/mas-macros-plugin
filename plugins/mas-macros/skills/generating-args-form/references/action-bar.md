# Action bar

The action bar sits below the tab content and holds the dialog's submit / dismiss
buttons. Every project has exactly one action bar. The default — Cancel + Run —
covers almost every macro; only deviate when the user asks.

## Shape

```json
"actionBar": {
  "alignment": "right",
  "buttons": [
    { "id": "action_cancel01", "text": "Cancel", "role": "cancel", "style": "secondary" },
    { "id": "action_run012345", "text": "Run", "role": "run", "style": "primary" }
  ]
}
```

| Field | Type | Notes |
| --- | --- | --- |
| `alignment` | `"right"` \| `"center"` \| `"left"` \| `"spread"` | Default `"right"`. |
| `buttons` | array | At least one button. Order is rendering order. |

## Button

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | Unique. Format `action_<8 chars>`. |
| `text` | string | Display label. |
| `role` | `"run"` \| `"cancel"` \| `"reset"` \| `"custom"` | Drives runner-dialog behaviour. |
| `style` | `"primary"` \| `"secondary"` \| `"danger"` | Visual variant. |

## Roles

- `run` — submit the form. The runner dialog reads the field values, builds the CLI args,
  and starts the macro. There is **always exactly one `run` button** in a normal form.
- `cancel` — close the dialog without running.
- `reset` — restore default values without closing.
- `custom` — does nothing on its own; the host app can listen for the click.

In Edit-Args mode (when the user clicks "Edit Args" on a DeviceCard rather than Run),
the host app relabels the `run` button to "Save" automatically — no need to add a
separate Save button in the .uibproj.

## Default

Always include this exact action bar unless the user asks otherwise:

```json
"actionBar": {
  "alignment": "right",
  "buttons": [
    { "id": "action_cancel01", "text": "Cancel", "role": "cancel", "style": "secondary" },
    { "id": "action_run012345", "text": "Run", "role": "run", "style": "primary" }
  ]
}
```
