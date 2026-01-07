import typer
from typing_extensions import Annotated

from future_ralph.core.run_manager import RunManager
from future_ralph.core.engine import IterationEngine
from future_ralph.core.models import RunConfig
from future_ralph.adapters.gemini import GeminiAdapter
from future_ralph.adapters.opencode import OpenCodeAdapter
from future_ralph.adapters.claude import ClaudeAdapter
from future_ralph.adapters.codex import CodexAdapter
from pathlib import Path

app = typer.Typer(help="Future-Ralph: A Heterogeneous Agent Wrapper")

@app.command()
def run(
    prompt: str = typer.Argument(..., help="The task for agents to perform"),
    detach: bool = typer.Option(False, "--detach", "-d", help="Run in background"),
    max_iters: int = typer.Option(5, help="Maximum number of futures to explore"),
):
    """
    Run agents to explore possible futures.
    """
    typer.echo(f"Exploring futures for: {prompt}")
    
    manager = RunManager()
    run_obj = manager.create_run(prompt)
    typer.echo(f"Run ID: {run_obj.id}")
    
    if detach:
        typer.echo("Running in detached mode... (Not fully implemented)")
        return

    # Initialize all known adapters
    possible_adapters = [
        GeminiAdapter(),
        OpenCodeAdapter(),
        ClaudeAdapter(),
        CodexAdapter(),
    ]
    
    # Filter for available adapters
    adapters = []
    for adapter in possible_adapters:
        detection = adapter.detect()
        if detection["found"]:
            adapters.append(adapter)
            typer.echo(f"Found agent: {adapter.capabilities().name}")
    
    if not adapters:
        typer.echo("Error: No supported agents found. Please run 'future-ralph setup' or install an agent CLI.")
        # For demo purposes if no agents are installed, we warn but don't crash
        # raise typer.Exit(1)
        return
    
    config = RunConfig(max_iters=max_iters)
    engine = IterationEngine(run_obj, config)
    
    best_future = engine.execute_run(prompt, adapters)
    
    if best_future and best_future.result.exit_code == 0:
        typer.echo(f"Success! Best future: {best_future.id} (Score: {best_future.score})")
    else:
        typer.echo("Failed to find a successful future.")


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
