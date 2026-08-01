from .connection import get_connection
from .models import ParameterRecord


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
            vehicle_id TEXT NOT NULL
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
            vehicle_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            parameter.name,
            parameter.value,
            parameter.unit,
            parameter.source,
            parameter.confidence,
            parameter.status,
            parameter.vehicle_id,
        ),
    )

    connection.commit()
    connection.close()

def get_parameters(vehicle_id: str) -> list[ParameterRecord]:
    """Return all parameters belonging to a vehicle."""

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
            vehicle_id
        FROM parameters
        WHERE vehicle_id = ?
        ORDER BY name
        """,
        (vehicle_id,),
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
        )
        for row in rows
    ]