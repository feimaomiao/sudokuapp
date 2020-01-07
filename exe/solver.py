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

class sudoku_board():
	def __init__(self, board):
		self.board = board

	def __repr__(self):
		return self.board

	def find_empty(self):
		for i in range(len(self.board)):
			for j in range(len(self.board[0])):
				if self.board[i][j]==0:
					return(i,j)
		return None

	def valid(self,number, position):
		for i in range(len(board[0])):
			if self.board[position[0]][i] == number and position[1]!= i:
				return False
		for i in range(len(board[0])):
			if board[i][position[1]] == number and position[0]!= i:
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
				board[row][col] = 0
		return False

board=[
	[7, 8, 0, 4, 0, 0, 1, 2, 0],
	[6, 0, 0, 0, 7, 5, 0, 0, 9],
	[0, 0, 0, 6, 0, 1, 0, 7, 8],
	[0, 0, 7, 0, 4, 0, 2, 6, 0],
	[0, 0, 1, 0, 5, 0, 9, 3, 0],
	[9, 0, 4, 0, 6, 0, 0, 0, 5],
	[0, 7, 0, 3, 0, 0, 0, 1, 2],
	[1, 2, 0, 0, 0, 7, 4, 0, 0],
	[0, 4, 9, 2, 0, 6, 0, 0, 7]
	]

sud = sudoku_board(board)
sud.solve()
print_board(sud.board)
















