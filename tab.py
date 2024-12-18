import tkinter


class Tab:
    def __init__(self, row_type):
        self.entry_rows: list[row_type] = []
        self.next_row_id = 0

    class EntryRow:
        def __init__(self, tab):
            self.tab = tab

            self.id = tab.next_row_id
            tab.next_row_id += 1

            self.widgets = None

        def forget(self):
            for widget in self.widgets:
                widget.grid_forget()

        def grid(self, row):
            for j in range(len(self.widgets)):
                self.widgets[j].grid(row=row, column=j, sticky=tkinter.W + tkinter.E)

    def forget_all(self):
        for row in self.entry_rows:
            row.forget()

    def grid_all(self):
        for i in range(len(self.entry_rows)):
            self.entry_rows[i].grid(i)

    def remove_row(self, deleted):
        self.forget_all()
        self.entry_rows = [row for row in self.entry_rows if row.id != deleted]
        self.grid_all()

    def add_row(self):
        self.forget_all()
        self.entry_rows.append(self.EntryRow(self))
        self.grid_all()

    def clear(self):
        self.forget_all()
        self.entry_rows = []
