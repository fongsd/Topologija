import pygame
import random 
from scipy.spatial import Delaunay
import numpy as np
import matplotlib.pyplot as plt
import copy
from krug import Krug

#TODO
#pocetak i kraj
#triangulacija
#centroidi
#triangulacija nad centroidima, pocetkom i krajem
#TA*

#kretanje pesaka po jedinici vremena(itearacije ili po sekundi)
#ta po jedinici vremena 
#iscrtavanje puta


pygame.init()

screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)


def nacrtaj_krug(krug : Krug):
    pygame.draw.circle(screen, (255, 20, 20), (krug.get_x(), krug.get_y()), 4, 0)


def nacrtaj_dugme():
    pygame.draw.rect(screen, (250, 0, 0), (10, 10, 60, 40), 0, 2)
    font = pygame.font.Font(size=38)
    number_of_pedestrian = font.render("500", True, (0, 200, 100))
    screen.blit(number_of_pedestrian, (15, 15, 59, 39))

def nacrtaj_tacke(lista):
    for i in range(len(lista)):
        pygame.draw.circle(screen, (100,100,100), (lista[i][0],lista[i][1]), 6, 0)

def nacrtaj_liniju(first, second):
    pygame.draw.line(screen, (0, 200, 0), (first.get_x(), first.get_y()),
                      (second.get_x(), second.get_y()), 1)


def nacrtaj_liniju_lista(first, second,boja):
    color=(0,200,0)
    if boja=="zelena":
        color=(0,200,0)
    elif boja=="plava":
        color=(0,0,255)

    pygame.draw.line(screen, color, (first[0], first[1]),
                      (second[0], second[1]), 1)

def dodaj_pocetak_i_cilj(x,y,ind):

    if ind==0:
        pygame.draw.circle(screen, (255, 255, 255), (x , y), 6, 0)

    if ind==1:
        pygame.draw.circle(screen, (200, 150, 0), (x, y), 6, 0)
        pygame.draw.circle(screen, (0, 0, 255), (x ,y ), 6, 0)

def spoji_delauney(lista,boja):
    for i in range(len(lista)-1):
        if i == (len(lista)-2):
            nacrtaj_liniju_lista(lista[i+1],lista[0],boja)
        nacrtaj_liniju_lista(lista[i],lista[i+1],boja)
        


def centri_trouglova(points,lista):

    ax = float((points[lista[0]])[0])
    ay = float((points[lista[0]])[1])
    
    bx = float((points[lista[1]])[0])
    by = float((points[lista[1]])[1])
    
    cx = float((points[lista[2]])[0])
    cy = float((points[lista[2]])[1])
   
    ux = (ax + bx + cx) / 3.0
    uy = (ay + by + cy) / 3.0
    return [ux,uy]
    

def __main__():

    nacrtaj_dugme()

    pedestrians = []
    list_of_all_points=[]
    circumcenters=[]
    ind=0

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
                    for i in range(50):
                        x_pos = random.random() * screen.get_width()
                        y_pos = random.random() * screen.get_height()
                        krug = Krug(x_pos, y_pos)
                        # nacrtaj_krug(krug)
                        pedestrians.append([x_pos,y_pos])
                else: 
                    dodaj_pocetak_i_cilj(x,y,ind)
                    circumcenters.append([x,y])
                    ind+=1
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    nacrtaj_tacke(pedestrians)

                if event.key==pygame.K_z:
                    pesaci=np.array(pedestrians)

                    tri = Delaunay(pesaci)
                    list_of_all_points = copy.deepcopy(pedestrians)
                    for i in range(len(tri.simplices)):
                        list_of_all_points.append(centri_trouglova(pedestrians,tri.simplices[i]))
                        circumcenters.append(centri_trouglova(pedestrians, tri.simplices[i]))

                    for i in range(len(tri.simplices)):
                        spoji_delauney(pesaci[tri.simplices[i]],"zelena")
                
                if event.key == pygame.K_b:

                    nacrtaj_tacke(circumcenters)
                    array_of_circumcenters=np.array(circumcenters)
                    tri2 = Delaunay(array_of_circumcenters)
                    for i in range(len(tri2.simplices)):
                        spoji_delauney(array_of_circumcenters[tri2.simplices[i]],"plava")
        
        pygame.display.update()

    pygame.quit()


__main__()