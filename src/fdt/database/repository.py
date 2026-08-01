from .connection import get_connection
from .models import ParameterRecord,ConfigurationRecord


def initialize_database() -> None:
    """Create the database tables if they do not exist."""

    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS parameters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            value REAL,
            unit TEXT NOT NULL,
            source TEXT NOT NULL,
            confidence TEXT NOT NULL,
            status TEXT NOT NULL,
            vehicle_id TEXT NOT NULL,
            configuration_version TEXT NOT NULL,
            UNIQUE(vehicle_id, configuration_version, name)
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS configurations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id TEXT NOT NULL,
            version TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            parent_version TEXT,
            UNIQUE(vehicle_id, version)
        )
        """
    )

    connection.commit()
    connection.close()


def insert_parameter(parameter: ParameterRecord) -> None:
    """Insert an engineering parameter into the database."""

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO parameters (
            name,
            value,
            unit,
            source,
            confidence,
            status,
            vehicle_id,
            configuration_version
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(vehicle_id, configuration_version, name)
        DO UPDATE SET
            value = excluded.value,
            unit = excluded.unit,
            source = excluded.source,
            confidence = excluded.confidence,
            status = excluded.status
        """,
        (
            parameter.name,
            parameter.value,
            parameter.unit,
            parameter.source,
            parameter.confidence,
            parameter.status,
            parameter.vehicle_id,
            parameter.configuration_version,
        ),
    )

    connection.commit()
    connection.close()


def get_parameters(
    vehicle_id: str,
    configuration_version: str,
) -> list[ParameterRecord]:
    """Return all parameters belonging to a vehicle configuration."""

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            name,
            value,
            unit,
            source,
            confidence,
            status,
            vehicle_id,
            configuration_version
        FROM parameters
        WHERE vehicle_id = ?
        AND configuration_version = ?
        ORDER BY name
        """,
        (vehicle_id, configuration_version),
    ).fetchall()

    connection.close()

    return [
        ParameterRecord(
            name=row[0],
            value=row[1],
            unit=row[2],
            source=row[3],
            confidence=row[4],
            status=row[5],
            vehicle_id=row[6],
            configuration_version=row[7],
        )
        for row in rows
    ]

def insert_configuration(
    configuration: ConfigurationRecord,
) -> None:
    """Insert or update a vehicle configuration."""

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO configurations (
            vehicle_id,
            version,
            name,
            description,
            parent_version
        )
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(vehicle_id, version)
        DO UPDATE SET
            name = excluded.name,
            description = excluded.description,
            parent_version = excluded.parent_version
        """,
        (
            configuration.vehicle_id,
            configuration.version,
            configuration.name,
            configuration.description,
            configuration.parent_version,
        ),
    )

    connection.commit()
    connection.close()

def get_configuration(
    vehicle_id: str,
    version: str,
) -> ConfigurationRecord | None:
    """Return a vehicle configuration."""

    connection = get_connection()

    row = connection.execute(
        """
        SELECT
            vehicle_id,
            version,
            name,
            description,
            parent_version
        FROM configurations
        WHERE vehicle_id = ?
        AND version = ?
        """,
        (vehicle_id, version),
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return ConfigurationRecord(
        vehicle_id=row[0],
        version=row[1],
        name=row[2],
        description=row[3],
        parent_version=row[4],
    )