import sys
import pygame
import numpy as np
import math
import time
import random
import tkinter as tk
from tkinter import ttk

from pygame.locals import *

# Global variables
R = 6 #no of rows
C = 7 #no of columns
comp = 0 #computer turn

# randomizing computer choice
computer_lower = 0
computer_upper = 0

COMPUTER  = 1 #computer piece
AI = 1 #AI_Agent turn
AI_AGENT = 2 # AI_AGENT piece
FREE = 0   #free place
WINDOW_LENGTH = 4

#colors of the board
white = (200,200,200)
black = (150,150,150)
red = (150,0,0)
blue = (0,0,150)

#a function to generate the board game
def generate_board():
    row = []
    for i in range(R):
        col = []
        for j in range(C):
            col.append(0)
        row.append(col)
        board = np.array(row)
    return board

# a function to print board
def print_board(game_board):
    print(np.flip(game_board, 0))

# drop a piece in a cell
def Drop(game_board, row, column, cell):
    game_board[row][column] = cell

# check whether this column is valid for placing gamepiece or not
def IsValidCell(game_board, column):
    if game_board[R-1][column] == 0 :
        return True
    else:
        return False

# a function to get next available row
def next_row(game_board, column):
    for i in range(R):
        if game_board[i][column] == 0:
            return i

# check whether this move is a winning move or not
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

#check if anyone will won
def willWon(game_board, cell):
# Check vertical
    for j in range(C):
        for i in range(R - 3):
            if (game_board[i][j] == cell and
                game_board[i + 1][j] == cell and
                game_board[i + 2][j] == cell and
                game_board[i + 3][j] == 0):
                return True , j

# Check horizontal
    for j in range(C - 3):
        for i in range(R):
            if (game_board[i][j] == cell and
                game_board[i][j + 1] == cell and
                game_board[i][j + 2] == cell and
                game_board[i][j + 3] == 0):
                return True , j + 3

        # Check negatively diagonals
    for j in range(C - 3):
        for i in range(3, R):
            if (game_board[i][j] == cell and
                game_board[i - 1][j + 1] == cell and
                game_board[i - 2][j + 2] == cell and
                game_board[i - 3][j + 3] == 0):
                return True , j + 3

        # Check positively diagonals
    for j in range(C-3):
        for i in range(R-3):
            if (game_board[i][j] == cell and
                game_board[i+1][j+1] == cell and
                game_board[i+2][j+2] == cell and
                game_board[i+3][j+3] == 0):
                return True , j+3
    return False, 0

# a function to calculate the score points of the move
def CalculateScore(window, cell):
    sc= 0
    o_cell = COMPUTER
    if cell == COMPUTER:
        o_cell = AI_AGENT

    if window.count(cell) == 4: #highest score for the winning move
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
    #increasing the points when placing the piece in the center of the board
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

# a function to check whether this is the last move or not
def IsLastMove(game_board):
    if HaveWon(game_board, COMPUTER ) or HaveWon(board, AI_AGENT) or len(GetValidCells(game_board)) == 0:
        return True
    else:
        return False

# applying minimax algorithim which will be used by the AI agent
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





# applying alpha beta algorthim which will be used by the AI agent

def alphabeta(game_board, depth, alpha, beta, maximizedP):
        valid_cells = GetValidCells(game_board)
        lastmove = IsLastMove(game_board)
        if depth == 0 or lastmove:
            if lastmove:
                if HaveWon(game_board, AI_AGENT): #AI_AGENT have won
                    return (None, 100000000000000)
                elif HaveWon(game_board, COMPUTER): #computer have won
                    return (None, -10000000000000)
                else: # Game is over, no more valid moves(Draw)
                    return (None, 0)
            else: # Depth is zero
                return (None, CellPoints(game_board, AI_AGENT))
       #maximizing the points of the column
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



# a function to return the valid cells for placing gamepiece
def GetValidCells(game_board):
	valid_cells = []
	for col in range(C):
		if IsValidCell(game_board, col):
			valid_cells.append(col)
	return valid_cells




# GUI for the board game
def MakeBoard(board):
    for c in range(C):
        for r in range(R):
            pygame.draw.rect(screen, black, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, white, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(C):
        for r in range(R):
            if board[r][c] == COMPUTER:
                pygame.draw.circle(screen, red, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_AGENT:
                pygame.draw.circle(screen, blue, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
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

#randomizing which one will start
turn = random.randint(comp, AI)


# function for the game to be played for the AI agent against the computer
def play_game(algo,level):
    board = generate_board()
    game_over = False
    turn = 0
    pygame.init()
    count =0
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if turn == 0 :
            iwin, col_won2 = willWon(board, 1)
            iswin, col_won = willWon(board, 2)
            count += 1
            # Agent's Move
            if algo == "minimax":
                if not iswin: #if compuer can't won in this turn
                    col, minimax_score = minimax(board, level, True)
                    print("mini")
                else:
                    if iwin:  #if agent will win in this turn
                        col=col_won2
                        print("mini")
                    else:  # if computer will win in this turn
                        col = col_won
                        print("rand")
                        print(col_won)
            elif algo == "alphabeta":
                if not iswin:
                    col, minimax_score = alphabeta(board, level,-math.inf,math.inf, True)
                    print("alphabeta")
                else:
                    if iwin:
                        col=col_won2
                        print("alphabeta")
                    else:
                        col = col_won
                        print("rand")
                        print(col_won)
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
            # col = random.randint(0, C-1)
            coll = random.randint(computer_lower,computer_upper)

            # col, minimax_score = alphabeta(board, 1,-math.inf,math.inf, True)
            if IsValidCell(board, coll):
                row = next_row(board, coll)
                Drop(board, row, coll, 2)

                if HaveWon(board, 2):
                    label = myfont.render("Computer wins!!", 1, blue)
                    screen.blit(label, (40, 10))
                    game_over = True

                turn = 0

        print_board(board)
        MakeBoard(board)
        time.sleep(0.5)

    pygame.time.wait(1000)
    return count


selected_level = None
selected_algorithm = None

def level_selected():
    global selected_level
    selected_level = level_combobox.get()
    window.destroy()
# choosing the level of diffculty to be applied
def select_level():
    global window, level_combobox

    # Create the main window
    window = tk.Tk()
    window.title("level Selection")

    # level Type Selection
    level_label = ttk.Label(window, text="Select level Type:")
    level_label.pack()

    level_combobox = ttk.Combobox(window, values=["Easy", "Medium","Hard"])
    level_combobox.pack()

    # Button to confirm selection
    confirm_button = ttk.Button(window, text="Confirm", command=level_selected)
    confirm_button.pack()

    # Run the main window loop
    window.mainloop()

    return selected_level


def algorithm_selected():
    global selected_algorithm
    selected_algorithm = algorithm_combobox.get()
    window.destroy()

# choosing the algorithm to be applied
def select_algorithm():
    global window, algorithm_combobox

    # Create the main window
    window = tk.Tk()
    window.title("Algorithm Selection")

    # Algorithm Type Selection
    algorithm_label = ttk.Label(window, text="Select Algorithm Type:")
    algorithm_label.pack()

    algorithm_combobox = ttk.Combobox(window, values=["minimax", "alphabeta"])
    algorithm_combobox.pack()

    # Button to confirm selection
    confirm_button = ttk.Button(window, text="Confirm", command=algorithm_selected)
    confirm_button.pack()

    # Run the main window loop
    window.mainloop()

    return selected_algorithm

# Start the Game
algorithm_type = select_algorithm()
print("Selected Algorithm:", algorithm_type)
level_type = select_level()
print("Selected Algorithm:", level_type)
if level_type == "Easy":
    level_type=1
elif level_type == "Medium":
    level_type=3
elif level_type == "Hard":
    level_type=5

steps=play_game(algorithm_type,level_type)
print("the steps: ",steps)