from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    database_url: str = "sqlite:///career_track.db"
    log_dir: Path = Path("logs")
    log_file: Path = Path("logs/career_track.log")
    log_level: str = "INFO"


settings = Settings()