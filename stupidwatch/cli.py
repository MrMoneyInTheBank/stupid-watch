import subprocess
import click
from .db import SessionRepository
from .timer import run_stopwatch


@click.group()
def cli():
    pass


@cli.command()
@click.argument("session_name")
def start(session_name: str) -> None:
    """Start a stopwatch for SESSION_NAME."""

    def on_stop(elapsed: float) -> None:
        SessionRepository.add_time(session_name, elapsed)
        session_info = SessionRepository.get_session(session_name)
        total_time = session_info.total_seconds if session_info else 0

        click.echo(f"\n⏱️  Session '{session_name}' ran for {elapsed:.2f} seconds.")
        click.echo(f"📊 Total for session '{session_name}': {total_time:.2f} seconds.")

    run_stopwatch(session_name, on_stop)


@cli.command()
def sessions() -> None:
    """List all sessions and their total times."""
    sessions = SessionRepository.list_sessions()
    if not sessions:
        click.echo("No sessions found.")
        return

    for session in sessions:
        name, total = session.name, session.total_seconds

        mins, secs = divmod(int(total), 60)
        hours, mins = divmod(mins, 60)
        click.echo(f"{name}: {hours}h {mins}m {secs}s")


@cli.command()
@click.argument("session_name")
def delete_session(session_name: str) -> None:
    """Delete a specific session."""
    SessionRepository.delete_session(session_name)


@cli.command()
@click.argument("session_name")
def tmux(session_name: str) -> None:
    """Coming soon."""
    # session_exists = subprocess.run(
    #     f"tmux has-session -t {session_name}", shell=True, stdout=subprocess.DEVNULL
    # )
    #
    # if session_exists.returncode == 0:
    #     click.echo(f"Tmux session: {session_name} already exists.")
    # else:
    #     subprocess.run(f"tmux new-session -d -s {session_name}", shell=True)
    #     subprocess.run(
    #         f'tmux send-keys -t {session_name} "watch start {session_name}" C-m',
    #         shell=True,
    #     )


if __name__ == "__main__":
    cli()
