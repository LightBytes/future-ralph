from typing import Protocol, runtime_checkable
import typer

@runtime_checkable
class Plugin(Protocol):
    def register(self, app: typer.Typer) -> None:
        """Register commands or functionality with the main Typer app."""
        ...
