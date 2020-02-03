import PIL, os, copy, time
from .gui import boardDimensions, initialise
from .solver import *
from tkinter import font
from tkinter import messagebox
from tkinter import *
class play_board(object):
	def __init__(self, board):
		self.starttime = time.time()
		self.selected = None
		self.dimensions = boardDimensions()
		# Do not cahnge. used to check which grid is empty.
		# board = [[1,1,1,1,1,1,1,1,0]]+ [[0,0,0,0,0,0,0,0,1] for i in range(8)]
		# print(board)
		self.board_unsolved = copy.deepcopy(board)
		# Board that user used to enter numbers[]
		self.board = copy.deepcopy(board)
		self.master = Tk()
		initialise(self.master, name='sudoku-play')
		self.canvas = Canvas(self.master, name='sudoku-game')
		self.canvas = Canvas(self.master,width=453,height=435)
		self.image= PIL.ImageTk.PhotoImage(PIL.Image.open(os.path.join(os.getcwd(),'exe','temp','temp.png')))
		self.canvas.create_image(0,0,anchor=NW,image=self.image)
		self.canvas.focus_set()
		self.canvas.bind('q', self.forcequit)
		self.canvas.bind('r', self.empty_screen)
		self.canvas.bind('<Up>', self.move_vertical)
		self.canvas.bind('<Down>', self.move_vertical)
		self.canvas.bind('<Left>', self.move_horizontal)
		self.canvas.bind('<Right>', self.move_horizontal)
		self.canvas.bind('<Button-1>', self.mouseClick)
		self.canvas.bind('<Return>', self.check)
		self.canvas.bind('<Key>', self.input_numbers)
		self.font = font.Font(family='Purisa', size=25, weight='bold')
		self.canvas.pack()
		self.master.mainloop()

	def check(self, event):
		print(self.board)
		for i in self.board:
			for j in i:
				if j == 0:
					messagebox.showerror("Wait...That's illegal", "You have not finished this puzzle yet!")
					self.canvas.itemconfigure('inputnums', fill='red')
					self.canvas.focus_force()
					return False
		self.check_solve()

	@staticmethod
	def toint(board):
		m = [[0 for i in range(9)] for j in range(9)]
		for i in range(9):
			for j in range(9):
				m[i][j] = int(board[i][j])
		return m


	def check_solve(self):
		self.board= self.toint(self.board)
		suboard = sudoku_board(self.board)
		solved = suboard.finished
		print(solved)
		if solved:
			self.master.withdraw()
			messagebox.showinfo("Success!", "Congratulations! You successfully solved the board\nYou solved this box in {} seconds".format(round(time.time()-self.starttime)))
			quit()
		else:
			self.master.withdraw()
			messagebox.showwarning("Whooops!", "Some of the numbers are not entered properly!")
			self.canvas.itemconfigure('inputnums', fill='red')
			self.master.deiconify()
			self.canvas.focus_force()
		return


	@staticmethod
	def move_one(l, cur, lr):
		current_pos = l.index(cur)
		if lr:
			mv = current_pos + 1
			if mv >= len(l):
				mv -= len(l)
		else:
			mv = current_pos - 1
			if mv <0:
				mv += len(l)
		return l[mv]


	def move_horizontal(self, event):
		pos = []
		print(ord(event.char))
		keys = {63235: True, 63234: False}
		if not bool(self.selected):
			for j in range(9):
				for i in range(9):
					if self.board_unsolved[j][i] ==0:
						pos.append(i)
				if len(pos) >= 1:
					print(pos)
					break
			if keys.get(ord(event.char)):
				k = 0
			else:
				k = -1
			self.show_focus(pos[k], j)
		else:
			pos = [i for i in range(9) if self.board_unsolved[self.selected[1]][i] == 0]
			print(pos)
			self.show_focus(self.move_one(pos, self.selected[0], keys.get(ord(event.char))), self.selected[1])
		return

	def move_vertical(self, event):
		pos = []
		keys = {63232: False, 63233: True}
		if not bool(self.selected):
			for j in range(9):
				for i in range(9):
					if self.board_unsolved[i][j] == 0:
						pos.append(i)
				if len(pos)>= 1:
					print(pos)
					break
			print(ord(event.char))
			if not keys.get(ord(event.char)):
				k = -1
			else:
				k = 0
			self.show_focus(j, pos[k])
		else:
			print(self.selected)
			pos = [i for i in range(9) if self.board_unsolved[i][self.selected[0]] == 0]
			print(pos)
			self.show_focus(self.selected[0], self.move_one(pos, self.selected[1], keys.get(ord(event.char))))
		return


	def mouseClick(self, event):
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
			self.selected = None
			return
		self.show_focus(loc_x, loc_y)
		return

	def forcequit(self, event):
		# removes created file
		os.remove('exe/temp/temp.png')
		self.master.overrideredirect(False)
		print('quit')
		# Clears any unfinished jobs
		self.master.update_idletasks()
		self.master.destroy()
		quit()
		
	def empty_screen(self, event):
		self.board = copy.deepcopy(self.board_unsolved)
		self.canvas.delete('inputnums')
		print(self.board)

	def show_focus(self, x ,y):
		self.selected = None
		self.canvas.delete('current_rectangle')
		print(x, y)
		xvalues =self.dimensions.x.get(x)
		yvalues= self.dimensions.y.get(y)
		if self.board_unsolved[y][x] != 0:
			print('not valid')
			return False
		self.canvas.create_rectangle(xvalues[0],yvalues[0],xvalues[1],yvalues[1],outline='blue',tags='current_rectangle',width=5)
		self.selected = (x, y)
		return

	def input_numbers(self, event):
		self.canvas.itemconfigure('inputnums', fill='green')
		xcoordinate = {0: 31,1: 76,2: 127,3: 178,4: 226,5: 276,6: 325,7: 376,8: 420}
		ycoordinate = {0: 30,1: 76,2: 122,3: 171,4: 216,5: 265,6: 312,7: 357,8: 405}
		if not bool(self.selected) or event.char not in '1234567890':
			print(event.char)
			return
		x, y = self.selected
		self.board[y][x] = event.char
		print(self.board)
		print(self.board[x][y])
		text = event.char
		if text == '0': 
			text = ' '
		tag = 'l{}{}'.format(x,y)
		print(tag)
		self.canvas.delete(str(tag))
		self.canvas.create_text(xcoordinate.get(x), ycoordinate.get(y), text=text, fill='green', font=self.font, anchor=CENTER, tags=(str(tag), 'inputnums'))
		return



