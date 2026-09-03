from dataclasses import dataclass


@dataclass
class Company:
    name: str
    website: str | None = None
    industry: str | None = None
    location: str | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Company name cannot be empty.")
