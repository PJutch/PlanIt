import tkinter
from tkinter import ttk

import tab


class Subjects(tab.Tab):
    def __init__(self, notebook, app):
        super().__init__(Subjects.EntryRow, app)

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

        save_button = ttk.Button(buttons, text="Сохранить", command=lambda: self.app.save())
        save_button.pack(anchor=tkinter.N, padx=6, pady=6, side='left')

        notebook.add(subjects, text="Предметы")

    class EntryRow(tab.Tab.EntryRow):
        def __init__(self, subjects):
            super().__init__(subjects)

            self.name = tkinter.StringVar()
            self.name.trace_add('write', lambda name, index, mode: subjects.app.tasks.subject_renamed())
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

    def subject_names(self):
        return [row.name.get() for row in self.entry_rows if row.name.get() and not row.name.get().isspace()]

    def target_scores(self):
        return {subject.name.get(): subject.score.get() for subject in self.entry_rows}

    def add_score(self, subject, score):
        for row in self.entry_rows:
            if row.name.get() == subject:
                row.achieved_score += score
                row.score_label['text'] = row.score_text()

    def load_data(self, data):
        for name, target_score in data.items():
            self.add_row()
            self.entry_rows[-1].name.set(name)
            self.entry_rows[-1].score.set(target_score)
