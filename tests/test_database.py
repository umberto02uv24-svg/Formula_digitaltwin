import fdt.database.connection as database_connection

from fdt.database.importer import import_vehicle_parameters
from fdt.database.models import ParameterRecord,ConfigurationRecord
from fdt.database.repository import (
    get_parameters,
    get_configuration,
    initialize_database,
    insert_parameter,
    insert_configuration,
)
from fdt.vehicle.config import FDT01_BASELINE_V1


def test_database_initialization(tmp_path, monkeypatch):
    """Check that the database can be initialized."""

    test_database_path = tmp_path / "test_fdt.db"

    monkeypatch.setattr(
        database_connection,
        "DATABASE_PATH",
        test_database_path,
    )

    initialize_database()

    assert test_database_path.exists()


def test_parameter_insertion(tmp_path, monkeypatch):
    """Check that an engineering parameter can be inserted."""

    test_database_path = tmp_path / "test_fdt.db"

    monkeypatch.setattr(
        database_connection,
        "DATABASE_PATH",
        test_database_path,
    )

    initialize_database()

    parameter = ParameterRecord(
        name="test_parameter",
        value=123.0,
        unit="-",
        source="Unit test",
        confidence="High",
        status="Validated",
        vehicle_id="TEST",
        configuration_version="1.0"
    )

    insert_parameter(parameter)

    parameters = get_parameters("TEST", "1.0")

    assert len(parameters) == 1
    assert parameters[0].name == "test_parameter"
    assert parameters[0].value == 123.0


def test_vehicle_parameter_import(tmp_path, monkeypatch):
    """Check that all vehicle parameters can be imported."""

    test_database_path = tmp_path / "test_fdt.db"

    monkeypatch.setattr(
        database_connection,
        "DATABASE_PATH",
        test_database_path,
    )

    import_vehicle_parameters(
        FDT01_BASELINE_V1,
        "FDT01",
        "1.0",
    )

    parameters = get_parameters("FDT01", "1.0")

    assert len(parameters) > 0
    
def test_configuration_insertion(tmp_path, monkeypatch):
    """Check that a vehicle configuration can be inserted and retrieved."""

    test_database_path = tmp_path / "test_fdt.db"

    monkeypatch.setattr(
        database_connection,
        "DATABASE_PATH",
        test_database_path,
    )

    initialize_database()

    configuration = ConfigurationRecord(
        vehicle_id="FDT01",
        version="1.0",
        name="Baseline",
        description="Initial F4 baseline configuration",
    )

    insert_configuration(configuration)

    result = get_configuration("FDT01", "1.0")

    assert result is not None
    assert result.vehicle_id == "FDT01"
    assert result.version == "1.0"
    assert result.name == "Baseline"