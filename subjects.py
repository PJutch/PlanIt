import tkinter
from tkinter import ttk

import save


class Subjects:
    def __init__(self, notebook):
        self.tasks = None

        self.entry_rows: list[Subjects.EntryRow] = []
        self.next_row_id = 0

        subjects = ttk.Frame(notebook)
        subjects.pack()

        self.entries = ttk.Frame(subjects)
        self.entries.columnconfigure(1, weight=1)
        self.entries.pack(fill=tkinter.X)

        buttons = ttk.Frame(subjects)
        buttons.pack()

        add_button = ttk.Button(buttons, text="Добавить", command=self.add_row)
        add_button.pack(anchor=tkinter.N, padx=6, pady=6, side='left')

        clear_button = ttk.Button(buttons, text="Очистить", command=self.clear)
        clear_button.pack(anchor=tkinter.N, padx=6, pady=6, side='left')

        save_button = ttk.Button(buttons, text="Сохранить", command=lambda: save.save(self, self.tasks))
        save_button.pack(anchor=tkinter.N, padx=6, pady=6, side='left')

        notebook.add(subjects, text="Предметы")

    class EntryRow:
        def __init__(self, subjects):
            self.id = subjects.next_row_id
            subjects.next_row_id += 1

            self.name = tkinter.StringVar()
            self.name.trace_add('write', lambda name, index, mode, sv=self.name: subjects.tasks.subject_renamed())
            self.score = tkinter.IntVar()
            self.achieved_score = 0
            self.score_label = ttk.Label(subjects.entries, text=self.score_text())
            self.widgets = [ttk.Label(subjects.entries, text='Название:'),
                            ttk.Entry(subjects.entries, textvariable=self.name),
                            self.score_label,
                            ttk.Entry(subjects.entries, textvariable=self.score),
                            ttk.Button(subjects.entries, text="Удалить", command=lambda: subjects.remove_row(self.id))]

        def score_text(self):
            return f'Балл {self.achieved_score} /'

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
        self.entry_rows = []

    def target_scores(self):
        return {subject.name.get(): subject.score.get() for subject in self.entry_rows}

    def add_score(self, subject, score):
        for row in self.entry_rows:
            if row.name.get() == subject:
                row.achieved_score += score
                row.score_label['text'] = row.score_text()
