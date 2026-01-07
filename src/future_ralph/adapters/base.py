from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class AttemptResult:
    stdout: str
    stderr: str
    exit_code: int
    duration_seconds: float
    diff: Optional[str] = None
    cost_info: Dict[str, Any] = field(default_factory=dict)
    
@dataclass
class ToolCapabilities:
    name: str
    supports_model_selection: bool = False
    supports_non_interactive: bool = True
    cost_confidence: str = "opaque" # exact, estimated, opaque
    supported_env_keys: List[str] = field(default_factory=list)

class BaseAdapter(ABC):
    @abstractmethod
    def detect(self) -> Dict[str, Any]:
        """
        Detect if the tool is available.
        Returns a dict with 'found', 'binary_path', 'version', 'notes'.
        """
        pass

    @abstractmethod
    def capabilities(self) -> ToolCapabilities:
        """
        Return the capabilities of the tool.
        """
        pass

    @abstractmethod
    def run(self, prompt: str, cwd: str, model: Optional[str] = None, timeout: Optional[int] = None) -> AttemptResult:
        """
        Run the agent on the task.
        """
        pass
