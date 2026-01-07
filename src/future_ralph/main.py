import typer
from typing_extensions import Annotated

app = typer.Typer(help="Future-Ralph: A Heterogeneous Agent Wrapper")

@app.command()
def run(
    prompt: str = typer.Argument(..., help="The task for agents to perform"),
    detach: bool = typer.Option(False, "--detach", "-d", help="Run in background"),
):
    """
    Run agents to explore possible futures.
    """
    typer.echo(f"Exploring futures for: {prompt}")
    if detach:
        typer.echo("Running in detached mode...")
    else:
        typer.echo("Running synchronously...")

@app.command()
def status():
    """
    Show status of running/detached futures.
    """
    typer.echo("Status: No active runs.")

@app.command()
def results(run_id: str):
    """
    Show results of a specific run.
    """
    typer.echo(f"Showing results for run: {run_id}")

@app.command()
def apply(future_id: str):
    """
    Apply a specific future to the current codebase.
    """
    typer.echo(f"Applying future: {future_id}")

@app.command()
def setup():
    """
    Launch the TUI setup assistant.
    """
    try:
        from future_ralph.tui.app import run_setup
        run_setup()
    except ImportError as e:
        typer.echo(f"Error importing TUI: {e}")
        typer.echo("Ensure 'textual' is installed.")

if __name__ == "__main__":
    app()
