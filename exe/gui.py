from tkinter import *
from PIL import Image, ImageTk
import pyscreenshot
import solver
import time
import random
class boardDimensions(object):
	def __init__(self):
		self.x = self.x_ranges()
		self.y = self.y_ranges()

	def __repr__(self):
		return(self.x,self.y)

	def x_ranges(self):
		r = {
		0: (8,54),
		1: (54,102),
		2: (104,149),
		3: (157,201),
		4: (203,250),
		5: (252,295),
		6: (303,346),
		7: (351, 396),
		8: (398, 445)
		}
		return r

	def y_ranges(self):
		r = {
		0: (8,53),
		1: (53,98),
		2: (98,143),
		3: (150,193),
		4: (193,239),
		5: (239,285),
		6: (292,335),
		7: (335,381),
		8: (381,426)
		}
		return r


def initialise(root):
	root.title('sudoku')
	root.resizable(False, False)
	root.minsize(453,435)
	root.update_idletasks()
	width = root.winfo_width()
	height = root.winfo_height()
	x = (root.winfo_screenwidth() // 2) - (width // 2)
	y = (root.winfo_screenheight() // 2) - (height // 2)
	root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
	return (x, y)

class board(object):
	def __init__(self, master):
		self.solvable = False
		self.solving = False
		self.verbose = False
		self.master= master
		self.solved_list = []
		self.tries = []
		self.selected = None
		self.numList = [[' ' for c in range(9)] for i in range(9)]
		self.canvas = Canvas(self.master,width=453,height=435)
		self.image= ImageTk.PhotoImage(Image.open('sudoku.png'))
		self.canvas.create_image(0,0,anchor=NW,image=self.image)
		self.canvas.pack()
		self.dimensions = boardDimensions()
		self.canvas.focus_set()
		self.canvas.bind('q',self.forcequit)
		self.canvas.bind('<Button-1>',self.mouseClick)
		self.canvas.bind('<Return>',self.solve)
		self.canvas.bind('<Key>', self.input_numbers)

	def mouseClick(self, event):
		self.selected = None
		print(event.x, event.y)
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
		self.master.update_idletasks()
		self.canvas.focus_set()
		if loc_x == None or loc_y == None:
			pass
		else:
			self.show_focus(loc_x,loc_y)
		return None
		

	def forcequit(self, event):
		self.master.overrideredirect(False)
		print('quit')
		self.master.update_idletasks()
		quit()

	def layer_of_text(self):
		self.canvas.delete('layertext')
		xcoordinate = {0: 31,1: 76,2: 127,3: 178,4: 226,5: 276,6: 325,7: 376,8: 420}
		ycoordinate = {0: 30,1: 76,2: 122,3: 171,4: 216,5: 265,6: 312,7: 357,8: 405}
		for i in range(9):
			for j in range(9):
				text =self.numList[i][j]
				self.canvas.create_text(xcoordinate.get(j), ycoordinate.get(i), text=text, fill='darkblue',font=('Purisa', 25),anchor=CENTER, tags='layertext')
		# return None


	def input_numbers(self, event):
		if event.char == 'v':
			self.verbose = not self.verbose 
		if not self.selected or event.char not in '123456789' or self.solving:
			print(event.char)
			print(selected)
			return
		else: 
			self.numList[self.selected[1]][self.selected[0]] = event.char
			self.layer_of_text()

	def transform(self, ll):
		rl = []
		for fsl in range(9):
			rl.append([])
			for snl in range(9):
				st = ll[fsl][snl]
				if st == ' ':
					st = '0'
				rl[fsl].append(int(st))
		return rl

	def solve(self, event):
		self.solving = True
		transformed = self.transform(self.numList)
		sudokuboard = solver.sudoku_board(transformed)
		sudokuboard.solve()
		self.tried = random.sample(sudokuboard.tried, random.randint(1,100)) if not self.verbose else sudokuboard.tried
		self.solved_list = sudokuboard.board
		self.solvable = bool(sudokuboard.finished)
		self.output() if self.solvable else self.find_culprit()

	def find_culprit(self):
		print(self.solvable)

	def output(self):
		# print(self.tried)
		for lists in self.tried:
			print(lists)
			self.numList = []
			self.numList = lists
			self.layer_of_text()
			self.master.update_idletasks()
			self.master.after(1, None)
		self.numList = self.solved_list
		self.layer_of_text()
		print(self.solvable)



	def show_focus(self, x ,y):
		if self.solving:
			return
		print(x, y)
		xvalues =self.dimensions.x.get(x)
		yvalues= self.dimensions.y.get(y)
		self.canvas.create_rectangle(xvalues[0],yvalues[0],xvalues[1],yvalues[1],outline='red',tags='current_rectangle',width=5)
		self.selected = (x, y)
		return None


if __name__ == '__main__':
	root = Tk()
	initialise(root)
	sudokuB = board(root)
	sudokuB.layer_of_text()
	root.mainloop()