import pygame
import time

pygame.font.init()

class Grid:
    def __init__(self, rows, cols, width, height, win, brd):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(brd[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.win = win

    def draw(self):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

class Cube:
    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x + 5, y + 5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

def redraw_window(win, board, time):
    win.fill((255,255,255))
    board.draw()

def print_gui(s):
    win = pygame.display.set_mode((540,600))
    board = Grid(s.shape[0], s.shape[0], 540, 540, win, s)
    redraw_window(win, board, 0)
    pygame.display.update()

# win = None
def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")

main()