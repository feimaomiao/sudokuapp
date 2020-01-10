import copy
import random
def print_board(board):
	for i in range(len(board)):
		if i%3 ==0 and i != 0:
			print('- '*12)

		for j in range(len(board[0])):
			if j%3 ==0 and j !=0:
				print(' | ', end='')

			if j==8:
				print(board[i][j])

			else:

				print(str(board[i][j])+' ', end='')
		

class sudoku_board(object):
	def __init__(self, board):
		self.board = copy.deepcopy(board)
		self.original_board = copy.deepcopy(board)
		self.tried = []
		self.finished = self.check_valid()
		self.solve() if self.finished else None

	def __repr__(self):
		return self.board

	def find_empty(self):
		for i in range(9):
			for j in range(9):
				if self.board[i][j]==0:
					return(i,j)
		return None

	def valid(self,number, position):
		for i in range(len(self.board[0])):
			if self.board[position[0]][i] == number and position[1]!= i:
				return False
		for i in range(len(self.board[0])):
			if self.board[i][position[1]] == number and position[0]!= i:
				return False
		xpos = position[1] //3
		ypos = position[0] //3
		for i in range(ypos*3, ypos*3+3):
			for j in range(xpos*3,xpos*3+3):
				if self.board[i][j] == number and (i,j)!= position:
					return False
		return True


	def solve(self):
		find= self.find_empty()
		if not find:
			return True
		else:
			row,col = find

		for i in range(1,10):
			if self.valid(i,(row,col)):
				self.board[row][col]= i
				if self.solve():
					return True
				self.board[row][col] = 0
			self.tried.append(copy.deepcopy(self.board))
		return False

	def check_valid(self):
		for i in range(9):
			for j in self.board[i]:
				if self.board[i].count(j)> 1 and j != 0:
					print(self.board[i])
					self.finished = False
					return False
			vert = [self.board[i][j] for j in range(9)]
			for j in vert:
				if vert.count(j) > 1 and j != 0:
					print(vert)
					self.finished = False
					return False
			group = []
			x0 = i%3*3
			x1 = i%3*3+3
			y0 = i//3*3
			y1 = i//3*3 +3
			for ys in range(y0,y1):
				for xs in range(x0, x1):
					group.append(self.board[ys][xs])
			for nums in group:
				if group.count(nums) >1 and nums != 0:
					print(group)
					self.finished = False
					return False
		return True



	def return_board(self):
		return self.board

board=[[7, 0, 3, 0, 0, 4, 0, 9, 0], [0, 0, 0, 5, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 7, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 4], [0, 0, 0, 0, 0, 0, 0, 0, 9], [3, 0, 0, 7, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 6, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 0, 0, 0, 0, 6, 0, 1, 0]]

# sud = sudoku_board(board)
# sud.solve()
# sud.check_valid()
# # print(sud.tries)
# print(sud.finished)
# print_board(sud.board)
sud = sudoku_board(board)
print_board(sud.board)

def generate_board():
	gen_board = [[0 for i in range(9)] for i in range(9)]
	possible = [i for i in range(1,10)]
	for i in range(20):
		print('i',i)
		board_copy = copy.deepcopy(gen_board)
		x = random.randrange(9)
		y = random.randrange(9)
		print(x, y)
		if board_copy[x][y] == 0:
			board_copy[x][y] = random.choice(possible)
			tester = sudoku_board(board_copy)
			if not tester.finished:
				i -= 1
				pass
			else:
				gen_board = copy.deepcopy(board_copy)
			del(tester)
		else:
			i -= 1
	return gen_board

















