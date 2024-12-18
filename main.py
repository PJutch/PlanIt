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

        self.subjects = Subjects(notebook)
        self.tasks = Tasks(notebook)

        self.subjects.tasks = self.tasks
        self.tasks.subjects = self.subjects

        save.load(self.subjects, self.tasks)

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    App().run()
