import os
from tkinter import messagebox
from tkinter import *

# Settings cells
HEIGHT_CELL, WIDTH_CELL = 20, 20
COUNT_CELLS_X = 20
COUNT_CELLS_Y = 20
COLOR_LIVE = '#f08b53'
COLOR_DIE = '#d6c496'

# Settings canvas
SIZE_MARGIN_TOP, SIZE_MARGIN_BOTTOM = 2, 0
SIZE_MARGIN_LEFT, SIZE_MARGIN_RIGHT = 2, 3
WIDTH_CANV = SIZE_MARGIN_LEFT + WIDTH_CELL * COUNT_CELLS_X + SIZE_MARGIN_RIGHT
HEIGHT_CANV = SIZE_MARGIN_TOP + HEIGHT_CELL * COUNT_CELLS_Y + SIZE_MARGIN_BOTTOM

X_START = SIZE_MARGIN_LEFT
X_END = WIDTH_CANV - SIZE_MARGIN_RIGHT
Y_START = SIZE_MARGIN_TOP
Y_END = HEIGHT_CANV - SIZE_MARGIN_BOTTOM

# Settings message
HEIGHT_MESSAGE = 20
MESSAGE_BEGIN = 'Hi! Click to begin :)'
MESSAGE_CHOICE_CELL = 'Please, choice the cells'
MESSAGE_RUN = 'Game is running!'

# Settings button
HEIGHT_BUTTON = 35
TEXT_BEGIN = 'Begin!'
TEXT_START = 'Start!'
TEXT_RESTART = 'Restart!'

# Type of state
STATE_BEGIN = 1
STATE_CHOICE_CELL = 2
STATE_RUN = 3

# Setting game
DELAY = 1


class Game:
    def __init__(self):
        self.window = Tk()
        self.window.title("Game of Life")
        self.window.geometry(f'{WIDTH_CANV}x{HEIGHT_MESSAGE + HEIGHT_CANV + HEIGHT_BUTTON}')
        self.window.resizable(width=False, height=False)
        self.window.protocol("WM_DELETE_WINDOW", self._close)
        self.window.configure(background="#353012")
        # self.window.wm_iconbitmap(f'{os.path.dirname(os.path.abspath(__file__))}/icon.ICO')
        self.window.wm_iconbitmap('icon.ICO')
        self.message = Label(self.window, text=MESSAGE_BEGIN,  borderwidth=1, relief="solid",
                             font=("Courier Bold", 12), background="#9aa710", foreground="white")
        self.message.pack(side=TOP, fill=X)

        self.canvas = Canvas(self.window, width=WIDTH_CANV, height=HEIGHT_CANV, bg='#353012',
                             highlightbackground="#353012")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._click_on_field)

        self.button = Button(self.window, command=self._click_on_button, text=TEXT_BEGIN,
                             font=("Courier Bold", 12),  background="#a74c1f", foreground="white")
        self.button.pack(side=BOTTOM, fill=X)

        self.markers = self._initializeField()
        self.state = STATE_BEGIN

        self.window.mainloop()

    def _click_on_button(self):
        if self.state == STATE_BEGIN:
            self.message.config(text=MESSAGE_CHOICE_CELL)
            self.button.config(text=TEXT_START)
            self.state = STATE_CHOICE_CELL
        elif self.state == STATE_CHOICE_CELL:
            self.message.config(text=MESSAGE_RUN)
            self.button.config(text=TEXT_RESTART)
            self.state = STATE_RUN
            self.window.after(DELAY, self._run)
        elif self.state == STATE_RUN:
            self.message.config(text=MESSAGE_CHOICE_CELL)
            self.button.config(text=TEXT_START)
            self.state = STATE_CHOICE_CELL
            self._clearField()

    def _click_on_field(self, event):
        if self.state == STATE_CHOICE_CELL:
            number_cell_x = min((X_START + event.x) // WIDTH_CELL, COUNT_CELLS_X - 1)
            number_cell_y = min((Y_START + event.y) // HEIGHT_CELL, COUNT_CELLS_Y - 1)
            x = X_START + WIDTH_CELL * number_cell_x
            y = Y_START + HEIGHT_CELL * number_cell_y
            self.markers[number_cell_y][number_cell_x] = 1
            self.canvas.create_rectangle(x, y, x + WIDTH_CELL, y + HEIGHT_CELL, fill=COLOR_LIVE, outline='#634a27')

    def _initializeField(self):
        markers = []
        for y in range(Y_START, Y_END, HEIGHT_CELL):
            row_markers = []
            for x in range(X_START, X_END, WIDTH_CELL):
                self.canvas.create_rectangle(x, y, x + WIDTH_CELL, y + HEIGHT_CELL, fill=COLOR_DIE, outline='white')
                row_markers.append(0)
            markers.append(row_markers)
        return markers

    def _clearField(self):
        for i, y in enumerate(range(Y_START, Y_END, HEIGHT_CELL)):
            for j, x in enumerate(range(X_START, X_END, WIDTH_CELL)):
                if self.markers[i][j] == 1:
                    self.canvas.create_rectangle(x, y, x + WIDTH_CELL, y + HEIGHT_CELL, fill=COLOR_DIE, outline='white')
                    self.markers[i][j] = 0

    def _run(self):
        if self.state != STATE_RUN:
            return
        new_markers = []
        count_lives = 0
        for i in range(COUNT_CELLS_Y):
            for j in range(COUNT_CELLS_X):
                count_around = 0
                for k in [i - 1, i, i + 1]:
                    for s in [j - 1, j, j + 1]:
                        s = COUNT_CELLS_X - 1 if s == -1 else s
                        s = 0 if s == COUNT_CELLS_X else s
                        k = COUNT_CELLS_Y - 1 if k == -1 else k
                        k = 0 if k == COUNT_CELLS_Y else k
                        count_around += self.markers[k][s]
                # for row in self.markers[max(i - 1, 0): min(i + 1, len(self.markers)) + 1]:
                #     count_around += sum(row[max(j - 1, 0): min(j + 1, len(self.markers[i])) + 1])
                if self.markers[i][j] == 0:
                    if count_around == 3:
                        count_lives += 1
                        new_markers.append((i, j, 1))
                elif self.markers[i][j] == 1:
                    if count_around - 1 not in [2, 3]:
                        new_markers.append((i, j, 0))
                    else:
                        count_lives += 1
        if len(new_markers) == 0 or count_lives == 0:
            self._click_on_button()
        else:
            for new_marker in new_markers:
                x = X_START + WIDTH_CELL * new_marker[1]
                y = Y_START + HEIGHT_CELL * new_marker[0]
                self.markers[new_marker[0]][new_marker[1]] = new_marker[2]
                if new_marker[2] == 0:
                    self.canvas.create_rectangle(x, y, x + WIDTH_CELL, y + HEIGHT_CELL, fill=COLOR_DIE,
                                                 outline='white')
                else:
                    self.canvas.create_rectangle(x, y, x + WIDTH_CELL, y + HEIGHT_CELL, fill=COLOR_LIVE,
                                                 outline='#634a27')
            self.window.after(DELAY, self._run)

    def _close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window.destroy()


game = Game()
