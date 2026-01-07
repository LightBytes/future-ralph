from future_ralph.adapters.gemini import GeminiAdapter
from future_ralph.adapters.opencode import OpenCodeAdapter
from future_ralph.adapters.claude import ClaudeAdapter
from future_ralph.adapters.codex import CodexAdapter
from unittest.mock import patch, MagicMock

def test_gemini_detection():
    adapter = GeminiAdapter()
    with patch("shutil.which", return_value="/usr/bin/gemini"):
        detection = adapter.detect()
        assert detection["found"] is True
        assert detection["binary_path"] == "/usr/bin/gemini"

def test_opencode_detection():
    adapter = OpenCodeAdapter()
    with patch("shutil.which", return_value="/usr/bin/opencode"):
        detection = adapter.detect()
        assert detection["found"] is True
        assert detection["binary_path"] == "/usr/bin/opencode"

def test_claude_detection():
    adapter = ClaudeAdapter()
    with patch("shutil.which", return_value="/usr/bin/claude"):
        detection = adapter.detect()
        assert detection["found"] is True
        assert detection["binary_path"] == "/usr/bin/claude"

def test_codex_detection():
    adapter = CodexAdapter()
    with patch("shutil.which", return_value="/usr/bin/openai"):
        detection = adapter.detect()
        assert detection["found"] is True
        assert detection["binary_path"] == "/usr/bin/openai"