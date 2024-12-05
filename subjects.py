import tkinter
from tkinter import ttk


class Subjects:
    def __init__(self, notebook):
        self.entry_rows = []
        self.next_row_id = 0

        subjects = ttk.Frame(notebook)
        subjects.pack()

        self.entries = ttk.Frame(subjects)
        self.entries.columnconfigure(0, weight=1)
        self.entries.pack(fill=tkinter.X)

        add_button = ttk.Button(subjects, text="Добавить", command=self.add_row)
        add_button.pack(anchor=tkinter.N, padx=6, pady=6)

        notebook.add(subjects, text="Предметы")

    class EntryRow:
        def __init__(self, subjects):
            self.id = subjects.next_row_id
            subjects.next_row_id += 1

            self.score = tkinter.IntVar()
            self.widgets = [ttk.Entry(subjects.entries),
                            ttk.Entry(subjects.entries, textvariable=self.score),
                            ttk.Button(subjects.entries, text="Удалить", command=lambda: subjects.remove_row(self.id))]

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
