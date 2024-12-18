import tkinter
from tkinter import ttk
from tkinter import messagebox

import save
from subjects import Subjects
from tasks import Tasks


class App:
    def __init__(self):
        self.window = tkinter.Tk()

        notebook = ttk.Notebook()
        notebook.pack(expand=True, fill=tkinter.BOTH)

        self.subjects = Subjects(notebook, self)
        self.tasks = Tasks(notebook, self)

        save.load(self.subjects, self.tasks)

        self.window.title('PlanIt')
        self.changed = False

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def run(self):
        self.window.mainloop()

    def save(self):
        save.save(self.subjects, self.tasks)
        self.changed = False
        self.window.title('PlanIt')

    def mark_changed(self):
        self.changed = True
        self.window.title('*PlanIt')

    def on_closing(self):
        if self.changed:
            save = messagebox.askyesnocancel(title='Сохранить?', message='Сохранить внесённые изменения?')
            if save:
                self.save()
            if save is not None:
                self.window.destroy()
        else:
            self.window.destroy()


if __name__ == '__main__':
    App().run()
