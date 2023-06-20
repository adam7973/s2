from sqlalchemy import Column, Integer, Date
from sqlalchemy.orm import declarative_base
from dateutil import parser

Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    distance = Column(Integer)
    frequence = Column(Integer)

    def valid(self):
        """Check if frequence is between 0 and 2 and if distance is a positive number."""
        return (
            int(self.frequence) >= 0
            and int(self.frequence) <= 2
            and int(self.distance) >= 0
        )

    def convert_to_tuple(self):
        """Convert instance of Project to tuple."""
        return self.id, self.distance, self.frequence

    @staticmethod
    def convert_from_tuple(tuple_):
        """Convert tuple to Project record."""
        project = Project(id=tuple_[0], distance=tuple_[1], frequence=tuple_[2])
        return project


class Telescope(Base):
    __tablename__ = "telescopes"
    id = Column(Integer, primary_key=True)
    range = Column(Integer)
    spectrum = Column(Integer)

    def valid(self):
        """Check if range is a positive number and spectrum is between 0 and 2."""
        return (
            int(self.range) >= 0 and int(self.spectrum) >= 0 and int(self.spectrum) <= 2
        )

    def convert_to_tuple(self):
        """Convert instance of Telescope to tuple."""
        return self.id, self.range, self.spectrum

    @staticmethod
    def convert_from_tuple(tuple_):
        """Convert tuple to Telescope record."""
        telescope = Telescope(id=tuple_[0], range=tuple_[1], spectrum=tuple_[2])
        return telescope


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    project_id = Column(Integer)
    telescope_id = Column(Integer)

    def valid(self):
        """Check if project and telescope id are positive."""
        return int(self.project_id) >= 0 and int(self.telescope_id) >= 0

    def convert_to_tuple(self):
        """Convert instance of Booking to tuple."""
        return self.id, self.date, self.project_id, self.telescope_id

    @staticmethod
    def convert_from_tuple(tuple_):
        """Convert tuple to Booking record."""
        try:
            date = parser.parse(tuple_[1])
            booking = Booking(
                id=tuple_[0], date=date, project_id=tuple_[2], telescope_id=tuple_[3]
            )
            return booking
        except:
            pass
