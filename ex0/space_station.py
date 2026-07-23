import sys
try:
    from pydantic import BaseModel, Field, ValidationError
except ImportError:
    print("Error: 'pydantic module is not installed")
    print("Please run: pip install pydantic")
    sys.exit(1)
from typing import Optional
from datetime import datetime


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    try:
        space = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2026, 7, 22, 7, 30, 0),
        )
        print("========================================")
        print("Valid station created:")
        print(f"ID: {space.station_id}")
        print(f"Name: {space.name}")
        print(f"Crew: {space.crew_size} people")
        print(f"Power: {space.power_level}%")
        print(f"Oxygen: {space.oxygen_level}%")
        if space.is_operational:
            print("Status: Operational")
        else:
            print("Status: Not Operational")
        print()
        print("========================================")
    except ValidationError as e:
        print(f"Expected validation error: {e}")

    try:
        space_invalide = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=25,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2026, 7, 22, 7, 30, 0),
        )
        print("========================================")
        print("Valid station created:")
        print(f"ID: {space_invalide.station_id}")
        print(f"Name: {space_invalide.name}")
        print(f"Crew: {space_invalide.crew_size} people")
        print(f"Power: {space_invalide.power_level}%")
        print(f"Oxygen: {space_invalide.oxygen_level}%")
        if space_invalide.is_operational:
            print("Status: Operational")
        else:
            print("Status: Not Operational")
        print()
        print("========================================")
    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]['msg'])


if __name__ == "__main__":
    main()
