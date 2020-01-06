from tkinter import *
from backtrack import *
class gui():
	def __init__(self):
		self.root = Tk()
		self.root.title('Suduku solver by Matthew Lam')
		self.root.minsize(500,400)

	def center(self):
	    self.root.update_idletasks()
	    width = self.root.winfo_width()
	    height = self.root.winfo_height()
	    x = (self.root.winfo_screenwidth() // 2) - (width // 2)
	    y = (self.root.winfo_screenheight() // 2) - (height // 2)
	    self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

k = gui()
k.root.mainloop()                                                               