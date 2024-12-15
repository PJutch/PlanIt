import random
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
        self.task_entries.columnconfigure(1, weight=1)
        self.task_entries.pack(fill=tkinter.X)

        add_button = ttk.Button(tasks, text="Добавить", command=self.add_row)
        add_button.pack(anchor=tkinter.N, padx=6, pady=6)

        sort_button = ttk.Button(tasks, text="Plan It!", command=self.sort)
        sort_button.pack(anchor=tkinter.N, padx=6, pady=6)

        clear_button = ttk.Button(tasks, text="Очистить", command=self.clear)
        clear_button.pack(anchor=tkinter.N, padx=6, pady=6)

        notebook.add(tasks, text="Домашки")

    class EntryRow:
        def __init__(self, tasks):
            self.tasks = tasks

            self.id = tasks.next_row_id
            tasks.next_row_id += 1

            self.subject = ttk.Combobox(tasks.task_entries)

            self.score = tkinter.IntVar()
            self.widgets = [ttk.Label(tasks.task_entries, text='Название:'),
                            ttk.Entry(tasks.task_entries),
                            ttk.Label(tasks.task_entries, text='Предмет:'),
                            self.subject,
                            ttk.Label(tasks.task_entries, text='Баллы:'),
                            ttk.Entry(tasks.task_entries, textvariable=self.score),
                            ttk.Label(tasks.task_entries, text='Дедлайн:'),
                            tkcalendar.DateEntry(tasks.task_entries),
                            ttk.Button(tasks.task_entries, text="Удалить", command=lambda: tasks.remove_row(self.id))]
            self.update_combobox()

        def forget(self):
            for widget in self.widgets:
                widget.grid_forget()

        def grid(self, row):
            for j in range(len(self.widgets)):
                self.widgets[j].grid(row=row, column=j, sticky=tkinter.W + tkinter.E)

        def update_combobox(self):
            self.subject['values'] = self.tasks.subjects.subject_names()

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

    def add_row(self):
        self.forget_all()
        self.entry_rows.append(self.EntryRow(self))
        self.grid_all()

    def subject_renamed(self):
        for row in self.entry_rows:
            row.update_combobox()

    def sort(self):
        self.forget_all()
        random.shuffle(self.entry_rows)
        self.grid_all()

    def clear(self):
        self.forget_all()
