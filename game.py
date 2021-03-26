import time
import tkinter as tk
from random import randint
from typing import Union

# This now works, I suppose...
# not responsive, I must mention

size_v, size_h = 10,12
total_mines = size_h * size_v // 5
flags = total_mines
moves_made = 0
grid: list[list[Union[int, str]]] = [[0 for _ in range(size_h)] for _ in range(size_v)]
covered = [[True for _ in range(size_h)] for _ in range(size_v)]
mine_list = []
frame_grid = []
color = {1: 'blue', 2: 'green', 3: 'red', 4: 'purple',
         5: 'yellow', 6: 'cyan', 7: 'magenta', 8: 'black'}


def print_grid(grid_g=None):
    if grid_g is None:
        grid_g = grid
    for line in grid_g:
        for elem in line:
            print(elem, end="  ")
        print("")


def raise_value(x, y):
    try:
        grid[x][y] += 1
    except TypeError:
        pass
    except IndexError:
        pass


def map_adj(func, v, h):
    """to map a function on cells adjacent to given cell"""

    '''top row'''
    if v > 0:
        if h > 0:
            func(v - 1, h - 1)
        func(v - 1, h)
        if h < size_h - 1:
            func(v - 1, h + 1)
    '''middle row'''
    if h > 0:
        func(v, h - 1)
    if h < size_h - 1:
        func(v, h + 1)
    '''bottom row'''
    if v < size_v - 1:
        if h > 0:
            func(v + 1, h - 1)
        func(v + 1, h)
        if h < size_h - 1:
            func(v + 1, h + 1)


def plant_mines(mines=total_mines, first_v=None, first_h=None):
    for m in range(mines):
        mine_planted = False
        while not mine_planted:
            ran_v = randint(0, size_v - 1)
            ran_h = randint(0, size_h - 1)

            if ran_v == first_v and ran_h == first_h:
                continue

            if grid[ran_v][ran_h] != 'X':
                grid[ran_v][ran_h] = 'X'
                map_adj(raise_value, ran_v, ran_h)
                mine_list.append((ran_v, ran_h))
                mine_planted = True


# print_grid(grid)


def draw_val(can, val):
    if val == 'X':
        can.configure(bg='#000000')
    else:
        can.configure(bg='#b0b0b0')
        if val:
            can.create_text(25, 25, text=str(val), fill=color[val], font=('Arial', 35))


class SizedButton:
    def __init__(self, root, height=50, width=50):
        self.f = tk.Frame(root, height=height, width=width)
        self.f.pack_propagate(0)  # don't shrink
        self.can = tk.Canvas(self.f)
        self.can.pack(fill=tk.BOTH, expand=1)
        self.can.pack_forget()
        self.btn = tk.Button(self.f, bg='gray')
        self.btn.bind("<Button-1>,")
        self.btn.pack(fill=tk.BOTH, expand=1)


window = tk.Tk()
window.title("Minesweeper :by lox")
window.geometry('+400+10')
flags_left = tk.Label(window, text=flags, font=("Arial", 20))
Title = tk.Label(window, text="Minesweeper", font=("Arial", 40))
moves_counter = tk.Label(window, text=moves_made, font=("Arial", 20))
new_button = tk.Button(window, text="New", font=("Arial", 20))

flags_left.grid(row=0, column=0, rowspan=3, columnspan=2)
Title.grid(row=0, column=2, rowspan=3, columnspan=size_h - 6)
moves_counter.grid(row=0, column=size_h - 4, rowspan=3, columnspan=2)
new_button.grid(row=0, column=size_h - 2, rowspan=3, columnspan=2)


def flags_update(num=None):
    global flags
    if num is None:
        flags = total_mines
    elif num in (-1, 1):
        flags += num
    flags_left.configure(text=flags)


def set_main_frame():
    global frame_grid
    main_frame = tk.Frame(window)
    main_frame.grid(row=3, column=0, columnspan=size_h, rowspan=size_v, padx=10, pady=10)
    frame_grid = []
    for i in range(size_v):
        frame_row = []
        for j in range(size_h):
            x = SizedButton(main_frame)
            x.f.grid(row=i, column=j)
            x.btn.bind("<Button-1>", lambda e, v=i, h=j: uncover(v, h))
            x.btn.bind("<Button-3>", flag)
            frame_row.append(x)  # not sure how to get frame pathname without _w, but this works.
        frame_grid.append(frame_row)


def uncover(v, h):
    global moves_made
    if moves_made == 0:
        plant_mines(first_v=v, first_h=h)
    """this will be used both through commands and by mouse"""
    "If the location is already uncovered or if the button is flagged, we ignore it"
    if not covered[v][h]:
        return
    x = frame_grid[v][h]
    if x.btn.cget('bg') == 'red':
        return

    "if not, hide the button,show the canvas, set to uncovered"
    moves_made += 1
    moves_counter.configure(text=moves_made)
    can = x.can
    draw_val(can, grid[v][h])
    can.pack()
    x.btn.pack_forget()
    covered[v][h] = False
    if check_win():
        win()

    "Now, if we hit a mine, we end the game"
    val = grid[v][h]
    if val == 'X':
        lose()
        return
    "We have covered flags and mines, and if the tiles are numbered, we are done."
    "However, if the tile is a zero, we need to open the adjacent tiles too:"
    if val == 0:
        map_adj(uncover, v, h)


def flag(event):
    btn = event.widget
    if btn.cget('bg') == 'red':
        btn.configure(bg='gray', activebackground="SystemButtonFace")
        flags_update(1)
    else:
        btn.configure(bg='red', activebackground='red')
        flags_update(-1)


def check_win():
    for v in range(size_v):
        for h in range(size_h):
            if grid[v][h] != 'X':
                if covered[v][h]:
                    return False
    return True


def win():
    print('You_win')
    result = tk.Label(text='You_Win', font=('Arial', '50'))
    result.grid(row=size_v // 2 - 2, column=size_h // 2 - 5, rowspan=4, columnspan=10)
    window.update()
    i = 0
    while i < len(mine_list):
        time.sleep(randint(100, 400) / 1000)
        v, h = mine_list[i]
        x = frame_grid[v][h]
        can = x.can
        can.configure(bg='green')
        can.pack()
        x.btn.pack_forget()
        covered[v][h] = False
        window.update()
        i += 1
    time.sleep(2)
    result.grid_remove()


def lose():
    print('You_lose')
    result = tk.Label(text='YouLose', font=('Arial', '50'))
    result.grid(row=size_v // 2 - 2, column=size_h // 2 - 5, rowspan=4, columnspan=10)
    window.update()
    to_reveal = []
    for mine in mine_list:
        v, h = mine
        to_reveal.append((frame_grid[v][h], grid[v][h]))

    for x, val in to_reveal:
        time.sleep(randint(100, 400) / 1000)
        draw_val(x.can, val)
        x.can.pack()
        x.btn.pack_forget()
        window.update()
    time.sleep(2)
    result.grid_remove()


def new():
    global grid, covered, moves_made, mine_list
    moves_made = 0
    moves_counter.configure(text=moves_made)
    grid = [[0 for _ in range(size_h)] for _ in range(size_v)]
    covered = [[True for _ in range(size_h)] for _ in range(size_v)]
    mine_list = []
    flags_update()
    set_main_frame()


new_button.configure(command=new)
new()
window.mainloop()
