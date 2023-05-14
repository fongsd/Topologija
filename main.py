import pygame
import random 
from krug import Krug

pygame.init()

screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)


def nacrtaj_krug(krug : Krug):
    pygame.draw.circle(screen, (255, 20, 20), (krug.get_x(), krug.get_y()), 4, 0)


def nacrtaj_dugme():
    pygame.draw.rect(screen, (250, 0, 0), (10, 10, 60, 40), 0, 2)
    font = pygame.font.Font(size=38)
    number_of_pedestrian = font.render("500", True, (0, 200, 100))
    screen.blit(number_of_pedestrian, (15, 15, 59, 39))

def nacrtaj_liniju(first, second):
    pygame.draw.line(screen, (0, 200, 0), (first.get_x(), first.get_y()),
                      (second.get_x(), second.get_y()), 1)
    


def __main__():

    nacrtaj_dugme()

    pedestrians = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    screen.fill((100, 100, 100))
            if pygame.mouse.get_pressed()[0] == True:
                x, y = pygame.mouse.get_pos()
                x = int(x)
                y = int(y)
                if x >= 10 and x <= 60 and y >= 10 and y<=40:
                    for i in range(100):
                        x_pos = random.random() * screen.get_width()
                        y_pos = random.random() * screen.get_height()
                        krug = Krug(x_pos, y_pos)
                        nacrtaj_krug(krug)
                        pedestrians.append(krug)
                    for i in range(len(pedestrians) - 1):
                        nacrtaj_liniju(pedestrians[i], pedestrians[i + 1])
        pygame.display.update()



__main__()