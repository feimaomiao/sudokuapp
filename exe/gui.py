from tkinter import *
from PIL import Image, ImageTk
from solver import *

def initialise(root):
	root.title('sudoku')
	root.minsize(453,435)
	root.update_idletasks()
	width = root.winfo_width()
	height = root.winfo_height()
	x = (root.winfo_screenwidth() // 2) - (width // 2)
	y = (root.winfo_screenheight() // 2) - (height // 2)
	root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

class board(object):
	def __init__(self, master):
		self.master= master
		self.numList = [[0 for c in range(9)] for i in range(9)]
		self.frame = Frame(self.master)
		
	def draw_board(self):
		render = ImageTk.PhotoImage(Image.open('sudoku.png'))
		self.img = Label(self.master, image=render)
		self.img.image=render
		self.img.pack()
		self.img.focus_set()
		self.img.bind('<Key>', self.mouseClick)
		self.img.bind('<Button-1>',self.mouseClick)


	def mouseClick(self, event):
		print(event)
		# self.frame.pack()
		p = Label(self.master, text='1', fg='blue',font=(None, 25))
		p.place(x=410,y=14)

	def layer_of_text(self):
		self.frame.pack()
		xcoordinate = {0: 17,1: 65,2: 114,3: 165,4: 215,5: 263,6: 314,7: 362,8: 410}
		ycoordinate = {0: 14,1: 59,2: 105,3: 150,4: 196,5: 247,6: 295,7: 341,8: 387}
		lst= []
		# self.frame.focus_set()
		for count, i in enumerate(self.numList):
			lst.append([])
			for j in i:
				# text = StringVar(self.master, j)
				lst[count].append(Label(self.master, text=j, fg='blue',font=(None,25)))
		print(lst)
		for i in range(9):
			for j in range(9):
				lst[i][j].place(x=xcoordinate.get(j), y=ycoordinate.get(i))
		self.frame.pack()


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
	sudokuB.draw_board()
	sudokuB.layer_of_text()
	root.mainloop()