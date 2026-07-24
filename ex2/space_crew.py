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
from datetime import datetime
from enum import Enum


class Rank(str, Enum):
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


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=10)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validat_contact_rule(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("ID Mission must with M.")

        commander_or_captain: bool = False
        for member in self.crew:
            if member.rank in (Rank.COMMANDER, Rank.CAPTAIN):
                commander_or_captain = True
                break
        if not commander_or_captain:
            raise ValueError(
                "Mission must have at least one Commander or Captain."
            )

        if self.duration_days > 365:
            experienced_count: int = 0
            for member in self.crew:
                if member.years_experience >= 5:
                    experienced_count += 1

            if experienced_count < len(self.crew) * 0.5:
                raise ValueError(
                    "Long missions need at least 50%"
                    " experienced crew (5+ years)"
                )

        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")

        return self


def Test_valid() -> None:
    print("Valid mission created:")
    try:
        Crew1 = CrewMember(
            member_id="SC001",
            name="Sarah Connor",
            rank=Rank.COMMANDER,
            age=45,
            specialization="Mission command",
            years_experience=15,
            is_active=True,
        )

        Crew2 = CrewMember(
            member_id="JS002",
            name="John Smith",
            rank=Rank.LIEUTENANT,
            age=45,
            specialization="Navigation",
            years_experience=15,
            is_active=True,
        )

        Crew3 = CrewMember(
            member_id="AJ003",
            name="Alice Johnson",
            rank=Rank.OFFICER,
            age=45,
            specialization="Engineering",
            years_experience=15,
            is_active=True,
        )

        Mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime(2026, 7, 24),
            duration_days=900,
            crew=[Crew1, Crew2, Crew3],
            budget_millions=2500.0,
        )

        print(f"Mission: {Mission.mission_name}")
        print(f"ID: {Mission.mission_id}")
        print(f"Destination: {Mission.destination}")
        print(f"Duration: {Mission.duration_days} days")
        print(f"Budget: ${Mission.budget_millions}M")
        print(f"Crew size : {len(Mission.crew)}")
        print("Crew members:")
        print(f"- {Crew1.name} ({Crew1.rank.value}) - {Crew1.specialization}")
        print(f"- {Crew2.name} ({Crew2.rank.value}) - {Crew2.specialization}")
        print(f"- {Crew3.name} ({Crew3.rank.value}) - {Crew3.specialization}")
    except ValidationError as e:
        print(e.errors()[0]['msg'])


def Test_invalid() -> None:
    try:
        C_inv1 = CrewMember(
            member_id="SC001",
            name="Sarah Connor",
            rank=Rank.CADET,
            age=45,
            specialization="Mission command",
            years_experience=15,
            is_active=True,
        )

        C_inv2 = CrewMember(
            member_id="JS002",
            name="John Smith",
            rank=Rank.LIEUTENANT,
            age=45,
            specialization="Navigation",
            years_experience=15,
            is_active=True,
        )

        C_inv3 = CrewMember(
            member_id="AJ003",
            name="Alice Johnson",
            rank=Rank.OFFICER,
            age=45,
            specialization="Engineering",
            years_experience=15,
            is_active=True,
        )

        Mission_invalid = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime(2026, 7, 24),
            duration_days=900,
            crew=[C_inv1, C_inv2, C_inv3],
            budget_millions=2500.0,
        )

        print(f"Mission: {Mission_invalid.mission_name}")
        print(f"ID: {Mission_invalid.mission_id}")
        print(f"Destination: {Mission_invalid.destination}")
        print(f"Duration: {Mission_invalid.duration_days} days")
        print(f"Budget: ${Mission_invalid.budget_millions}M")
        print(f"Crew size : {len(Mission_invalid.crew)}")
        print("Crew members:")
        print(
            f"- {C_inv1.name} ({C_inv1.rank.value}) - {C_inv1.specialization}"
        )
        print(
            f"- {C_inv2.name} ({C_inv2.rank.value}) - {C_inv2.specialization}"
        )
        print(
            f"- {C_inv3.name} ({C_inv3.rank.value}) - {C_inv3.specialization}"
        )
    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]['msg'].replace("Value error, ", ""))


def main() -> None:
    print("Space Mission Crew Validation")
    print("=========================================")
    Test_valid()
    print()
    print("=========================================")
    Test_invalid()


if __name__ == "__main__":
    main()
