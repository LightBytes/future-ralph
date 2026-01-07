from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from enum import Enum
from future_ralph.adapters.base import AttemptResult

class FutureStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class Future:
    id: str
    year: int
    tool_name: str
    status: FutureStatus = FutureStatus.PENDING
    result: Optional[AttemptResult] = None
    score: float = 0.0
    is_treehouse: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RunConfig:
    max_iters: int = 5
    timeout_per_iter: int = 300
    test_cmd: str = "pytest"
    stop_on_success: bool = True
    auto_apply: bool = False
