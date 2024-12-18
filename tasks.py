import datetime
import locale
import tkinter
from tkinter import ttk

import tkcalendar

import plan
import tab
import save


def make_gray_style(base):
    style = ttk.Style()
    style.configure(f'Gray.{base}', foreground='gray')


class Tasks(tab.Tab):
    def __init__(self, notebook):
        super().__init__(Tasks.EntryRow)

        self.subjects = None
        tasks = ttk.Frame(notebook)
        tasks.pack()

        self.task_entries = ttk.Frame(tasks)
        self.task_entries.columnconfigure(2, weight=1)
        self.task_entries.pack(fill=tkinter.X)

        buttons = ttk.Frame(tasks)
        buttons.pack()

        add_button = ttk.Button(buttons, text="Добавить", command=self.add_row)
        add_button.pack(anchor=tkinter.N, padx=6, pady=6, side='left')

        sort_button = ttk.Button(buttons, text="Plan It!", command=self.sort)
        sort_button.pack(anchor=tkinter.N, padx=6, pady=6, side='left')

        clear_button = ttk.Button(buttons, text="Очистить", command=self.clear)
        clear_button.pack(anchor=tkinter.N, padx=6, pady=6, side='left')

        save_button = ttk.Button(buttons, text="Сохранить", command=lambda: save.save(self.subjects, self))
        save_button.pack(anchor=tkinter.N, padx=6, pady=6, side='left')

        notebook.add(tasks, text="Домашки")

        make_gray_style('TCheckbutton')
        make_gray_style('TLabel')
        make_gray_style('TEntry')
        make_gray_style('TCombobox')
        make_gray_style('TButton')

    class EntryRow(tab.Tab.EntryRow):
        def __init__(self, tasks):
            super().__init__(tasks)

            self.subject_var = tkinter.StringVar()
            self.subject = ttk.Combobox(tasks.task_entries, textvariable=self.subject_var)
            self.subject_var.trace_add('write', lambda name, index, mode: self.subject_updated())
            self.old_subject = ''

            self.done = tkinter.BooleanVar()
            self.done.set(False)

            self.name = tkinter.StringVar()
            self.time = tkinter.IntVar()
            self.deadline = tkcalendar.DateEntry(tasks.task_entries, locale=locale.getdefaultlocale()[0])

            self.score = tkinter.IntVar()
            self.score.trace_add('write', lambda name, index, mode: self.score_updated())
            self.old_score = 0

            self.widgets = [ttk.Checkbutton(tasks.task_entries, variable=self.done,
                                            command=lambda:
                                                self.marked_done() if self.done.get()
                                                else self.marked_not_done()),
                            ttk.Label(tasks.task_entries, text='Название:'),
                            ttk.Entry(tasks.task_entries),
                            ttk.Label(tasks.task_entries, text='Предмет:'),
                            self.subject,
                            ttk.Label(tasks.task_entries, text='Баллы:'),
                            ttk.Entry(tasks.task_entries, textvariable=self.score),
                            ttk.Label(tasks.task_entries, text='Часы бота:'),
                            ttk.Entry(tasks.task_entries, textvariable=self.time),
                            ttk.Label(tasks.task_entries, text='Дедлайн:'),
                            self.deadline,
                            ttk.Button(tasks.task_entries, text="Удалить", command=lambda: tasks.remove_row(self.id))]
            self.update_combobox()

        def update_combobox(self):
            self.subject['values'] = self.tab.subjects.subject_names()

        def gray_out(self):
            for widget in self.widgets:
                if isinstance(widget, ttk.Checkbutton):
                    widget['style'] = 'Gray.TCheckbutton'
                elif isinstance(widget, ttk.Label):
                    widget['style'] = 'Gray.TLabel'
                elif isinstance(widget, ttk.Entry):
                    widget['style'] = 'Gray.TEntry'
                elif isinstance(widget, ttk.Combobox):
                    widget['style'] = 'Gray.TCombobox'
                elif isinstance(widget, ttk.Button):
                    widget['style'] = 'Gray.TButton'

        def ungray_out(self):
            for widget in self.widgets:
                if isinstance(widget, ttk.Checkbutton):
                    widget['style'] = 'TCheckbutton'
                elif isinstance(widget, ttk.Label):
                    widget['style'] = 'TLabel'
                elif isinstance(widget, ttk.Entry):
                    widget['style'] = 'TEntry'
                elif isinstance(widget, ttk.Combobox):
                    widget['style'] = 'TCombobox'
                elif isinstance(widget, ttk.Button):
                    widget['style'] = 'TButton'

        def marked_done(self):
            self.tab.subjects.add_score(self.subject.get(), self.score.get())
            self.gray_out()

        def marked_not_done(self):
            self.tab.subjects.add_score(self.subject.get(), -self.score.get())
            self.ungray_out()

        def score_updated(self):
            if self.done.get():
                self.tab.subjects.add_score(self.subject.get(), self.score.get() - self.old_score)
            self.old_score = self.score.get()

        def subject_updated(self):
            if self.done.get():
                self.tab.subjects.add_score(self.old_subject, -self.score.get())
                self.tab.subjects.add_score(self.subject.get(), self.score.get())
            self.old_subject = self.subject.get()

    def subject_renamed(self):
        for row in self.entry_rows:
            row.update_combobox()

    def sort(self):
        self.forget_all()

        order = plan.plan(int(datetime.datetime.now().timestamp() / 3600),
                          self.subjects.target_scores(), self.tasks())

        for row in self.entry_rows:
            row.gray_out()
        for i in order:
            self.entry_rows[i].ungray_out()
        self.entry_rows = ([self.entry_rows[i] for i in order]
                           + [entry_row for i, entry_row in enumerate(self.entry_rows) if i not in order])

        self.grid_all()

    def tasks(self):
        return [plan.Task(row.done.get(), row.name.get(), row.subject.get(), row.score.get(), row.time.get() * 3,
                          (row.deadline.get_date() - datetime.date(1970, 1, 1)).days * 24)
                for row in self.entry_rows]

    def saved_data(self):
        return [{
            'done': row.done.get(),
            'name': row.name.get(),
            'subject': row.subject.get(),
            'score': row.score.get(),
            'time': row.time.get(),
            'deadline': row.deadline.get_date().isoformat()
        } for row in self.entry_rows]

    def load_data(self, data):
        for row in data:
            self.add_row()
            self.entry_rows[-1].done.set(row['done'])
            self.entry_rows[-1].name.set(row['name'])
            self.entry_rows[-1].subject.set(row['subject'])
            self.entry_rows[-1].score.set(row['score'])
            self.entry_rows[-1].time.set(row['time'])
            self.entry_rows[-1].deadline.set_date(datetime.datetime.fromisoformat(row['deadline']))
