import typer
import subprocess
from typing import Optional
import sys

from future_ralph.core.run_manager import RunManager
from future_ralph.core.engine import IterationEngine
from future_ralph.core.models import RunConfig
from future_ralph.core.config import ConfigManager
from future_ralph.adapters.gemini import GeminiAdapter
from future_ralph.adapters.opencode import OpenCodeAdapter
from future_ralph.adapters.claude import ClaudeAdapter
from future_ralph.adapters.codex import CodexAdapter

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points

from future_ralph.core.plugin import Plugin

_plugins: list[Plugin] = []
_config_manager = ConfigManager()


def load_plugins(app: typer.Typer):
    """Load plugins from entry points."""
    global _plugins
    try:
        discovered_plugins = entry_points(group="future_ralph.plugins")
        for entry_point in discovered_plugins:
            try:
                plugin_cls = entry_point.load()
                # Instantiate and register
                plugin = plugin_cls()
                if isinstance(plugin, Plugin):
                    plugin.register(app)
                    _plugins.append(plugin)
                elif hasattr(plugin, "register"):
                    plugin.register(app)
                    # If it doesn't strictly follow protocol but has register, we still add it
                    _plugins.append(plugin)  # type: ignore
            except Exception as e:
                typer.echo(f"Failed to load plugin {entry_point.name}: {e}")
    except Exception:
        # Graceful fallback if something goes wrong with entry_points
        pass


def trigger_post_run(
    run_id: str, prompt: str, status: str, best_future_id: Optional[str] = None
):
    for plugin in _plugins:
        if hasattr(plugin, "post_run"):
            try:
                plugin.post_run(run_id, prompt, status, best_future_id)
            except Exception as e:
                typer.echo(f"Plugin error in post_run: {e}")


app = typer.Typer(help="Future-Ralph: A Heterogeneous Agent Wrapper")

# Load plugins immediately
load_plugins(app)


@app.command()
def run(
    prompt: str = typer.Argument(..., help="The task for agents to perform"),
    detach: bool = typer.Option(False, "--detach", "-d", help="Run in background"),
    max_iters: Optional[int] = typer.Option(
        None, help="Maximum number of futures to explore"
    ),
):
    """
    Run agents to explore possible futures.
    """
    typer.echo(f"Exploring futures for: {prompt}")

    manager = RunManager()
    run_obj = manager.create_run(prompt)
    typer.echo(f"Run ID: {run_obj.id}")

    if detach:
        typer.echo("Starting detached run...")
        # Spawn background process
        iters_arg = str(max_iters) if max_iters is not None else "default"
        cmd = [
            sys.executable,
            "-m",
            "future_ralph.main",
            "internal-run",
            run_obj.id,
            prompt,
            iters_arg,
        ]
        subprocess.Popen(cmd, start_new_session=True)
        typer.echo("Run detached. Use 'future-ralph status' to check progress.")
        return

    _execute_run_logic(run_obj, prompt, max_iters)


@app.command(hidden=True)
def internal_run(run_id: str, prompt: str, max_iters_arg: str):
    """
    Internal command for detached execution.
    """
    manager = RunManager()
    run_obj = manager.get_run(run_id)
    if not run_obj:
        return

    max_iters = int(max_iters_arg) if max_iters_arg != "default" else None
    _execute_run_logic(run_obj, prompt, max_iters)


def _execute_run_logic(run_obj, prompt: str, max_iters: Optional[int]):
    # Load persistent config
    config = _config_manager.load()

    # Determine effective settings (CLI overrides Config)
    effective_max_iters = max_iters if max_iters is not None else config.max_iters

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
        # Check if tool is allowed by config (if list is empty, allow all)
        tool_name = adapter.capabilities().name
        if config.active_tools and tool_name not in config.active_tools:
            continue

        detection = adapter.detect()
        if detection["found"]:
            adapters.append(adapter)
            typer.echo(f"Found agent: {tool_name}")

    if not adapters:
        typer.echo(
            "Error: No supported agents found. Please run 'future-ralph setup' or install an agent CLI."
        )
        return

    run_config = RunConfig(
        max_iters=effective_max_iters,
        timeout_per_iter=config.timeout_per_iter,
        test_cmd=config.test_cmd,
        stop_on_success=config.stop_on_success,
    )
    engine = IterationEngine(run_obj, run_config)

    best_future = engine.execute_run(prompt, adapters)

    status = "failed"
    best_id = None
    if best_future and best_future.result and best_future.result.exit_code == 0:
        typer.echo(
            f"Success! Best future: {best_future.id} (Score: {best_future.score})"
        )
        status = "success"
        best_id = best_future.id
    else:
        typer.echo("Failed to find a successful future.")

    trigger_post_run(run_obj.id, prompt, status, best_id)


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
