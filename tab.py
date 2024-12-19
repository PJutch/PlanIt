import tkinter


class Tab:
    def __init__(self, row_type, app):
        self._entry_rows: list[row_type] = []
        self.__next_row_id = 0

        self.app = app

    def next_row_id(self):
        res = self.__next_row_id
        self.__next_row_id += 1
        return res

    class EntryRow:
        def __init__(self, tab):
            self.tab = tab
            self.id = self.tab.next_row_id()
            self._widgets = None

        def forget(self):
            for widget in self._widgets:
                widget.grid_forget()

        def grid(self, row):
            for j in range(len(self._widgets)):
                self._widgets[j].grid(row=row, column=j, sticky=tkinter.W + tkinter.E)

    def forget_all(self):
        for row in self._entry_rows:
            row.forget()

    def grid_all(self):
        for i in range(len(self._entry_rows)):
            self._entry_rows[i].grid(i)

    def remove_row(self, deleted):
        self.forget_all()
        self._entry_rows = [row for row in self._entry_rows if row.id != deleted]
        self.grid_all()

        self.app.mark_changed()

    def add_row(self):
        self.forget_all()
        self._entry_rows.append(self.EntryRow(self))
        self.grid_all()

        self.app.mark_changed()

    def clear(self):
        self.forget_all()
        self._entry_rows = []
