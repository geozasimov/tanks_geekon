
# GeekPaste

from tkinter import Tk, Canvas, mainloop, NW
from PIL import Image, ImageTk
import random

# размер карты в пикселях
window_width = 600
window_height = 600

# создаем холст
tk = Tk()
c = Canvas(tk, width=window_width, height=window_height, bg='white')
c.pack()

# карта
game_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# размеры блока
block_width = window_width // 12
block_height = window_height // 12

bullets = []

images = {
    "brick": ImageTk.PhotoImage(Image.open("images/-color-stone-wall_tanks.jpg").resize((block_width, block_height))),
    "grass": ImageTk.PhotoImage(Image.open("images/grass_tanks.jpg").resize((block_width, block_height))),
    "bullet_up": ImageTk.PhotoImage((Image.open("images/weapon_tanks.jpg").resize((10, 30)))),
    "bullet_down": ImageTk.PhotoImage((Image.open("images/weapon_tanks.jpg").resize((10, 30)).rotate(180))),
    "bullet_left": ImageTk.PhotoImage((Image.open("images/weapon_tanks.jpg").resize((10, 30)).rotate(90))),
    "bullet_right": ImageTk.PhotoImage((Image.open("images/weapon_tanks.jpg").resize((10, 30)).rotate(270))),
    "tank_up": ImageTk.PhotoImage((Image.open("images/tanks.gif").convert('RGBA').resize((block_width, block_height)))),
    "tank_down": ImageTk.PhotoImage(
        (Image.open("images/tanks.gif").convert('RGBA').resize((block_width, block_height)).rotate(180))),
    "tank_left": ImageTk.PhotoImage(
        (Image.open("images/tanks.gif").convert('RGBA').resize((block_width, block_height)).rotate(90))),
    "tank_right": ImageTk.PhotoImage(
        (Image.open("images/tanks.gif").convert('RGBA').resize((block_width, block_height)).rotate(270)))
}

# рисуем карту
for i in range(12):
    for j in range(12):
        if game_map[i][j] == 0:
            c.create_image(i * block_width, j * block_height, image=images['grass'], anchor=NW)
        if game_map[i][j] == 1:
            c.create_image(i * block_width, j * block_height, image=images['brick'], anchor=NW)


def rotate(game_object, direction):
    # напишите функцию поворота танка: нужно спрятать все картинки и показать нужную
    keys = ["up", "down", "left", "right"]
    for key in keys:
        image = game_object[key]
        c.itemconfigure(image, state='hidden')
    needed = game_object[direction]
    c.itemconfigure(needed, state='normal')
    game_object["direction"] = direction


def move(game_object, dx, dy):
    # напишите функцию перемещения всех 4 картинок танка на (x, y) пикселей
    keys = ["up", "down", "left", "right"]
    for key in keys:
        item = game_object[key]
        c.move(item, dx, dy)


def delete(game_object, objects_lists):
    # реализуйте функцию удаления танка/пули (c.delete(image))
    keys = ["up", "down", "left", "right"]
    for key in keys:
        image = game_object[key]
        c.delete(image)
    objects_lists.remove(game_object)


def coords(game_object):
    # внесите изменения в предыдущую версию, чтобы функция снова заработала
    x, y = c.coords(game_object['up'])
    return (int(x // block_width), int(y // block_height))


def get_tank(x, y, direction):
    tank = {
        "life": 3,
        "direction": direction,
        "up": c.create_image(x * block_width, y * block_height, image=images['tank_up'], anchor=NW, state='normal'),
        "down": c.create_image(x * block_width, y * block_height, image=images['tank_down'], anchor=NW, state='hidden'),
        "left": c.create_image(x * block_width, y * block_height, image=images['tank_left'], anchor=NW, state='hidden'),
        "right": c.create_image(x * block_width, y * block_height, image=images['tank_right'], anchor=NW,
                                state='hidden')
    }
    rotate(tank, direction)
    return tank


def get_bullet(x, y, direction):
    if direction == 'left':
        # выбираем точку на 10 пикселей левее границы клетки с танком
        # по высоте - середина блока
        rx = block_width * x - 10
        ry = block_height * y + block_height // 2
    elif direction == 'right':
        # выбираем точку на 10 пикселей правее правой границы клетки с танком
        rx = block_width * (x + 1) + 10
        ry = block_height * y + block_height // 2
    elif direction == 'up':
        # выбираем точку на 10 пикселей выше верхней границы
        rx = block_width * x + block_width // 2
        ry = block_height * y - 10
    else:
        # выбираем точку на 10 пикселей нижней границы
        rx = block_width * x + block_width // 2
        ry = block_height * (y + 1) + 10

    bullet = {
        "direction": 'up',
        "up": c.create_image(rx, ry, image=images['bullet_up'], state='normal'),
        "down": c.create_image(rx, ry, image=images['bullet_down'], state='hidden'),
        "left": c.create_image(rx, ry, image=images['bullet_left'], state='hidden'),
        "right": c.create_image(rx, ry, image=images['bullet_right'], state='hidden')
    }

    rotate(bullet, direction)
    return bullet


bullets = []
tanks = []

my_tank = get_tank(6, 6, 'up')


def move_bullets():
    for bullet in bullets[:]:
        x, y = coords(bullet)
        for tank in tanks[:]:
            if coords(tank) == coords(bullet):
                tank["life"] -= 1
                if tank["life"] == 0:
                    if tank == my_tank:
                        tk.destroy()
                    else:
                        delete(tank, tanks)

            # если жизнь танка равна нулю, проверить наш ли это танк.
            # TODO: если наш - закрыть окно (tk.destroy()), если не наш - просто удалить его из списка и из игры.
        if is_available(*coords(bullet)) == False:
            delete(bullet, bullets)
        else:
            x, y = 0, 0
            direct = bullet["direction"]
            if direct == "up":
                x, y = 0, -20
            if direct == "down":
                x, y = 0, 20
            if direct == "left":
                x, y = -20, 0
            if direct == "right":
                x, y = 20, 0
            move(bullet, x, y)
    c.after(50, move_bullets)


# проверка доступности клетки
def is_available(i, j):
    if i < 0 or i >= 12 or j < 0 or j >= 12:
        return False
    if game_map[i][j] == 1:
        return False
    # добавляем проверку на столкновение с другим танком
    for tank in tanks:
        if coords(tank) == (i, j):
            return False
    return True


# нажатие клавиш
def keyDown(key):
    dx = 0
    dy = 0
    x, y = coords(my_tank)
    if key.char == 'a':
        rotate(my_tank, 'left')
        if is_available(x - 1, y):
            dx = -1
    if key.char == 'd':
        rotate(my_tank, 'right')
        if is_available(x + 1, y):
            dx = 1
    if key.char == 'w':
        rotate(my_tank, 'up')
        if is_available(x, y - 1):
            dy = -1
    if key.char == 's':
        rotate(my_tank, 'down')
        if is_available(x, y + 1):
            dy = 1
        # обработка нажатий стрелочек на клавиатуре - стрельба
        # коды клавиш работают на Win, на мак используйте 8320768, 8255233, 8189699, 8124162
    if key.keycode == 38:
        rotate(my_tank, 'up')
        bullets.append(get_bullet(x, y, 'up'))
    if key.keycode == 40:
        rotate(my_tank, 'down')
        bullets.append(get_bullet(x, y, 'down'))
    if key.keycode == 39:
        rotate(my_tank, 'right')
        bullets.append(get_bullet(x, y, 'right'))
    if key.keycode == 37:
        rotate(my_tank, 'left')
        bullets.append(get_bullet(x, y, 'left'))
    move(my_tank, dx * block_width, dy * block_height)


def move_tanks():
    for tank in tanks:
        # игнорируем наш танк
        if tank == my_tank:
            continue
        x, y = coords(tank)
        dx = 0
        dy = 0
        # далее спрашиваем танк, что он хочет делать
        action = get_action(tank)
        if action == "go_up":
            rotate(tank, 'up')
            if is_available(x, y - 1):
                dy = -1
        if action == "go_down":
            rotate(tank, 'down')
            if is_available(x, y + 1):
                dy = 1
        if action == "go_left":
            rotate(tank, 'left')
            if is_available(x - 1, y):
                dx = -1
        if action == "go_right":
            rotate(tank, 'right')
            if is_available(x + 1, y):
                dx = 1
        if action == "fire_up":
            rotate(tank, 'up')
            bullets.append(get_bullet(x, y, 'up'))
        if action == "fire_down":
            rotate(tank, 'down')
            bullets.append(get_bullet(x, y, 'down'))
        if action == "fire_left":
            rotate(tank, 'left')
            bullets.append(get_bullet(x, y, 'left'))
        if action == "fire_right":
            rotate(tank, 'right')
            bullets.append(get_bullet(x, y, 'right'))
        move(tank, dx * block_width, dy * block_height)

    # через полсекунды повторяем
    c.after(500, move_tanks)


def get_action(tank):
    return random.choice(['go_up', 'go_down', 'go_left', 'go_right', 'fire_up', 'fire_down', 'fire_left', 'fire_right'])


# добавляем наш танк в общий список
tanks.append(my_tank)
# создаем 5 танков на случайных позициях
for i in range(5):
    x = 0
    y = 0
    while not is_available(x, y):
        x = random.randint(1, 11)
        y = random.randint(1, 11)
    tanks.append(get_tank(x, y, 'up'))
c.after(50, move_bullets)
c.after(1000, move_tanks)

# при нажатии любой клавиши вызываем keyDown
tk.bind("<KeyPress>", keyDown)

mainloop()