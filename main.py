import tkinter
from tkinter import ttk

from subjects import Subjects
from tasks import Tasks

if __name__ == '__main__':
    window = tkinter.Tk()
    window.title('PlanIt')

    notebook = ttk.Notebook()
    notebook.pack(expand=True, fill=tkinter.BOTH)

    subjects = Subjects(notebook)
    tasks = Tasks(notebook)

    subjects.tasks = tasks
    tasks.subjects = subjects

    window.mainloop()
