import sys
try:
    from pydantic import BaseModel, Field, ValidationError
except ImportError:
    print("Error: 'pydantic module is not installed")
    print("Please run: pip install pydantic")
    sys.exit(1)
from typing import Optional
from datetime import datetime
from enum import Enum


class Rank(Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


def main() -> None:


if __name__ == "__main__":
    main()
