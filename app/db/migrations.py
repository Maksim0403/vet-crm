from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine


def upgrade_pet_owner_column(engine: Engine) -> None:
    """Bring databases created before user ownership was added up to date."""
    inspector = inspect(engine)
    if "pets" not in inspector.get_table_names():
        return
    if "owner_id" in {column["name"] for column in inspector.get_columns("pets")}:
        return

    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE pets ADD COLUMN owner_id INTEGER"))
