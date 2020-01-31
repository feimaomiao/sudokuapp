from tkinter import *
# import tkinter.font
from tkinter import filedialog
from tkinter import font
from PIL import Image, ImageTk, ImageGrab
from .solver import *
import os, copy, time, random

font1 = "Courier 12"

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
		5: (252,297),
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
	
def initialise(root, name='sudoku-solver'):
	# Set window title
	root.title(name)
	# Set the window size and not allow user to change the size
	root.resizable(False, False)
	root.minsize(453,435)
	root.update_idletasks()
	width = root.winfo_width()
	height = root.winfo_height()
	print(root.winfo_screenwidth(), root.winfo_screenheight())
	x = (root.winfo_screenwidth() // 2) - (width // 2)
	y = (root.winfo_screenheight() // 2) - (height // 2)
	# Set root size and put to center
	root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
	return (x, y)

from .play_board import play_board

class board(object):
	def __init__(self):
		# Set user variables
		self.solvable = False
		self.solving = False
		self.verbose = False
		self.generated = False
		self.print_all = True
		self.master= Tk()
		self.font = font.Font(family='Purisa', size=25, weight='bold')
		# Initialises the root window
		initialise(self.master)
		print(self.master.winfo_x(), self.master.winfo_y())
		self.solved_list = []
		self.tries = []
		self.selected = None
		# Add in default numlist
		self.numList = [[' ' for c in range(9)] for i in range(9)]
		self.canvas = Canvas(self.master,width=453,height=435)
		self.image= ImageTk.PhotoImage(Image.open(os.path.join(os.getcwd(),'exe','sudoku.png')))
		# Put image into canvas
		self.canvas.create_image(0,0,anchor=NW,image=self.image)
		self.copy_of_board = []
		self.canvas.pack()
		self.dimensions = boardDimensions()
		# Put focus to canvas and set binding
		self.canvas.focus_set()
		self.canvas.bind('<Button-1>',self.mouseClick)
		self.canvas.bind('<Return>',self.solve)
		self.quitbind = self.canvas.bind('q',self.forcequit)
		self.canvas.bind('p', lambda action: self.set_nottrue('print_all'))
		self.canvas.bind('v', lambda action: self.set_nottrue('verbose'))
		self.canvas.bind('r', lambda action: self.clear_screen())
		self.canvas.bind('a', lambda action: self.change_focus('<Left>',3))
		self.canvas.bind('d', lambda action: self.change_focus('<Right>',3))
		self.canvas.bind('s', lambda action: self.change_focus('<Down>',3))
		self.canvas.bind('w', lambda action: self.change_focus('<Up>',3))
		# self.canvas.bind('h', self.help)
		self.canvas.bind('g', lambda action: self.generate_board())
		self.canvas.bind('<Left>', lambda action: self.change_focus('<Left>'))
		self.canvas.bind('<Right>', lambda action: self.change_focus('<Right>'))
		self.canvas.bind('<Up>', lambda action: self.change_focus('<Up>'))
		self.canvas.bind('<Down>', lambda action: self.change_focus('<Down>'))
		self.canvas.bind('<Key>', self.input_numbers)
		# Mainloop
		self.master.mainloop()

	def set_nottrue(self, action):
		if action == 'verbose':
			self.verbose = not(self.verbose)
		else:
			self.print_all = not(self.print_all)
		return


	def clear_screen(self):
		# Re-initialise the window
		self.numList = [[' ' for c in range(9)] for i in range(9)]
		self.solvable = False
		self.solving = False
		self.selected = None
		self.layer_of_text()
		return

	def change_focus(self, direction,no =1):
		# Change rectangle with arrow or wasd keys
		self.canvas.delete('current_rectangle')
		csx,csy = (0,0) if not self.selected else self.selected
		if direction == '<Left>':
			csx -= no
			if csx<0: csx+=9
			if not self.selected: csx = 8
			self.show_focus(csx, csy)
		elif direction == '<Right>':
			csx += no
			if csx >8: csx -= 9
			if not self.selected: csx = 0
			self.show_focus(csx, csy)
		elif direction == '<Up>':
			csy -= no
			if csy <0: csy += 9
			if not self.selected: csy = 8
			self.show_focus(csx, csy)
		else:
			csy += no
			if csy >8: csy -= 9
			if not self.selected: csy = 0
			self.show_focus(csx, csy)
		return

	def mouseClick(self, event):
		# Sense mouse click to certain location
		self.selected = None
		print(event.x, event.y)
		self.canvas.delete('current_rectangle')
		loc_y= None
		loc_x = None
		# Get location with dimension
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
			# Clicked on line
			pass
		else:
			# Put a rectangle on board with certaini dimension
			self.show_focus(loc_x,loc_y)
		return None
	
	def generate_board(self):
		try:
			self.canvas.delete('current_rectangle')
			self.canvas.unbind("q")
			self.numList = []
			# Hide the canvas including the photo
			self.canvas.pack_forget()
			var = StringVar()
			# Create a new frame to ask for the user input.
			frame = Frame(self.master, bg='black')
			frame.pack(fill=BOTH, expand = 1)
			# Add four radiobuttons and set different commannds
			easy = Radiobutton(frame, text='easy', command= lambda: var.set('easy'),indicatoron = 0)
			medium = Radiobutton(frame, text='medium', command= lambda: var.set('medium'),indicatoron = 0)
			hard= Radiobutton(frame, text='hard', command=lambda: var.set('hard'),indicatoron = 0)
			insane= Radiobutton(frame, text='insane', command= lambda: var.set('insane'),indicatoron = 0)
			for i in sorted(frame.children):
				frame.children[i].pack()
			hard.wait_variable(var)
			self.numList, self.correct= return_generated_board(var.get())
			print(self.numList, self.correct)
			frame.destroy()
			print('Canvas created')
			self.canvas.pack()
			self.layer_of_text()
			self.master.tk.call('set','fontmap(%s)'%font1, 'Purisa 25 bold')
			res = self.master.tk.call('array', 'get', 'fontmap')
			print(res)
			self.canvas.postscript(fontmap='fontMap',colormode='color',file=os.path.join(os.getcwd(), 'exe/temp/temp')+'.eps')
			img=Image.open('exe/temp/temp.eps')
			img.save('exe/temp/temp.png', 'png')
			os.remove('exe/temp/temp.eps')
			self.generated=True
			self.master.overrideredirect(False)
			print('quit')
			self.master.update_idletasks()
			self.master.destroy()
			return
		except SystemExit:
			print('it doesnt work')
			hard.set('hard')
		except TimeoutError:
			hard.set('hard')
			print('go')
			quit()

	def forcequit(self, event):
		self.master.overrideredirect(False)
		print('quit')
		self.master.update_idletasks()
		self.master.destroy()
		return

	def layer_of_text(self):
		self.canvas.delete('layertext')
		xcoordinate = {0: 31,1: 76,2: 127,3: 178,4: 226,5: 276,6: 325,7: 376,8: 420}
		ycoordinate = {0: 30,1: 76,2: 122,3: 171,4: 216,5: 265,6: 312,7: 357,8: 405}
		for i in range(9):
			for j in range(9):
				text =self.numList[i][j] if self.numList[i][j] != 0 else ' '
				self.canvas.create_text(xcoordinate.get(j), ycoordinate.get(i), text=text, fill='darkblue',font=self.font,anchor=CENTER, tags='layertext')
		return 

	@timeout(2)
	def input_numbers(self, event):
		try:
			# lets user input number
			if not self.selected or event.char not in '0123456789' or self.solving: pass
			else: 
				inputed = event.char
				if inputed == '0':      
					inputed = ' '
				self.numList[self.selected[1]][self.selected[0]] = inputed
				self.numList  = self.transform(self.numList)
				test = sudoku_board(self.numList)
				if test.finished:
					self.numList[self.selected[1]][self.selected[0]] = inputed
					self.layer_of_text()
				else:   
					self.numList[self.selected[1]][self.selected[0]] = 0
					self.layer_of_text()
		except TimeoutError:
			pass

	@staticmethod
	def transform(ll):
		# change spaces for output to int 0s
		rl = []
		for fsl in range(9):
			rl.append([])
			for snl in range(9):
				st = ll[fsl][snl]
				if st == ' ' or st == '':   st = '0'
				rl[fsl].append(int(st))
		return rl

	def solve(self, event):
		if self.solving:    return
		self.solving = True
		transformed = self.transform(self.numList)
		sudokuboard = sudoku_board(transformed)
		self.solvable = sudokuboard.finished
		print(self.verbose)
		print(self.print_all)
		try:                
			if self.verbose:
				self.tried = sudokuboard.tried 
			else:
				self.tried=random.sample(sudokuboard.tried,random.randrange(20,100))
		except ValueError:  
			pass
		self.solved_list = sudokuboard.board
		print(sudokuboard.sum)
		self.output()
		return

	def output(self):
		try:
			if self.tried == None: 
				self.print_all = False
		except AttributeError:
			self.print_all= False
		if self.print_all:
			for lists in self.tried:
				self.numList = []
				self.numList = lists
				self.layer_of_text()
				self.canvas.after(1, None)
				self.master.update_idletasks()
		self.numList = self.solved_list
		self.layer_of_text()
		return

	def show_focus(self, x ,y):
		if self.solving:    return
		print(x, y)
		xvalues =self.dimensions.x.get(x)
		yvalues= self.dimensions.y.get(y)
		self.canvas.create_rectangle(xvalues[0],yvalues[0],xvalues[1],yvalues[1],outline='red',tags='current_rectangle',width=5)
		self.selected = (x, y)
		return  

def main():
	sudokuB = board()
	if not sudokuB.generated:
		print('Thank you!')
		raise SystemExit
	print(sudokuB)
	thing = play_board(sudokuB.numList)
	quit()
