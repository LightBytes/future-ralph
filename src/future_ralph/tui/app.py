from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Button, Label
from textual.containers import Container

class ToolDetectionScreen(Static):
    def compose(self) -> ComposeResult:
        yield Label("Tool Detection (Placeholder)")
        yield Label("Checking for OpenCode... [Found]")
        yield Label("Checking for Gemini... [Not Found]")

class SetupApp(App):
    CSS = """
    Screen {
        layout: vertical;
        align: center middle;
    }
    Container {
        border: solid green;
        padding: 1;
    }
    """
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("Future-Ralph Setup Assistant", classes="title"),
            Button("Start Detection", id="start"),
            ToolDetectionScreen(classes="hidden"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start":
            # Logic to switch screens or show detection would go here
            self.query_one(ToolDetectionScreen).remove_class("hidden")

def run_setup():
    app = SetupApp()
    app.run()
