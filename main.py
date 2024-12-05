import tkinter
from tkinter import ttk
import tkcalendar

entry_rows = []
next_row_id = 0


class EntryRow:
    def __init__(self):
        global next_row_id
        self.id = next_row_id
        next_row_id += 1

        self.score = tkinter.IntVar()
        self.widgets = [ttk.Entry(frame),
                        ttk.Entry(frame, textvariable=self.score),
                        tkcalendar.DateEntry(frame),
                        ttk.Button(frame, text="Удалить", command=lambda: remove_row(self.id))]

    def forget(self):
        for widget in self.widgets:
            widget.grid_forget()

    def grid(self, row):
        for j in range(len(self.widgets)):
            self.widgets[j].grid(row=row, column=j, sticky=tkinter.W + tkinter.E)


def remove_row(deleted):
    global entry_rows

    for row in entry_rows:
        row.forget()

    entry_rows = [row for row in entry_rows if row.id != deleted]

    for i in range(len(entry_rows)):
        entry_rows[i].grid(i)


def add_row():
    global entry_rows

    for row in entry_rows:
        row.forget()

    entry_rows.append(EntryRow())

    for i in range(len(entry_rows)):
        entry_rows[i].grid(i)


if __name__ == '__main__':
    window = tkinter.Tk()
    window.title('PlanIt')

    frame = ttk.Frame(window)
    frame.columnconfigure(0, weight=1)
    frame.pack(fill=tkinter.X)

    add_button = ttk.Button(text="Добавить", command=add_row)
    add_button.pack(anchor=tkinter.N, padx=6, pady=6)

    window.mainloop()
