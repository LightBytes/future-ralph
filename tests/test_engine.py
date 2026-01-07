from unittest.mock import MagicMock, patch
from future_ralph.core.engine import IterationEngine
from future_ralph.core.models import RunConfig, FutureStatus
from future_ralph.core.run_manager import Run
from pathlib import Path
import shutil


def test_engine_execution():
    run_dir = Path("test_engine_run")
    if run_dir.exists():
        shutil.rmtree(run_dir)
    run_dir.mkdir()

    run_mock = MagicMock(spec=Run)
    run_mock.dir = run_dir
    run_mock.logger = MagicMock()

    config = RunConfig(max_iters=2, test_cmd="exit 0")
    engine = IterationEngine(run_mock, config)

    adapter_mock = MagicMock()
    adapter_mock.capabilities.return_value.name = "test_agent"
    adapter_mock.run.return_value.exit_code = 0
    adapter_mock.run.return_value.stdout = "OK"
    adapter_mock.run.return_value.stderr = ""
    adapter_mock.run.return_value.diff = "some diff"

    with patch("subprocess.run") as mock_test:
        mock_test.return_value.returncode = 0

        best = engine.execute_run("test prompt", [adapter_mock])

        assert best is not None
        assert best.status == FutureStatus.COMPLETED
        assert len(engine.futures) == 1  # Stopped on success

    shutil.rmtree(run_dir)
