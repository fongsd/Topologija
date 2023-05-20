import pygame
import random 
import time
import math
from krug import Krug
from scipy.spatial import Delaunay
import numpy as np
import copy
pygame.init()


#TODO v1.0
#-pocetak i kraj - treba odraditi click eventove GOTOVO
#-triangulacija GOTOVO
#-centroidi GOTOVO
#-triangulacija nad centroidima, pocetkom i krajem GOTOVO 
#-TA*

#-kretanje pesaka po jedinici vremena(iteracija ili po sekundi) GOTOVO
#-pomeranje centroida i trouglova po jedinici vremena GOTOVO
#-TA* po jedinici vremena da radi
#-iscrtavanje puta 

#TODO v1.1 
#-nalazenje preseka izmedju precnika putanje i puta izmedju dva centorida
            #ideja:
                #-za svaki par centroida 
                    #-za svakog pesaka izracunamo razdaljinu izmedju njega i par centroida
                        #- ako je duzina veca ili jednaka od poluprecnika putanje pesaka/jedinici vremena 
                            #-onda moze da se robot krece tim putem
                        #- inace ne sme da se krece
                            #-linija se obiji u crveno
            
            # za sad samo da se linija oboji u crveno ako ima presek sa odredjenim pesakom




screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
screen.fill("black")

putanje = []
pocetne_putanje = []
centroidi = []
pedestrians = []
trenutne_putanje = []
trouglovi = 0
start = (0, 0)
end = (0, 0)

def nacrtaj_krug(krug : Krug, boja):
    pygame.draw.circle(screen, boja, (krug.get_x(), krug.get_y()), 4, 0)

def nacrtaj_putanje(pedestrians : list, color):
    for i in pedestrians:
        dx = int(random.random() * 15)
        # dy = int(random.random() * 10)
        # s = round(random.random()* 2) - 1 
        # k = round(random.random() * 2 ) - 1
        # print(s, k)
        pygame.draw.line(screen, color, (i.get_x(), i.get_y()), 
                         (i.get_x() + dx, i.get_y() + dx), 4)
        putanje.append((i.get_x() + dx, i.get_y() + dx))



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



def kretanje():
    global pedestrians
    global putanje
    for i in range(10):
        screen.fill("black")
        pomeranje_pesaka()
        # triangulacija_temena()
        # pomeranje_centroida()


        putanje = []
        pygame.display.update()
        time.sleep(1)
    screen.fill("black")
    pomeranje_pesaka()
    pygame.display.update()


def pomeranje_pesaka():
    global pedestrians
    global putanje
    stari = copy.deepcopy(pedestrians)
    nacrtaj_putanje(pedestrians, "red")
    for i in range(len(pedestrians)):
            # nacrtaj_krug(pedestrians[i], "black")
            nacrtaj_obim(pedestrians[i], putanje[i][0], putanje[i][1])
            nacrtaj_krug(pedestrians[i], "white")
            # nacrtaj_obim(pedestrians[i], putanje[i][0], putanje[i][1])
    triangulacija_temena()
    for i in range(len(pedestrians)):
            pedestrians[i] = Krug(putanje[i][0], putanje[i][1])
            # pygame.draw.line(screen, "black", (pedestrians[i].get_x(), pedestrians[i].get_y())
                                            #    , (stari[i].get_x(), stari[i].get_y()), 4)
    
def pomeranje_centroida():
    pass


def triangulacija_temena():
    global centroidi
    global pedestrians
    pedestrians_xy = []
    pedestrians_x_coord = []
    pedestrians_y_coord = []
    for i in pedestrians:
        pedestrians_x_coord.append(i.get_x())
        pedestrians_y_coord.append(i.get_y())
    for i in range(len(pedestrians_x_coord)):
        pedestrians_xy.append((pedestrians_x_coord[i], pedestrians_y_coord[i]))
                    
    tri = Delaunay(np.array(pedestrians_xy))
    centroidi = []
    centroidi.append(start)
    centroidi.append(end)
    for trougao in tri.simplices:
        spoji_temena(pedestrians, trougao[0], trougao[1], trougao[2])
        centroid = nadji_centroid(pedestrians, trougao[0], trougao[1], trougao[2])
        centroidi.append(centroid)
    povezi_centroide()

def povezi_centroide():
    global centroidi
    triCentroid = Delaunay(centroidi)
    for i in triCentroid.simplices:
        spoji_centroide(centroidi[i[0]], centroidi[i[1]], centroidi[i[2]])

    for i in centroidi:
        pygame.draw.circle(screen, "blue", i, 7)    
 
def vreme_sudara(a_start_x, a_start_y, b_start_x, b_start_y, vxa , vya, vxb, vyb ): #racunanje po x-u  , analogno po y
    M = np.array([[vxa , vxb ],[vya  , vyb ]])
    cons = np.array([b_start_x - a_start_x, b_start_y - a_start_y])
    result=np.linalg.solve(M,cons)
    ta=round(result[0],2)
    tb=round(result[1],2)
    return (ta, tb) #vracamo vremena za obe tacke tj pesaka
# ne sme t da bude negativno....

def tacka_sudara(t , start_x , start_y, vx , vy): #za racunanje x koordinate tacke sudara
    return (start_x + vx * t    , start_y + vy * t)


def euclid_distance(a,b): #proveriti
    return math.dist(a,b)


def dodaj_susede(tacka,lista): #funkcija za pronalazenje susednih cvorova u grafu kretanja
    susedi=[]
    lista2=np.array(lista)
    d= Delaunay(lista2)
    tmp=[]
    ind=0
    for i,x in enumerate(lista2[d.simplices]):  
        ind=0
        for j,y in enumerate(x):
            
            if  list(y) != tacka:
                tmp.append(list(y))
                
            elif list(y) == tacka:
                ind=1
                
            if ind==1 and j==2:
                [susedi.append(k) for k in tmp if k not in susedi]

        tmp.clear()
        
    return susedi


def h(n):#heuristika udaljenosti od pocetka
    H={} 

    for i in range(len(centroidi)):
        H["{}".format(i)]=random.randint(10,40)

        # H["{}".format(i)]=euclid_distance(list([centroidi[0][0], centroidi[0][1]]),list([pedestrians[i][0],pedestrians[i][1]]))
    return H[n]

def h2(n):#heuristika udaljeniosti od cilja
    H={} 

    for i in range(len(centroidi)):
        H["{}".format(i)]=euclid_distance([centroidi[1][0], centroidi[1][1]],[(pedestrians[i]).get_x(),(pedestrians[i]).get_y()])
    return H[n]


def indeks_suseda(tacka,lista):
    for i,x in enumerate(lista):
        if list(x)==list(tacka):
            return i


def definisi_graf(centroidi):
    G={}
    for i,centroid in enumerate(centroidi):
        susedi=dodaj_susede(list(centroid),centroidi)
        G["{}".format(i)]=[[str(indeks_suseda(j,centroidi)),euclid_distance(list(j),list(centroid))] for j in susedi]

    return G

# G=definisi_graf(points)  <---- points je np.array
# G

def astar(G, start, stop):
    open_list = set([start])
    closed_list = set([])
    
    g = {}      #g - dict 
    g[start] = 0
    
    parents = {}
    parents[start] = None
    
    iteration = 0
    while len(open_list) > 0:
        iteration += 1
        n = None
        for v in open_list:
            if n == None or g[v] + h(v) < g[n] + h(n): 
                n = v
        if n == None:
            print("Ne postoji put!")
            return []
        
        if n == stop:
            print("Postoji put!")
            # print(iteration)
            path = [stop]
            tmp = parents[stop]
            while tmp != None:
                path.append(tmp)
                tmp = parents[tmp]
            path.reverse()
            return path
        
        for m, weight in G[n]:
            if m not in open_list and m not in closed_list:
                open_list.add(m)
                parents[m] = n
                g[m] = g[n] + weight
            else:
                if g[m] > g[n] + weight:
                    g[m] = g[n] + weight
                    parents[m] = n
                    
                    if m in closed_list:
                        closed_list.remove(m)
                        open_list.add(m)
        
        open_list.remove(n)
        closed_list.add(n)

# def napravi_listu_od_krugova(lits_krugova)
def spoji_temena_redom(lista,color="orange"):
    for i in range(len(lista)-1):
         pygame.draw.line(screen, color, (lista[i][0], lista[i][1]),
                      (lista[i+1][0],lista[i+1][1]), 7)        





def __main__():
    global trouglovi
    global putanje
    global centroidi
    nacrtaj_dugme()
    global start, end
    global pedestrians
    br_unosa = 0
    br_linija = 0
    running = True
    astar_indikator=0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # print(br_linija)
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
                        for i in range(6):
                            x_pos = abs(random.random() * screen.get_width() - 200) + 100 # da ne bi bili previse blizu ivici
                            y_pos = abs(random.random() * screen.get_height() - 200) + 100
                            krug = Krug(x_pos, y_pos)
                            nacrtaj_krug(krug, "white")
                            pedestrians.append(krug)
                            dx = random.random() * 10
                            dy = random.random() * 15
                            pocetne_putanje.append((dx, dy))
                        nacrtaj_putanje(pedestrians, "red")
                    elif br_unosa<2:
                        if br_unosa < 1:
                            start = (x, y)
                            br_unosa +=1
                        elif br_unosa == 1:
                            end = (x, y) 
                            br_unosa+=1
                        centroidi.append((x, y))
                        pygame.draw.circle(screen, "purple", (x, y), 10)
                    pygame.display.update()     
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_t:
                    triangulacija_temena()
                    # nacrtaj_putanje(pedestrians, "red")

                # if event.key == pygame.K_v:
                #     nacrtaj_trenutne_putanje(pedestrians, "red")

                if event.key == pygame.K_c:
                        for i in centroidi:
                            # print(i)
                            pygame.draw.circle(screen, "blue", i, 5)
                        # print(len(tri))

                        povezi_centroide()
                            # spoji_temena(centroidi, Krug(centroidi[i[0]]), )

                if event.key == pygame.K_p:
                    astar_indikator=1
                    kretanje() #"live" kretanje 


                if event.key == pygame.K_a and astar_indikator==1:
                    G=definisi_graf(centroidi)
                    s=indeks_suseda(list(start),centroidi)
                    print("Pocetak",s)

                    f=indeks_suseda(list(end),centroidi)
                    print('Kraj',f)

                    l=astar(G,str(s),str(f))

                    lista_indeksa=[int(s) for s in l]
                    print("Lista temena kroz putanje",lista_indeksa)
                    put=[list(centroidi[k]) for k in  lista_indeksa]
                    # print(put)
                    spoji_temena_redom(put,"orange")


                # if event.key == pygame.K_k :
                #     for i in range(len(pedestrians)):
                #         poz_x = pedestrians[i].get_x()
                #         poz_y = pedestrians[i].get_y()
                #         dx = trenutne_putanje[i][0]
                #         dy = trenutne_putanje[i][1]
                #         krug = Krug(poz_x, poz_y)
                #         nacrtaj_obim(krug, dx, dy)

                # if event.key == pygame.K_l:
                #     for i in range(len(pedestrians) - 1):
                #         br_linija+=1
                #         nacrtaj_liniju(pedestrians[i], pedestrians[i + 1]) # ovde se pravi triangulacija tacaka
              
                # if event.key == pygame.K_1:
                #     for i in range(len(pedestrians) - 1):
                #         # sused = int(random.random() * len(pedestrians) - 1)
                #         izmeni_boju(pedestrians[i], pedestrians[i + 1], "yellow")
                #         print("menja se boja linije")
                #         pygame.display.update()
                #         time.sleep(0.02)
                # if event.key == pygame.K_2:
                #     for i in range(20):
                #         # sused = int(random.random() * len(pedestrians) - 1)
                #         izmeni_boju(pedestrians[i], pedestrians[i + 1], "green")
                #         print("menja se boja linije")
                #         pygame.display.update() # need to update screen every time before pause and next drawing 
                #         time.sleep(0.2)
            pygame.display.update()


__main__()