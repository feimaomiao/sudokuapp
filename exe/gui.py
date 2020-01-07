from tkinter import *
from math import ceil
from PIL import Image, ImageTk
from solver import *

def initialise(root,transparent= False):
	root.title('sudoku')
	root.resizable(False, False)
	root.minsize(453,435)
	root.update_idletasks()
	root.overrideredirect(True)
	root.attributes('-alpha', 0.0) if transparent else None
	width = root.winfo_width()
	height = root.winfo_height()
	x = (root.winfo_screenwidth() // 2) - (width // 2)
	y = (root.winfo_screenheight() // 2) - (height // 2)
	root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

class board(object):
	def __init__(self, master):
		self.master= master
		self.numList = [[0 for c in range(9)] for i in range(9)]
		
	def draw_board(self):
		render = ImageTk.PhotoImage(Image.open('sudoku.png'))
		self.img = Label(self.master, image=render)
		self.img.image=render
		self.img.pack()
		# self.img.bind('<Key>', self.mouseClick)
		# self.img.bind('<Button-1>',self.mouseClick)


	def mouseClick(self, event):
		self.clicker.destroy()
		self.master.update_idletasks()
		self.master.overrideredirect(False)
		# self.master.bind('<Key>', quit)
		loc_x =event.x
		loc_y = event.y
		yposition = round((loc_y/453) *9)
		xposition = ceil((loc_x/435) *9) - 1
		print(xposition, yposition)
		self.layer_of_text()

	def quit(self, event):
		self.clicker.update_idletasks()
		self.master.update_idletasks()
		self.clicker.overrideredirect(False)
		self.master.overrideredirect(False)
		quit()

	def layer_of_text(self):
		xcoordinate = {0: 17,1: 65,2: 114,3: 165,4: 215,5: 263,6: 314,7: 362,8: 410}
		ycoordinate = {0: 14,1: 59,2: 105,3: 150,4: 196,5: 247,6: 295,7: 341,8: 387}
		lst= []
		
		for count, i in enumerate(self.numList):
			lst.append([])
			for j in i:
				# text = StringVar(self.master, j)
				lst[count].append(Label(self.master, text=j, fg='blue',font=(None,25)))
		for i in range(9):
			for j in range(9):
				lst[i][j].place(x=xcoordinate.get(j), y=ycoordinate.get(i))
		# self.img.bind('<Button-1>',self.mouseClick)
		self.clicker = Tk()
		# self.clicker.attributes('-alpha',0.0)
		initialise(self.clicker, True)
		self.clicker.focus_set()
		self.clicker.bind('<Button-1>', self.mouseClick)
		self.clicker.bind('<Return>', self.mouseClick)
		self.clicker.bind('q', self.quit)






# A.y == 14
# B.Y == 59
# C.Y == 105
# D.Y == 150
# E.Y == 196
# F.Y == 247
# G.Y == 295
# H.Y == 341
# I.Y == 387

# 0.x == 17
# 1.x == 65
# 2.x == 114
# 3.x == 165
# 4.x == 215
# 5,x == 263
# 6.x == 314
# 7.x == 362
# 8.x == 410

# 0, 1, 2, 3, 4, 5, 6, 7 ,8 ,9
# a
# b
# c
# ...

if __name__ == '__main__':
	root = Tk()
	initialise(root)
	sudokuB = board(root)
	# root.bind('<Button-1>', sudokuB.mouseClick)
	sudokuB.draw_board()
	sudokuB.layer_of_text()
	root.mainloop()