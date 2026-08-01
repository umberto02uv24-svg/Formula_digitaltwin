from dataclasses import dataclass
from typing import Optional


@dataclass
class VehicleConfiguration:
    """A specific configuration of a vehicle."""

    vehicle_id: str
    version: str
    name: str
    description: str
    parent_version: Optional[str] = None