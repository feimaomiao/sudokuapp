import copy, random, os
from functools import wraps
import errno
import signal
def initialise(root, name='sudoku-solver'):
	# Set window title
	root.title(name)
	# Set the window size and not allow user to change the size
	root.resizable(False, False)
	root.minsize(453,435)
	root.update_idletasks()
	width = root.winfo_width()
	height = root.winfo_height()
	x = (root.winfo_screenwidth() // 2) - (width // 2)
	y = (root.winfo_screenheight() // 2) - (height // 2)
	# Set root size and put to center
	root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
	return

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

class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator

class sudoku_board(object):
	def __init__(self, board):
		# Make copy instead of direct modify
		self.sum = 0
		self.board = board
		self.tried = []
		# Check if user inputted a valid board
		self.finished = self.check_valid()
		# self.solve() if self.finished else None

	def find_empty(self):
		for i in range(9):
			for j in range(9):
				if self.board[i][j]==0:	
					return(i,j)
		return 

	def valid(self,number, position):
		# Checks if number is valid in certain position
		for i in range(9):
			# self.sum += 1
			# horizontal
			if self.board[position[0]][i] == number and position[1]!= i:	
				return False
			# vertical
			if self.board[i][position[1]] == number and position[0]!= i:	
				return False
		# groups	
		xpos, ypos = (position[1] //3*3, position[0]//3*3)
		for i in range(ypos, ypos+3):
			for j in range(xpos,xpos+3):
				# self.sum += 1
				if self.board[i][j] == number and (i,j)!= position:			
					return False
		return True

	def solve(self,generate=False):
		try:
			# check if there are empty grids
			find= self.find_empty()
			if not find: 	return True
			else: 			row,col = find

			for i in range(1,10):
				self.sum += 1
				if self.sum >= 50000:
					return True
				# append to try. Try is used in fancy 
				if self.valid(i,(row,col)):
					if not generate:
						self.tried.append(copy.deepcopy(self.board)) 
					# check if number is valid
					self.board[row][col]= i
					# recursion -- check until all empty files are checked
					if self.solve(generate=generate):
						return True
					# location is not valid and location returns zero
					self.board[row][col] = 0
		except (KeyboardInterrupt, TimeoutError):
			return True
		return False

	def check_valid(self):
		# check if whole board is valid
		for i in range(9):

			# Horizontal lines
			for j in self.board[i]:
				if self.board[i].count(j) > 1 and j != 0:
					return False

			# vertical lines		
			vert = [self.board[j][i] for j in range(9)]
			for j in vert:
				if vert.count(j) > 1 and j != 0:
					return False

			# Groups
			group = []
			x0, x1 = (i%3*3, i%3*3+3)
			y0, y1 = (i//3*3,i//3*3 +3)
			for ys in range(y0,y1):
				for xs in range(x0, x1):
					group.append(self.board[ys][xs])
			for nums in group:
				if group.count(nums) >1 and nums != 0:
					return False
		return True

def board_valid(selfboard):
	# check if whole board is valid
	for i in range(9):

		# Horizontal lines
		for j in selfboard[i]:
			if selfboard[i].count(j) > 1 and j != 0:
				return False

		# vertical lines		
		vert = [selfboard[j][i] for j in range(9)]
		for j in vert:
			if vert.count(j) > 1 and j != 0:
				return False

		# Groups
		group = []
		x0, x1 = (i%3*3, i%3*3+3)
		y0, y1 = (i//3*3,i//3*3 +3)
		for ys in range(y0,y1):
			for xs in range(x0, x1):
				group.append(selfboard[ys][xs])
		for nums in group:
			if group.count(nums) >1 and nums != 0:
				return False
	return True	


@timeout(5)
def return_generated_board(difficulty='insane',board=[]):
	try:
		@timeout(5)
		def generate_unsolved_board(times=25):
			# function that generates an unsolved board to return as a game
			board_copy = [[0 for i in range(9)] for i in range(9)]
			possible = [i for i in range(1,10)]
			for i in range(times):
				# x amd u value (coordinates) of the selected grid
				x = random.randrange(9)
				y = random.randrange(9)
				# check if this grid has already been used
				if board_copy[x][y] == 0:
					# randomly assigns number to the location
					board_copy[x][y] = random.randrange(1,10)
					# Check if it is a posible number
					if not board_valid(board_copy):	
						board_copy[x][y] = 0
						pass
					else: 						
						pass
					# recycles to save space and speeds up the progress
				else:
					# will continues the loop
					pass
			# returns a copy with ~15 grid entered
			return board_copy

		# initialise boards
		generated_board = board
		rboard = []
		amount_of_empty_spots = 0
		# can work as a module
		if board==[]:	
			try:
				generated_board = generate_unsolved_board()
			# Function timeouts at around 5 seconds
			except TimeoutError as e:
				generated_board = generate_unsolved_board()
			except KeyboardInterrupt:
				generated_board = generate_unsolved_board()
		rboard_obj = sudoku_board(generated_board)
		# Solves the board
		rboard_obj.solve(generate=True)
		# Creates a copy of the board
		rboard = rboard_obj.board
		# assigns the board and empties grids
		if difficulty == 'easy':		
			amount_of_empty_spots = random.randrange(25,45)
		elif difficulty == 'medium':	
			amount_of_empty_spots = random.randrange(35,50)
		elif difficulty == 'hard':		
			amount_of_empty_spots = random.randrange(40,60)
		elif difficulty == 'insane':	
			amount_of_empty_spots = random.randrange(60, 75)
		else:							
			amount_of_empty_spots = random.randrange(15,75)
		for i in range(amount_of_empty_spots):
			rboard[random.randrange(9)][random.randrange(9)]=0
		return rboard
	except TimeoutError as e:
		try:
			return return_generated_board()
		except TimeoutError as e:
			return return_generated_board(10)
	except KeyboardInterrupt:
		return return_generated_board()


def test_if_valid():
	# Tests if the generated board is avaliable
	import time
	total = []
	for i in range(100):
		start= time.time()
		board = return_generated_board()
		obj = sudoku_board(board)
		if not obj.check_valid():
			print('Wrong')
			break
		print('Yes')
		total.append(time.time()-start)
	return total













