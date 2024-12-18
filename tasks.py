import datetime
import locale
import tkinter
from tkinter import ttk

import tkcalendar

import plan
import tab


def make_gray_style(base):
    style = ttk.Style()
    style.configure(f'Gray.{base}', foreground='gray')


def set_gray_style(widget):
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


def set_normal_style(widget):
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


class Tasks(tab.Tab):
    def __init__(self, notebook, app):
        super().__init__(Tasks.EntryRow, app)

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

        save_button = ttk.Button(buttons, text="Сохранить", command=lambda: self.app.save())
        save_button.pack(anchor=tkinter.N, padx=6, pady=6, side='left')

        notebook.add(tasks, text="Домашки")

        make_gray_style('TCheckbutton')
        make_gray_style('TLabel')
        make_gray_style('TEntry')
        make_gray_style('TCombobox')
        make_gray_style('TButton')

    class EntryRow(tab.Tab.EntryRow):
        class Subtask:

            def __init__(self, row):
                self.row = row

                self.id = row.next_subtask_id
                row.next_subtask_id += 1

                self.done = tkinter.BooleanVar()
                self.done.set(False)
                self.done.trace_add('write', lambda name, index, mode: row.tab.app.mark_changed())

                self.name = tkinter.StringVar()
                self.name.trace_add('write', lambda name, index, mode: row.tab.app.mark_changed())

                self.widgets = [ttk.Checkbutton(row.subtask_frame, variable=self.done,
                                                command=lambda:
                                                self.marked_done() if self.done.get()
                                                else self.marked_not_done()),
                                ttk.Label(row.subtask_frame, text='Название:'),
                                ttk.Entry(row.subtask_frame, textvariable=self.name),
                                ttk.Button(row.subtask_frame, text="Удалить",
                                           command=lambda: row.remove_subtask(self.id))]

            def gray_out(self):
                for widget in self.widgets:
                    set_gray_style(widget)

            def ungray_out(self):
                for widget in self.widgets:
                    set_normal_style(widget)

            def marked_done(self):
                self.row.update_done()
                self.gray_out()

            def marked_not_done(self):
                self.row.update_done()
                self.ungray_out()

            def forget(self):
                for widget in self.widgets:
                    widget.grid_forget()

            def grid(self, row):
                for j in range(len(self.widgets)):
                    self.widgets[j].grid(row=row, column=j, sticky=tkinter.W + tkinter.E)

        def __init__(self, tasks):
            super().__init__(tasks)

            self.subject_var = tkinter.StringVar()
            self.subject = ttk.Combobox(tasks.task_entries, textvariable=self.subject_var)
            self.subject_var.trace_add('write', lambda name, index, mode: self.subject_updated())
            self.old_subject = ''

            self.done = tkinter.BooleanVar()
            self.done.set(False)
            self.done.trace_add('write', lambda name, index, mode: self.tab.app.mark_changed())

            self.name = tkinter.StringVar()
            self.name.trace_add('write', lambda name, index, mode: self.tab.app.mark_changed())

            self.time = tkinter.IntVar()
            self.time.trace_add('write', lambda name, index, mode: self.tab.app.mark_changed())

            self.deadline_variable = tkinter.StringVar()
            self.deadline_variable.trace_add('write', lambda name, index, mode: self.tab.app.mark_changed())

            self.deadline = tkcalendar.DateEntry(tasks.task_entries, locale=locale.getdefaultlocale()[0],
                                                 textvariable=self.deadline_variable)

            self.score = tkinter.IntVar()
            self.score.trace_add('write', lambda name, index, mode: self.score_updated())
            self.old_score = 0

            self.widgets = [ttk.Checkbutton(tasks.task_entries, variable=self.done,
                                            command=lambda:
                                            self.marked_done() if self.done.get()
                                            else self.marked_not_done()),
                            ttk.Label(tasks.task_entries, text='Название:'),
                            ttk.Entry(tasks.task_entries, textvariable=self.name),
                            ttk.Label(tasks.task_entries, text='Предмет:'),
                            self.subject,
                            ttk.Label(tasks.task_entries, text='Баллы:'),
                            ttk.Entry(tasks.task_entries, textvariable=self.score),
                            ttk.Label(tasks.task_entries, text='Часы бота:'),
                            ttk.Entry(tasks.task_entries, textvariable=self.time),
                            ttk.Label(tasks.task_entries, text='Дедлайн:'),
                            self.deadline,
                            ttk.Button(tasks.task_entries, text="Добавить", command=self.add_subtask),
                            ttk.Button(tasks.task_entries, text="Удалить", command=lambda: tasks.remove_row(self.id))]
            self.update_combobox()

            self.subtasks = []
            self.next_subtask_id = 0
            self.subtask_frame = ttk.Frame(tasks.task_entries)

        def update_combobox(self):
            self.subject['values'] = self.tab.app.subjects.subject_names()

        def gray_out(self):
            for widget in self.widgets:
                set_gray_style(widget)

        def ungray_out(self):
            for widget in self.widgets:
                set_normal_style(widget)

        def marked_done(self):
            self.tab.app.subjects.add_score(self.subject.get(), self.get_score())
            self.gray_out()

            for subtask in self.subtasks:
                subtask.done.set(True)
                subtask.gray_out()

        def marked_not_done(self):
            self.tab.app.subjects.add_score(self.subject.get(), -self.get_score())
            self.ungray_out()

            for subtask in self.subtasks:
                subtask.done.set(False)
                subtask.ungray_out()

        def update_done(self):
            done = all(subtask.done.get() for subtask in self.subtasks)
            if done and not self.done.get():
                self.done.set(True)
                self.tab.app.subjects.add_score(self.subject.get(), self.get_score())
                self.gray_out()
            elif not done and self.done.get():
                self.done.set(False)
                self.tab.app.subjects.add_score(self.subject.get(), -self.get_score())
                self.ungray_out()

        def score_updated(self):
            try:
                if self.done.get():
                    self.tab.app.subjects.add_score(self.subject.get(), self.score.get() - self.old_score)
                self.old_score = self.score.get()

                self.tab.app.mark_changed()
            except tkinter.TclError:
                pass

        def subject_updated(self):
            if self.done.get():
                self.tab.app.subjects.add_score(self.old_subject, -self.get_score())
                self.tab.app.subjects.add_score(self.subject.get(), self.get_score())
            self.old_subject = self.subject.get()

            self.tab.app.mark_changed()

        def grid(self, row):
            for j in range(len(self.widgets)):
                self.widgets[j].grid(row=2 * row, column=j, sticky=tkinter.W + tkinter.E)
            self.subtask_frame.grid(row=2 * row + 1, column=1, columnspan=len(self.widgets),
                                    sticky=tkinter.W + tkinter.E)

        def add_subtask(self):
            for subtask in self.subtasks:
                subtask.forget()
            self.subtasks.append(self.Subtask(self))
            for i in range(len(self.subtasks)):
                self.subtasks[i].grid(i)

            self.tab.app.mark_changed()

        def remove_subtask(self, deleted):
            for subtask in self.subtasks:
                subtask.forget()
            self.subtasks = [subtask for subtask in self.subtasks if subtask.id != deleted]
            for i in range(len(self.subtasks)):
                self.subtasks[i].grid(i)

            self.tab.app.mark_changed()

        def get_score(self):
            try:
                return self.score.get()
            except tkinter.TclError:
                return 0

        def get_time(self):
            try:
                return self.time.get()
            except tkinter.TclError:
                return 0

    def subject_renamed(self):
        for row in self.entry_rows:
            row.update_combobox()

    def sort(self):
        self.forget_all()

        order = plan.plan(int(datetime.datetime.now().timestamp() / 3600),
                          self.app.subjects.target_scores(), self.tasks())

        for row in self.entry_rows:
            row.gray_out()
        for i in order:
            self.entry_rows[i].ungray_out()
        self.entry_rows = ([self.entry_rows[i] for i in order]
                           + [entry_row for i, entry_row in enumerate(self.entry_rows) if i not in order])

        self.grid_all()

        self.app.mark_changed()

    def tasks(self):
        return [plan.Task(row.done.get(), row.name.get(), row.subject.get(), row.get_score(), row.get_time() * 3,
                          (row.deadline.get_date() - datetime.date(1970, 1, 1)).days * 24)
                for row in self.entry_rows]

    def saved_data(self):
        return [{
            'done': row.done.get(),
            'name': row.name.get(),
            'subject': row.subject.get(),
            'score': row.get_score(),
            'time': row.get_time(),
            'deadline': row.deadline.get_date().isoformat(),
            'subtasks': [{
                'name': subtask.name.get(),
                'done': subtask.done.get()
            } for subtask in row.subtasks]
        } for row in self.entry_rows]

    def load_data(self, data):
        for row in data:
            self.add_row()

            for subtask in row['subtasks']:
                self.entry_rows[-1].add_subtask()
                self.entry_rows[-1].subtasks[-1].name.set(subtask['name'])

                if subtask['done']:
                    self.entry_rows[-1].subtasks[-1].done.set(True)
                    self.entry_rows[-1].subtasks[-1].gray_out()

            if row['done']:
                self.entry_rows[-1].done.set(True)
                self.entry_rows[-1].gray_out()

            self.entry_rows[-1].name.set(row['name'])
            self.entry_rows[-1].subject.set(row['subject'])
            self.entry_rows[-1].score.set(row['score'])
            self.entry_rows[-1].time.set(row['time'])
            self.entry_rows[-1].deadline.set_date(datetime.datetime.fromisoformat(row['deadline']))
