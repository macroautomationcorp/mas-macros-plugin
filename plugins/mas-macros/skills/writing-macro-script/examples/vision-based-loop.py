"""
Vision-driven loop: find an image, tap it, wait for the next screen, repeat.

Demonstrates:
- mas.images() registry
- wait_for_object instead of busy-poll
- App-state guard between iterations
- ImageNotFoundError handling at the iteration boundary
"""
import time

import mas
from mas.exceptions import ImageNotFoundError


PKG = "com.example.app"

# Image IDs come from the macro's Image Library in the desktop app.
# Replace the 0s with your real IDs before running.
images = mas.images({
    "play_btn":    0,   # TODO
    "claim_btn":   0,   # TODO
    "home_screen": 0,   # TODO
})


def run_iteration() -> None:
    """One pass: tap Play, wait for the claim button, tap it, return home."""
    play = mas.wait_for_object(images.play_btn, timeout_ms=10000)
    if play is None:
        raise ImageNotFoundError("Play button never appeared")
    mas.click(*play.center)

    claim = mas.wait_for_object(images.claim_btn, timeout_ms=20000)
    if claim is None:
        raise ImageNotFoundError("Claim button never appeared")
    mas.click(*claim.center)

    # Return to home before the next iteration
    home = mas.wait_for_object(images.home_screen, timeout_ms=10000)
    if home is None:
        raise ImageNotFoundError("Did not return to home screen")


def main() -> None:
    mas.open_app(PKG, timeout_ms=5000)

    for i in range(50):
        if not mas.is_app_focused(PKG):
            print(f"[iter {i}] app not focused, restarting")
            mas.open_app(PKG, timeout_ms=10000)

        try:
            run_iteration()
            print(f"[iter {i}] done")
        except ImageNotFoundError as e:
            print(f"[iter {i}] missed an image, skipping: {e}")
            time.sleep(2)


if __name__ == "__main__":
    main()
