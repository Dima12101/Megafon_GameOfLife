from graphics import *
import threading
import random

# Settings field
SIZE_SPLIT = 20

# Settings window
HEIGHT_WIN, WIDTH_WIN = 400, 400
SIZE_MARGIN = 40
TITLE_BEGIN = 'Hi! Click to begin :)'
TITLE_CHOICE_CELL = 'Please, choice the cells'
TITLE_RUN = 'Game is running!'

# Settings button
HEIGHT_BUTTON, WIDTH_BUTTON = 20, 100
TEXT_BEGIN = 'Begin!'
TEXT_START = 'Start!'
TEXT_RESTART = 'Restart!'

# Type of state
STATE_BEGIN = 1
STATE_CHOICE_CELL = 2
STATE_RUN = 3

# Colors cell
COLOR_LIVE = 'green'
COLOR_DIE = 'white'


class Game:
    def __init__(self):
        self.win = GraphWin("Game of Life", HEIGHT_WIN, WIDTH_WIN)
        self.title = self.Title(self.win, TITLE_BEGIN)
        self.cells, self.markers = self._initializeField()
        self.button = self.Button(self.win, TEXT_BEGIN)
        self.state = STATE_BEGIN

    def _initializeField(self):
        cells = []
        markers = []
        height_cell = (HEIGHT_WIN - (SIZE_MARGIN * 2)) // SIZE_SPLIT
        width_cell = (WIDTH_WIN - (SIZE_MARGIN * 2)) // SIZE_SPLIT
        for y in range(SIZE_MARGIN, HEIGHT_WIN - SIZE_MARGIN, height_cell):
            row_cells = []
            row_markers = []
            for x in range(SIZE_MARGIN, WIDTH_WIN - SIZE_MARGIN, width_cell):
                cell = Rectangle(Point(x, y), Point(x + width_cell, y + height_cell))
                cell.setFill(COLOR_DIE)
                cell.draw(self.win)
                row_cells.append(cell)
                row_markers.append(0)
            cells.append(row_cells)
            markers.append(row_markers)
        return cells, markers

    class Title:
        def __init__(self, win, text):
            self.obj = Text(Point(WIDTH_WIN // 2, SIZE_MARGIN // 2), text)
            self.obj.setStyle('italic')
            self.obj.draw(win)

        def setText(self, text):
            self.obj.setText(text)

    class Button:
        def __init__(self, win, name):
            self.obj = Rectangle(
                Point(WIDTH_WIN // 2 - WIDTH_BUTTON // 2, HEIGHT_WIN - SIZE_MARGIN // 2 - HEIGHT_BUTTON // 2),
                Point(WIDTH_WIN // 2 + WIDTH_BUTTON // 2, HEIGHT_WIN - SIZE_MARGIN // 2 + HEIGHT_BUTTON // 2))
            self.obj.setFill("green")
            self.text = Text(Point(WIDTH_WIN // 2, HEIGHT_WIN - SIZE_MARGIN // 2), name)

            self.obj.draw(win)

            self.text.draw(win)

        def setName(self, name):
            self.text.setText(name)

        def isClick(self, click):
            b_point1 = self.obj.getP1()  # (lower left)
            b_point2 = self.obj.getP2()  # (upper right)
            return b_point1.getX() < click.getX() < b_point2.getX() and b_point1.getY() < click.getY() < b_point2.getY()

    def _clearField(self):
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                cell.setFill(COLOR_DIE)
                self.markers[i][j] = 0

    def _run(self):
        while True:
            new_markers = []
            for i in range(len(self.cells)):
                row_new_markers = []
                for j in range(len(self.cells[i])):
                    count_around = 0
                    for row in self.markers[max(i - 1, 0): min(i + 1, len(self.cells)) + 1]:
                        count_around += sum(row[max(j - 1, 0): min(j + 1, len(self.cells[i])) + 1])
                    if self.markers[i][j] == 0:
                        if count_around == 3:
                            row_new_markers.append(1)
                        else:
                            row_new_markers.append(0)
                    elif self.markers[i][j] == 1:
                        if count_around - 1 in [2, 3]:
                            row_new_markers.append(1)
                        else:
                            row_new_markers.append(0)
                new_markers.append(row_new_markers)
            for i, row in enumerate(self.cells):
                for j, cell in enumerate(row):
                    if new_markers[i][j] == 1:
                        cell.setFill(COLOR_LIVE)
                        self.markers[i][j] = 1
                    else:
                        cell.setFill(COLOR_DIE)
                        self.markers[i][j] = 0

    def _clickButton(self):
        if self.state == STATE_BEGIN:
            self.title.setText(TITLE_CHOICE_CELL)
            self.button.setName(TEXT_START)
            self.state = STATE_CHOICE_CELL
        elif self.state == STATE_CHOICE_CELL:
            self.title.setText(TITLE_RUN)
            self.button.setName(TEXT_RESTART)
            self.state = STATE_RUN
            self._run()
        elif self.state == STATE_RUN:
            self.title.setText(TITLE_CHOICE_CELL)
            self.button.setName(TEXT_START)
            self.state = STATE_CHOICE_CELL
            self._clearField()

    def _choice_cell(self, click):
        if SIZE_MARGIN < click.getX() < WIDTH_WIN - SIZE_MARGIN and \
                SIZE_MARGIN < click.getY() < HEIGHT_WIN - SIZE_MARGIN:
            for i, row in enumerate(self.cells):
                for j, cell in enumerate(row):
                    cell_p1 = cell.getP1()  # (lower left)
                    cell_p2 = cell.getP2()  # (upper right)
                    if cell_p1.getX() < click.getX() < cell_p2.getX() and cell_p1.getY() < click.getY() < cell_p2.getY():
                        cell.setFill(COLOR_LIVE)
                        self.markers[i][j] = 1

    def launch(self):
        while True:
            clickPoint = self.win.getMouse()

            if clickPoint is not None:
                if self.button.isClick(clickPoint):
                    self._clickButton()
                if self.state == STATE_CHOICE_CELL:
                    self._choice_cell(clickPoint)

    def close(self):
        self.win.close()


def main():
    game = Game()
    game.launch()
    game.close()


if __name__ == '__main__':
    main()
