import plan
from subjects import Subjects
from tasks import Tasks

import tkinter
from tkinter import ttk

if __name__ == '__main__':
    window = tkinter.Tk()
    window.title('PlanIt')

    notebook = ttk.Notebook()
    notebook.pack(expand=True, fill=tkinter.BOTH)

    subjects = Subjects(notebook)
    tasks = Tasks(notebook)

    subjects.tasks = tasks
    tasks.subjects = subjects

    print(plan.plan(0, {'math': 5, 'english': 5},
                    [plan.Task('math_homework', 'math', 5, 3, 10),
                     plan.Task('math_homework', 'math', 5, 3, 10),
                     plan.Task('english_homework', 'english', 7, 4, 10),
                     plan.Task('english_homework', 'english', 7, 4, 10)]))

    window.mainloop()
