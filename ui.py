
import tkinter as tk


class Interface:

    def __init__(self):
        self.win = tk.Tk()
        self.win.geometry('1200x800')

        self.menu_bar = tk.Menu(self.win)
        self.test_menu = tk.Menu(self.menu_bar)

        self.menu_bar.add_cascade(label='test_menu', menu=self.test_menu)
        self.win.config(menu=self.menu_bar)

    def run(self):
        self.win.mainloop()
