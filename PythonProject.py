import pygame
pygame.init()
from math import *


PI = 3.1415926535

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 191, 255)
BLACK = (0, 0, 0)

WIDTH = 500 # Ширина призмы
HEIGHT = 500 # Высота призмы
NUM_CELL_X = 1000 # Количество отрезков, на которые мы делим ось x
NUM_CELL_Y = 1000 # Количество отрезков, на которые мы делим ось y
dX = WIDTH / NUM_CELL_X # Длина 1 отрезка по оси х
dY = HEIGHT / NUM_CELL_Y # Длина 1 отрезка по оси y

ANGLE_STEPS = 540

# Функция распределения показателя преломления в призме:
def n(x, y):
    return 1 + x / 500

def f(sin_alpha, x, y, n1, vertical, reverse, reflection):
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
            return sin_alpha, x ,y, n1, vertical, not reverse, True

        hypotenuse = sqrt(dX ** 2 + (floor(y / dY) * dY - y) ** 2)
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

        hypotenuse = sqrt(dY ** 2 + (dX * (floor(x / dX) + (0 if reverse else 1)) - x) ** 2)
        if (-1 if reverse else 1) * sin((dX * (floor(x / dX) + (0 if reverse else 1)) - x) / hypotenuse) >= sin_beta:
            x_new = x + (-1 if reverse else 1) * dY * tan(asin(sin_beta))
            y_new = y - dY / 2
            return sin_beta, x_new, y_new, n2, False, reverse, False
        else:
           x_new = dX * (floor(x / dX) + (0 if reverse else 1))
           y_new = y - (-1 if reverse else 1) * (dX * (floor(x / dX) + (0 if reverse else 1)) - x) / tan(asin(sin_beta))
           return cos(asin(sin_beta)), x_new, y_new, n2, True, reverse, False
    

print("Введите y-координату начальной точки от 0 до {}: ".format(HEIGHT), end='')
y0 = float(input())
x0 = 0
print("Введите y-координату конечной точки от 0 до {}: ".format(HEIGHT), end='')
y_end = float(input())
x_end = WIDTH

results = []
sin_end = 2
for angle in range(1 - int(ANGLE_STEPS / 2),  int(ANGLE_STEPS / 2)):
    sin_alpha = sin(PI * angle / ANGLE_STEPS)
    x, y, n1, vertical, reverse, reflection = x0, y0, 1, True, False, False
    points = []
    while x >= 0 and x <= WIDTH and y >= 0 and y <= HEIGHT:
        points.append((x + 50, y + 50))
        sin_alpha, x, y, n1, vertical, reverse, reflection = f(sin_alpha, x, y, n1, vertical, reverse, reflection)
    if x >= WIDTH: x = WIDTH
    points.append((x + 50, y + 50))

    if abs(y - y_end) <= 1 and x >= WIDTH:
        sin_end = sin_alpha
        plot_end = points
    results.append(points)

    if (angle % 10) == 0: print(int(100 * (angle / ANGLE_STEPS + 0.5)), "%")

sc = pygame.display.set_mode((WIDTH + 100, HEIGHT + 100))
pygame.display.set_caption("Направленная дальняя связь")
running = True
while running:
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    sc.fill(WHITE)
    pygame.draw.rect(sc, BLUE, (50, 50, WIDTH, HEIGHT))

    for i in results[::10]:
        pygame.draw.lines(sc, RED, False, i)

    font = pygame.font.Font(None, 25)
    if sin_end != 2:
        pygame.draw.lines(sc, BLACK, False, plot_end, 3)
        text = font.render("Необходимый угол падения: %.3f" %(180 * asin(sin_end) / PI), True, BLACK)
    else:
        text = font.render("Нет решений :(", True, BLACK)
    sc.blit(text, (50 , 25))

    pygame.display.update()