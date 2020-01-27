from .gui import boardDimensions, initialise
import PIL
# from PIL import Image, ImageTk
import os
from tkinter import *
import copy
class play_board(object):
	def __init__(self, board):
		self.dimensions = boardDimensions()
		# Do not cahnge. used to check which grid is empty.
		self.board_unsolved = copy.deepcopy(board)
		self.board = copy.deepcopy(board)
		self.master = Tk()
		initialise(self.master, name='sudoku-play')
		self.canvas = Canvas(self.master, name='sudoku-game')
		self.canvas = Canvas(self.master,width=453,height=435)
		self.image= PIL.ImageTk.PhotoImage(PIL.Image.open(os.path.join(os.getcwd(),'exe','temp','temp.png')))
		self.canvas.create_image(0,0,anchor=NW,image=self.image)
		self.canvas.focus_set()
		self.canvas.bind('q', self.forcequit)
		self.canvas.bind('<Button-1>', self.mouseClick)
		self.canvas.pack()
		self.master.mainloop()

	def mouseClick(self, event):
		self.canvas.delete('current_rectangle')
		loc_y= None
		loc_x = None
		for count, items in enumerate(self.dimensions.x.values()):
			if event.x in range(items[0], items[1]):
				loc_x = list(self.dimensions.x.keys())[count]
				break
		for count,items in enumerate(self.dimensions.y.values()):
			if event.y in range(items[0],items[1]):
				loc_y = list(self.dimensions.y.keys())[count]
				break
		print(loc_x,loc_y)
		if loc_x == None or loc_y == None:
			print('This is erroor')
			return
		self.show_focus(loc_x, loc_y)

	def forcequit(self, event):
		os.remove('exe/temp/temp.png')
		self.master.overrideredirect(False)
		print('quit')
		self.master.update_idletasks()
		self.master.destroy()
		raise SystemExit

	def show_focus(self, x ,y):
		self.selected = None
		print(x, y)
		xvalues =self.dimensions.x.get(x)
		yvalues= self.dimensions.y.get(y)
		if self.board_unsolved[y][x] != 0:
			return
		self.canvas.create_rectangle(xvalues[0],yvalues[0],xvalues[1],yvalues[1],outline='blue',tags='current_rectangle',width=5)
		self.selected = (x, y)
		return 

	def input_numbers(self, event):
		if not bool(self.selected) or event.char not in '1234567890':
			return
		self.board[x][y] = event.char
		print(self.board)
		

