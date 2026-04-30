"""
Data-collection macro: walk a list of screens, OCR a value off each,
persist the results, and surface them in a runtime table.

Pairs with:
- A .uibrt defining `status` (runtime-label) and `results` (runtime-table)
  with columns ["Screen", "Value", "Status"].

Demonstrates:
- mas.read_text with a Region for OCR off a fixed strip
- mas.storage.save / retrieve to checkpoint progress across runs
- Rendering aggregated results in a runtime table
- Resume-from-last-checkpoint pattern
"""
import time

import mas
from mas.exceptions import ImageNotFoundError
from mas.types import Region


SCREENS = [f"screen_{i}" for i in range(20)]
TASK_NAME = "ocr_collection"

# Region of the screen where the value to OCR is rendered.
VALUE_REGION = Region(x1=120, y1=200, x2=600, y2=260)

# Image IDs from the desktop app's Image Library.
images = mas.images({
    "next_btn": 0,   # TODO
    "screen_loaded": 0,  # TODO
})


def parse_value(raw: str) -> int | None:
    cleaned = raw.replace(",", "").strip()
    try:
        return int(cleaned)
    except ValueError:
        return None


def main() -> None:
    state = mas.retrieve(TASK_NAME)
    start = state.get("last_index", 0)
    results: list[dict] = state.get("results", [])

    mas.ui.set_text("status", f"Resuming from index {start}/{len(SCREENS)}")
    mas.ui.set_table_data("results", [
        {"Screen": r["screen"], "Value": str(r["value"]), "Status": r["status"]}
        for r in results
    ])

    for i in range(start, len(SCREENS)):
        screen_id = SCREENS[i]
        mas.ui.set_text("status", f"Reading {screen_id} ({i + 1}/{len(SCREENS)})")

        # Tap Next, wait for the screen to render before OCR
        next_btn = mas.find_object(images.next_btn)
        if next_btn:
            mas.click(*next_btn.center)
        if mas.wait_for_object(images.screen_loaded, timeout_ms=10000) is None:
            row = {"screen": screen_id, "value": None, "status": "load timeout"}
        else:
            try:
                ocr = mas.read_text(region=VALUE_REGION, psm=7)
                value = parse_value(ocr.text)
                row = {
                    "screen": screen_id,
                    "value": value,
                    "status": "OK" if value is not None else f"unparseable: {ocr.text!r}",
                }
            except ImageNotFoundError as e:
                row = {"screen": screen_id, "value": None, "status": f"OCR failed: {e}"}

        results.append(row)

        mas.ui.append_table_row("results", {
            "Screen": row["screen"],
            "Value": str(row["value"]),
            "Status": row["status"],
        })

        # Checkpoint after every iteration
        mas.save(TASK_NAME, {"last_index": i + 1, "results": results})

        time.sleep(0.5)

    mas.ui.set_text("status", f"Done. Collected {sum(1 for r in results if r['value'] is not None)} / {len(results)} values.")


if __name__ == "__main__":
    main()
