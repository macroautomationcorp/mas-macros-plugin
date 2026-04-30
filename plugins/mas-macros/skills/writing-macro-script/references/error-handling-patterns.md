# Error handling patterns

Macros run unattended for long periods. Good error handling is the difference
between "stops cleanly with a useful log line" and "spends 6 hours stuck on one
screen". Match the pattern to the operation.

## Exception cheat-sheet

```python
from mas.exceptions import (
    MASError,                 # base class for everything below
    RPCError,                 # base class for RPC-layer errors
    DeviceNotConnectedError,  # no device — usually fatal
    DeviceNotFoundError,      # device disappeared mid-run
    ImageNotFoundError,       # find_object / wait_for_object didn't find — often expected
    TimeoutError,             # wait_for_object / continuous_mode timed out
    CommandFailedError,       # device-side command failed (rare)
    ConnectionError,          # couldn't reach the RPC server
)
```

Catch the **specific** exception you can recover from. Let the rest propagate so
the run terminates with a real stack trace.

## Pattern: optional vision lookup

Don't `try/except` around `find_object` — it returns `None` when nothing matches.

```python
match = mas.find_object(images.banner)
if match:
    mas.click(*match.center)
# else just continue
```

## Pattern: mandatory vision wait with timeout

`wait_for_object` returns `None` on timeout (no exception). Convert to an explicit
error if the screen really must be reached:

```python
home = mas.wait_for_object(images.home_screen, timeout_ms=30000)
if home is None:
    raise RuntimeError("Did not reach home screen within 30s")
```

## Pattern: retry-on-transient-failure

Useful for things like emulator stalls or app crashes. Wrap a single iteration
of a loop, not the whole loop:

```python
for i in range(N):
    for attempt in range(3):
        try:
            do_iteration(i)
            break
        except CommandFailedError as e:
            mas.ui.append_text("log", f"[iter {i}] command failed: {e}, retry {attempt+1}/3")
            time.sleep(2)
    else:
        mas.ui.append_text("log", f"[iter {i}] giving up after 3 attempts")
        raise
```

## Pattern: app-state guard

Long-running macros benefit from periodically verifying the target app is still
in the foreground. Re-open if it crashed.

```python
PKG = "com.example.app"

for i in range(N):
    if not mas.is_app_focused(PKG):
        mas.ui.append_text("log", f"[iter {i}] app not focused, restarting")
        mas.open_app(PKG, timeout_ms=10000)

    do_iteration(i)
```

## Pattern: clean shutdown

Use `try/finally` to make sure resources / state are flushed even if the loop
errors out mid-run:

```python
results = []
try:
    for i in range(N):
        results.append(do_iteration(i))
finally:
    mas.save("scrape_results", {"completed": len(results), "items": results})
    mas.ui.set_text("status", f"Stopped at iteration {len(results)}/{N}")
```

## What NOT to do

### ❌ Catch-all `except Exception`

```python
try:
    do_thing()
except Exception:
    pass    # silent failure → debugging nightmare
```

If you really need to suppress something, log it:

```python
try:
    do_thing()
except CommandFailedError as e:
    mas.ui.append_text("log", f"command failed (continuing): {e}")
```

### ❌ Busy-poll instead of `wait_for_object`

```python
# bad — wasteful client-side polling
while True:
    if mas.find_object(images.home):
        break
    time.sleep(0.5)
```

```python
# good — server-side wait
home = mas.wait_for_object(images.home, timeout_ms=30000)
if home is None:
    raise TimeoutError("home screen never appeared")
```

### ❌ Catching `DeviceNotConnectedError` and continuing

The device is gone — there's nothing to do. Let it propagate so the run fails
loudly. The host app shows the error and the user reconnects.
