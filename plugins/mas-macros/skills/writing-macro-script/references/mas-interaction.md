# `mas` interaction reference

Four functions for driving the device: `click`, `swipe`, `input_text`, `key_press`.

## `mas.click(x, y, delay_ms=1000)`

Single tap at `(x, y)` in pixel space.

```python
mas.click(150, 300)
mas.click(150, 300, delay_ms=500)
```

The `delay_ms` is a wait *after* the click so the UI has time to react. Default
1 s — drop it to 0–200 ms in tight loops.

Common: tap the centre of an `ObjectMatch`:

```python
match = mas.find_object(images.login_btn)
if match:
    mas.click(*match.center)
```

## `mas.swipe(from_coords, to_coords, duration_ms=1000)`

Swipe from one point to another.

```python
# Scroll up (swipe down)
mas.swipe((500, 500), (500, 1500), duration_ms=400)

# Drag-and-drop (slow swipe)
mas.swipe((200, 300), (800, 300), duration_ms=1000)
```

`duration_ms` controls swipe speed. Short (200–400 ms) for scrolling, longer
(800–1500 ms) for drag-and-drop where you need the gesture recognised as a hold.

## `mas.input_text(text, delay_ms=0)`

Type into the focused field. **You must click into the field first** — `input_text`
sends keystrokes to whatever has focus.

```python
mas.click(150, 200)              # focus the field
mas.input_text("user@example.com")
mas.input_text("password", delay_ms=300)
```

## `mas.key_press(key_code, modifiers=None, duration_ms=100)`

Press a hardware key.

```python
from mas.types import KeyCode, Modifier

mas.key_press(KeyCode.BACK)
mas.key_press(KeyCode.HOME)
mas.key_press(KeyCode.ENTER)
mas.key_press(KeyCode.POWER, duration_ms=3000)              # long press
mas.key_press(KeyCode.A, modifiers=[Modifier.CTRL])         # Ctrl+A (desktop)
```

Common Android `KeyCode`s: `BACK`, `HOME`, `MENU`, `ENTER`, `ESCAPE`, `SPACE`,
`VOLUME_UP`, `VOLUME_DOWN`, `POWER`, `CAMERA`. See `mas/types.py` for the full
enum.
