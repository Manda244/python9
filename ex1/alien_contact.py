import sys
try:
    from pydantic import (
        BaseModel,
        Field,
        ValidationError,
        model_validator
    )
except ImportError:
    print("Error: 'pydantic module is not installed")
    print("Please run: pip install pydantic")
    sys.exit(1)
from typing import Optional
from datetime import datetime
from enum import Enum


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType 
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def validat_contact_rule(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError("ID must start with AC.")
        if (
            self.contact_type == ContactType.PHYSICAL 
            and
            not self.is_verified
        ):
            raise ValueError("Using physical contact, must be verified.")
        if (
            self.contact_type == ContactType.TELEPATHIC
            and
            not self.witness_count >= 3
        ):
            raise ValueError("Using telepathic contact, witness_count must be >= 3.")
        if not self.signal_strength > 0.7:
            raise ValueError("signal_strength must be > 0.7.")
        return self 


def Test_valid() -> None:
    try:
        alien = AlienContact(
            contact_id="AC_2024_001",
            timestamp="2026-07-30 14:15:06",
            location="Area 51, Nevada",
            contact_type=ContactType.RADIO,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
            is_verified=True,
        )
        print(f"ID: {alien.contact_id}")
        print(f"Type: {alien.contact_type.value}")
        print(f"Location: {alien.location}")
        print(f"Signal: {alien.signal_strength}/10")
        print(f"Duration: {alien.duration_minutes} minutes")
        print(f"Witnesses: {alien.witness_count}")
        print(f"Message: {alien.message_received}")
    except ValidationError as e:
        print(e.errors()[0]['msg'])


def Test_invalid() -> None:
    try:
        alien_invalid = AlienContact(
            contact_id="AC_2024_001",
            timestamp="2026-07-30 14:15:06",
            location="Area 51, Nevada",
            contact_type=ContactType.RADIO,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=2,
            message_received="Greetings from Zeta Reticuli",
            is_verified=True,
        )
        print(f"ID: {alien_invalid.contact_id}")
        print(f"Type: {alien_invalid.contact_type.value}")
        print(f"Location: {alien_invalid.location}")
        print(f"Signal: {alien_invalid.signal_strength}/10")
        print(f"Duration: {alien_invalid.duration_minutes} minutes")
        print(f"Witnesses: {alien_invalid.witness_count}")
        print(f"Message: {alien_invalid.message_received}")
    except ValidationError as e:
        print(e.errors()[0]['msg'])


def main() -> None:
    print("Alien Contact Log Validation")
    print("======================================")
    Test_valid()
    print()
    print("======================================")
    Test_invalid()


if __name__ == "__main__":
    main()
