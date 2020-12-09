from math import *
import matplotlib.pyplot as plt

PI = 3.1415926535

WIDTH = 500 # Ширина призмы
HEIGHT = 500 # Высота призмы
NUM_CELL_X = 1000 # Количество отрезков, на которые мы делим ось x
NUM_CELL_Y = 1000 # Количество отрезков, на которые мы делим ось y
dX = WIDTH / NUM_CELL_X # Длина 1 отрезка по оси х
dY = HEIGHT / NUM_CELL_Y # Длина 1 отрезка по оси y

ANGLE_STEPS = 360

def f(sin_alpha, x, y, n1, vertical, reverse, reflection, n):
    # vertical содержит данные об ориентации границы, на которой происходит преломление
    # vertical = True, если граница ориентирована вертикально (параллельно х)
    # vertical = False, если граница ориентирована горизонтально (параллельно y)
    if vertical:
        if reflection: n2 = n1
        else: n2 = n(x + (-1 if reverse else 1) * dX / 2, dY * (floor(y / dY) + 0.5))

        # Закон Снеллиуса:
        sin_beta = n1 * sin_alpha / n2
        # Проверка на полное внутреннее отражение:
        if abs(sin_beta) > 1:
            return sin_alpha, x, y, n1, vertical, not reverse, True

        hypotenuse = sqrt(pow(dX, 2) + pow(floor(y / dY) * dY - y, 2))
        if sin((y - floor(y / dY) * dY) / hypotenuse) >= sin_beta:
            x_new = x + (-1 if reverse else 1) * dX
            y_new = y - dX * tan(asin(sin_beta))
            return sin_beta, x_new, y_new, n2, True, reverse, False
        else:
            x_new = x + (-1 if reverse else 1) * (y - dY * floor(y / dY)) / tan(asin(sin_beta))
            y_new = dY * floor(y / dY)
            return cos(asin(sin_beta)), x_new, y_new, n2, False, reverse, False
    else:
        if reflection: n2 = n1
        else: n2 = n((floor(x / dX) + 0.5) * dX, y - dY / 2)

        # Закон Снеллиуса:
        sin_beta = n1 * sin_alpha / n2
        # Проверка на полное внутреннее отражение:
        if abs(sin_beta) > 1:
            return -sin_alpha, x, y, n1, vertical, not reverse, True

        hypotenuse = sqrt(pow(dY, 2) + pow(dX * (floor(x / dX) + (0 if reverse else 1)) - x, 2))
        if (-1 if reverse else 1) * sin((dX * (floor(x / dX) + (0 if reverse else 1)) - x) / hypotenuse) >= sin_beta:
            x_new = x + (-1 if reverse else 1) * dY * tan(asin(sin_beta))
            y_new = y - dY / 2
            return sin_beta, x_new, y_new, n2, False, reverse, False
        else:
           x_new = dX * (floor(x / dX) + (0 if reverse else 1))
           y_new = y - (-1 if reverse else 1) * (dX * (floor(x / dX) + (0 if reverse else 1)) - x) / tan(asin(sin_beta))
           return cos(asin(sin_beta)), x_new, y_new, n2, True, reverse, False


def drawing_plot(data):
    fig, axs = plt.subplots()
    axs.scatter(list(data.keys()), list(data.values()))
    axs.grid()
    plt.ylabel('Вычисляемый угол')
    fig.suptitle('Зависимость вычисляемого угла от фазы.')
    plt.show()


def angle_calc(n, y0, y_end, precision = 2, draw_plot = False):
    x0, x_end = 0, WIDTH
    data_for_drawing = {}
    results = [ [] for _ in range(precision)]
    mins = 0, HEIGHT, []
    sin_end = 0
    for p in range(precision):
        print("===============")
        print("PHASE", p)

        for i in range(1 - int(ANGLE_STEPS / 2),  int(ANGLE_STEPS / 2)):
            angle = (PI * i / (pow(10, p) * ANGLE_STEPS)) + asin(sin_end)

            sin_alpha, x, y, n1, vertical, reverse, reflection = sin(angle), x0, y0, 1, True, False, False
            points = []

            while 0 <= x <= WIDTH and 0 <= y <= HEIGHT:
                points.append((x + 50, y + 50))
                sin_alpha, x, y, n1, vertical, reverse, reflection = f(sin_alpha, x, y, n1, vertical, reverse, reflection, n)

            if x >= WIDTH: x = WIDTH
            points.append((x + 50, y + 50))
            results[p].append(points)

            # Выбираем угол, при к-ом конечные полученная и заданная точки наиболее близки: 
            if x >= WIDTH and abs(y - y_end) < mins[1]:
                mins = sin(angle), abs(y - y_end), points
            
            if (i % 10) == 0: print(int(100 * (i / ANGLE_STEPS + 0.5)), "%")
        
        if mins[1] == HEIGHT: return results, False, 0, 0
        
        sin_end = mins[0]
        data_for_drawing['phase ' + str(p)] = 180 * asin(sin_end) / PI

        # Увеличиваем точность разбиения для следующей фазы:
        global dX
        global dY
        dX /= 2
        dY /= 2

    if (mins[2][-1][0] - 50 >= WIDTH and abs(mins[2][-1][1] - 50 - y_end) <= 1):
        if draw_plot:
            drawing_plot(data_for_drawing)
        return results, True, asin(sin_end), mins[2]
    else:
        return results, False, 0, 0



