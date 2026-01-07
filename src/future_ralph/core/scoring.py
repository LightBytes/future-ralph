from abc import ABC, abstractmethod
from typing import List, Optional
from future_ralph.core.models import Future, FutureStatus

class BaseScoringPolicy(ABC):
    @abstractmethod
    def score(self, future: Future) -> float:
        """Calculate a score for a completed future."""
        pass

    @abstractmethod
    def select_best(self, futures: List[Future]) -> Optional[Future]:
        """Select the best future from a list, excluding Treehouse if necessary."""
        pass

class DefaultScoringPolicy(BaseScoringPolicy):
    def score(self, future: Future) -> float:
        if not future.result:
            return -1.0
        
        score = 0.0
        # If tests passed (exit code 0)
        if future.result.exit_code == 0:
            score += 100.0
        else:
            # Penalize failures
            score -= 10.0
            
        # Penalize huge diffs (heuristic: smaller diffs are better if they work)
        if future.result.diff:
            score -= (len(future.result.diff) / 1000.0)
            
        return score

    def select_best(self, futures: List[Future]) -> Optional[Future]:
        # Filter for completed, non-treehouse futures
        valid_futures = [f for f in futures if f.status == FutureStatus.COMPLETED and not f.is_treehouse]
        if not valid_futures:
            return None
        
        return max(valid_futures, key=lambda f: f.score)
