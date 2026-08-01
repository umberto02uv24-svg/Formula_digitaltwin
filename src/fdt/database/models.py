from dataclasses import dataclass
from typing import Optional


@dataclass
class ParameterRecord:
    """Database representation of an engineering parameter."""

    name: str
    value: Optional[float]
    unit: str
    source: str
    confidence: str
    status: str
    vehicle_id: str
    configuration_version: str

@dataclass
class ConfigurationRecord:
    """Database representation of a vehicle configuration."""

    vehicle_id: str
    version: str
    name: str
    description: str
    parent_version: Optional[str] = None