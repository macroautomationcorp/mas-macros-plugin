# `mas.images()` registry

Images used by `find_object` / `find_objects` / `find_any_object` / `wait_for_object`
are stored in the macro's **Image Library** in the desktop app. Each upload gets an
integer ID. The script declares those IDs once with readable names, then refers to
them by name.

## Why declare them

Without `mas.images(...)`, you'd be passing raw ints around:

```python
# bad — meaningless integers in code
mas.click(*mas.find_object(123).center)
```

With `mas.images(...)`, the code reads cleanly and a typo becomes an `AttributeError`
instead of a missing-image runtime failure deep in a loop:

```python
# good
images = mas.images({"login_btn": 123})
match = mas.find_object(images.login_btn)
```

## Usage

Declare once near the top of the script:

```python
import mas

images = mas.images({
    "login_btn":   123,
    "home_screen": 456,
    "settings":    789,
})
```

Then reference:

```python
mas.find_object(images.login_btn)
mas.find_objects(images.settings, max_matches=5)
mas.find_any_object([images.login_btn, images.home_screen])
mas.wait_for_object(images.home_screen, timeout_ms=10000)
```

## Rules

- Image names must be valid Python identifiers (`isidentifier()`).
- Recommended: `snake_case`, descriptive — `login_btn`, `home_screen`, `gold_icon`.
- `mas.images(...)` returns a read-only `ImageMap`. Each entry is an `ImageRef`
  with `.id` (int) and `.name` (str).
- An `ImageRef` works wherever a raw `int` is accepted (it's `__int__`-compatible
  and `__eq__`s by id).

## Where the IDs come from

The user uploads template images to the macro's Image Library via the desktop app's
asset panel. Each image gets an integer ID assigned by the host. **The script
doesn't generate these IDs — the user supplies them.**

When generating a macro that uses vision, ask the user for the IDs (or leave a
placeholder block at the top with comments instructing them to fill them in):

```python
images = mas.images({
    # Fill these in from the desktop app's Image Library:
    "login_btn":   0,   # TODO
    "home_screen": 0,   # TODO
})
```

## Cross-device portability

IDs are project-scoped, not device-scoped. The same `mas.images(...)` block works
on any device the macro runs against. Templates are matched against whatever
screenshot is captured on the running device.
