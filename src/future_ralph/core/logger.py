import json
import time
from pathlib import Path
from typing import Any, Dict, Optional


class RunLogger:
    def __init__(self, run_dir: Path):
        self.run_dir = run_dir
        self.log_file = run_dir / "run.jsonl"
        self._setup_logging()

    def _setup_logging(self):
        # We use a custom logger that writes JSONL
        pass

    def log(self, event: str, data: Optional[Dict[str, Any]] = None):
        entry = {"timestamp": time.time(), "event": event, "data": data or {}}
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def log_attempt(self, attempt_id: str, result: Dict[str, Any]):
        self.log("attempt_completed", {"attempt_id": attempt_id, "result": result})
