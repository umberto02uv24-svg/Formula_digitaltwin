from fdt.database.repository import (
    initialize_database,
    insert_configuration,
)
from fdt.database.models import ConfigurationRecord
from fdt.database.importer import import_vehicle_parameters
from fdt.vehicle.config import FDT01_BASELINE_V1


def main() -> None:
    """Initialize the FDT01 V1.0 baseline."""

    initialize_database()

    configuration = ConfigurationRecord(
        vehicle_id="FDT01",
        version="1.0",
        name="Baseline",
        description="Initial Formula 4 baseline configuration",
    )

    insert_configuration(configuration)

    import_vehicle_parameters(
        FDT01_BASELINE_V1,
        "FDT01",
        "1.0",
    )

    print("FDT01 V1.0 baseline initialized.")


if __name__ == "__main__":
    main()