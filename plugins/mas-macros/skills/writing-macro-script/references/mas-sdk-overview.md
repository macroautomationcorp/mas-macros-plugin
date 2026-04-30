# `mas` SDK overview

The `mas` package exposes a flat-ish API. Most calls are top-level (`mas.click`,
`mas.find_object`, `mas.save`); a few are namespaced (`mas.ui.set_text`).

## Import style

```python
import mas
```

That's it for normal use. Specific types and exceptions live in submodules:

```python
from mas.types import KeyCode, Region, Modifier
from mas.exceptions import (
    MASError, RPCError, DeviceNotConnectedError,
    ImageNotFoundError, TimeoutError, CommandFailedError,
)
```

## Namespace map

| Surface | Calls | Reference |
| --- | --- | --- |
| **Interaction** | `mas.click`, `mas.swipe`, `mas.input_text`, `mas.key_press` | `mas-interaction.md` |
| **Vision** | `mas.take_screenshot`, `mas.find_object`, `mas.find_objects`, `mas.find_any_object`, `mas.read_text`, `mas.wait_for_object` | `mas-vision.md` |
| **Storage** | `mas.save`, `mas.retrieve`, `mas.retrieve_all`, `mas.clear` | `mas-storage.md` |
| **App control** | `mas.open_app`, `mas.close_app`, `mas.get_app_state`, `mas.is_app_focused`, `mas.get_current_app` | `mas-app.md` |
| **Image registry** | `mas.images({...})`, `mas.ImageRef` | `mas-images.md` |
| **Device info** | `mas.get_device_info`, `mas.get_screen_size`, `mas.get_host_machine_id` | (small surface — see SDK source) |
| **Misc** | `mas.get_clipboard` | (small surface) |
| **Runtime UI** | `mas.ui.set_text`, `mas.ui.set_progress`, `mas.ui.add_data_point`, `mas.ui.append_text`, `mas.ui.set_table_data`, `mas.ui.wait_for_event`, `mas.ui.on_click`, `mas.ui.batch` | `mas-ui-quick-reference.md` |

## Types

Common types from `mas.types`:

- `Coordinates` — `tuple[int, int]` for `(x, y)` pixel positions.
- `Region` — `dataclass(x1, y1, x2, y2)` for rectangular regions in pixel space.
- `KeyCode` — `Enum` of hardware key codes (`KeyCode.HOME`, `KeyCode.BACK`, `KeyCode.ENTER`, `KeyCode.VOLUME_UP`, …).
- `Modifier` — `Enum` for key modifiers (`Modifier.SHIFT`, `Modifier.CTRL`, `Modifier.ALT`, `Modifier.META`).
- `Screenshot` — returned by `take_screenshot()`; has `base64`, `width`, `height`, `timestamp`.
- `ObjectMatch` — returned by `find_object()`; has `x`, `y`, `width`, `height`, `confidence`, `.center` property → `(cx, cy)`, `.template_id` → matched image id.
- `TextRecognitionResult` — returned by `read_text()`; has `.text` (full string) plus per-word data.
- `ColorConversion` — `Enum` for OCR pre-processing.
- `SearchStrategy` — `"first_match" | "best_match" | "priority_order"` for `find_any_object`.

## Exceptions

All exceptions inherit from `MASError`. Catch the specific ones you can recover
from; let unknown errors propagate.

- `RPCError` — base class for all RPC-layer errors.
- `DeviceNotConnectedError` — no device bound to this script's port. Usually fatal.
- `DeviceNotFoundError` — device disappeared mid-run.
- `ImageNotFoundError` — `find_object` / `wait_for_object` couldn't find the image. Often expected; handle locally.
- `TimeoutError` — server-side timeout (`continuous_mode`, `wait_for_object`). Often expected; handle locally.
- `CommandFailedError` — device-side command (click, swipe, …) failed.
- `ConnectionError` — couldn't reach the RPC server.
- `ParseError`, `InvalidRequestError`, `MethodNotFoundError`, `InvalidParamsError`, `InternalError` — typically programmer errors.

See `error-handling-patterns.md` for idiomatic usage.
