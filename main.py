import subjects
import tasks

import tkinter
from tkinter import ttk


if __name__ == '__main__':
    window = tkinter.Tk()
    window.title('PlanIt')

    notebook = ttk.Notebook()
    notebook.pack(expand=True, fill=tkinter.BOTH)

    tasks.Tasks(notebook)
    subjects.Subjects(notebook)

    window.mainloop()
