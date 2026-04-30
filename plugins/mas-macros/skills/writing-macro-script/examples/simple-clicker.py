"""
Minimal example: open an app, tap N times at fixed coordinates, close.

No args form, no runtime dashboard — just the SDK.
"""
import time

import mas


PKG = "com.example.app"


def main() -> None:
    mas.open_app(PKG, timeout_ms=5000)

    for i in range(20):
        mas.click(540, 1200, delay_ms=300)
        time.sleep(0.2)
        print(f"tap {i + 1}/20")

    mas.close_app(PKG)


if __name__ == "__main__":
    main()
