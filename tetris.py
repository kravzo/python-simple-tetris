import random
from tkinter import *


glass = []
figures = []
current_figure = []
next_figure = []
lines = 0
score = 0
x_init = 5
y_init = 5
delay = 300


def init_variables():
    global glass
    global figures
    global lines
    global score
    glass = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    figures = [[[0, 0], [-1, 0], [0, 1], [1, 1]],
               [[0, 0], [-1, 0], [1, 0], [2, 0]],
               [[0, 0], [-1, 0], [0, 1], [-1, 1]],
               [[0, 0], [1, 0], [0, 1], [-1, 1]],
               [[0, 0], [-1, 0], [1, 0], [0, 1]],
               [[0, 0], [-1, 0], [1, 0], [1, 1]],
               [[0, 0], [-1, 0], [-1, 1], [1, 0]]]
    lines = 0
    score = 0


def get_figure(figure, source):
    figure.clear()
    for brick in source:
        figure.append(brick.copy())


def move_left(e):
    if is_it_ledge(current_figure):
        pass
    else:
        for brick in current_figure:
            brick[0] -= 1
        drawGlass()


def move_right(e):
    if is_it_redge(current_figure):
        pass
    else:
        for brick in current_figure:
            brick[0] += 1
        drawGlass()


def rotate_straight(e):
    rotate("straight")


def rotate_counter(e):
    rotate("counter")


def rotate(direction):
    shadow_figure = []
    for brick in current_figure:
        shadow_figure.append(brick.copy())
    x_offset = shadow_figure[0][0]
    y_offset = shadow_figure[0][1]
    side_adjust = 0
    vert_adjust = 0
    for brick in shadow_figure:
        brick[0] -= x_offset
        brick[1] -= y_offset
        if direction == "straight":
            brick[0], brick[1] = -brick[1], brick[0]
        else:
            brick[0], brick[1] = brick[1], -brick[0]
        brick[0] += x_offset
        if brick[0] > 9 and brick[0] - 9 > side_adjust:
            side_adjust = brick[0] - 9
        if brick[0] < 0 and brick[0] < side_adjust:
            side_adjust = brick[0]
        brick[1] += y_offset
        if brick[1] < 0 and brick[1] < vert_adjust:
            vert_adjust = brick[1]
    if side_adjust != 0:
        for brick in shadow_figure:
            brick[0] -= side_adjust
    if vert_adjust != 0:
        for brick in shadow_figure:
            brick[1] -= vert_adjust
    crosses = False
    for brick in shadow_figure:
        if brick[1] > 19 or glass[brick[0]][brick[1]] == 1:
            crosses = True
    if not crosses:
        current_figure.clear()
        for brick in shadow_figure:
            current_figure.append(brick)
    drawGlass()


def is_it_redge(figure):
    for brick in current_figure:
        if brick[0] > 8 or glass[brick[0] + 1][brick[1]] == 1:
            return True
    return False


def is_it_ledge(figure):
    for brick in current_figure:
        if brick[0] < 1 or glass[brick[0] - 1][brick[1]] == 1:
            return True
    return False


def drawGlass():
    canv.create_rectangle(5, 5, 205, 405, fill="lightgray", outline="black")
    for col in range(0, 10):
        for row in range(0, 20):
            if glass[col][row] == 1:
                x = x_init + 20 * col
                y = y_init + 20 * row
                canv.create_rectangle(x, y, x + 20, y + 20, fill="gray", outline="black")
    draw_figure(current_figure, x_init, y_init)



def draw_figure(figure, x0, y0):
    for brick in figure:
        x = x0 + 20 * brick[0]
        y = y0 + 20 * brick[1]
        canv.create_rectangle(x, y, x + 20, y + 20, fill="gray", outline="black")


def falling():
    for brick in current_figure:
        brick[1] += 1
    drawGlass()


def chek_and_eat():
    global score
    global lines
    full_lines = []
    for row in range(1, 20, 1):
        line_full = True
        for brick in glass:
            if brick[row] == 0:
                line_full = False
        if line_full:
            full_lines.append(row)
    for line in full_lines:
        for col in glass:
            for row in range(line, 0, -1):
                col[row] = col[row - 1]
        if len(full_lines) > 3:
            score += 300
        else:
            score += 100
        lines += 1


def timer_event():
    global current_figure
    global delay
    fell = False
    score_label.config(text="Score:" + str(score) + '\n' + "Lines:" + str(lines))
    for brick in current_figure:
        if brick[1] > 18:
            fell = True
        elif glass[brick[0]][brick[1] + 1] == 1:
            fell = True
    if fell:
        if delay != 300:
            delay = 300
        for brick in current_figure:
            glass[brick[0]][brick[1]] = 1
        chek_and_eat()
        for col in glass:
            if col[0] == 1:
                score_label.config(text="Score:" + str(score) + '\n' + "Lines:" + str(lines) + '\n' + "Game over")
                new_game_btn["state"] = "normal"
                return
        get_figure(current_figure, next_figure)
        for brick in current_figure:
            brick[0] += 5
        get_figure(next_figure, figures[random.randint(0, 6)])
    else:
        falling()
    drawGlass()
    canv.create_rectangle(210, 335, 330, 405, fill="lightgray", outline="black")
    draw_figure(next_figure, 250, 350)
    root.after(delay, timer_event)


def figure_drop(e):
    global delay
    delay = 50


def new_game():
    new_game_btn["state"] = "disabled"
    init_variables()
    get_figure(next_figure, figures[random.randint(0, 6)])
    get_figure(current_figure, figures[random.randint(0, 6)])
    for brick in current_figure:
        brick[0] += 5
    root.after(1000, timer_event)


root = Tk()
root.title("Tetris")
root.minsize(width=400, height=410)
root.maxsize(width=400, height=410)
canv = Canvas(height=410, width=400, background="lightgray")
canv.pack()
score_label = Label(root, text="Score:" + str(score) + '\n' + "Lines:" + str(lines),
                    font='Helvetica 17 bold', background="lightgray", justify="left")
score_label.place(x=210, y=5)
info_label = Label(root, text="Controls:\n\n<Left arrow> - move left\n<Right arrow> - move right\n" +
                              "<Up arrow> - rotate counter-\nclockwise\n<Down arrow> - rotate clockwise\n" +
                              "<Space> - drop figure down",
                   font='Helvetica 8', background="lightgray", justify="left")
info_label.place(x=210, y=150)
new_game_btn = Button(root, text="New Game", command=new_game)
new_game_btn.place(x=230, y=280)
root.bind('<Left>', move_left)
root.bind('<Right>', move_right)
root.bind('<Down>', rotate_straight)
root.bind('<Up>', rotate_counter)
root.bind('<space>', figure_drop)
root.mainloop()
