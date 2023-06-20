from sqlalchemy.orm import Session
from sqlalchemy import select, extract
from tkinter import messagebox

import itasql
import itadata


def booking_makes_sense(booking):
    with Session(itasql.engine) as session:
        telescope = session.scalars(
            select(itadata.Telescope).where(
                itadata.Telescope.id == booking.telescope_id
            )
        ).first()
        project = session.scalars(
            select(itadata.Project).where(itadata.Project.id == booking.project_id)
        ).first()
        records = (
            session.query(itadata.Booking)
            .where(itadata.Booking.telescope_id == booking.telescope_id)
            .where(extract("day", itadata.Booking.date) == booking.date.day)
            .where(extract("month", itadata.Booking.date) == booking.date.month)
            .where(extract("year", itadata.Booking.date) == booking.date.year)
        ).count()
    if telescope == None:
        messagebox.showwarning("", "No telescope with that id")
        return False
    if project == None:
        messagebox.showwarning("", "No project with that id")
        return False
    if records > 0:
        messagebox.showwarning("", "The telescope is already in use on that day")
        return False
    if telescope.range < project.distance:
        messagebox.showwarning("", "The telescope does not have enough range")
        return False
    if telescope.spectrum != project.frequence:
        messagebox.showwarning("", "The telescope has a different frequence")
        return False
    return True
