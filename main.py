import sys
import pygame
import numpy as np
import math
import time
import random
from pygame.locals import *

R = 6
C = 7
comp = 0
computer_lower = 0
computer_upper = 0
COMPUTER  = 1
AI = 1
AI_AGENT = 2
FREE = 0
WINDOW_LENGTH = 4
white = (200,200,200)
black = (150,150,150)
red = (150,0,0)
blue = (0,0,150)

def generate_board():
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
def Drop(game_board, row, column, cell):
    game_board[row][column] = cell

def IsValidCell(game_board, column):
    if game_board[R-1][column] == 0 :
        return True
    else:
        return False

def next_row(game_board, column):
    for i in range(R):
        if game_board[i][column] == 0:
            return i



def HaveWon(game_board, cell):

# Check vertical
    for j in range(C):
        for i in range(R - 3):
            if (game_board[i][j] == cell and
                game_board[i + 1][j] == cell and
                game_board[i + 2][j] == cell and
                game_board[i + 3][j] == cell):
                return True

# Check horizontal
    for j in range(C - 3):
        for i in range(R):
            if (game_board[i][j] == cell and
                game_board[i][j + 1] == cell and
                game_board[i][j + 2] == cell and
                game_board[i][j + 3] == cell):
                return True

        # Check negatively diagonals
    for j in range(C - 3):
        for i in range(3, R):
            if (game_board[i][j] == cell and
                game_board[i - 1][j + 1] == cell and
                game_board[i - 2][j + 2] == cell and
                game_board[i - 3][j + 3] == cell):
                return True

        # Check positively diagonals
    for j in range(C-3):
        for i in range(R-3):
            if (game_board[i][j] == cell and
                game_board[i+1][j+1] == cell and
                game_board[i+2][j+2] == cell and
                game_board[i+3][j+3] == cell):
                return True



def CalculateScore(window, cell):
    sc= 0
    o_cell = COMPUTER
    if cell == COMPUTER:
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

def CellPoints(game_board, token):
    points = 0
    ## Score center column
    game_board_center = [int(i) for i in list(game_board[:, C//2])]
    board_center_count = game_board_center.count(token)
    points += board_center_count * 3

    ## Vertical points
    for i in range(C):
        column_board = [int(k) for k in list(game_board[:,i])]
        for j in range(R-3):
            window = column_board[j:j+WINDOW_LENGTH]
            points += CalculateScore(window, token)

    ## Horizontal points
    for i in range(R):
        row_board = [int(k) for k in list(game_board[i, :])]
        for j in range(C - 3):
            window = row_board[j:j + WINDOW_LENGTH]
            points += CalculateScore(window, token)

    ##negative diagonal points
    for i in range(R-3):
        for j in range(C-3):
            window = [game_board[i+3-k][j+k] for k in range(WINDOW_LENGTH)]
            points += CalculateScore(window, token)

    ##posiive diagonal points
    for i in range(R-3):
        for j in range(C-3):
            window = [game_board[i+k][j+k] for k in range(WINDOW_LENGTH)]
            points += CalculateScore(window, token)

    return points

def IsLastMove(game_board):
    if HaveWon(game_board, COMPUTER ) or HaveWon(board, AI_AGENT) or len(GetValidCells(game_board)) == 0:
        return True
    else:
        return False

def minimax(game_board, depth, maximizedP):
        valid_cells = GetValidCells(game_board)
        lastmove = IsLastMove(game_board)
        if depth == 0 or lastmove:
            if lastmove:
                if HaveWon(game_board, AI_AGENT):
                    return (None, 100000000000000)
                elif HaveWon(game_board, COMPUTER):
                    return (None, -10000000000000)
                else: # Game is over, no more valid moves
                    return (None, 0)
            else: # Depth is zero
                return (None, CellPoints(game_board, AI_AGENT))
        if maximizedP:
            val = -math.inf
            column = random.choice(valid_cells)
            for coll in valid_cells:
                ROW = next_row(game_board, coll)
                game_board_copy = board.copy()
                Drop(game_board_copy, ROW, coll, AI_AGENT)
                new_score = minimax(game_board_copy, depth-1, False)[1]
                if new_score > val:
                    val = new_score
                    column = coll
            return column, val

        else: # Minimizing player
            val = math.inf
            column = random.choice(valid_cells)
            for coll in valid_cells:
                ROW = next_row(game_board, coll)
                game_board_copy = board.copy()
                Drop(game_board_copy, ROW, coll, COMPUTER)
                new_score = minimax(game_board_copy, depth-1, True)[1]
                if new_score > val:
                    val = new_score
                    column = coll
            return column, val






def alphabeta(game_board, depth, alpha, beta, maximizedP):
        valid_cells = GetValidCells(game_board)
        lastmove = IsLastMove(game_board)
        if depth == 0 or lastmove:
            if lastmove:
                if HaveWon(game_board, AI_AGENT):
                    return (None, 100000000000000)
                elif HaveWon(game_board, COMPUTER):
                    return (None, -10000000000000)
                else: # Game is over, no more valid moves
                    return (None, 0)
            else: # Depth is zero
                return (None, CellPoints(game_board, AI_AGENT))
        if maximizedP:
            val = -math.inf
            column = random.choice(valid_cells)
            for coll in valid_cells:
                ROW = next_row(game_board, coll)
                game_board_copy = board.copy()
                Drop(game_board_copy, ROW, coll, AI_AGENT)
                new_score = alphabeta(game_board_copy, depth-1, alpha, beta, False)[1]
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
                ROW = next_row(game_board, coll)
                game_board_copy = board.copy()
                Drop(game_board_copy, ROW, coll, COMPUTER)
                new_score = alphabeta(game_board_copy, depth-1, alpha, beta, True)[1]
                if new_score < val:
                    val = new_score
                    column = coll
                beta = min(beta, val)
                if alpha >= beta:
                    break
            return column, val





def GetValidCells(game_board):
	valid_cells = []
	for col in range(C):
		if IsValidCell(game_board, col):
			valid_cells.append(col)
	return valid_cells




def MakeBoard(board):
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


board = generate_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 100

width = C * SQUARESIZE
height = (R + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
MakeBoard(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)


turn = random.randint(comp, AI)


def play_game():
    board = generate_board()
    game_over = False
    turn = 0
    flag = 0
    pygame.init()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if turn == 0:
            # Agent's Move
            # if flag == 1:
            #     col, minimax_score = minimax(board, 5, True)
            # elif flag == 2:
            col, minimax_score = alphabeta(board, 1,-math.inf,math.inf, True)
            computer_lower = col-1
            computer_upper = col+1
            if IsValidCell(board, col):
                row = next_row(board, col)
                Drop(board, row, col, 1)
                if HaveWon(board, 1):
                    label = myfont.render("Agent wins!!", 1, red)
                    screen.blit(label, (40, 10))
                    game_over = True

                turn = 1

        else:
            # Computer's Move
            if computer_lower < 0:
                computer_lower = 0
            if computer_upper > 6:
                computer_upper = 6

            col = random.randint(computer_lower,computer_upper)
            # col, minimax_score = alphabeta(board, 1,-math.inf,math.inf, True)
            if IsValidCell(board, col):
                row = next_row(board, col)
                Drop(board, row, col, 2)

                if HaveWon(board, 2):
                    label = myfont.render("Computer wins!!", 1, blue)
                    screen.blit(label, (40, 10))
                    game_over = True

                turn =0

        print_board(board)
        MakeBoard(board)
        time.sleep(1)

    pygame.time.wait(1000)





# Start the Game
play_game()