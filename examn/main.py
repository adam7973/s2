#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
import itasql

padx = 8
pady = 4
rowheight = 24
treeview_background = "#eeeeee"
treeview_foreground = "black"
treeview_selected = "#773333"

# itasql.init()


# def edit_container(_, tree):
#     index_selected = tree.focus()
#     values = tree.item(index_selected, 'values')

main_win = tk.Tk()
main_win.title("ITA booking")
main_win.geometry("500x500")

style = ttk.Style()
style.theme_use("default")

style.configure(
    "Treeview",
    background=treeview_background,
    foreground=treeview_foreground,
    rowheight=rowheight,
    fieldbackground=treeview_background,
)
style.map("Treeview", background=[("selected", treeview_selected)])

frame_container = tk.LabelFrame(main_win, text="Projects")
frame_container.grid(row=0, column=0, padx=padx, pady=pady, stick=tk.N)

tree_frame_container = tk.Frame(frame_container)
tree_frame_container.grid(row=0, column=0, padx=padx, pady=pady)
tree_scroll_container = tk.Scrollbar(tree_frame_container)
tree_scroll_container.grid(row=0, column=1, padx=0, pady=pady, sticky="ns")
tree_container = ttk.Treeview(
    tree_frame_container, yscrollcommand=tree_scroll_container.set, selectmode="browse"
)
tree_container.grid(row=0, column=0, padx=0, pady=pady)
tree_scroll_container.config(command=tree_container.yview)

tree_container["columns"] = ("id", "distance", "frequence")
tree_container.column("#0", width=0, stretch=tk.NO)  # Suppress empty first col
tree_container.column("id", anchor=tk.E, width=40)
tree_container.column("distance", anchor=tk.E, width=100)
tree_container.column("frequence", anchor=tk.W, width=40)
tree_container.heading("#0", text="", anchor=tk.W)
tree_container.heading("id", text="Id", anchor=tk.CENTER)
tree_container.heading("distance", text="Distance", anchor=tk.CENTER)
tree_container.heading("frequence", text="Frequence", anchor=tk.CENTER)

# tree_container.bind("<ButtonRelease-1>", lambda event: edit_container(event, tree_container))

controls_frame_container = tk.Frame(frame_container)
controls_frame_container.grid(row=3, column=0, padx=padx, pady=pady)

edit_frame_container = tk.Frame(controls_frame_container)
edit_frame_container.grid(row=0, column=0, padx=padx, pady=pady)
