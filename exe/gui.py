from tkinter import *
from tkinter import messagebox, filedialog, font
from PIL import Image, ImageTk
from .solver import *
from .play_board import play_board
import os, copy, time, random, PIL, sys
from stat import S_IRWXG

# os.environ["PATH"] += ":/usr/local/bin:/usr/local/bin/gs"
global font1
font1 = "Courier 12"


class suboard(object):
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
		self.solved_list = []
		self.tries = []
		self.selected = None
		# Add in default numlist
		self.numList = [[' ' for c in range(9)] for i in range(9)]
		self.canvas = Canvas(self.master,width=453,height=435)
		self.copy_of_board = []
		self.canvas.pack()
		self.dimensions = boardDimensions()
		self.canvas.focus_set()
		self.file = Image.open('exe/sudoku.png')
		self.image= ImageTk.PhotoImage(self.file)
		self.canvas.create_image((0,0),anchor=NW,image=self.image)
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
		self.canvas.bind('h', self.usrhelp)
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

	def usrhelp(self, event=None):
		STRING = r''''r': Clear Screen
'g': Generate board to play
'p': Set Flag 'print all'
'v': Set Flag 'Verbose'
'up','left','down','right': Move to up, left, down and right 1 grid respectively
'w','a','s','d': Move to up, left, down and right 3 grids respectively
'''
		messagebox.showinfo('Seems like you need some help', STRING)
		self.canvas.focus_force()


	def clear_screen(self):
		# Re-initialise the window
		self.numList = [[' ' for c in range(9)] for i in range(9)]
		self.solvable = False
		self.solving = False
		self.selected = None
		self.layer_of_text()
		return

	@timeout(2)
	def change_focus(self, direction,no =1):
		try:
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
		except TimeoutError:
			return

	def mouseClick(self, event):
		# Sense mouse click to certain location
		self.selected = None
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
		# message to tell the users that the randomizer would take a long time to output the numbers
		messagebox.showinfo("Before you start", "The generate function is a heavily randomized function.\
			\nThis action would take up to 10 seconds to generate a board.\
			\nThe random function will start after you choose the difficulty")
		try:
			# Deletes current rectangle or it ill be included in postscript file
			self.canvas.delete('current_rectangle')
			# Unbinds quit function because forcequit during waitvar would raise an error
			self.canvas.unbind("q")
			self.numList = []
			# Hide the canvas including the photo
			self.canvas.pack_forget()
			var = StringVar()
			# Create a new frame to ask for the user input.
			frame = Frame(self.master, bg='black')
			frame.pack(fill=BOTH, expand = 1)
			self.master.overrideredirect(True)
			# Add four radiobuttons and set different commannds
			easy = Radiobutton(frame, text='easy', command= lambda: var.set('easy'),indicatoron = 0)
			medium = Radiobutton(frame, text='medium', command= lambda: var.set('medium'),indicatoron = 0)
			hard= Radiobutton(frame, text='hard', command=lambda: var.set('hard'),indicatoron = 0)
			insane= Radiobutton(frame, text='insane', command= lambda: var.set('insane'),indicatoron = 0)
			for i in sorted(frame.children):
				# Packs the four radiobuttons
				frame.children[i].pack()
			# Waits for user to choose one before continuing
			hard.wait_variable(var)
			generatestarttime = time.time()
			# Get 
			self.numList= return_generated_board(var.get())
			messagebox.showinfo("Generation finished", f"The generation function has been finished.\nThe generation used {round(time.time() - generatestarttime, 6)} seconds")
			frame.destroy()
			self.canvas.pack()
			self.layer_of_text()

			# Sets text in postscript
			self.master.tk.call('set','fontmap(%s)'%font1, 'Purisa 25 bold')
			# Creates postscript file and saves as eps photo
			self.canvas.postscript(fontmap='fontMap',colormode='color',file='exe/temp/temp'+'.eps')
			# Opens postscript eps file and opens as png
			messagebox.showinfo('test',os.path.dirname(os.path.abspath('exe/temp/temp.eps')))
			img = Image.open(os.path.abspath('exe/temp/temp.eps'))
			messagebox.showinfo('test', 'line 193')
			os.chmod('exe/temp',0o777)
			os.chmod('exe/temp/temp.eps', 0o777)
			messagebox.showinfo('test','line 188,{}'.format(os.path.dirname(os.path.abspath('exe'))))
			messagebox.showinfo('test2','line 189{}'.format(os.access(os.path.join(os.path.dirname(os.path.abspath('exe')), 'exe','temp'), os.W_OK)))
			# with open(os.path.join(os.path.dirname(os.path.abspath('exe')), 'exe','temp','temp.png'), 'wb') as png_file:
			# 	messagebox.showinfo('inf','201')
			# 	img.save(png_file)
			img.save(os.path.join('exe','temp','temp.png'), 'png')
			messagebox.showinfo('success','line 204')
			os.remove('exe/temp/temp.eps')
			self.generated=True
			self.master.overrideredirect(False)
			self.master.update_idletasks()
			self.master.destroy()
			return
		except Exception as e:
			messagebox.showinfo('error', '{}'.format(e))

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
			if not self.selected or event.char not in '0123456789' or self.solving: self.usrhelp()
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
		self.master.update_idletasks()
		if self.solving:
			return
		starttime = time.time()
		self.solving = True
		# Clears the board, empties the board.
		self.show_focus(0, 0)
		transformed = self.transform(self.numList)
		sudokuboard = sudoku_board(transformed)
		# print('printall',self.print_all, '\nverbose',self.verbose)
		sudokuboard.solve(generate=not self.print_all)
		self.solvable = sudokuboard.finished
		try:                
			# Verbose tries
			if self.verbose:
				self.tried = sudokuboard.tried 
			else:
				self.tried=random.sample(sudokuboard.tried,random.randrange(20,100))
		except ValueError:  
			# Random number>length of board tries
			pass

		# Returns solved list
		self.solved_list = sudokuboard.board
		self.solving = False
		# output attempts
		return self.output(starttime = starttime, tries=sudokuboard.sum)

	def output(self, starttime, tries):
		try:
			# Catches error which occurs when the user does not ask for verbose//Catch error in which no error is thrown
			if self.tried == None: 
				self.print_all = False
		except AttributeError:
			self.print_all= False

		# Print tries
		if self.print_all:
			for lists in self.tried:
				# initialise list and output
				self.numList = lists
				self.layer_of_text()
				# Waits one milisecond to let user see what is happening
				self.canvas.after(1, None)
				self.master.update_idletasks()

		self.numList = self.solved_list
		# Show solved sudoku board
		self.layer_of_text()
		# Force show full number before informing the user the statistics.
		self.master.update_idletasks()
		# Tells user the statistics of the solve
		messagebox.showinfo("Board solved", f"Your board has been solved.\n\n{round(time.time()-starttime, 5)} seconds used\n\nA total of {tries} attempts are tried")
		self.canvas.focus_force()
		self.layer_of_text()

	def show_focus(self, x ,y):
		if self.solving:    
			# Current rectangle should be deleted
			self.canvas.delete('current_rectangle')
			return
		# Connect to x and y dimensions
		xvalues =self.dimensions.x.get(x)
		yvalues= self.dimensions.y.get(y)

		# Create rectangle object
		self.canvas.create_rectangle(xvalues[0],yvalues[0],xvalues[1],yvalues[1],outline='red',tags='current_rectangle',width=5)

		# Sets selected objects
		self.selected = (x, y)
		return  

def main():
	# Creates board object
	sudokuB = suboard()
	# Reaches this line if board object quits
	if not sudokuB.generated:
		# Did not quit by generate function
		print('Thank you!')
		# Quit
		return

	# Quits by generate -- links to generate function
	print(sudokuB)

	# Creates a play board for sudoku
	board = play_board(sudokuB.numList)
	return
