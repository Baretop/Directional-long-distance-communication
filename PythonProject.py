import pygame
pygame.init()
from solver import *

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 191, 255)
BLACK = (0, 0, 0)

# Функция распределения показателя преломления в призме:
def n(x, y):
    return 1 + x / 500

print("Введите y-координату начальной точки от 0 до {}: ".format(HEIGHT), end='')
y0 = float(input())
print("Введите y-координату конечной точки от 0 до {}: ".format(HEIGHT), end='')
y_end = float(input())

# Cтепень точности вычисления:
precision = 3
# Выводим зависимость искомого угла от фазы:
draw_plot = True 
# Вызываем функцию angle_calc из модуля solver
results, success, angle, plot_end = angle_calc(n, y0, y_end, precision, draw_plot)

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

    # С помощью results[p] можно получить траектории всех лучей на p фазе: 
    for i in results[0][::5]:
        pygame.draw.lines(sc, RED, False, i)

    font = pygame.font.Font(None, 25)
    if success:
        pygame.draw.lines(sc, BLACK, False, plot_end, 3)
        text = font.render("Необходимый угол падения: %.4f" %(180 * angle / PI), True, BLACK)
    else:
        text = font.render("Нет решений :(", True, BLACK)
    sc.blit(text, (50 , 25))

    pygame.display.update()