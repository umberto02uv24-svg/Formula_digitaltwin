import fdt.database.connection as database_connection

from fdt.database.importer import import_vehicle_parameters
from fdt.database.models import ParameterRecord
from fdt.database.repository import (
    get_parameters,
    initialize_database,
    insert_parameter,
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
    )

    insert_parameter(parameter)

    parameters = get_parameters("TEST")

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
    )

    parameters = get_parameters("FDT01")

    assert len(parameters) > 0