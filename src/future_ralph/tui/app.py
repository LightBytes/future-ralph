from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import (
    Header,
    Footer,
    Static,
    Button,
    Label,
    Input,
    Checkbox,
    DataTable,
)
from textual.screen import Screen
from future_ralph.core.config import ConfigManager, RalphConfig
from future_ralph.adapters.gemini import GeminiAdapter
from future_ralph.adapters.opencode import OpenCodeAdapter
from future_ralph.adapters.claude import ClaudeAdapter
from future_ralph.adapters.codex import CodexAdapter


class ToolDetection(Static):
    def on_mount(self) -> None:
        self.adapters = [
            GeminiAdapter(),
            OpenCodeAdapter(),
            ClaudeAdapter(),
            CodexAdapter(),
        ]
        self.detect_tools()

    def detect_tools(self) -> None:
        table = self.query_one(DataTable)
        table.clear()
        table.add_columns("Tool", "Status", "Path")

        self.found_tools = []

        for adapter in self.adapters:
            info = adapter.detect()
            status = "✅ Found" if info["found"] else "❌ Not Found"
            path = info.get("binary_path") or "N/A"
            if info["found"]:
                self.found_tools.append(adapter.capabilities().name)

            table.add_row(adapter.capabilities().name, status, path)

    def compose(self) -> ComposeResult:
        yield Label("Tool Detection", classes="section-title")
        yield DataTable()
        yield Button("Rescan", id="rescan")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "rescan":
            self.detect_tools()


class ConfigForm(Static):
    def compose(self) -> ComposeResult:
        yield Label("Global Settings", classes="section-title")
        yield Label("Test Command:")
        yield Input(placeholder="pytest", id="test_cmd", value="pytest")
        yield Label("Max Iterations:")
        yield Input(placeholder="5", id="max_iters", value="5")
        yield Label("Timeout (seconds):")
        yield Input(placeholder="300", id="timeout", value="300")
        yield Checkbox("Stop on Success", value=True, id="stop_success")


class SetupScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Vertical(
                ToolDetection(id="detection"),
                ConfigForm(id="config"),
                Horizontal(
                    Button("Save & Exit", variant="success", id="save"),
                    Button("Cancel", variant="error", id="cancel"),
                    classes="buttons",
                ),
            )
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.app.exit()
        elif event.button.id == "save":
            self.save_config()

    def save_config(self) -> None:
        detection = self.query_one(ToolDetection)

        test_cmd = self.query_one("#test_cmd", Input).value
        max_iters = int(self.query_one("#max_iters", Input).value or 5)
        timeout = int(self.query_one("#timeout", Input).value or 300)
        stop_success = self.query_one("#stop_success", Checkbox).value

        config = RalphConfig(
            max_iters=max_iters,
            timeout_per_iter=timeout,
            test_cmd=test_cmd,
            stop_on_success=stop_success,
            active_tools=detection.found_tools,
        )

        manager = ConfigManager()
        manager.save(config)
        self.app.exit(result="Saved")


class SetupApp(App):
    CSS = """
    Screen {
        layout: vertical;
        padding: 1;
    }
    .section-title {
        text-style: bold;
        margin-top: 1;
        margin-bottom: 1;
    }
    DataTable {
        height: auto;
        margin-bottom: 2;
    }
    .buttons {
        margin-top: 2;
        align: center middle;
        height: 3;
    }
    Button {
        margin-right: 2;
    }
    """

    def on_mount(self) -> None:
        self.push_screen(SetupScreen())


def run_setup():
    app = SetupApp()
    app.run()
