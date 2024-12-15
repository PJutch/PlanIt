import tkinter
from tkinter import ttk


class Subjects:
    def __init__(self, notebook):
        self.tasks = None

        self.entry_rows = []
        self.next_row_id = 0

        subjects = ttk.Frame(notebook)
        subjects.pack()

        self.entries = ttk.Frame(subjects)
        self.entries.columnconfigure(1, weight=1)
        self.entries.pack(fill=tkinter.X)

        add_button = ttk.Button(subjects, text="Добавить", command=self.add_row)
        add_button.pack(anchor=tkinter.N, padx=6, pady=6)

        clear_button = ttk.Button(subjects, text="Очистить", command=self.clear)
        clear_button.pack(anchor=tkinter.N, padx=6, pady=6)

        notebook.add(subjects, text="Предметы")

    class EntryRow:
        def __init__(self, subjects):
            self.id = subjects.next_row_id
            subjects.next_row_id += 1

            self.name = tkinter.StringVar()
            self.name.trace_add('write', lambda name, index, mode, sv=self.name: subjects.tasks.subject_renamed())
            self.score = tkinter.IntVar()
            self.widgets = [ttk.Label(subjects.entries, text='Название:'),
                            ttk.Entry(subjects.entries, textvariable=self.name),
                            ttk.Label(subjects.entries, text='Целевой балл:'),
                            ttk.Entry(subjects.entries, textvariable=self.score),
                            ttk.Button(subjects.entries, text="Удалить", command=lambda: subjects.remove_row(self.id))]

        def forget(self):
            for widget in self.widgets:
                widget.grid_forget()

        def grid(self, row):
            for j in range(len(self.widgets)):
                self.widgets[j].grid(row=row, column=j, sticky=tkinter.W + tkinter.E)

    def forget_all(self):
        for row in self.entry_rows:
            row.forget()

    def grid_all(self):
        for i in range(len(self.entry_rows)):
            self.entry_rows[i].grid(i)

    def remove_row(self, deleted):
        self.forget_all()
        self.entry_rows = [row for row in self.entry_rows if row.id != deleted]
        self.grid_all()
        self.tasks.subject_renamed()

    def add_row(self):
        self.forget_all()
        self.entry_rows.append(self.EntryRow(self))
        self.grid_all()

    def subject_names(self):
        return [row.name.get() for row in self.entry_rows if row.name.get() and not row.name.get().isspace()]

    def clear(self):
        self.forget_all()
