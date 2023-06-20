#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import itadata
import itasql
import utils

padx = 8
pady = 4
rowheight = 24
treeview_background = "#eeeeee"
treeview_foreground = "black"
treeview_selected = "#773333"
evenrow = "#cccccc"
oddrow = "#dddddd"


# used by all frames
def read_table(tree, class_):
    count = 0  # keep track of odd and event for colors
    data = itasql.select_all(class_)
    for record in data:
        if count % 2 == 0:
            tree.insert(
                parent="",
                index="end",
                iid=count,
                text="",
                values=record.convert_to_tuple(),
                tags=("evenrow"),
            )
        else:
            tree.insert(
                parent="",
                index="end",
                iid=count,
                text="",
                values=record.convert_to_tuple(),
                tags=("oddrow"),
            )
        count += 1


def refresh_treeview(tree, class_):
    empty_treeview(tree)
    read_table(tree, class_)


def empty_treeview(tree):
    tree.delete(*tree.get_children())


main_win = tk.Tk()
main_win.title("AspIT")
main_win.geometry("1200x500")

style = ttk.Style()
style.theme_use("default")

# configure the treeview colors
style.configure(
    "Treeview",
    background=treeview_background,
    foreground=treeview_foreground,
    rowheight=rowheight,
    fieldbackground=treeview_background,
)
style.map("Treeview", background=[("selected", treeview_selected)])


# region projects
def edit_projects(_, tree):
    selected = tree.focus()  # get item clicked
    values = tree.item(selected, "values")  # get values of clicked item
    clear_projects_entries()
    fill_projects_entries(values)


def fill_projects_entries(values):
    entry_id_projects.insert(0, values[0])
    entry_dist_projects.insert(0, values[1])
    entry_freq_projects.insert(0, values[2])


def read_project_entries():
    return entry_id_projects.get(), entry_dist_projects.get(), entry_freq_projects.get()


def update_projects_entry(tree, record):
    project = itadata.Project.convert_from_tuple(record)
    itasql.update_record(project)
    clear_projects_entries()
    # refresh_treeview(tree, itadata.Project)


def delete_projects_entry(tree, record):
    project = itadata.Project.convert_from_tuple(record)
    itasql.delete_projects_record(project)
    clear_projects_entries()
    refresh_treeview(tree, itadata.Project)


def clear_projects_entries():
    entry_dist_projects.delete(0, tk.END)
    entry_freq_projects.delete(0, tk.END)
    entry_id_projects.delete(0, tk.END)


def create_project_record(tree, record):
    project = itadata.Project.convert_from_tuple(record)
    if project.valid():
        itasql.create_record(project)
        clear_projects_entries()
        refresh_treeview(tree, itadata.Project)
    else:
        messagebox.showwarning("", "Something went wrong, please check your input")


# frame containing everything for the Projects section
frame_projects = tk.LabelFrame(main_win, text="Projekt")
frame_projects.grid(row=0, column=0, padx=padx, pady=pady, stick=tk.N)

# treeview
tree_frame_projects = tk.Frame(frame_projects)
tree_frame_projects.grid(row=0, column=0, padx=padx, pady=pady)
tree_scroll_projects = tk.Scrollbar(tree_frame_projects)
tree_scroll_projects.grid(row=0, column=1, padx=0, pady=pady, sticky="ns")
tree_projects = ttk.Treeview(
    tree_frame_projects,
    yscrollcommand=tree_scroll_projects.set,
    selectmode="browse",
)
tree_projects.grid(row=0, column=0, padx=0, pady=pady)
tree_scroll_projects.config(command=tree_projects.yview)

tree_projects["columns"] = ("id", "distance", "frequence")
tree_projects.column("#0", width=0, stretch=tk.NO)  # Suppress empty first col
tree_projects.column("id", anchor=tk.E, width=40)
tree_projects.column("distance", anchor=tk.E, width=100)
tree_projects.column("frequence", anchor=tk.W, width=300)
tree_projects.heading("#0", text="", anchor=tk.W)
tree_projects.heading("id", text="Id", anchor=tk.CENTER)
tree_projects.heading("distance", text="Afstand", anchor=tk.CENTER)
tree_projects.heading("frequence", text="Frekvens", anchor=tk.CENTER)
tree_projects.tag_configure("oddrow", background=oddrow)
tree_projects.tag_configure("evenrow", background=evenrow)

tree_projects.bind(
    "<ButtonRelease-1>", lambda event: edit_projects(event, tree_projects)
)

# controls (entry fields, buttons) and labels
controls_frame_projects = tk.Frame(frame_projects)
controls_frame_projects.grid(row=3, column=0, padx=padx, pady=pady)

# frame for labels and entries
edit_frame_projects = tk.Frame(controls_frame_projects)
edit_frame_projects.grid(row=0, column=0, padx=padx, pady=pady)

label_id_projects = tk.Label(edit_frame_projects, text="Id")
label_id_projects.grid(row=0, column=0, padx=padx, pady=pady)
entry_id_projects = tk.Entry(edit_frame_projects, width=4, justify="right")
entry_id_projects.grid(row=1, column=0, padx=padx, pady=pady)

label_dist_projects = tk.Label(edit_frame_projects, text="Afstand")
label_dist_projects.grid(row=0, column=1, padx=padx, pady=pady)
entry_dist_projects = tk.Entry(edit_frame_projects, width=10, justify="right")
entry_dist_projects.grid(row=1, column=1, padx=padx, pady=pady)

label_freq_projects = tk.Label(edit_frame_projects, text="Frekvens")
label_freq_projects.grid(row=0, column=2, padx=padx, pady=pady)
entry_freq_projects = tk.Entry(edit_frame_projects, width=25, justify="right")
entry_freq_projects.grid(row=1, column=2, padx=padx, pady=pady)

# frame for buttons

button_frame_projects = tk.Frame(controls_frame_projects)
button_frame_projects.grid(row=1, column=0, padx=padx, pady=pady)
# buttons
button_create_projects = tk.Button(
    button_frame_projects,
    text="Create",
    command=lambda: create_project_record(tree_projects, read_project_entries()),
)
button_create_projects.grid(row=0, column=1, padx=padx, pady=pady)
button_update_projects = tk.Button(
    button_frame_projects,
    text="Update",
    command=lambda: update_projects_entry(tree_projects, read_project_entries()),
)
button_update_projects.grid(row=0, column=2, padx=padx, pady=pady)
button_delete_projects = tk.Button(
    button_frame_projects,
    text="Delete",
    command=lambda: delete_projects_entry(tree_projects, read_project_entries()),
)
button_delete_projects.grid(row=0, column=3, padx=padx, pady=pady)
button_clear_projects = tk.Button(
    button_frame_projects, text="Clear Entry Boxes", command=clear_projects_entries
)
button_clear_projects.grid(row=0, column=4, padx=padx, pady=pady)

# endregion


# region telescopes
def edit_telescopes(_, tree):
    selected = tree.focus()  # get item clicked
    values = tree.item(selected, "values")  # get values of clicked item
    clear_telescopes_entries()
    fill_telescopes_entries(values)


def fill_telescopes_entries(values):
    entry_id_telescope.insert(0, values[0])
    entry_range_telescope.insert(0, values[1])
    entry_spectrum_telescope.insert(0, values[2])


def read_telescope_entries():
    return (
        entry_id_telescope.get(),
        entry_range_telescope.get(),
        entry_spectrum_telescope.get(),
    )


def update_telescopes_entry(tree, record):
    telescope = itadata.Telescope.convert_from_tuple(record)
    itasql.update_record(telescope)
    clear_telescopes_entries()
    # refresh_treeview(tree, itadata.Project)


def delete_telescopes_entry(tree, record):
    telescope = itadata.Telescope.convert_from_tuple(record)
    itasql.delete_telescopes_record(telescope)
    clear_projects_entries()
    refresh_treeview(tree, itadata.Telescope)


def clear_telescopes_entries():
    entry_range_telescope.delete(0, tk.END)
    entry_spectrum_telescope.delete(0, tk.END)
    entry_id_telescope.delete(0, tk.END)


def create_telescope_record(tree, record):
    telescope = itadata.Telescope.convert_from_tuple(record)
    if telescope.valid():
        itasql.create_record(telescope)
        clear_telescopes_entries()
        refresh_treeview(tree, itadata.Telescope)
    else:
        messagebox.showwarning("", "Something went wrong, please check your input")


# frame containing everything for the Telescope section
frame_telescope = tk.LabelFrame(main_win, text="Teleskop")
frame_telescope.grid(row=0, column=1, padx=padx, pady=pady, stick=tk.N)

# treeview
tree_frame_telescope = tk.Frame(frame_telescope)
tree_frame_telescope.grid(row=0, column=0, padx=padx, pady=pady)
tree_scroll_telescope = tk.Scrollbar(tree_frame_telescope)
tree_scroll_telescope.grid(row=0, column=1, padx=0, pady=pady, sticky="ns")
tree_telescope = ttk.Treeview(
    tree_frame_telescope,
    yscrollcommand=tree_scroll_telescope.set,
    selectmode="browse",
)
tree_telescope.grid(row=0, column=0, padx=0, pady=pady)
tree_scroll_telescope.config(command=tree_telescope.yview)

tree_telescope["columns"] = ("id", "range", "spectrum")
tree_telescope.column("#0", width=0, stretch=tk.NO)  # Suppress empty first col
tree_telescope.column("id", anchor=tk.E, width=40)
tree_telescope.column("range", anchor=tk.E, width=100)
tree_telescope.column("spectrum", anchor=tk.W, width=100)
tree_telescope.heading("#0", text="", anchor=tk.W)
tree_telescope.heading("id", text="Id", anchor=tk.CENTER)
tree_telescope.heading("range", text="Range", anchor=tk.CENTER)
tree_telescope.heading("spectrum", text="Spektrum", anchor=tk.CENTER)

tree_telescope.bind(
    "<ButtonRelease-1>", lambda event: edit_telescopes(event, tree_telescope)
)

# controls (entry fields, buttons) and labels
controls_frame_telescope = tk.Frame(frame_telescope)
controls_frame_telescope.grid(row=3, column=0, padx=padx, pady=pady)

# frame for labels and entries
edit_frame_telescope = tk.Frame(controls_frame_telescope)
edit_frame_telescope.grid(row=0, column=0, padx=padx, pady=pady)

label_id_telescope = tk.Label(edit_frame_telescope, text="Id")
label_id_telescope.grid(row=0, column=0, padx=padx, pady=pady)
entry_id_telescope = tk.Entry(edit_frame_telescope, width=4, justify="right")
entry_id_telescope.grid(row=1, column=0, padx=padx, pady=pady)

label_range_telescope = tk.Label(edit_frame_telescope, text="Range")
label_range_telescope.grid(row=0, column=1, padx=padx, pady=pady)
entry_range_telescope = tk.Entry(edit_frame_telescope, width=10, justify="right")
entry_range_telescope.grid(row=1, column=1, padx=padx, pady=pady)

label_spektrum_telescope = tk.Label(edit_frame_telescope, text="Spektrum")
label_spektrum_telescope.grid(row=0, column=2, padx=padx, pady=pady)
entry_spectrum_telescope = tk.Entry(edit_frame_telescope, width=10, justify="right")
entry_spectrum_telescope.grid(row=1, column=2, padx=padx, pady=pady)

# frame for buttons

button_frame_telescope = tk.Frame(controls_frame_telescope)
button_frame_telescope.grid(row=1, column=0, padx=padx, pady=pady)
# buttons
button_create_telescope = tk.Button(
    button_frame_telescope,
    text="Create",
    command=lambda: create_telescope_record(tree_telescope, read_telescope_entries()),
)
button_create_telescope.grid(row=0, column=1, padx=padx, pady=pady)
button_update_telescope = tk.Button(
    button_frame_telescope,
    text="Update",
    command=lambda: update_telescopes_entry(tree_telescope, read_telescope_entries()),
)
button_update_telescope.grid(row=0, column=2, padx=padx, pady=pady)
button_delete_telescope = tk.Button(
    button_frame_telescope,
    text="Delete",
    command=lambda: delete_telescopes_entry(tree_telescope, read_telescope_entries()),
)
button_delete_telescope.grid(row=0, column=3, padx=padx, pady=pady)
button_clear_telescope = tk.Button(
    button_frame_telescope,
    text="Clear Entry Boxes",
    command=clear_telescopes_entries,
)
button_clear_telescope.grid(row=0, column=4, padx=padx, pady=pady)
# endregion


# region booking
def edit_bookings(_, tree):
    selected = tree.focus()  # get item clicked
    values = tree.item(selected, "values")  # get values of clicked item
    clear_booking_entries()
    fill_bookings_entries(values)


def fill_bookings_entries(values):
    entry_id_booking.insert(0, values[0])
    entry_date_booking.insert(0, values[1])
    entry_projid_booking.insert(0, values[2])
    entry_telid_booking.insert(0, values[3])


def read_booking_entries():
    return (
        entry_id_booking.get(),
        entry_date_booking.get(),
        entry_projid_booking.get(),
        entry_telid_booking.get(),
    )


def update_booking_entry(tree, record):
    booking = itadata.Booking.convert_from_tuple(record)
    itasql.update_record(booking)
    clear_booking_entries()
    # refresh_treeview(tree, itadata.Project)


def delete_booking_entry(tree, record):
    booking = itadata.Booking.convert_from_tuple(record)
    itasql.delete_bookings_record(booking)
    clear_booking_entries()
    refresh_treeview(tree, itadata.Booking)


def clear_booking_entries():
    entry_id_booking.delete(0, tk.END)
    entry_date_booking.delete(0, tk.END)
    entry_projid_booking.delete(0, tk.END)
    entry_telid_booking.delete(0, tk.END)


def create_bookings_record(tree, record):
    booking = itadata.Booking.convert_from_tuple(record)
    if booking.valid():
        if utils.booking_makes_sense(booking):
            itasql.create_record(booking)
            clear_booking_entries()
            refresh_treeview(tree, itadata.Booking)
    else:
        messagebox.showwarning("", "Something went wrong, please check your input")


# frame containing everything for the Bookings section
frame_booking = tk.LabelFrame(main_win, text="Booking")
frame_booking.grid(row=0, column=2, padx=padx, pady=pady, stick=tk.N)

# treeview
tree_frame_booking = tk.Frame(frame_booking)
tree_frame_booking.grid(row=0, column=0, padx=padx, pady=pady)
tree_scroll_booking = tk.Scrollbar(tree_frame_booking)
tree_scroll_booking.grid(row=0, column=1, padx=0, pady=pady, sticky="ns")
tree_booking = ttk.Treeview(
    tree_frame_booking, yscrollcommand=tree_scroll_booking.set, selectmode="browse"
)
tree_booking.grid(row=0, column=0, padx=0, pady=pady)
tree_scroll_booking.config(command=tree_booking.yview)

tree_booking["columns"] = ("id", "date", "project_id", "telescope_id")
tree_booking.column("#0", width=0, stretch=tk.NO)  # Suppress empty first col
tree_booking.column("id", anchor=tk.E, width=40)
tree_booking.column("date", anchor=tk.E, width=100)
tree_booking.column("project_id", anchor=tk.E, width=100)
tree_booking.column("telescope_id", anchor=tk.W, width=100)
tree_booking.heading("#0", text="", anchor=tk.W)
tree_booking.heading("id", text="Id", anchor=tk.CENTER)
tree_booking.heading("date", text="Dato", anchor=tk.CENTER)
tree_booking.heading("project_id", text="Projekt Id", anchor=tk.CENTER)
tree_booking.heading("telescope_id", text="Teleskop Id", anchor=tk.CENTER)

tree_booking.bind("<ButtonRelease-1>", lambda event: edit_bookings(event, tree_booking))

# controls (entry fields, buttons) and labels
controls_frame_booking = tk.Frame(frame_booking)
controls_frame_booking.grid(row=3, column=0, padx=padx, pady=pady)

# frame for labels and entries
edit_frame_booking = tk.Frame(controls_frame_booking)
edit_frame_booking.grid(row=0, column=0, padx=padx, pady=pady)

label_id_booking = tk.Label(edit_frame_booking, text="Id")
label_id_booking.grid(row=0, column=0, padx=padx, pady=pady)
entry_id_booking = tk.Entry(edit_frame_booking, width=4, justify="right")
entry_id_booking.grid(row=1, column=0, padx=padx, pady=pady)

label_date_booking = tk.Label(edit_frame_booking, text="Date")
label_date_booking.grid(row=0, column=1, padx=padx, pady=pady)
entry_date_booking = tk.Entry(edit_frame_booking, width=10, justify="right")
entry_date_booking.grid(row=1, column=1, padx=padx, pady=pady)

label_projid_booking = tk.Label(edit_frame_booking, text="Projekt Id")
label_projid_booking.grid(row=0, column=2, padx=padx, pady=pady)
entry_projid_booking = tk.Entry(edit_frame_booking, width=10, justify="right")
entry_projid_booking.grid(row=1, column=2, padx=padx, pady=pady)

label_telid_booking = tk.Label(edit_frame_booking, text="Teleskop Id")
label_telid_booking.grid(row=0, column=3, padx=padx, pady=pady)
entry_telid_booking = tk.Entry(edit_frame_booking, width=10, justify="right")
entry_telid_booking.grid(row=1, column=3, padx=padx, pady=pady)
# frame for buttons

button_frame_booking = tk.Frame(controls_frame_booking)
button_frame_booking.grid(row=1, column=0, padx=padx, pady=pady)
# buttons
button_create_booking = tk.Button(
    button_frame_booking,
    text="Create",
    command=lambda: create_bookings_record(tree_booking, read_booking_entries()),
)
button_create_booking.grid(row=0, column=1, padx=padx, pady=pady)
button_update_booking = tk.Button(
    button_frame_booking,
    text="Update",
    command=lambda: update_booking_entry(tree_booking, read_booking_entries()),
)
button_update_booking.grid(row=0, column=2, padx=padx, pady=pady)
button_delete_booking = tk.Button(
    button_frame_booking,
    text="Delete",
    command=lambda: delete_booking_entry(tree_booking, read_booking_entries()),
)
button_delete_booking.grid(row=0, column=3, padx=padx, pady=pady)
button_clear_booking = tk.Button(
    button_frame_booking, text="Clear Entry Boxes", command=clear_booking_entries
)
button_clear_booking.grid(row=0, column=4, padx=padx, pady=pady)
# endregion

if __name__ == "__main__":
    refresh_treeview(tree_projects, itadata.Project)
    refresh_treeview(tree_telescope, itadata.Telescope)
    refresh_treeview(tree_booking, itadata.Booking)
    main_win.mainloop()
