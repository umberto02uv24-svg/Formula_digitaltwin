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