from future_ralph.adapters.gemini import GeminiAdapter
from unittest.mock import patch, MagicMock

def test_gemini_detection():
    adapter = GeminiAdapter()
    with patch("shutil.which", return_value="/usr/bin/gemini"):
        detection = adapter.detect()
        assert detection["found"] is True
        assert detection["binary_path"] == "/usr/bin/gemini"

def test_gemini_run():
    adapter = GeminiAdapter()
    with patch("subprocess.run") as mock_run:
        mock_result = MagicMock()
        mock_result.stdout = "Output"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        result = adapter.run("Test prompt", cwd=".", timeout=10)
        
        assert result.exit_code == 0
        assert result.stdout == "Output"
        mock_run.assert_called_once()
