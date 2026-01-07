import yaml
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, ConfigDict

class RalphConfig(BaseModel):
    max_iters: int = 5
    timeout_per_iter: int = 300
    test_cmd: str = "pytest"
    stop_on_success: bool = True
    active_tools: list[str] = []

    model_config = ConfigDict(extra='ignore')

class ConfigManager:
    def __init__(self, config_path: Optional[Path] = None):
        if config_path:
            self.config_path = config_path
        else:
            # Default to ~/.config/future-ralph/config.yaml
            self.config_path = Path.home() / ".config" / "future-ralph" / "config.yaml"
    
    def load(self) -> RalphConfig:
        if not self.config_path.exists():
            return RalphConfig()
        
        try:
            with open(self.config_path, "r") as f:
                data = yaml.safe_load(f) or {}
                return RalphConfig(**data)
        except Exception:
            return RalphConfig()

    def save(self, config: RalphConfig):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w") as f:
            yaml.dump(config.model_dump(), f)
