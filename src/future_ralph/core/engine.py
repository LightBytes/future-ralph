import subprocess
from typing import List
from future_ralph.core.models import Future, FutureStatus, RunConfig
from future_ralph.core.run_manager import Run
from future_ralph.core.scoring import DefaultScoringPolicy
from future_ralph.adapters.base import BaseAdapter

class IterationEngine:
    def __init__(self, run: Run, config: RunConfig):
        self.run = run
        self.config = config
        self.policy = DefaultScoringPolicy()
        self.futures: List[Future] = []

    def run_iteration(self, iteration: int, adapter: BaseAdapter, prompt: str) -> Future:
        year = 2000 + (iteration * 10)
        future_id = f"future_{year}"
        future = Future(id=future_id, year=year, tool_name=adapter.capabilities().name)
        self.futures.append(future)
        
        self.run.logger.log("iteration_started", {"iteration": iteration, "year": year, "tool": future.tool_name})
        
        future.status = FutureStatus.RUNNING
        
        # 1. Run Agent
        result = adapter.run(prompt, cwd=str(self.run.dir), timeout=self.config.timeout_per_iter)
        future.result = result
        
        # 2. Run Tests (in the directory where the agent made changes)
        # Note: In v1, we assume the agent modified files in the current repo or a copy.
        # For simplicity in this skeleton, we run the test command in the current CWD.
        # test_start = time.time()
        test_proc = subprocess.run(
            self.config.test_cmd, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        # test_duration = time.time() - test_start
        
        # Overwrite attempt exit code with test exit code if tests ran
        # This is a v1 simplification: success is defined by tests passing.
        future.result.exit_code = test_proc.returncode
        
        # 3. Score
        future.score = self.policy.score(future)
        future.status = FutureStatus.COMPLETED
        
        self.run.logger.log("iteration_completed", {
            "future_id": future.id,
            "score": future.score,
            "exit_code": future.result.exit_code
        })
        
        return future

    def execute_run(self, prompt: str, adapters: List[BaseAdapter]):
        for i in range(1, self.config.max_iters + 1):
            # Simple policy: cycle through adapters or just use the first for now
            adapter = adapters[(i - 1) % len(adapters)]
            
            future = self.run_iteration(i, adapter, prompt)
            
            if future.result and future.result.exit_code == 0 and self.config.stop_on_success:
                self.run.logger.log("run_success_stop", {"future_id": future.id})
                break
        
        best = self.policy.select_best(self.futures)
        if best:
            self.run.logger.log("best_future_selected", {"future_id": best.id, "score": best.score})
        
        return best
