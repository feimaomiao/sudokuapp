import copy, random, os
from functools import wraps
import errno
import signal

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
		self.board = copy.deepcopy(board)
		self.tried = []
		# Check if user inputted a valid board
		self.finished = self.check_valid()
		self.solve() if self.finished else None

	def find_empty(self):
		for i in range(9):
			for j in range(9):
				if self.board[i][j]==0:	return(i,j)
		return None

	def valid(self,number, position):
		# Checks if number is valid in certain position
		for i in range(9):
			# horizontal
			if self.board[position[0]][i] == number and position[1]!= i:	return False
			# vertical
			if self.board[i][position[1]] == number and position[0]!= i:	return False
		# groups	
		xpos, ypos = (position[1] //3*3, position[0]//3*3)
		for i in range(ypos, ypos+3):
			for j in range(xpos,xpos+3):
				if self.board[i][j] == number and (i,j)!= position:			return False
		return True


	def solve(self):
		# check if there are empty grids
		find= self.find_empty()
		if not find: 	return True
		else: 			row,col = find

		for i in range(1,10):
			self.sum += 1
			# append to try. Try is used in fancy 
			if self.valid(i,(row,col)):
				if random.choice([1,2])==1:
					self.tried.append(copy.deepcopy(self.board)) 
				# check if number is valid
				self.board[row][col]= i
				# recursion -- check until all empty files are checked
				if self.solve():
					self.finished = True
					return True
				# location is not valid and location returns zero
				self.board[row][col] = 0


		return False

	def check_valid(self):
		# check if whole board is valid
		for i in range(9):

			# Horizontal lines
			for j in self.board[i]:
				if self.board[i].count(j) > 1 and j != 0:
					self.finished = False
					return False

			# vertical lines		
			vert = [self.board[j][i] for j in range(9)]
			for j in vert:
				if vert.count(j) > 1 and j != 0:
					self.finished = False
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
					self.finished = False
					return False
		return True


def return_generated_board(difficulty='easy',board=[]):
	@timeout(5)
	def generate_unsolved_board(times=20):
		# function that generates an unsolved board to return as a game
		board_copy = [[0 for i in range(9)] for i in range(9)]
		possible = [i for i in range(1,10)]
		tester= None
		for i in range(times):
			del(tester)
			print('i',i)
			# x amd u value (coordinates) of the selected grid
			x = random.randrange(9)
			y = random.randrange(9)
			# check if this grid has already been used
			if board_copy[x][y] == 0:
				# randomly assigns number to the location
				board_copy[x][y] = random.choice(possible)
				tester = sudoku_board(board_copy)
				# Check if it is a posible number
				if not tester.check_valid():	
					print('Its the culprit here')
					board_copy[x][y] = 0
				else: 							
					continue
				# recycles to save space and speeds up the progress
			else:
				print('Got lucky')
				tester= None
				# will continues the loop
				continue

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
			try:
				generated_board = generate_unsolved_board(10)
			# If the computer is so slow
			except TimeoutError:
				generated_board = generate_unsolved_board(5)
	rboard_obj = sudoku_board(generated_board)
	# Solves the board
	rboard_obj.solve()
	# Creates a copy of the board
	rboard = copy.deepcopy(rboard_obj.board)
	# assigns the board and empties grids
	if difficulty == 'easy':		amount_of_empty_spots = random.randrange(25,45)
	elif difficulty == 'medium':	amount_of_empty_spots = random.randrange(35,50)
	elif difficulty == 'hard':		amount_of_empty_spots = random.randrange(40,60)
	elif difficulty == 'insane':	amount_of_empty_spots = random.randrange(60, 75)
	else:							amount_of_empty_spots = random.randrange(15,75)
	for i in range(amount_of_empty_spots):
		rm_x = random.randrange(9)
		rm_y = random.randrange(9)
		rboard[rm_x][rm_y]=0
	return (rboard,rboard_obj.board)




















