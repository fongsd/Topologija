import pygame
import random 
import time
import math
from krug import Krug
from scipy.spatial import Delaunay
import numpy as np
import copy
pygame.init()


#TODO
#-pocetak i kraj - treba odraditi click eventove GOTOVO
#-triangulacija 
#-centroidi
#-triangulacija nad centroidima, pocetkom i krajem
#-TA*

#-kretanje pesaka po jedinici vremena(iteracija ili po sekundi)
#-TA* po jedinici vremena da radi
#-iscrtavanje puta

screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
screen.fill("white")

putanje = []
trouglovi = 0


def nacrtaj_krug(krug : Krug, boja):
    pygame.draw.circle(screen, boja, (krug.get_x(), krug.get_y()), 4, 0)

def nacrtaj_putanje(pedestrians : list, color):
    for i in pedestrians:
        dx = int(random.random() * 30)
        dy = int(random.random() * 30)
        s = round(random.random()* 2) - 1 
        k = round(random.random() * 2 ) - 1
        # print(s, k)
        pygame.draw.line(screen, color, (i.get_x(), i.get_y()), 
                         (i.get_x() + pow(-1, s) * dx, i.get_y() + pow(-1, k) * dy), 4)
        putanje.append((i.get_x() + pow(-1, s) * dx, i.get_y() + pow(-1, k) * dy))

def nacrtaj_dugme():
    pygame.draw.rect(screen, (250, 0, 0), (10, 10, 60, 40), 0, 2)
    font = pygame.font.Font(size=38)
    number_of_pedestrian = font.render("50", True, (0, 200, 100))
    screen.blit(number_of_pedestrian, (15, 15, 59, 39))

def nacrtaj_liniju(first, second):
    pygame.draw.line(screen, (0, 200, 0), (first.get_x(), first.get_y()),
                      (second.get_x(), second.get_y()), 1)
    

def izmeni_boju(start, end, boja : str):
    pygame.draw.line(screen, boja, (start.get_x(), start.get_y()), (end.get_x(), end.get_y()), width=3)


def nacrtaj_obim(krug : Krug, dx, dy):
    r = math.sqrt((krug.get_x() - dx) * (krug.get_x() - dx) + (krug.get_y() - dy) * (krug.get_y() - dy))
    r+=1
    # print((krug.get_x(), krug.get_y()))
    pygame.draw.circle(screen, "green", (krug.get_x(), krug.get_y()), r, 2)


def spoji_temena(pedestrians, prva, druga, treca):
    pygame.draw.line(screen, "purple", (pedestrians[prva].get_x(), pedestrians[prva].get_y()), (pedestrians[druga].get_x(), pedestrians[druga].get_y()), 1)
    pygame.draw.line(screen, "purple", (pedestrians[druga].get_x(), pedestrians[druga].get_y()), (pedestrians[treca].get_x(), pedestrians[treca].get_y()), 1)
    pygame.draw.line(screen, "purple", (pedestrians[prva].get_x(), pedestrians[prva].get_y()), (pedestrians[treca].get_x(), pedestrians[treca].get_y()), 1)
    global trouglovi
    trouglovi += 1

def spoji_centroide(prvo, drugo, trece):
    pygame.draw.line(screen, "green", (prvo[0], prvo[1]), (drugo[0], drugo[1]), 2)
    pygame.draw.line(screen, "green", (prvo[0], prvo[1]), (trece[0], trece[1]), 2)
    pygame.draw.line(screen, "green", (trece[0], trece[1]), (drugo[0], drugo[1]), 2)


def nadji_centroid(pedestrians, prvo_teme, drugo_teme, trece_teme):
    x_coord = (pedestrians[prvo_teme].get_x() + pedestrians[drugo_teme].get_x() + pedestrians[trece_teme].get_x())/3
    y_coord = (pedestrians[prvo_teme].get_y() + pedestrians[drugo_teme].get_y() + pedestrians[trece_teme].get_y())/3
    return (x_coord, y_coord)

    # global trouglovi
    # print(trouglovi)

def promena_slike():
    for i in range(10):
        stari = copy.deepcopy(pedestrians)
        for i in range(len(pedestrians)):
            nacrtaj_krug(pedestrians[i], "white")
            pedestrians[i] = Krug(putanje[i][0], putanje[i][1])
            pygame.draw.line(screen, "white", (pedestrians[i].get_x(), pedestrians[i].get_y())
                                        , (stari[i].get_x(), stari[i].get_y()), 4)
            nacrtaj_krug(pedestrians[i], "black")
            putanje = []
        nacrtaj_putanje(pedestrians, "red")
        pygame.display.update()
        time.sleep(0.5)

def __main__():
    global trouglovi
    global putanje
    nacrtaj_dugme()

    pedestrians = []
    centroidi = []
    br_unosa = 0
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
                    if x >= 10 and x <= 60 and y >= 10 and y<=40:
                        for i in range(50):
                            x_pos = random.random() * screen.get_width()
                            y_pos = random.random() * screen.get_height()
                            krug = Krug(x_pos, y_pos)
                            nacrtaj_krug(krug, "black")
                            pedestrians.append(krug)
                    else:
                        if br_unosa <= 1:
                            pygame.draw.circle(screen, "green", (x, y), 10)
                            centroidi.append((x, y))
                        br_unosa +=1 
                    pygame.display.update()     
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_t:
                    pedestrians_xy = []
                    pedestrians_x_coord = []
                    pedestrians_y_coord = []
                    for i in pedestrians:
                        pedestrians_x_coord.append(i.get_x())
                        pedestrians_y_coord.append(i.get_y())
                    for i in range(len(pedestrians_x_coord)):
                        pedestrians_xy.append((pedestrians_x_coord[i], pedestrians_y_coord[i]))
                    
                    tri = Delaunay(np.array(pedestrians_xy))
                    for trougao in tri.simplices:
                        spoji_temena(pedestrians, trougao[0], trougao[1], trougao[2])
                        centroid = nadji_centroid(pedestrians, trougao[0], trougao[1], trougao[2])
                        centroidi.append(centroid)

                if event.key == pygame.K_v:
                    nacrtaj_putanje(pedestrians, "red")

                if event.key == pygame.K_c:
                        for i in centroidi:
                            # print(i)
                            pygame.draw.circle(screen, "blue", i, 5)
                        # print(len(tri))

                        triCentroid = Delaunay(centroidi)
                        for i in triCentroid.simplices:
                            spoji_centroide(centroidi[i[0]], centroidi[i[1]], centroidi[i[2]])
                            # spoji_temena(centroidi, Krug(centroidi[i[0]]), )

                if event.key == pygame.K_p:
                    for i in range(10):
                        stari = copy.deepcopy(pedestrians)
                        for i in range(len(pedestrians)):
                            nacrtaj_krug(pedestrians[i], "white")
                            pedestrians[i] = Krug(putanje[i][0], putanje[i][1])
                            pygame.draw.line(screen, "white", (pedestrians[i].get_x(), pedestrians[i].get_y())
                                                               , (stari[i].get_x(), stari[i].get_y()), 4)
                            nacrtaj_krug(pedestrians[i], "black")
                        putanje = []
                        nacrtaj_putanje(pedestrians, "red")
                        pygame.display.update()
                        time.sleep(0.5)

                if event.key == pygame.K_k :
                    for i in range(len(pedestrians)):
                        poz_x = pedestrians[i].get_x()
                        poz_y = pedestrians[i].get_y()
                        dx = putanje[i][0]
                        dy = putanje[i][1]
                        krug = Krug(poz_x, poz_y)
                        nacrtaj_obim(krug, dx, dy)

                if event.key == pygame.K_l:
                    for i in range(len(pedestrians) - 1):
                        br_linija+=1
                        nacrtaj_liniju(pedestrians[i], pedestrians[i + 1]) # ovde se pravi triangulacija tacaka
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


__main__()