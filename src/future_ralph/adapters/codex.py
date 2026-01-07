import shutil
import subprocess
import time
from typing import Any, Dict, Optional
from future_ralph.adapters.base import BaseAdapter, AttemptResult, ToolCapabilities


class CodexAdapter(BaseAdapter):
    def detect(self) -> Dict[str, Any]:
        # Checks for 'openai' CLI as a proxy for Codex/GPT access
        path = shutil.which("openai")
        if path:
            return {
                "found": True,
                "binary_path": path,
                "version": "unknown",
                "notes": [],
            }
        return {
            "found": False,
            "binary_path": None,
            "version": None,
            "notes": ["openai CLI not found in PATH"],
        }

    def capabilities(self) -> ToolCapabilities:
        return ToolCapabilities(
            name="codex",
            supports_model_selection=True,
            cost_confidence="exact",  # OpenAI often provides usage stats
            supported_env_keys=["OPENAI_API_KEY"],
        )

    def run(
        self,
        prompt: str,
        cwd: str,
        model: Optional[str] = "gpt-3.5-turbo",
        timeout: Optional[int] = None,
    ) -> AttemptResult:
        start_time = time.time()
        # Using openai CLI: openai chat completions create -m <model> -g user "<prompt>"
        cmd = [
            "openai",
            "chat",
            "completions",
            "create",
            "-m",
            model or "gpt-3.5-turbo",
            "-g",
            "user",
            prompt,
        ]

        try:
            result = subprocess.run(
                cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout
            )
            duration = time.time() - start_time

            return AttemptResult(
                stdout=result.stdout,
                stderr=result.stderr,
                exit_code=result.returncode,
                duration_seconds=duration,
                diff=None,
                cost_info={
                    "estimated_tokens": len(prompt) / 4
                },  # CLI output parsing would be needed for exact
            )
        except subprocess.TimeoutExpired:
            return AttemptResult(
                stdout="",
                stderr="Timeout expired",
                exit_code=124,
                duration_seconds=time.time() - start_time,
                diff=None,
            )
        except Exception as e:
            return AttemptResult(
                stdout="",
                stderr=str(e),
                exit_code=1,
                duration_seconds=time.time() - start_time,
                diff=None,
            )
