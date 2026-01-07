import uuid
import datetime
from pathlib import Path
from typing import Optional
from future_ralph.core.logger import RunLogger


class Run:
    def __init__(self, run_id: str, run_dir: Path):
        self.id = run_id
        self.dir = run_dir
        self.logger = RunLogger(run_dir)


class RunManager:
    def __init__(self, base_dir: Path = Path("runs")):
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def create_run(self, prompt: str) -> Run:
        run_id = f"{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:8]}"
        run_dir = self.base_dir / run_id
        run_dir.mkdir()

        # Initialize run metadata
        run = Run(run_id, run_dir)
        run.logger.log("run_started", {"prompt": prompt, "run_id": run_id})
        return run

    def get_run(self, run_id: str) -> Optional[Run]:
        run_dir = self.base_dir / run_id
        if not run_dir.exists():
            return None
        return Run(run_id, run_dir)

    def list_runs(self):
        return sorted(
            [d.name for d in self.base_dir.iterdir() if d.is_dir()], reverse=True
        )
