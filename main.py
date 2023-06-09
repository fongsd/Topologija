import json
import pygame
import random 
import time
import math
from krug import Krug
from scipy.spatial import Delaunay
import numpy as np
import copy
from matplotlib import pyplot as plt
from PIL import Image
import glob
import os


pygame.init()

mapa_temena={}

screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
screen.fill("black")
# nedozvoljeni_putevi=[]
parensts_astar={}
G={}
astar_G = {}
putanje = []
pocetne_putanje = []
centroidi = []
pedestrians = []
# trenutne_putanje = []
# trouglovi = 0
astar_pocetne_putanje = []
astar_pesaci = []
astar_centroidi = []
start = (0, 0)
start_indeks='0'
end = (300, 300)
end_indeks='1'
# velocity = 0

# indikator_inicijalizacije=0
# dx=[]
# dy=[]

def ucitaj_pesake():
    file_path = open("podaci.json", "r")
    podaci = json.load(file_path)
    return podaci


def nacrtaj_krug(krug : Krug, boja):
    pygame.draw.circle(screen, boja, (krug.get_x(), krug.get_y()), 4, 0)

def nacrtaj_putanje(pedestrians : list, color):
    global pocetne_putanje
    brzine_pesaka = []
    for poz, i in enumerate(pedestrians):
        pygame.draw.line(screen, color, (i.get_x(), i.get_y()), 
                         (i.get_x() + 10 * pocetne_putanje[poz][0], i.get_y() +  10 * pocetne_putanje[poz][1]), 4)
        putanje.append((i.get_x() + 10 * pocetne_putanje[poz][0], i.get_y() + 10 * pocetne_putanje[poz][1]))
        brzine_pesaka.append(((i.get_x(), i.get_y()),(10 * pocetne_putanje[poz][0], 10 * pocetne_putanje[poz][1]))) # lista parova (pozicija pesaka, njegova brzina)

    return brzine_pesaka

def nacrtaj_dugme():
    pygame.draw.rect(screen, (250, 0, 0), (10, 10, 80, 40), 0, 2)
    font = pygame.font.Font(size=27)
    pocetak = font.render("START", True, (0, 200, 100))
    screen.blit(pocetak, (15, 15, 80, 39))

def nacrtaj_liniju(first, second):
    pygame.draw.line(screen, (0, 200, 0), (first.get_x(), first.get_y()),
                      (second.get_x(), second.get_y()), 1)

def nacrtaj_obim(krug : Krug, dx, dy):
    r = math.sqrt((krug.get_x() - dx) * (krug.get_x() - dx) + (krug.get_y() - dy) * (krug.get_y() - dy))
    r+=1
    pygame.draw.circle(screen, "green", (krug.get_x(), krug.get_y()), r, 2)

def spoji_temena(pedestrians, prva, druga, treca):
    pygame.draw.line(screen, "purple", (pedestrians[prva].get_x(), pedestrians[prva].get_y()), (pedestrians[druga].get_x(), pedestrians[druga].get_y()), 1)
    pygame.draw.line(screen, "purple", (pedestrians[druga].get_x(), pedestrians[druga].get_y()), (pedestrians[treca].get_x(), pedestrians[treca].get_y()), 1)
    pygame.draw.line(screen, "purple", (pedestrians[prva].get_x(), pedestrians[prva].get_y()), (pedestrians[treca].get_x(), pedestrians[treca].get_y()), 1)

def spoji_centroide(prvo, drugo, trece):
    pygame.draw.line(screen, "green", (prvo[0], prvo[1]), (drugo[0], drugo[1]), 2)
    pygame.draw.line(screen, "green", (prvo[0], prvo[1]), (trece[0], trece[1]), 2)
    pygame.draw.line(screen, "green", (trece[0], trece[1]), (drugo[0], drugo[1]), 2)

    return [prvo, drugo, trece]

def brzine_centroida(prvo_teme, drugo_teme):
    vx_first = prvo_teme[0]
    vy_first = prvo_teme[1]
    vx_second = drugo_teme[0]
    vy_second = drugo_teme[1]

    return math.dist(prvo_teme, drugo_teme)

def nadji_centroid(pedestrians, prvo_teme, drugo_teme, trece_teme):
    x_coord = (pedestrians[prvo_teme].get_x() + pedestrians[drugo_teme].get_x() + pedestrians[trece_teme].get_x())/3
    y_coord = (pedestrians[prvo_teme].get_y() + pedestrians[drugo_teme].get_y() + pedestrians[trece_teme].get_y())/3
    return (x_coord, y_coord)

def indeks_najblizeg_centroida(c,centroidi):
    distance=float('inf')
    indeks=0
    for i,centroid in enumerate(centroidi):
        dist=euclid_distance(list(c),list(centroid))
        if dist<distance:
            distance=dist
            indeks=i
    
    return indeks

def kretanje():
    global pedestrians
    global centroidi
    global putanje
    global G
    global start_indeks,end_indeks
  
    tmp=[]
    l=[]
    lista_koordinata=[]
    pomocni=copy.deepcopy(centroidi[int(start_indeks)])
    lista_koordinata.append(list(pomocni))
    c_tmp=[]
    indeks=0
    for i in range(15):
        screen.fill("black")
        G.clear()
        # time.sleep(2)
        G=definisi_graf(centroidi)

        start_indeks=indeks_suseda(list(start),centroidi)
        end_indeks=indeks_suseda(list(end),centroidi)
        
        print("START I END:",start_indeks,end_indeks)
        
        if i==0:
            tmp = astar(G,centroidi[start_indeks],centroidi[end_indeks])
            if tmp != None:
                if len(tmp)==2:
                    c_tmp=copy.deepcopy(list(tmp[1]))
                else:
                    c_tmp=copy.deepcopy(list(tmp[0]))


        else:
            indeks=indeks_najblizeg_centroida(c_tmp,centroidi)
            tmp = astar(G,centroidi[indeks],centroidi[end_indeks])
            if len(tmp)==2:
                c_tmp=copy.deepcopy(list(tmp[1]))
            else:
                c_tmp=copy.deepcopy(list(tmp[0]))

        if len(tmp)==1:
            break

        elif len(tmp)==0:
            l=[]
            break

        elif len(tmp)>1:
            if tmp not in l:
                lista_koordinata.append(list(c_tmp))
                l.append(tmp)
                

        pomeranje_pesaka()
        putanje = []
        
        for i in range(len(lista_koordinata)-1):
            pygame.draw.line(screen,"white", (lista_koordinata[i][0], lista_koordinata[i][1]),
                          (lista_koordinata[i+1][0],lista_koordinata[i+1][1]), 10)
            pygame.draw.circle(screen, "red", lista_koordinata[i], 7) 
            # time.sleep(0.2) 

        pygame.image.save(screen, f"kretanje{i}.png")


        pygame.display.update()
        # time.sleep(0.2)    

        # print(l) 
        # print("Lista koordinata",lista_koordinata)

    screen.fill('black')
    pomeranje_pesaka()

    for i in range(len(lista_koordinata)-1):
        pygame.draw.line(screen,"pink", (lista_koordinata[i][0], lista_koordinata[i][1]),
                      (lista_koordinata[i+1][0],lista_koordinata[i+1][1]), 6)
        pygame.draw.circle(screen, "red", lista_koordinata[i], 7) 
        # time.sleep(0.2) 

    pygame.image.save(screen, f"kretanje{i+1}.png")

    return lista_koordinata



def pomeranje_pesaka():

    global centroidi
    global pedestrians
    global putanje
    global velocity
    stari = copy.deepcopy(pedestrians)
    brzine_pesaka = nacrtaj_putanje(pedestrians, "red") # uredjen par (trenutna pozicija pesaka, brzina == sledeca pozicija)
    for i in range(len(pedestrians)):
            nacrtaj_obim(pedestrians[i], putanje[i][0], putanje[i][1])
            nacrtaj_krug(pedestrians[i], "white")
    susedni_centroidi = triangulacija_temena() # lista listi susednih temena
    for i in range(len(pedestrians)):
            pedestrians[i] = Krug(putanje[i][0], putanje[i][1])

    # print("Centroids length pomeranje_pesaka:",len(centroidi))

def provera_grane(fst,scnd):
    global centroidi
    global pedestrians
    global putanje
    global velocity

    nedozvoljene_putanja=[]            

    brzine_pesaka = nacrtaj_putanje(pedestrians, "red") # uredjen par (trenutna pozicija pesaka, brzina == sledeca pozicija)

    susedni_centroidi = triangulacija_temena() # lista listi susednih temena


    for i in susedni_centroidi: # susedna temena

        first = i[0] # prvo teme
        second = i[1] # drugo teme
        third = i[2] # trece teme

        #lista temena trougla
        lista=[list(first),list(second), list(third)]
        
        fst1=list(fst)
        scnd1=list(scnd)

        #ako 2 tacke koje obrazuju deo putanje su zapravo temena trougla
        if (fst1 in lista) and (scnd1 in lista):                

            for (trenutna_pozicija, putanja) in brzine_pesaka:
                vektor_v = (second[0] - first[0], second[1] - first[1])
                vektor_u = (trenutna_pozicija[0] - first[0], trenutna_pozicija[1] - first[1])
                sledeca_pozicija_pesaka = (trenutna_pozicija[0] + putanja[0], trenutna_pozicija[1] + putanja[1])
                vektor_W = (sledeca_pozicija_pesaka[0] - first[0], sledeca_pozicija_pesaka[1] - first[1])



                if angle(first, second, trenutna_pozicija):
                    if orijentacija(vektor_v, vektor_u) != orijentacija(vektor_v, vektor_W) :
                        pygame.draw.line(screen, "red", first, second, 5)
                        if (list(first),list(second)) not in nedozvoljene_putanja:
                            nedozvoljene_putanja.append((list(first),list(second)))
                        nacrtaj_krug(Krug(trenutna_pozicija[0], trenutna_pozicija[1]), "red")
                        nacrtaj_krug(Krug(sledeca_pozicija_pesaka[0], sledeca_pozicija_pesaka[1]), "red")
                        pygame.display.update()
                        # time.sleep(0.2)



                vektor_v = (third[0] - first[0], third[1] - first[1])
                vektor_u = (trenutna_pozicija[0] - first[0], trenutna_pozicija[1] - first[1])
                sledeca_pozicija_pesaka = (trenutna_pozicija[0] + putanja[0], trenutna_pozicija[1] + putanja[1])
                vektor_W = (sledeca_pozicija_pesaka[0] - first[0], sledeca_pozicija_pesaka[1] - first[1])


                if angle(first, third, trenutna_pozicija):
                    if orijentacija(vektor_v, vektor_u) != orijentacija(vektor_v, vektor_W) :
                        pygame.draw.line(screen, "red", first, third, 5)
                        
                        if (list(first),list(third)) not in nedozvoljene_putanja:
                            nedozvoljene_putanja.append((list(first),list(third)))
                        
                        nacrtaj_krug(Krug(trenutna_pozicija[0], trenutna_pozicija[1]), "red")
                        nacrtaj_krug(Krug(sledeca_pozicija_pesaka[0], sledeca_pozicija_pesaka[1]), "red")
                        pygame.display.update()
                        # time.sleep(0.2)

                vektor_v = (third[0] - second[0], third[1] - second[1])
                vektor_u = (trenutna_pozicija[0] - second[0], trenutna_pozicija[1] - second[1])
                sledeca_pozicija_pesaka = (trenutna_pozicija[0] + putanja[0], trenutna_pozicija[1] + putanja[1])
                vektor_W = (sledeca_pozicija_pesaka[0] - second[0], sledeca_pozicija_pesaka[1] - second[1])

                if angle(second, third, trenutna_pozicija):
                    if orijentacija(vektor_v, vektor_u) != orijentacija(vektor_v, vektor_W) :
                        pygame.draw.line(screen, "red", third, second, 5)
                        
                        if (list(second),list(third)) not in nedozvoljene_putanja:
                            nedozvoljene_putanja.append((list(second),list(third)))

                        nacrtaj_krug(Krug(trenutna_pozicija[0], trenutna_pozicija[1]), "red")
                        nacrtaj_krug(Krug(sledeca_pozicija_pesaka[0], sledeca_pozicija_pesaka[1]), "red")
                        pygame.display.update()
                        # time.sleep(0.2)

    return nedozvoljene_putanja

def angle(first, second, third): # two end points and pedestrian point
    vektor_u = (second[0] - first[0], second[1] - first[1])
    vektor_v = (third[0] - first[0], third[1] - first[1])
    vektor_w = (second[0] - third[0], second[1] - third[1])

    a1 = vektor_u[0] * vektor_v[0] + vektor_u[1] * vektor_v[1]
    b1 = math.sqrt(vektor_u[0] * vektor_u[0] + vektor_u[1] * vektor_u[1]) * math.sqrt(vektor_v[0] * vektor_v[0] + vektor_v[1] * vektor_v[1])

    degree1 = math.degrees(math.acos(a1/b1))


    a2 = vektor_u[0] * vektor_w[0] + vektor_u[1] * vektor_w[1]
    b2 = math.sqrt(vektor_u[0] * vektor_u[0] + vektor_u[1] * vektor_u[1]) * math.sqrt(vektor_w[0] * vektor_w[0] + vektor_w[1] * vektor_w[1])

    degree2 = math.degrees(math.acos(a2/b2))

    # print(degree1, degree2)
    return degree1 <= 90 and degree2 <= 90


def triangulacija_temena():
    global centroidi
    global astar_centroidi
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
    # mapa_temena = {}
    mapa_temena.clear()
    mapa_temena[start]=sorted(pedestrians_xy)

    mapa_temena[end]=sorted(pedestrians_xy, reverse=True)

    for trougao in tri.simplices:
        spoji_temena(pedestrians, trougao[0], trougao[1], trougao[2])
        centroid = nadji_centroid(pedestrians, trougao[0], trougao[1], trougao[2])
        centroidi.append(centroid)
        mapa_temena[centroid]=[pedestrians_xy[trougao[0]],
                               pedestrians_xy[trougao[1]],
                               pedestrians_xy[trougao[2]]]

    for centroid in centroidi:
        font = pygame.font.Font(size=30)
        koordinate_centroida = font.render(str(np.round(centroid)), True, (255, 215, 0))
        screen.blit(koordinate_centroida, (centroid[0]-20,centroid[1]-20,centroid[0]+20,centroid[1]+20))
    return povezi_centroide()

def astar_povezi_centroide():
    lista_susednih_temena_triangulacije = []
    global astar_centroidi
    triCentroid = Delaunay(astar_centroidi)
    for i in triCentroid.simplices:
        tmp_lista =  spoji_centroide(astar_centroidi[i[0]], astar_centroidi[i[1]], astar_centroidi[i[2]]) # fja vraca [prva, druga, treca]
        lista_susednih_temena_triangulacije.append(tmp_lista) # lista susednih temena centroida

    for i in astar_centroidi:
        pygame.draw.circle(screen, "blue", i, 7)    
    return lista_susednih_temena_triangulacije

def astar_triangulacija_temena():
    global astar_centroidi
    global astar_pesaci
    pedestrians_xy = []
    pedestrians_x_coord = []
    pedestrians_y_coord = []

    for i in astar_pesaci:
        pedestrians_x_coord.append(i.get_x())
        pedestrians_y_coord.append(i.get_y())
    for i in range(len(pedestrians_x_coord)):
        pedestrians_xy.append((pedestrians_x_coord[i], pedestrians_y_coord[i]))
                
    tri = Delaunay(np.array(pedestrians_xy))

    astar_centroidi = []
    astar_centroidi.append(start)
    astar_centroidi.append(end)

    mapa_temena.clear()

    mapa_temena[start]=sorted(pedestrians_xy)

    mapa_temena[end]=sorted(pedestrians_xy, reverse=True)

    for trougao in tri.simplices:

        centroid = nadji_centroid(astar_pesaci, trougao[0], trougao[1], trougao[2])
        astar_centroidi.append(centroid)
        mapa_temena[centroid]=[pedestrians_xy[trougao[0]],
                               pedestrians_xy[trougao[1]],
                               pedestrians_xy[trougao[2]]]
        
    return astar_povezi_centroide()

def povezi_centroide():
    lista_susednih_temena_triangulacije = []
    global centroidi
    triCentroid = Delaunay(centroidi)
    for i in triCentroid.simplices:
        tmp_lista =  spoji_centroide(centroidi[i[0]], centroidi[i[1]], centroidi[i[2]]) # fja vraca [prva, druga, treca]
        lista_susednih_temena_triangulacije.append(tmp_lista) # lista susednih temena centroida

    for i in centroidi:
        pygame.draw.circle(screen, "blue", i, 7)    
    return lista_susednih_temena_triangulacije
 
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

#funkcija za pronalazenje susednih cvorova u grafu kretanja
def dodaj_susede(tacka,lista): 
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

            
def h(n):#heuristika - udaljenost od cilja
    H={}
    global centroidi
    for i,centroid in enumerate(centroidi):
        najblizi_centroid=centroidi[indeks_najblizeg_centroida(centroid, centroidi)]
        H[najblizi_centroid]=euclid_distance(list(centroid),list(end))

    return H[centroidi[indeks_najblizeg_centroida(n,centroidi)]]


def h2(n):#heuristika -udaljenost od pocetka
    H={}
    global centroidi
    for i,centroid in enumerate(centroidi):
        najblizi_centroid=centroidi[indeks_najblizeg_centroida(centroid, centroidi)]
        H[najblizi_centroid]=euclid_distance(list(centroid),list(start))

    return H[centroidi[indeks_najblizeg_centroida(n,centroidi)]]

def indeks_suseda(tacka,lista):
    for i,x in enumerate(lista):
        if list(x)==list(tacka):
            return i


def definisi_graf(centroidi):
    G={}
    for i,centroid in enumerate(centroidi):
        susedi=dodaj_susede(list(centroid),centroidi)
        susedi.sort(reverse = True)

        G[centroid]=[[tuple(j),euclid_distance(list(j),list(centroid))] for j in susedi]

    return G

def astar_definisi_graf(centroidi):
    global astar_G
    astar_G={}
    for i,centroid in enumerate(centroidi):
        susedi=dodaj_susede(list(centroid),centroidi)
        astar_G[centroid]=[[tuple(j),euclid_distance(list(j),list(centroid))] for j in susedi]

    return astar_G    

def astar( G,start, stop):
    # global G
    global centroidi
    open_list = set([start])
    closed_list = set([])

    g = {}      #g - dict 
    g[start] = 0
    ind=0
    parents = {}
    parents[start] = None
    

    global parensts_astar
    parensts_astar[start]=None

    iteration = 0
    while len(open_list) > 0:
        ind+=1
        iteration += 1
        n = None
        for v in open_list:
            if n == None or g[v]+h(v) < g[n]+h(n) : 
                n = v
        if n == None:
            print("Ne postoji put!")
            s=parensts_astar.pop(m) 
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
            print("####path",path)
            if len(path)==1:
                return [path[0]]
            
            return [start,path[1]]
        

        # G=definisi_graf(centroidi)proe
        for m, weight in G[n]:
            # print("a*:", n," : ",m)

            if provera_grane2(n,m) == False:
                pygame.draw.line(screen, "red", n, m)
                    # pygame.display.update()
                # time.sleep(0.2)
                continue

            elif m not in open_list and m not in closed_list :
                open_list.add(m)
                if ind==1:
                    parensts_astar[m]=n
                parents[m] = n
                g[m] = g[n] + weight
            else:
                if g[m] > g[n] + weight :
                    g[m] = g[n] + weight
                    parents[m]=n
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
         pygame.display.update()
        #  time.sleep(0.2)      

def orijentacija(first, second):

    return np.linalg.det([first, second]) >= 0 

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  
    elif val > 0:
        return 1 
    else:
        return -1  

# prava B
def tacke_sa_razlicite_strane_prave(A, B, A1_index, A2_index, B1_index, B2_index):
    A1 = A[A1_index]
    A2 = A[A2_index]
    B1 = B[B1_index]
    B2 = B[B2_index]

    o1 = orientation(B1, B2, A1)
    o2 = orientation(B1, B2, A2)

    if o1 != o2:
        return True  # Tacke su na razlicitoj strani
    else:
        return False  # Tacke su na istoj strani

#funkcija kojom dobijamo a,b,c iz opsteg oblika prave(ax+by+c=0)
def jednacina_prave(point1,point2):
    a=list(point2)[1]-list(point1)[1] #y2-y1
    b=list(point1)[0]-list(point2)[0] #x1-x2
    c=list(point2)[1]*list(point1)[0] -list(point2)[1]*list(point1)[0]
    # c = y1 * x2 - y2 * x1
    return a,b,c

def rastojanje_tacke_od_prave(point,a,b,c):
    x1 = list(point)[0]
    y1 = list(point)[1]
    d = abs(a*x1 + b*y1 + c) / (math.sqrt(a**2 + b**2)+0.001)

    return d

def pronadji_najblize_pesake(lista, path):
    
    lista_pesaka=[]
    
    for p in lista:
        lista_pesaka.append([p.get_x(),p.get_y()])
    
    pivot=[10,799] #donji levi ugao
    l1=[]
    l2=[]
    above=[]
    below=[]
    
    for i,p in enumerate(lista_pesaka):
        if tacke_sa_razlicite_strane_prave(lista_pesaka,path,0,i,0,1):
            l1.append(p)

    [l2.append(p) for p in lista_pesaka if p not in l1]
    
    tmp_lista=[]
    if len(l1)>0:
        tmp_lista=[l1[0],pivot]
    else:
        tmp_lista=[l2[0],pivot]

    if tacke_sa_razlicite_strane_prave(tmp_lista,path,0,1,0,1):
        if len(l1)>0:
            above=l1
            below=l2
        else:
            above=l2
            below=l1
    else:
        if len(l1)>0:
            above=l2
            below=l1
        else:
            above=l1
            below=l2

    tmp_distance=[]
    distances1=[]
    distances2=[]

    pygame.draw.line(screen,"purple", (path[0][0],path[0][1]),(path[1][0],path[1][1]), 7)
    a,b,c=jednacina_prave(path[0],path[1])


    for pesak in below:
        distances1.append(rastojanje_tacke_od_prave(pesak,a,b,c))
    
    tmp_distance=copy.deepcopy(distances1)
    distances1=sorted(distances1)
    below1=[]
    
    below1=below

    for pesak in above:
        distances2.append(rastojanje_tacke_od_prave(pesak,a,b,c))

    distances2sorted=[]
    tmp_distance2=copy.deepcopy(distances2)
    distances2sorted=sorted(distances2,reverse=True)

    above1=above

    return above1,below1

#funkcija koja vraca iz liste pesaka najblizeg zadatoj pravoj
def nadji_najblizeg_putu(lista_pesaka,put1,put2):

    a,b,c=jednacina_prave(put1,put2)
    distances=[]
    for p in lista_pesaka:
        distances.append(rastojanje_tacke_od_prave(p,a,b,c))

    distances_tmp=copy.deepcopy(distances)
    distances=sorted(distances)

    najblizi_pesak=lista_pesaka[distances_tmp.index(distances[0])]
    
    return najblizi_pesak


def nadji_najblizeg_tacki(lista_pesaka,p1):
    distances=[]
    for p in lista_pesaka:
        distances.append(euclid_distance(list(p),list(p1)))

    distances_tmp=copy.deepcopy(distances)
    distances=sorted(distances)

    najblizi_pesak=lista_pesaka[distances_tmp.index(distances[0])]
    
    return najblizi_pesak


def dinamicki_kanal(pesaci , putanja):
    
    above = []
    below = []
    above_result=[]
    below_result=[]
    
    for i in range(len(putanja)-1):
        above2=[]
        below2=[]
        above2, below2 = pronadji_najblize_pesake(pesaci ,[putanja[i],putanja[i+1]])
        [above.append(a) for a in above2]
        [below.append(b) for b in below2]

        above=sorted(above)
        below=sorted(below)
        
        if len(above)>0 and len(below)>0:
            a_tmp=[a for a in above if a[0]>putanja[i][0] and a[0]<putanja[i+1][0] and a[1]<putanja[i][1]]
            if len(a_tmp)>0:
                najblizi_pesak=nadji_najblizeg_tacki(a_tmp,putanja[i])
                above_result.append(najblizi_pesak)

            b_tmp=[b for b in below if b[0]>putanja[i][0] and b[0]<putanja[i+1][0] ]
            if len(b_tmp)>0:
                najblizi_pesak=nadji_najblizeg_tacki(b_tmp,putanja[i])
                below_result.append(najblizi_pesak)
                # bellow_result.append(b_tmp[0])


    return above_result,below_result


def astar_pomeranje_pesaka():
    global astar_pesaci
    global astar_pocetne_putanje
    pass

def astar_astar(start, stop):
    # global G
    global astar_centroidi
    open_list = set([start])
    closed_list = set([])
    global astar_G
    g = {}      #g - dict 
    g[start] = 0
    ind=0
    parents = {}
    parents[start] = None
    

    global parensts_astar
    parensts_astar[start]=None

    iteration = 0
    while len(open_list) > 0:
        ind+=1
        iteration += 1
        n = None
        for v in open_list:
            if n == None or g[v] < g[n]  : 
                n = v
        if n == None:
            print("Ne postoji put!")
            s=parensts_astar.pop(m) #nisam siguran
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
            print("####path",path)
            if len(path)==1:
                return [path[0]]
            
            return [start,path[1]]
        
        for m, weight in astar_G[n]:
            # print("a*:", n," : ",m)

            screen.fill("black")
            nedozvoljene_putanje = provera_grane(n,m)
            # pygame.display.update()
            # time.sleep(1)

            ntmp=n
            mtmp=m
            edge1=(list(ntmp),list(mtmp))
            edge2=(list(mtmp),list(ntmp))
            

            if edge1 in nedozvoljene_putanje or edge2 in nedozvoljene_putanje:
                continue
            # if provera_grane2(n,m) == False:
            #     pygame.draw.line(screen, "red", n, m)
            #         # pygame.display.update()
            #     # time.sleep(0.2)
            #     continue

            elif m not in open_list and m not in closed_list :
                open_list.add(m)
                if ind==1:
                    parensts_astar[m]=n
                parents[m] = n
                g[m] = g[n] + weight
            else:
                if g[m] > g[n] + weight :
                    g[m] = g[n] + weight
                    parents[m]=n
                    if m in closed_list:
                        closed_list.remove(m)
                        open_list.add(m)
        open_list.remove(n)
        closed_list.add(n)
    
def astar_crtanje():
    # print("A STAR ", astar_centroidi)
    global astar_G
    global astar_pesaci, astar_pocetne_putanje, astar_centroidi

    _ = astar_triangulacija_temena()
    # print("A STAR ", astar_centroidi)

    astar_G = {}
    global start_indeks,end_indeks
    global centroidi
    path=[]
    tmp=[]
    l=[]
    lista_koordinata=[]

    pomocni=copy.deepcopy(astar_centroidi[int(start_indeks)])
    lista_koordinata.append(list(pomocni))
    c_tmp=[]
    indeks=0
    for i in range(15):
        screen.fill("black")

        astar_G.clear()
        astar_G=astar_definisi_graf(astar_centroidi)
        # print(G)

        start_indeks=indeks_suseda(list(start),astar_centroidi)
        end_indeks=indeks_suseda(list(end),astar_centroidi)
        
        print("START I END:",start_indeks,end_indeks)
        
        if i==0:
            tmp = astar_astar(astar_centroidi[start_indeks],astar_centroidi[end_indeks])
            if len(tmp)==2:
                c_tmp=copy.deepcopy(list(tmp[1]))
            else:
                c_tmp=copy.deepcopy(list(tmp[0]))


        else:
            indeks=indeks_najblizeg_centroida(c_tmp,astar_centroidi)
            tmp = astar_astar(astar_centroidi[indeks],astar_centroidi[end_indeks])
            if len(tmp)==2:
                c_tmp=copy.deepcopy(list(tmp[1]))
            else:
                c_tmp=copy.deepcopy(list(tmp[0]))

        if len(tmp)==1:
            break

        elif len(tmp)==0:
            l=[]
            break

        elif len(tmp)>1:
            if tmp not in l:
                lista_koordinata.append(list(c_tmp))
                l.append(tmp)
            

        astar_pomeranje_pesaka()

        
        for i in range(len(lista_koordinata)-1):
            pygame.draw.line(screen,"orange", (lista_koordinata[i][0], lista_koordinata[i][1]),
                          (lista_koordinata[i+1][0],lista_koordinata[i+1][1]), 10)
            pygame.draw.circle(screen, "red", lista_koordinata[i], 7) 
            # time.sleep(0.2) 

        pygame.image.save(screen, f"astar_crtanje{i}.png")

        putanje = []
        pygame.display.update()
        # time.sleep(0.2)    

        # print(l) 
        # print("Lista koordinata",lista_koordinata)

    screen.fill('black')
    astar_pomeranje_pesaka()

    for i in range(len(lista_koordinata)-1):
        pygame.draw.line(screen,"orange", (lista_koordinata[i][0], lista_koordinata[i][1]),
                      (lista_koordinata[i+1][0],lista_koordinata[i+1][1]), 10)
        pygame.draw.circle(screen, "red", lista_koordinata[i], 7) 
        # time.sleep(0.2) 
    
    return lista_koordinata

def pronalazenjet1t2( lista , vektori, i, j, dthresh=30):
    cx=lista[i][0]-lista[j][0]
    cy=lista[i][1]-lista[j][1]

    vx=vektori[i][0]-vektori[j][0]
    vy=vektori[i][1]-vektori[j][1]

    pod_korenom=8*cx*vx*cy*vy - 4*cx*cx*vy*vy - 4*cy*cy*vx*vx + 4*dthresh*dthresh*vx*vx + 4*dthresh*dthresh*vy*vy

    if pod_korenom<0:
        return None

    t1= (- 2 * cx * vx - 2 * cx * vx - math.sqrt(pod_korenom))/( 2 * cx*cx + 2 * cy*cy - 2 * dthresh*dthresh)
    t2= (- 2 * cx * vx - 2 * cx * vx + math.sqrt(pod_korenom))/( 2 * cx*cx + 2 * cy*cy - 2 * dthresh*dthresh)

    if t1==t2:
        return (t1,None)

    else:
        return (t1,t2)


def napravi_listu_pesaka(pesaci):
    pedestrians_xy = []
    pedestrians_x_coord = []
    pedestrians_y_coord = []

    for i in pesaci:
        pedestrians_x_coord.append(i.get_x())
        pedestrians_y_coord.append(i.get_y())

    for i in range(len(pedestrians_x_coord)):
        pedestrians_xy.append((pedestrians_x_coord[i], pedestrians_y_coord[i]))         

    return pedestrians_xy


def izracunaj_vektor_za_centroid(centroid,vektori_pesaka):
    global putanje
    
    lista_temena=mapa_temena[centroidi[indeks_najblizeg_centroida(centroid,centroidi)]]
    t1=lista_temena[0]
    t2=lista_temena[1]
    t3=lista_temena[2]

    pedestrians_list=napravi_listu_pesaka(pedestrians)
    
    indeks1=indeks_najblizeg_centroida(t1,pedestrians_list)
    indeks2=indeks_najblizeg_centroida(t2,pedestrians_list)
    indeks3=indeks_najblizeg_centroida(t3,pedestrians_list)

    vektor_centroida_x=(vektori_pesaka[indeks1][0] + vektori_pesaka[indeks2][0] + vektori_pesaka[indeks3][0])/3.0 
    vektor_centroida_y=(vektori_pesaka[indeks1][1] + vektori_pesaka[indeks2][1] + vektori_pesaka[indeks3][1])/3.0

    return [vektor_centroida_x,vektor_centroida_y]


def izracunaj_vreme_preseka_sa_kretanjem(c1, c2, pesak1, pesak2, brzina_robota, c1_brzina, c2_brzina, pesak1_brzina, pesak2_brzina, threshold):
    dt = 0.01
    max_iter = 1000

    robot_pozicija = copy.deepcopy(c1)
    A_trenutno = copy.deepcopy(c1)
    B_trenutno = copy.deepcopy(c2)
    ivica_pocetak_trenutno = copy.deepcopy(pesak1)
    ivica_kraj_trenutno = copy.deepcopy(pesak2)

    robot_positions = [copy.deepcopy(robot_pozicija)]
    A_positions = [copy.deepcopy(A_trenutno)]
    B_positions = [copy.deepcopy(B_trenutno)]
    ivica_pocetak_positions = [copy.deepcopy(ivica_pocetak_trenutno)]
    ivica_kraj_positions = [copy.deepcopy(ivica_kraj_trenutno)]

    for i in range(max_iter):
        p1 = np.array(robot_pozicija)
        p2 = np.array(ivica_kraj_trenutno)
        p3 = np.array(ivica_pocetak_trenutno)

        distance = np.linalg.norm(np.cross(p2 - p1, p1 - p3)) / np.linalg.norm(p2 - p1)
        if distance <= threshold:
            vreme_preseka = i * dt
            return vreme_preseka, robot_positions, A_positions, B_positions, ivica_pocetak_positions, ivica_kraj_positions

        robot_pozicija = (robot_pozicija[0] + brzina_robota[0] * dt, robot_pozicija[1] + brzina_robota[1] * dt)
        A_trenutno = (A_trenutno[0] + c1_brzina[0] * dt ,A_trenutno[1] + c1_brzina[1] * dt)
        B_trenutno = (B_trenutno[0] + c2_brzina[0] * dt, B_trenutno[1] + c2_brzina[1] * dt)
        ivica_pocetak_trenutno = (ivica_pocetak_trenutno[0] + pesak1_brzina[0] * dt, ivica_pocetak_trenutno[1] + pesak1_brzina[1] * dt)
        ivica_kraj_trenutno = (ivica_kraj_trenutno[0] + pesak2_brzina[0] * dt,
        ivica_kraj_trenutno[1] + pesak2_brzina[1] * dt)

        robot_positions.append(copy.deepcopy(robot_pozicija))
        A_positions.append(copy.deepcopy(A_trenutno))
        B_positions.append(copy.deepcopy(B_trenutno))
        ivica_pocetak_positions.append(copy.deepcopy(ivica_pocetak_trenutno))
        ivica_kraj_positions.append(copy.deepcopy(ivica_kraj_trenutno))

    return None, robot_positions, A_positions, B_positions, ivica_pocetak_positions, ivica_kraj_positions


def resi_kvadratnu(a, b, c): 
    
    if a == 0:
        a = 0.01

    # Izračunajmo diskriminantu za zadate parametre
    D = b**2 - 4*a*c
    
    # diskriminanta je manja od 0 => nema realnih rešenja
    if D < 0:  
        return []
    
    # jedno rešenje kvadratne jednacine
    elif D == 0:  
        return [-b / (2*a)]
    
     # dva rešenja kvadratne jednacine => [x1 , x2]
    else:  
        return [(-b - math.sqrt(D)) / (2*a), (-b + math.sqrt(D)) / (2*a)]


def daljina_veca_od_praga(p1, p2, v1, v2, Dthresh):
    a = (v1[0] - v2[0])**2 + (v1[1] - v2[1])**2
    b = 2 * ((p1[0] - p2[0]) * (v1[0] - v2[0]) + (p1[1] - p2[1]) * (v1[1] - v2[1]))
    c = (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 - Dthresh**2

    # Vraćamo vreme za koje je rastojanje veće od praga
    return resi_kvadratnu(a, b, c)

def provera_grane2(c1,c2):
    
    c2_tmp=[]
    indeks_c2=indeks_najblizeg_centroida(c2,centroidi)

    [vc2x,vc2y]=izracunaj_vektor_za_centroid(c2, copy.deepcopy(pocetne_putanje))
    [vc1x,vc1y]=izracunaj_vektor_za_centroid(c1, copy.deepcopy(pocetne_putanje))
    
    #naredna pozicija centroida c2
    c2_tmp=[c2[0]+vc2x , c2[1]+vc2y]

    vx=c2_tmp[0]-c1[0]
    vy=c2_tmp[1]-c1[1]
    #vx i vy predstavljaju vektor robota
    vx=(vx/max(vx,vy)) * 3.0
    vy=(vy/max(vx,vy)) * 3.0
    #putanjee!!!
    
    # pygame.draw.circle(screen,"orange",c1,10)
    # pygame.draw.circle(screen,"orange",c2,10)
    # pygame.display.update()
    # time.sleep(0.1)
    # pygame.draw.circle(screen,"purple",c1,10)
    # pygame.draw.circle(screen,"purple",c2,10)
    # pygame.display.update()

    c11 = centroidi[indeks_najblizeg_centroida(c1, centroidi)]
    temena_c1=mapa_temena[c11]

    c22 = centroidi[indeks_najblizeg_centroida(c2, centroidi)]
    temena_c2=mapa_temena[c22]

    # print("C1/C11:",c1,c11)
    # print("C2/C22:",c2,c22)

    # print("Temena c1 ",temena_c1)
    # print("Temena c2 ",temena_c2)

    temena=[]
    for i in temena_c1:
        for j in temena_c2:
            if i==j:
                temena.append(i)


    print("Temena:",temena)
    pedestrians_list=napravi_listu_pesaka(pedestrians)

    try: 
        teme1=temena[0]
        teme2=temena[1]

        indeks_pesaka1=indeks_najblizeg_centroida(teme1,pedestrians_list)
        indeks_pesaka2=indeks_najblizeg_centroida(teme2,pedestrians_list)

        brzina_pesaka1=pocetne_putanje[indeks_pesaka1]
        brzine_pesaka2=pocetne_putanje[indeks_pesaka2]

        threshold=35
        lista_vremena=daljina_veca_od_praga(teme1,teme2,brzina_pesaka1,brzine_pesaka2,threshold)
        # print("lista vremena:",lista_vremena)

        t, robot_positions, c1_positions, c2_positions, pesak1_positions, pesak2_positions=izracunaj_vreme_preseka_sa_kretanjem(c1,c2_tmp,teme1,teme2, [vx, vy], (vc1x,vc1y),(vc2x,vc2y), brzina_pesaka1,brzine_pesaka2,threshold)
        # print("VREME", t)


        if len(lista_vremena)==0:
            return True

        if len(lista_vremena)==1:
            return lista_vremena[0] == t

        t1=lista_vremena[0]
        t2=lista_vremena[1]


        if t1 < 0:
            t1=0

        if t2<0:
            t2=0

        if t==None:
            return True

        elif t1 < t and t < t2: 
            return True   

        return False
    
    except:
        nedozvoljena_grana=provera_grane(c1,c2)
        print("NEDOZVOLJENI PUTEVI:",nedozvoljena_grana)
        if ((c1,c2) in nedozvoljena_grana) or ((c2,c1) in nedozvoljena_grana):
            return False
        else:
            return True


def __main__():

    global putanje
    global centroidi
    global astar_G
    nacrtaj_dugme()
    global start, end
    global start_indeks,end_indeks
    global pedestrians
    br_unosa = 0
    global astar_centroidi
    global astar_pesaci
    global astar_pocetne_putanje
    running = True
    astar_indikator=0
    
    [os.remove(png) for png in glob.glob("*png")]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print(len(pedestrians))
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    screen.fill((100, 100, 100))

            if pygame.MOUSEBUTTONDOWN == event.type:
                if pygame.mouse.get_pressed()[0] == True:
                    x, y = pygame.mouse.get_pos()
                    x = int(x)
                    start = (150, 700)
                    end = (1000, 150)
                    centroidi.append(start)
                    centroidi.append(end)
                    astar_centroidi.append(start)
                    astar_centroidi.append(end)

                 
                    if x >= 10 and x <= 60 and y >= 10 and y<=40:
                        podaci = ucitaj_pesake()
                        for k,v in podaci.items():
                            krug = Krug(v[0][0], v[0][1])
                            pedestrians.append(krug)
                            nacrtaj_krug(krug, "white")
                            pocetne_putanje.append((v[1][0], v[1][1]))
                    
                        nacrtaj_putanje(pedestrians, "red")
                        pygame.draw.circle(screen, "blue", start, 10)
                        pygame.draw.circle(screen, "blue", end, 10)
                        pygame.display.update()
                        # time.sleep(5)     
                        astar_pocetne_putanje = copy.deepcopy(pocetne_putanje)
                        astar_pesaci = copy.deepcopy(pedestrians)
                        astar_triangulacija_temena()
                        astar_centroidi = copy.deepcopy(centroidi)
                        #pravljenje poecetne slike animacije
                        pygame.image.save(screen, f"animation_first_frame.png")
                        
                        print(len(astar_pesaci), len(astar_centroidi), len(astar_pocetne_putanje))
                        first_edge = astar_crtanje()
                    # elif br_unosa<2:
                   
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_t:
                    triangulacija_temena()
                    # nacrtaj_putanje(pedestrians, "red")

                #iscrtavanje centroida i njihovo povezivanje
                if event.key == pygame.K_c:
                        for i in centroidi:
                            pygame.draw.circle(screen, "blue", i, 5)

                        povezi_centroide()

                #pokretanje dinamickog a* algoritma
                if event.key == pygame.K_p:
                    putanje=[]
                    lista_koordinata=kretanje() #"live" kretanje 
                    #iscrtavanje inicijalnog(staticnog a* algoritma)
                    for i in range(len(first_edge)-1):
                        pygame.draw.line(screen,"orange", (first_edge[i][0], first_edge[i][1]),(first_edge[i+1][0],first_edge[i+1][1]), 10)
                        pygame.draw.circle(screen, "red", first_edge[i], 7) 
                        pygame.image.save(screen, f"topologija{i}.png")
                    
                #pokusaj dinamickog kanala
                if event.key == pygame.K_q:
                    l=[]
                    l.append(lista_koordinata[0])
                    l.append(lista_koordinata[1])
                    # print("PATH(l)",l)
                    above , below=pronadji_najblize_pesake(list(pedestrians),l)
                   
                    spoji_temena_redom(sorted(above),"red")
                    spoji_temena_redom(sorted(below),"blue")
                    
                    above_r,below_r=dinamicki_kanal(pedestrians,lista_koordinata)

                    spoji_temena_redom(above_r,"pink")
                    spoji_temena_redom(below_r,"yellow")
                    
                #iscrtavanje polinomijalne aproksimacije a* putanje
                if event.key == pygame.K_d:
                    x=[i[0] for i in lista_koordinata]
                    y=[800-i[1] for i in lista_koordinata]
                
                    mymodel = np.poly1d(np.polyfit(x,y, 2))
                
                    myline = np.linspace(10, 1100 , 100)
                
                    plt.scatter(x, y)
                    plt.plot(myline, mymodel(myline))
                    plt.show()    

                #cuvanje animacije nakon zavrsetka rada algoritma
                if event.key == pygame.K_g:
                    frames = []
                    imgs = glob.glob("*.png")
                    imgs=sorted(imgs)
                    for i in imgs:
                        new_frame = Image.open(i)
                        frames.append(new_frame)

                    frames[0].save('animated.gif', format='GIF',
                                   append_images=frames[1:],
                                   save_all=True,
                                   duration=1000, loop=0)
                    # im = Image.open('animated.gif')
                    # im.show()

            pygame.display.update()

__main__()