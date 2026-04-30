# `mas` vision reference

Six functions: `take_screenshot`, `find_object`, `find_objects`, `find_any_object`,
`read_text`, `wait_for_object`.

## `mas.take_screenshot() -> Screenshot`

Grab the current screen.

```python
ss = mas.take_screenshot()
print(f"{ss.width}x{ss.height} at {ss.timestamp}")
```

Useful for **reusing one capture across multiple lookups** instead of taking a
separate screenshot per `find_object` call:

```python
ss = mas.take_screenshot()
btn = mas.find_object(images.login_btn, screenshot=ss)
icon = mas.find_object(images.settings, screenshot=ss)
```

## `mas.find_object(image_id, *, threshold=0.8, screenshot=None, continuous_mode=False, timeout_ms=1000, capture_interval_ms=500, max_matches=1, search_region=None) -> ObjectMatch | None`

Template-match a single image against the screen. Returns the best match (with
confidence ≥ threshold) or `None`.

```python
images = mas.images({"login_btn": 123})

match = mas.find_object(images.login_btn)
if match:
    mas.click(*match.center)
```

- `threshold` — `0.0` to `1.0`. `0.8` is a sensible default. Raise to `0.9+` for
  stricter matching when many similar UI elements are on screen.
- `screenshot` — pass an existing capture to avoid re-grabbing.
- `continuous_mode=True` — keep retrying internally up to `timeout_ms`. Cheaper
  than a Python loop because the search runs server-side.
- `search_region` — `Region(x1, y1, x2, y2)` to restrict where to look. Speeds up
  matching and avoids false positives elsewhere on screen.

## `mas.find_objects(image_id, ..., max_matches=10) -> list[ObjectMatch]`

Like `find_object` but returns every match (sorted best-first) up to `max_matches`.

```python
matches = mas.find_objects(images.list_item, max_matches=20)
for m in matches:
    mas.click(*m.center)
```

## `mas.find_any_object(image_ids, ...) -> ObjectMatch | None`

Try several templates, return the first / best match. Useful when the same UI
element has variants (different languages, themes, states).

```python
match = mas.find_any_object(
    [images.btn_en, images.btn_fr, images.btn_es],
    search_strategy="best_match",
)
if match:
    print(f"Matched template id {match.template_id}")
    mas.click(*match.center)
```

`search_strategy`:
- `"first_match"` (default) — return first hit.
- `"best_match"` — try all, return highest confidence.
- `"priority_order"` — try in given order, return first that meets threshold.

## `mas.read_text(region=None, screenshot=None, model="eng_best", psm=7, color_conversion=ColorConversion.NONE, timeout_ms=30000) -> TextRecognitionResult`

Run OCR over the screen (or a region of it).

```python
from mas.types import Region

result = mas.read_text()                                   # whole screen
result = mas.read_text(region=Region(0, 0, 500, 100))      # top strip
print(result.text)
```

- `model` — Tesseract language pack. Default `"eng_best"`.
- `psm` — Tesseract page segmentation mode (1–13). `7` (single line) is good for
  buttons / labels; `6` (uniform block) for paragraphs; `3` (auto) for general use.
- `color_conversion` — pre-processing. `ColorConversion.GRAYSCALE` or
  `ColorConversion.BINARY` often improves matching on noisy backgrounds.
- Timeout is generous because OCR is slow.

## `mas.wait_for_object(image_id, timeout_ms=10000, threshold=0.8) -> ObjectMatch | None`

Block server-side until the image appears or the timeout expires. Use this
instead of busy-polling `find_object` from Python.

```python
mas.click(*menu_btn.center)
home = mas.wait_for_object(images.home_screen, timeout_ms=30000)
if home is None:
    raise TimeoutError("App didn't reach home screen in 30s")
```

## Common patterns

### Find-then-tap

```python
images = mas.images({"login": 123})
btn = mas.wait_for_object(images.login, timeout_ms=10000)
if btn is None:
    raise RuntimeError("Login button not visible")
mas.click(*btn.center)
```

### Multi-screenshot batch (one capture, many lookups)

```python
ss = mas.take_screenshot()
status = mas.find_object(images.status_ok, screenshot=ss)
banner = mas.find_object(images.banner, screenshot=ss)
```

### OCR a value off the screen

```python
result = mas.read_text(region=Region(120, 200, 600, 260), psm=7)
gold = int(result.text.replace(",", ""))
```
