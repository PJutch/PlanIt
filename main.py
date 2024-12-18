import tkinter
from tkinter import ttk

import save
from subjects import Subjects
from tasks import Tasks


class App:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title('PlanIt')

        notebook = ttk.Notebook()
        notebook.pack(expand=True, fill=tkinter.BOTH)

        self.subjects = Subjects(notebook, self)
        self.tasks = Tasks(notebook, self)

        save.load(self.subjects, self.tasks)

        self.changed = False

    def run(self):
        self.window.mainloop()

    def save(self):
        save.save(self.subjects, self.tasks)
        self.changed = False

    def mark_changed(self):
        self.changed = True


if __name__ == '__main__':
    App().run()
