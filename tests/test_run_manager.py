from future_ralph.core.run_manager import RunManager
from pathlib import Path
import shutil

def test_run_creation():
    test_runs_dir = Path("test_runs")
    if test_runs_dir.exists():
        shutil.rmtree(test_runs_dir)
    
    manager = RunManager(base_dir=test_runs_dir)
    run = manager.create_run("Test Prompt")
    
    assert run.dir.exists()
    assert (run.dir / "run.jsonl").exists()
    
    # Cleanup
    shutil.rmtree(test_runs_dir)
