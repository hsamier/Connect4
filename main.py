import pygame
import numpy as np

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (0,0,255)

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


def print_board(board):
	print(np.flip(board, 0))


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

