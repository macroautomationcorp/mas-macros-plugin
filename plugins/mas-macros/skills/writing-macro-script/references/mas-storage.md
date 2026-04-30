# `mas.storage` reference

Persistent JSON-style key-value storage scoped to a (machine, port, task) triple.
Useful for resuming runs across executions, accumulating results, sharing state
between scheduled runs of the same macro.

The data lives on the host's local SQLite store, not on the device.

## Composite key

Every saved entry is keyed by `(machine_id, port, task_name)`:

- `machine_id` — defaults to `mas.get_host_machine_id()` (the host PC's id).
- `port` — defaults to the device's port (`mas.get_current_device_port()`).
- `task_name` — caller-supplied. Pick a stable string per macro/task.

Saving the same key updates in place. Different ports for the same `task_name`
get separate entries — useful when running the same macro across multiple
emulators in a group.

## `mas.save(task_name, data, machine_id=None, port=0) -> bool`

```python
mas.save("daily_summary", {
    "gold_collected": 12500,
    "runs_completed": 8,
    "last_run_at": "2026-05-01T10:30:00Z",
})
```

`data` must be JSON-serialisable (dicts, lists, str, int, float, bool, None).
Returns `True` on success.

## `mas.retrieve(task_name, machine_id=None, port=0) -> dict`

Returns the stored dict, or `{}` if nothing saved yet.

```python
state = mas.retrieve("daily_summary")
gold = state.get("gold_collected", 0)
```

## `mas.retrieve_all(task_name) -> list[dict]`

All entries for the given `task_name` across every (machine, port). Useful for
"summary across all devices" patterns.

```python
results = mas.retrieve_all("daily_summary")
total_gold = sum(r.get("gold_collected", 0) for r in results)
```

## `mas.clear(task_name, machine_id=None, port=0) -> bool`

Delete one entry.

```python
mas.clear("daily_summary")
```

## Common patterns

### Resume from last checkpoint

```python
state = mas.retrieve("crawler")
start_index = state.get("last_index", 0)

for i in range(start_index, total):
    do_step(i)
    mas.save("crawler", {"last_index": i + 1})
```

### Per-device counters

```python
state = mas.retrieve("counter")
state["runs"] = state.get("runs", 0) + 1
mas.save("counter", state)
```

### Aggregate across all devices in a group

```python
results = mas.retrieve_all("scrape_results")
mas.ui.set_table_data("totals", [
    {"Device": r.get("device", "?"), "Items": str(r.get("count", 0))}
    for r in results
])
```
