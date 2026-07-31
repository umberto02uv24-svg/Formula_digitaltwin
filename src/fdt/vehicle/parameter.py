from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ParameterStatus(Enum):
    """Status of an engineering parameter."""

    TBD = "TBD"
    ESTIMATED = "Estimated"
    BENCHMARK = "Benchmark"
    CALCULATED = "Calculated"
    VALIDATED = "Validated"


class ConfidenceLevel(Enum):
    """Confidence level associated with a parameter."""

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


@dataclass
class EngineeringParameter:
    """Engineering parameter with traceability information."""

    value: Optional[float]
    unit: str
    source: str
    confidence: ConfidenceLevel
    status: ParameterStatus