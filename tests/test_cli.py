from typer.testing import CliRunner
from future_ralph.main import app

runner = CliRunner()

def test_run_command():
    result = runner.invoke(app, ["run", "Fix bug"])
    assert result.exit_code == 0
    assert "Exploring futures for: Fix bug" in result.stdout

def test_status_command():
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "Status: No active runs." in result.stdout
