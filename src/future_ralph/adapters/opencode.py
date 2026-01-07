import shutil
import subprocess
import time
from typing import Any, Dict, Optional
from future_ralph.adapters.base import BaseAdapter, AttemptResult, ToolCapabilities


class OpenCodeAdapter(BaseAdapter):
    def detect(self) -> Dict[str, Any]:
        path = shutil.which("opencode")
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
            "notes": ["opencode CLI not found in PATH"],
        }

    def capabilities(self) -> ToolCapabilities:
        return ToolCapabilities(
            name="opencode",
            supports_model_selection=True,
            cost_confidence="estimated",  # Assuming local/hybrid
            supported_env_keys=["OPENCODE_API_KEY"],
        )

    def run(
        self,
        prompt: str,
        cwd: str,
        model: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> AttemptResult:
        start_time = time.time()
        cmd = ["opencode", "run", prompt]
        if model:
            cmd.extend(["--model", model])

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
                diff=None,  # Future: capture diff
                cost_info={"estimated_tokens": len(prompt) / 4},
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
