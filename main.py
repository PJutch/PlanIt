import tkinter
from tkinter import ttk
from tkinter import messagebox

import save
from subjects import Subjects
from tasks import Tasks


class App:
    def __init__(self):
        self.__window = tkinter.Tk()

        notebook = ttk.Notebook()
        notebook.pack(expand=True, fill=tkinter.BOTH)

        self.subjects = Subjects(notebook, self)
        self.tasks = Tasks(notebook, self)

        save.load(self.subjects, self.tasks)

        self.__window.title('PlanIt')
        self.__changed = False

        self.__window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def run(self):
        self.__window.mainloop()

    def save(self):
        save.save(self.subjects, self.tasks)
        self.__changed = False
        self.__window.title('PlanIt')

    def mark_changed(self):
        self.__changed = True
        self.__window.title('*PlanIt')

    def on_closing(self):
        if self.__changed:
            save = messagebox.askyesnocancel(title='Сохранить?', message='Сохранить внесённые изменения?')
            if save:
                self.save()
            if save is not None:
                self.__window.destroy()
        else:
            self.__window.destroy()


if __name__ == '__main__':
    App().run()
