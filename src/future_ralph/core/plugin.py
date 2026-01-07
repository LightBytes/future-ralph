from typing import Protocol, runtime_checkable, Any, Dict, List, Optional
import typer

@runtime_checkable
class Plugin(Protocol):
    def register(self, app: typer.Typer) -> None:
        """Register commands or functionality with the main Typer app."""
        ...

    def post_run(self, run_id: str, prompt: str, status: str, best_future_id: Optional[str] = None) -> None:
        """Called after a run completes."""
        ...

    def post_iteration(self, run_id: str, iteration: int, future_data: Dict[str, Any]) -> None:
        """Called after each iteration."""
        ...
