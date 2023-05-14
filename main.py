import pygame
import random 
import time
from krug import Krug
pygame.init()

screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)


def nacrtaj_krug(krug : Krug):
    pygame.draw.circle(screen, (255, 20, 20), (krug.get_x(), krug.get_y()), 7, 0)


def nacrtaj_dugme():
    pygame.draw.rect(screen, (250, 0, 0), (10, 10, 60, 40), 0, 2)
    font = pygame.font.Font(size=38)
    number_of_pedestrian = font.render("500", True, (0, 200, 100))
    screen.blit(number_of_pedestrian, (15, 15, 59, 39))

def nacrtaj_liniju(first, second):
    pygame.draw.line(screen, (0, 200, 0), (first.get_x(), first.get_y()),
                      (second.get_x(), second.get_y()), 1)
    

def izmeni_boju(start, end, boja : str):
    pygame.draw.line(screen, boja, (start.get_x(), start.get_y()), (end.get_x(), end.get_y()), width=3)

# def __main__():

nacrtaj_dugme()

pedestrians = []
br_linija = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            print(br_linija)
            print(len(pedestrians))
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                screen.fill((100, 100, 100))
        if pygame.MOUSEBUTTONDOWN == event.type:
            if pygame.mouse.get_pressed()[0] == True:
                x, y = pygame.mouse.get_pos()
                x = int(x)
                y = int(y)
                if x >= 10 and x <= 60 and y >= 10 and y<=40:
                    for i in range(500):
                        x_pos = random.random() * screen.get_width()
                        y_pos = random.random() * screen.get_height()
                        krug = Krug(x_pos, y_pos)
                        nacrtaj_krug(krug)
                        pedestrians.append(krug)
                pygame.display.update()     
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                for i in range(len(pedestrians) - 1):
                    br_linija+=1
                    nacrtaj_liniju(pedestrians[i], pedestrians[i + 1])
            if event.key == pygame.K_1:
                for i in range(len(pedestrians) - 1):
                    # sused = int(random.random() * len(pedestrians) - 1)
                    izmeni_boju(pedestrians[i], pedestrians[i + 1], "yellow")
                    print("menja se boja linije")
                    pygame.display.update()
                    time.sleep(0.02)
            if event.key == pygame.K_2:
                for i in range(20):
                    # sused = int(random.random() * len(pedestrians) - 1)
                    izmeni_boju(pedestrians[i], pedestrians[i + 1], "green")
                    print("menja se boja linije")
                    pygame.display.update() # need to update screen every time before pause and next drawing 
                    time.sleep(0.2)
        pygame.display.update()


