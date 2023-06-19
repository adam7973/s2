from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import Column, Integer, Date
from sqlalchemy import create_engine, select

Database = "sqlite:///ita.db"
Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    distance = Column(Integer)
    frequence = Column(Integer)


class Telescope(Base):
    __tablename__ = "telescopes"
    id = Column(Integer, primary_key=True)
    range = Column(Integer)
    spectrum = Column(Integer)


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    project_id = Column(Integer)
    telescope_id = Column(Integer)


def init():
    engine = create_engine(Database, echo=False)
    Base.metadata.create_all(engine)
