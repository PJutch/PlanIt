import tkinter
from tkinter import ttk


entry_rows = []


def remove_row(row_index):
    for widget in entry_rows[row_index]:
        widget.pack_forget()
    del entry_rows[row_index]


def add_row():
    entry_rows.append([ttk.Entry(frame),
                       ttk.Button(frame, text="Удалить", command=lambda: None)])

    for i in range(len(entry_rows[-1])):
        entry_rows[-1][i].grid(column=i, row=len(entry_rows) - 1, sticky=tkinter.W+tkinter.E)

    add_button.pack_forget()
    add_button.pack(anchor=tkinter.N, padx=6, pady=6)


if __name__ == '__main__':
    window = tkinter.Tk()
    window.title('PlanIt')

    frame = ttk.Frame(window)
    frame.columnconfigure(0, weight=1)
    frame.pack(fill=tkinter.X)

    add_button = ttk.Button(text="Добавить", command=add_row)
    add_row()

    window.mainloop()
