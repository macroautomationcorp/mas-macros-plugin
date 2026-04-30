# `mas` app control reference

Five functions for controlling Android applications by package name.

## Finding the package name

The `package_name` argument is the Android package identifier — never the
human-readable app name. The fastest way to look it up is the Google Play Store
URL: open the app's page and read the `id=` query parameter.

For example, **Puzzle Bricks Legend**:

```
https://play.google.com/store/apps/details?id=com.puzzlegames.puzzlebrickslegend&hl=en
                                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                              package_name = com.puzzlegames.puzzlebrickslegend
```

If the user gives a Play Store URL or just the app name, extract the `id=` param
or ask them to look it up — don't guess. Inventing a package name (e.g.
`com.example.app`, `com.companyname.appname`) will silently fail with
`get_app_state(...) == 0` (NOT_INSTALLED) at runtime.

## `mas.open_app(package_name, timeout_ms=2000) -> None`

Launch (or resume) an app. Blocks up to `timeout_ms` waiting for the app to
become foreground.

```python
mas.open_app("com.instagram.android")
mas.open_app("com.example.app", timeout_ms=5000)
```

## `mas.close_app(package_name) -> None`

Force-stop the app.

```python
mas.close_app("com.instagram.android")
```

## `mas.get_app_state(package_name) -> int`

Numeric state code:

| Code | Meaning |
| --- | --- |
| `4` | Running in foreground |
| `3` | Running in background |
| `2` | Running in background, suspended |
| `1` | Not running (installed but stopped) |
| `0` | Not installed |

```python
state = mas.get_app_state("com.example.app")
if state == 0:
    raise RuntimeError("Target app is not installed")
if state != 4:
    mas.open_app("com.example.app")
```

## `mas.is_app_focused(package_name) -> bool`

Convenience wrapper for `get_app_state(...) == 4`.

```python
if not mas.is_app_focused("com.example.app"):
    mas.open_app("com.example.app")
```

## `mas.get_current_app() -> str`

Package name of whatever's currently in the foreground.

```python
current = mas.get_current_app()
print(f"Current app: {current}")
```

## Common patterns

### Open if not already open

```python
PKG = "com.example.app"

if not mas.is_app_focused(PKG):
    mas.open_app(PKG, timeout_ms=5000)
```

### Restart

```python
PKG = "com.example.app"
mas.close_app(PKG)
mas.open_app(PKG)
```

### Detect crash mid-loop

```python
PKG = "com.example.app"

for i in range(100):
    do_step(i)
    if not mas.is_app_focused(PKG):
        mas.ui.append_text("log", f"App crashed at step {i}, restarting")
        mas.open_app(PKG)
```
