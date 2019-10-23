from graphics import *

FIELD = []
SIZE_SPLIT = 20
HEIGHT_WIN, WIDTH_WIN = 400, 400
SIZE_MARGIN = 40


def createField(win):
    height_cell = (HEIGHT_WIN - (SIZE_MARGIN * 2)) // SIZE_SPLIT
    width_cell = (WIDTH_WIN - (SIZE_MARGIN * 2)) // SIZE_SPLIT
    for y in range(SIZE_MARGIN, HEIGHT_WIN - SIZE_MARGIN, height_cell):
        row_cells = []
        for x in range(SIZE_MARGIN, WIDTH_WIN - SIZE_MARGIN, width_cell):
            cell = Rectangle(Point(x, y), Point(x + width_cell, y + height_cell))
            cell.draw(win)
            row_cells.append(cell)
        FIELD.append(row_cells)

def run():
    ...


def main():
    win = GraphWin("Game of Life", HEIGHT_WIN, WIDTH_WIN)
    createField(win)
    message = Text(Point(WIDTH_WIN // 2, SIZE_MARGIN // 2), 'Put the cells ^-^')
    message.draw(win)

    win.getMouse()
    win.close()


if __name__ == '__main__':
    main()