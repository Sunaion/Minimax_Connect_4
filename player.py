import board
import random
import math

# The aim of this coursework is to implement the minimax algorithm to determine the next move for a game of Connect.
# The goal in Connect is for a player to create a line of the specified number of pieces, either horizontally, vertically or diagonally.
# It is a 2-player game with each player having their own type of piece, "X" and "O" in this instantiation.
# You will implement the strategy for the first player, who plays "X". The opponent, who always goes second, plays "O".
# The number of rows and columns in the board varies, as does the number of pieces required in a line to win.
# Each turn, a player must select a column in which to place a piece. The piece then falls to the lowest unfilled location.
# Rows and columns are indexed from 0. Thus, if at the start of the game you choose column 2, your piece will fall to row 0 of column 2. 
# If the opponent also selects column 2 their piece will end up in row 1 of column 2, and so on until column 2 is full (as determined
# by the number of rows). 
# Note that board locations are indexed in the data structure as [row][column]. However, you should primarily be using checkFull(), 
# checkSpace() etc. in board.py rather than interacting directly with the board.gameBoard structure.
# It is recommended that look at the comments in board.py to get a feel for how it is implemented. 
#
# Your task is to complete the two methods, 'getMove()' and 'getMoveAlphaBeta()'.
#
# getMove() should implement the minimax algorithm, with no pruning. It should return a number, between 0 and (maxColumns - 1), to
# select which column your next piece should be placed in. Remember that columns are zero indexed, and so if there are 4 columns in
# you must return 0, 1, 2 or 3. 
#
# getMoveAlphaBeta() should implement minimax with alpha-beta pruning. As before, it should return the column that your next
# piece should be placed in.
#
# The only imports permitted are those already imported. You may not use any additional resources. Doing so is likely to result in a 
# mark of zero. Also note that this coursework is NOT an exercise in Python proficiency, which is to say you are not expected to use the
# most "Pythonic" way of doing things. Your implementation should be readable and commented appropriately. Similarly, the code you are 
# given is intended to be readable rather than particularly efficient or "Pythonic".
#
# IMPORTANT: You MUST TRACK how many nodes you expand in your minimax and minimax with alpha-beta implementations.
# IMPORTANT: In your minimax with alpha-beta implementation, when pruning you MUST TRACK the number of times you prune.
class Player:
	
	def __init__(self, name):
		self.name = name
		self.numExpanded = 0 # Use this to track the number of nodes you expand
		self.numPruned = 0 # Use this to track the number of times you prune 

	# heuristic score function used to evaluate an entire gameboard for a specific player
	def heuristic_score_function(self, gameboard, player):
		# check win conditions first for X and O
		win = gameboard.checkWin()
		if win and player == "X":
			return 99999
		if win and player == "O":
			return -99999

		# we keep track of a total score calculated from evaluating each position in the board
		total_score = 0
		rows = gameboard.numRows
		columns = gameboard.numColumns
		board = gameboard.gameBoard
		# iterating over every possible position in the board (that isnt empty)
		for row in range(rows):
			for column in range(columns):
				if board[row][column].value == "X":
					# since max wants to maximise its value, we do += as it returns a positive score
					total_score += self.evaluate_cur_position(gameboard, "X", row, column)
				if board[row][column].value == "O":
					# since min wants to minimise  its value, we use -= as evaluate_cur_position returns a positive value, but we negate this with -
					total_score -= self.evaluate_cur_position(gameboard, "O", row, column)

		return total_score

	
	# evaluation of a position in the board
	def evaluate_cur_position(self, gameboard, player, row, col):
		# total score that will be returned for a specific position
		score = 0
		board = gameboard.gameBoard
		total_rows = gameboard.numRows
		total_cols = gameboard.numColumns
		win_number = gameboard.winNum
		other_player = "X"

		if player == "X":
			other_player = "O"

		# the premise of this function is that it detects if the piece has horizontal/vertical and diagonal potential to be in a position (i.e. for 4 in a row, it is surrounded by empty spaces or pieces of the same colour)
		# if such,  the function adds a score of 100  for each possible plane - 400 score achievable for a single postion in total
		# horizontal - using sliding window
		left_horizontal = 0 
		for l in range(col,-1,-1):
			if board[row][l].value != other_player:
				left_horizontal += 1
			else:
				break
		
		right_horizontal = 0
		for r in range(col+1,total_cols):
			if board[row][r].value != other_player:
				right_horizontal += 1
			else:
				break
		
		# # we only have to do this because we know the 4 in a row selected contains the row,col piece in this selected row - and only once, so score incremented by 100. 
		# # If there are multiple pieces in this row, they will be counted in a separate instance of evaluate_cur_position()
		if left_horizontal + right_horizontal >= win_number:
			score += 100

		# vertical

		down_vertical = 0 
		for d in range(row,-1,-1):
			if board[d][col].value != other_player:
				down_vertical += 1
			else:
				break
		
		up_vertical = 0
		for u in range(row+1,total_rows):
			if board[u][col].value != other_player:
				up_vertical += 1
			else:
				break
		
		if down_vertical + up_vertical >= win_number:
			score += 100


		# positive gradient diagonal

		left_positive = 0
		left_col = col
		for l in range(row,-1,-1):
			if left_col < 0:
				break
			if board[l][left_col].value != other_player:
				left_positive += 1
			else:
				break
			left_col -= 1
		
		right_positive = 0
		right_col = col+1
		for r in range(row+1,total_rows):
			if right_col >= total_cols:
				break
			if board[r][right_col].value != other_player:
				right_positive += 1
			else:
				break
			right_col += 1
		
		if left_positive + right_positive >= win_number:
			score += 100

		# negative gradient diagonal

		left_negative = 0
		left_col = col
		for l in range(row,total_rows):
			if left_col < 0:
				break
			if board[l][left_col].value != other_player:
				left_negative += 1
			else:
				break
			left_col -= 1
		
		right_negative = 0
		right_col = col+1
		for r in range(row-1,-1,-1):
			if right_col >= total_cols:
				break
			if board[r][right_col].value != other_player:
				right_negative += 1
			else:
				break
			right_col += 1
		
		if left_negative + right_negative >= win_number:
			score += 100

		return score

	# retrieves empty columns
	def find_empty_columns(self, gameboard):
		cols = []
		colfills = gameboard.colFills
		for i in range(gameboard.numColumns):
			if colfills[i] < gameboard.numRows:
				cols.append(i)
		return cols

	
	def evaluate_column(self, gameboard, player, col):
		# we must evaluate each child of every parent node in the search tree to be able to order the children for effective pruning
		board_copy = gameboard.copy()
		board_copy.addPiece(col,player)
		return (col,self.heuristic_score_function(board_copy,player))

	
	# for ordered_positions - sorting
	def get_position_score(self, column):
		return column[1]

	# minimax algorithm - recursive
	# uses depth to signify depth of the search tree
	# max boolean variable (changed for alpha-beta minimax)
	# this function returns two values (column heuristic value, column) as a tuple - we must know this because otherwise we cannot keep track of each column and what heuristic value is assigned to it. We have separate variables for each parent to store the highest/lowest column so far and its heuristic value. At the end the algorithm returns the column to be chosen from
	def minimax(self, gameboard, depth, max):
		# increment the number of nodes expanded 
		self.numExpanded += 1

		# we check for wins or if the board is full, that way we can return whether the board is a win, a loss or a draw for a player. 
		win = gameboard.checkWin()
		boardfull = gameboard.checkFull()

		# we use very high values/low values since we have heuristic function at depth == 0 to return heuristic values for a given board. If max wins at a node they want to win and choose that branch over any other branch. So a really high value is returned
		# same for min (but wants to choose a very low value)
		if boardfull or win:
			if win and not max:
				return (999999,None)
			elif win and max:
				return (-99999,None)
			else:
				return (0,None)
		# does not expand any more so heuristic value of board is calculated
		if depth == 0:
			player = gameboard.lastPlay[2]
			return (self.heuristic_score_function(gameboard, player),None)

		# fetch empty columns
		columns = self.find_empty_columns(gameboard)

		# max turn (to start)
		if max:
			# start with a very negative eval, so it will be replaced by the heuristic value of the first child returned and so on until we find our most promising child for the parent (max) to choose
			eval = -99999999
			eval_col = columns[0]
			# we evaluate every possible branch in this parent
			for column in columns:
				# use board copy to not interfere with the current board/ memory issues
				board_copy = gameboard.copy()
				# we simulate adding an "X" to simulate the next move in the game, and recursively call minimax but now we decrease the depth and call for mins go instead (to play against max)
				board_copy.addPiece(column,"X")
				child_eval = self.minimax(board_copy,depth-1,False)[0]
				# if the heuristic value of the child node is the highest seen, it is stored in eval and the column in eval_col
				if child_eval > eval:
					eval = child_eval
					eval_col = column
			# after all are evaluated, the values are returned
			return (eval,eval_col)
		else:
			# same for min but we try to get the lowest heurstic value column
			eval = 99999999
			eval_col = columns[0]
			for column in columns:
				board_copy = gameboard.copy()
				board_copy.addPiece(column,"O")
				child_eval = self.minimax(board_copy,depth-1,True)[0]
				if child_eval < eval:
					eval = child_eval
					eval_col = column
			# same process as max
			return (eval,eval_col)

			
	# Minimax Alpha/Beta pruning - pruning positions that dont affect the outcome

	# alpha, beta parameters, max -> max_turn as max is a keyword used in this function, not in minimax()
	def minimaxAlphaBeta(self, gameboard, alpha, beta, depth, max_turn):

		self.numExpanded += 1	
		
		win = gameboard.checkWin()
		boardfull = gameboard.checkFull()
		
		# Must check the board after adding a piece for wins/losses, or a draw
		if boardfull or win:
			if win and not max_turn:
				return (99999,None)
			elif win and max_turn:
				return (-99999,None)
			else:
				return (0,None)

		# MOVE ORDERING IMPLEMENTATION
		# we evaluate every child node in the search tree and add to a list
		# this is sorted in descending order (for max) or ascending (for min), which allows the algorithm to choose the most promising child to explore first (DFS)
		# Used to prune nodes early on, as a high scoring (or low) can allow the algorithm to prune off the rest of the children
		columns = self.find_empty_columns(gameboard)
		ordered_positions = []
		player = ""
		if max_turn:
			player = "X"
		else:
			player = "O"
		
		# added to ordering_positions - an array containing tuples (column, heuristic value of column)
		for col in columns:
			ordered_positions.append(self.evaluate_column(gameboard, player, col))



		if max_turn:
			# sort in descending order, get the highest heuristic value
			ordered_positions.sort(key=self.get_position_score, reverse=True)
			eval = -99999999
			# set to the most promising column (with highest heuristic value)
			eval_col = ordered_positions[0][0]
			for column in range(len(ordered_positions)):
				chosen_column = ordered_positions[column][0]

				# memoization - we have just calculated these values
				# at depth == 1, no more expansions should happen after calling minimaxAlphaBeta() on that node, thus we can just use the calculated heuristic values from ordered_positions
				# also calculates wins/losses/draws
				if depth == 1:
					child_eval = ordered_positions[column][1]
				else:
					# otherwise do as normal - recursively call function
					board_copy = gameboard.copy()
					board_copy.addPiece(chosen_column,"X")
					child_eval = self.minimaxAlphaBeta(board_copy, alpha, beta, depth-1,False)[0]
				# replacing column if higher heuristic value column is found/ win is found
				if child_eval > eval:
					eval = child_eval
					eval_col = chosen_column
				# max is trying to maximise the alpha value
				alpha = max(alpha, eval)
				# min has found a beta value that is less than alpha, so expanding past this point would be useless, since min will just choose the beta value over the current alpha value
				if beta <= alpha:
					self.numPruned += 1
					break
			return (eval,eval_col)
		else:
			# same for min, however we sort in ascending order (to get the most negative heuristic value)
			ordered_positions.sort(key=self.get_position_score)
			eval = 99999999
			eval_col = ordered_positions[0][0]
			for column in range(len(ordered_positions)):
				chosen_column = ordered_positions[column][0]

				# memoization - we have just calculated these values
				if depth == 1:
					child_eval = ordered_positions[column][1]
				else:
					# same thing here as with max
					board_copy = gameboard.copy()
					board_copy.addPiece(chosen_column,"O")
					child_eval = self.minimaxAlphaBeta(board_copy,alpha, beta, depth-1,True)[0]
				if child_eval < eval:
					eval = child_eval
					eval_col = chosen_column
				# min is trying to minimise beta, because its trying to go for the smallest value
				beta = min(beta, eval)
				# again no point to expand if we want max to win, since beta will choose the smaller branch - no point expanding a branch if the parent can never be chosen by min
				if beta <= alpha:
					self.numPruned += 1
					break
			return (eval,eval_col)


	def getMove(self, gameBoard):
		# the most optimal position for a first move is the middle column of the board
		if gameBoard.lastPlay[2] == "":
			return math.floor(gameBoard.numColumns/2)
		# calling minimax with a maximum depth of 5 for the search tree generated by minimax call - returns a column to place a piece
		return self.minimax(gameBoard, 5, True)[1]

	def getMoveAlphaBeta(self, gameBoard):
		# optimal position is middle
		if gameBoard.lastPlay[2] == "":
			return math.floor(gameBoard.numColumns/2)
		# calling minimax alpha/beta with a maximum depth of 6 - returns column to place a piece
		return self.minimaxAlphaBeta(gameBoard,-9999999,9999999,6,True)[1]