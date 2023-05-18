import sys
import pygame
import numpy as np
import math
import time
import random
white = (200,200,200)
black = (150,150,150)
red = (150,0,0)
blue = (0,0,150)

R = 6
C = 7

comp = 0
AI = 1

FREE = 0
COMPUTER  = 1
AI_AGENT = 2

WINDOW_LENGTH = 4
def create_board():
    row = []
    for i in range(R):
        col = []
        for j in range(C):
            col.append(0)
        row.append(col)
        board = np.array(row)
    return board


def print_board(game_board):
    print(np.flip(game_board, 0))

#
def drop_piece(game_board, row, column, cell):
    game_board[row][column] = cell

def is_valid_location(game_board, column):
    return game_board[R-1][column] == 0

def get_next_open_row(game_board, column):
    for i in range(R):
        if game_board[i][column] == 0:
            return i



def winning_move(game_board, cell):

# Check vertical
    for j in range(C):
        for i in range(R - 3):
            if game_board[i][j] == cell and game_board[i + 1][j] == cell and game_board[i + 2][j] == cell and game_board[i + 3][j] == cell:
                return True

# Check horizontal
    for j in range(C - 3):
        for i in range(R):
            if game_board[i][j] == cell and game_board[i][j + 1] == cell and game_board[i][
                j + 2] == cell and game_board[i][j + 3] == cell:
                return True

        # Check negatively diagonals
    for j in range(C - 3):
        for i in range(3, R):
            if game_board[i][j] == cell and game_board[i - 1][j + 1] == cell and game_board[i - 2][
                j + 2] == cell and game_board[i - 3][j + 3] == cell:
                return True

        # Check positively diagonals
    for j in range(C-3):
        for i in range(R-3):
            if game_board[i][j] == cell and game_board[i+1][j+1] == cell and game_board[i+2][j+2] == cell and game_board[i+3][j+3] == cell:
                return True



def evaluate_window(window, cell):
    sc= 0
    o_cell = COMPUTER
    if o_cell == COMPUTER:
        o_cell = AI_AGENT

    if window.count(cell) == 4:
        sc+=100
    elif window.count(cell) == 3 and window.count(FREE) == 1:
        sc+=20
    elif window.count(cell) == 2 and window.count(FREE) == 2:
        sc+=10

    if window.count(o_cell) == 3 and window.count(FREE) == 1:
        sc-=1

    return sc

def score_position(game_board, token):
		points = 0

		## Score center column
		game_board_center = [int(i) for i in list(game_board[:, C//2])]
		board_center_count = game_board_center .count(token)
		points += board_center_count * 3

		## Vertical points
		for i in range(C):
			column_board = [int(k) for k in list(game_board[:,i])]
			for j in range(R-3):
				window = column_board[j:j+WINDOW_LENGTH]
				points += evaluate_window(window, token)

		## Horizontal points
		for i in range(R):
			row_board = [int(k) for k in list(game_board[i, :])]
			for j in range(C - 3):
				window = row_board[j:j + WINDOW_LENGTH]
				points += evaluate_window(window, token)

		##negative diagonal points
		for i in range(R-3):
			for j in range(C-3):
				window = [game_board[i+3-k][j+k] for k in range(WINDOW_LENGTH)]
				points += evaluate_window(window, token)

		##posiive diagonal points
		for i in range(R-3):
			for j in range(C-3):
				window = [game_board[i+k][j+k] for k in range(WINDOW_LENGTH)]
				points += evaluate_window(window, token)

		return points

def is_terminal_node(game_board):
	return winning_move(game_board, COMPUTER ) or winning_move(board, AI_AGENT) or len(get_valid_locations(game_board)) == 0


def minimax(game_board, depth, alpha, beta, maximizedP):
	valid_cells = get_valid_locations(game_board)
	terminal = is_terminal_node(game_board)
	if depth == 0 or terminal:
		if terminal:
			if winning_move(game_board, AI_AGENT):
				return (None, 100000000000000)
			elif winning_move(game_board, COMPUTER):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(game_board, AI_AGENT))
	if maximizedP:
		val = -math.inf
		column = random.choice(valid_cells)
		for coll in valid_cells:
			ROW = get_next_open_row(game_board, coll)
			game_board_copy = board.copy()
			drop_piece(game_board_copy, ROW, coll, AI_AGENT)
			new_score = minimax(game_board_copy, depth-1, alpha, beta, False)[1]
			if new_score > val:
				val = new_score
				column = coll
			alpha = max(alpha, val)
			if alpha >= beta:
				break
		return column, val

	else: # Minimizing player
		val = math.inf
		column = random.choice(valid_cells)
		for coll in valid_cells:
			ROW = get_next_open_row(game_board, coll)
			game_board_copy = board.copy()
			drop_piece(game_board_copy, ROW, coll, COMPUTER)
			new_score = minimax(game_board_copy, depth-1, alpha, beta, True)[1]
			if new_score < val:
				val = new_score
				column = coll
			beta = min(beta, val)
			if alpha >= beta:
				break
		return column, val

def get_valid_locations(game_board):
	valid_cells = []
	for col in range(C):
		if is_valid_location(game_board, col):
			valid_cells.append(col)
	return valid_cells

def get_valid_locations(game_board):
        valid_cells = []
        for col in range(C):
            if is_valid_location(game_board, col):
                valid_cells.append(col)
        return valid_cells




def draw_board(board):
    for c in range(C):
        for r in range(R):
            pygame.draw.rect(screen, black, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, white, (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(C):
        for r in range(R):
            if board[r][c] == COMPUTER:
                pygame.draw.circle(screen, red, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_AGENT:
                pygame.draw.circle(screen, blue, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


board = create_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 100

width = C * SQUARESIZE
height = (R + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)


turn = random.randint(comp, AI)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()


		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, white, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == comp:
				pygame.draw.circle(screen, red, (posx, int(SQUARESIZE/2)), RADIUS)

		pygame.display.update()

		# Ask for Player 1 Input
		if turn == comp:
			# posx = event.pos[0]
			# col = int(math.floor(posx/SQUARESIZE))
			col = random.randint(0, C-1)
			if is_valid_location(board, col):
				row = get_next_open_row(board, col)
				drop_piece(board, row, col, COMPUTER)

				if winning_move(board, COMPUTER):
					label = myfont.render("Player 1 wins!!", 1, red)
					screen.blit(label, (40,10))
					game_over = True

				turn += 1
				turn = turn % 2

				print_board(board)
				draw_board(board)


	# # Ask for Player 2 Input
	if turn == AI and not game_over:

		#col = random.randint(0, COLUMN_COUNT-1)
		#col = pick_best_move(board, AI_PIECE)
		col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

		if is_valid_location(board, col):
			#pygame.time.wait(500)
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, AI_AGENT)

			if winning_move(board, AI_AGENT):
				label = myfont.render("Player 2 wins!!", 1, blue)
				screen.blit(label, (40,10))
				game_over = True

			print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2

	if game_over:
		pygame.time.wait(3000)