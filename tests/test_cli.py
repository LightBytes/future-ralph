from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from future_ralph.main import app

runner = CliRunner()

@patch("future_ralph.main.CodexAdapter")
@patch("future_ralph.main.ClaudeAdapter")
@patch("future_ralph.main.OpenCodeAdapter")
@patch("future_ralph.main.GeminiAdapter")
@patch("future_ralph.main.RunManager")
@patch("future_ralph.main.IterationEngine")
def test_run_command(mock_engine, mock_manager, mock_gemini, mock_opencode, mock_claude, mock_codex):
    # Setup mocks
    mock_gemini.return_value.detect.return_value = {"found": True}
    mock_gemini.return_value.capabilities.return_value.name = "gemini"
    
    mock_opencode.return_value.detect.return_value = {"found": False}
    mock_claude.return_value.detect.return_value = {"found": False}
    mock_codex.return_value.detect.return_value = {"found": False}

    mock_manager_instance = mock_manager.return_value
    mock_run = MagicMock()
    mock_run.id = "test-run-id"
    mock_manager_instance.create_run.return_value = mock_run

    mock_engine_instance = mock_engine.return_value
    mock_future = MagicMock()
    mock_future.result.exit_code = 0
    mock_future.score = 100
    mock_future.id = "future_2010"
    mock_engine_instance.execute_run.return_value = mock_future

    result = runner.invoke(app, ["run", "Fix bug"])
    
    assert result.exit_code == 0
    assert "Found agent: gemini" in result.stdout
    assert "Success! Best future: future_2010" in result.stdout

def test_status_command():
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "Status: No active runs." in result.stdout
