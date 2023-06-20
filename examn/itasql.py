from sqlalchemy import create_engine, select, update, delete
from sqlalchemy.orm import Session
from itadata import Base, Project, Booking, Telescope

# these lines are to allow for FORING KEYs
from sqlalchemy.engine import Engine
from sqlalchemy import event


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# end

Database = "sqlite:///ita.db"


def select_all(classparam):
    """
    Return a list of all records in classparam.

    :param classparam: itadata Class to get records from
    """
    with Session(engine) as session:
        records = session.scalars(select(classparam))
        result = []
        for record in records:
            result.append(record)
    return result


def create_record(record):
    """Create a new record in the database."""
    with Session(engine) as session:
        record.id = None  # let sqlalchemy create the id by itself
        session.add(record)
        session.commit()


def get_record(classparam, record_id):
    with Session(engine) as session:
        record = session.scalars(
            select(classparam).where(classparam.id == record_id)
        ).first()
    return record


# Projects
def update_projects_record(record):
    """Update a record in the projects table."""
    with Session(engine) as session:
        session.execute(
            update(Project)
            .where(Project.id == record.id)
            .values(distance=record.distance, frequence=record.frequence)
        )
        session.commit()


def delete_projects_record(record):
    """Delete a record from the Projects table."""
    with Session(engine) as session:
        session.execute(delete(Project).where(Project.id == record.id))
        session.commit()


# Telescopes
def update_telescopes_record(record):
    """Update a record in the telescopes table."""
    with Session(engine) as session:
        session.execute(
            update(Telescope)
            .where(Telescope.id == record.id)
            .values(range=record.range, spectrum=record.spectrum)
        )
        session.commit()


def delete_telescopes_record(record):
    """Delete a record from the telescopes table."""
    with Session(engine) as session:
        session.execute(delete(Telescope).where(Telescope.id == record.id))
        session.commit()


# Bookings


def update_bookings_record(record):
    """Update a record in the bookings table."""
    with Session(engine) as session:
        session.execute(
            update(Booking)
            .where(Booking.id == record.id)
            .values(
                date=record.date,
                project_id=record.project_id,
                telescope_id=record.telescope_id,
            )
        )
        session.commit()


def delete_bookings_record(record):
    """Delete a record from the bookings table."""
    with Session(engine) as session:
        session.execute(delete(Booking).where(Booking.id == record.id))
        session.commit()


engine = create_engine(Database, echo=False)
Base.metadata.create_all(engine)
