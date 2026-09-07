from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///career_track.db",
    )
    log_dir: Path = Path("logs")
    log_file: Path = Path("logs/career_track.log")
    log_level: str = "INFO"


settings = Settings()