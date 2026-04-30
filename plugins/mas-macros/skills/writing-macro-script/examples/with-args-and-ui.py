"""
Args-driven loop with a live runtime dashboard.

Pairs with:
- A .uibproj defining a "General" tab with `iterations` (slider) and `dry_run` (checkbox).
- A .uibrt defining `status` (runtime-label), `main_bar` (runtime-progress),
  `cpu_chart` (runtime-chart, line), and `log` (runtime-textarea).

Demonstrates:
- Reading args via from src.script_args import args
- mas.ui.* updates batched per iteration to minimise RPC chatter
- Status / progress / chart / log driven from one loop
"""
import time

import mas
from src.script_args import args


def main() -> None:
    n = int(args.general.iterations)
    dry_run = bool(args.general.dry_run)

    mas.ui.set_text("status", "Starting...")
    mas.ui.set_progress("main_bar", 0)
    mas.ui.append_text("log", f"Begin run (n={n}, dry_run={dry_run})")

    for i in range(n):
        # Pretend work
        time.sleep(0.1)
        cpu = 30 + (i * 7) % 50

        # Drive every widget in one RPC round-trip
        with mas.ui.batch():
            mas.ui.set_text("status", f"Iteration {i + 1}/{n}")
            mas.ui.set_progress("main_bar", int((i + 1) / n * 100))
            mas.ui.add_data_point("cpu_chart", value=cpu, label=f"t={i}", series="CPU")
            if i % 10 == 0:
                mas.ui.append_text("log", f"[{i + 1}/{n}] CPU={cpu}%")

        if not dry_run:
            mas.click(540, 1200, delay_ms=200)

    mas.ui.set_text("status", "Done")
    mas.ui.append_text("log", "Run complete")


if __name__ == "__main__":
    main()
