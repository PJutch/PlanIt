import tkinter
from tkinter import ttk
import tkcalendar


class Tasks:
    def __init__(self, notebook):
        self.entry_rows = []
        self.next_row_id = 0

        tasks = ttk.Frame(notebook)
        tasks.pack()

        self.task_entries = ttk.Frame(tasks)
        self.task_entries.columnconfigure(0, weight=1)
        self.task_entries.pack(fill=tkinter.X)

        add_button = ttk.Button(tasks, text="Добавить", command=self.add_row)
        add_button.pack(anchor=tkinter.N, padx=6, pady=6)

        notebook.add(tasks, text="Домашки")

    class EntryRow:
        def __init__(self, tasks):
            self.id = tasks.next_row_id
            tasks.next_row_id += 1

            self.score = tkinter.IntVar()
            self.widgets = [ttk.Entry(tasks.task_entries),
                            ttk.Entry(tasks.task_entries, textvariable=self.score),
                            tkcalendar.DateEntry(tasks.task_entries),
                            ttk.Button(tasks.task_entries, text="Удалить", command=lambda: tasks.remove_row(self.id))]

        def forget(self):
            for widget in self.widgets:
                widget.grid_forget()

        def grid(self, row):
            for j in range(len(self.widgets)):
                self.widgets[j].grid(row=row, column=j, sticky=tkinter.W + tkinter.E)

    def remove_row(self, deleted):
        for row in self.entry_rows:
            row.forget()

        self.entry_rows = [row for row in self.entry_rows if row.id != deleted]

        for i in range(len(self.entry_rows)):
            self.entry_rows[i].grid(i)

    def add_row(self):
        for row in self.entry_rows:
            row.forget()

        self.entry_rows.append(self.EntryRow(self))

        for i in range(len(self.entry_rows)):
            self.entry_rows[i].grid(i)
