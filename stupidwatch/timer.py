import time
import signal
import sys
from typing import Callable
from rich.console import Console
from rich.live import Live
from rich.text import Text

console = Console()


def run_stopwatch(session_name: str, on_stop: Callable[[float], None]) -> None:
    start_time = time.time()

    def handle_exit(signum, frame):
        elapsed = time.time() - start_time
        on_stop(elapsed)
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    frames = ["⏳", "⌛️"]
    frame_index = 0

    with Live(console=console, refresh_per_second=4) as live:
        while True:
            elapsed = time.time() - start_time
            mins, secs = divmod(int(elapsed), 60)
            hours, mins = divmod(mins, 60)
            display = Text(
                f"{frames[frame_index % len(frames)]}  {session_name}: {hours}h {mins}m {secs}s (Ctrl+C to stop)",
                style="bold green",
            )
            live.update(display)
            frame_index += 1
            time.sleep(0.5)
