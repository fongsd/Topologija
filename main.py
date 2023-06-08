import pygame
import random 
import time
import math
from krug import Krug
from scipy.spatial import Delaunay
import numpy as np
import copy
pygame.init()
from matplotlib import pyplot as plt


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



#PROBLEM PRI POMERANJU JE NESTAJANJE NEKIH CENTROIDA->AZURIRANJE G-A
#iz tog razlohga nastaju problemi sa indeksima


screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
screen.fill("black")


nedozvoljeni_putevi=[]
parensts_astar={}
G={}

putanje = []
pocetne_putanje = []
centroidi = []
pedestrians = []
trenutne_putanje = []
trouglovi = 0

start = (0, 0)
start_indeks='0'
end = (0, 0)
end_indeks='1'
velocity = 0

indikator_inicijalizacije=0
dx=[]
dy=[]



def nacrtaj_krug(krug : Krug, boja):
    pygame.draw.circle(screen, boja, (krug.get_x(), krug.get_y()), 4, 0)



#da li seta zbog radnoma
def nacrtaj_putanje(pedestrians : list, color):
    brzine_pesaka = []
    for poz, i in enumerate(pedestrians):
        dx = int(random.random() * 3)
        dy = int(random.random() * 3)
        # s = round(random.random()* 2) - 1 
        # k = round(random.random() * 2 ) - 1
        # print(s, k)
        pygame.draw.line(screen, color, (i.get_x(), i.get_y()), 
                         (i.get_x() + dx * velocity, i.get_y() + dy * velocity), 4)
        putanje.append((i.get_x() + dx * velocity, i.get_y() + dy * velocity))
        brzine_pesaka.append(((i.get_x(), i.get_y()), (dx * velocity, dy * velocity))) # lista parova (pozicija pesaka, njegova brzina)

    return brzine_pesaka


    return brzine_pesaka

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
    # da li nam je potreban skup brzina izmedju dva suseda ili mogu da se ponavljaju?
    return [prvo, drugo, trece]

#!!!moze eucledian_distance
def brzine_centroida(prvo_teme, drugo_teme): 
    vx_first = prvo_teme[0]
    vy_first = prvo_teme[1]
    vx_second = drugo_teme[0]
    vy_second = drugo_teme[1]

    return math.dist(prvo_teme, drugo_teme)

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

def indeks_najblizeg_centroida(c):
    global centroidi
    distance=float('inf')
    indeks=0
    for i,centroid in enumerate(centroidi):
        dist=euclid_distance(list(c),list(centroid))
        if dist<distance:
            distance=dist
            indeks=i
    
    print("############INDEKS:",indeks,centroidi[indeks])
    return indeks



def kretanje():
    global pedestrians
    global centroidi
    global putanje
    global G
    global start_indeks,end_indeks
  
    path=[]
    tmp=[]
    l=[]
    lista_koordinata=[]
    pomocni=copy.deepcopy(centroidi[int(start_indeks)])
    lista_koordinata.append(list(pomocni))
    c_tmp=[]
    indeks=0
    for i in range(10):
        screen.fill("black")
        #!!!!
        G=definisi_graf(centroidi)
        print(G)

        start_indeks=str(indeks_suseda(list(start),centroidi))
        end_indeks=str(indeks_suseda(list(end),centroidi))
        
        print("START I END:",start_indeks,end_indeks)
        
        if i==0:
            path,tmp = astar(start_indeks,end_indeks)
            if len(tmp)==2:
                c_tmp=copy.deepcopy(centroidi[int(tmp[1])])
            else:
                c_tmp=copy.deepcopy(centroidi[int(tmp[0])])


        elif len(tmp)==2:
            indeks=indeks_najblizeg_centroida(c_tmp)
            path,tmp = astar(str(indeks),end_indeks)
            if len(tmp)==2:
                c_tmp=copy.deepcopy(centroidi[int(tmp[1])])
            else:
                c_tmp=copy.deepcopy(centroidi[int(tmp[0])])

        if len(path)==1:
            # # indeks=indeks_najblizeg_centroida(c_tmp)
            # if tmp not in l:
            #     # lista_koordinata.append(list(int_tmp))
            #     lista_koordinata.append(list(c_tmp))

            #     l.append(tmp)
            break

        elif len(path)==0 and len(tmp)==0:
            l=[]
            break

        elif len(path)>1:
            if tmp not in l:
                lista_koordinata.append(list(c_tmp))
                l.append(tmp)
            

        pomeranje_pesaka()

        # triangulacija_temena()
        # pomeranje_centroida()


        putanje = []
        pygame.display.update()
        time.sleep(1)    

        print(l) 
        print("Lista koordinata",lista_koordinata)

    screen.fill('black')
    pomeranje_pesaka()
    # pygame.display.update()
    for i in range(len(pedestrians)):
            nacrtaj_krug(pedestrians[i], "white")

    for i in range(len(lista_koordinata)-1):
        pygame.draw.line(screen,"white", (lista_koordinata[i][0], lista_koordinata[i][1]),
                      (lista_koordinata[i+1][0],lista_koordinata[i+1][1]), 10)
        pygame.draw.circle(screen, "red", lista_koordinata[i], 7) 
        time.sleep(2) 

    # lista_indeksa=[int(s[0]) for s in l]
    # print("Lista temena kroz putanje",lista_indeksa)
    # put=[list(centroidi[k]) for k in  lista_indeksa]
    # # print(put)
    # print("Lista koordinata",lista_koordinata)
    # spoji_temena_redom(put,"orange")

    return lista_koordinata



def pomeranje_pesaka():
    
    print("############################# ITERACIJA ######################")
    global centroidi
    global pedestrians
    global putanje
    global velocity
    stari = copy.deepcopy(pedestrians)
    brzine_pesaka = nacrtaj_putanje(pedestrians, "red") # uredjen par (trenutna pozicija pesaka, brzina == sledeca pozicija)
    for i in range(len(pedestrians)):
            # nacrtaj_krug(pedestrians[i], "black")
            nacrtaj_obim(pedestrians[i], putanje[i][0], putanje[i][1])
            nacrtaj_krug(pedestrians[i], "white")
            # nacrtaj_obim(pedestrians[i], putanje[i][0], putanje[i][1])
    susedni_centroidi = triangulacija_temena() # lista listi susednih temena
    for i in range(len(pedestrians)):
            pedestrians[i] = Krug(putanje[i][0], putanje[i][1])
            # pygame.draw.line(screen, "black", (pedestrians[i].get_x(), pedestrians[i].get_y())
                                            #    , (stari[i].get_x(), stari[i].get_y()), 4)
   
    # print("Susedni centroidi:",sus)
    print("Centroids length pomeranje_pesaka:",len(centroidi))
    # brzine_pesaka = nacrtaj_putanje(pedestrians, "red") # uredjen par (trenutna pozicija pesaka, brzina == sledeca pozicija)

    # susedni_centroidi = triangulacija_temena() # lista listi susednih temena

def provera_grane(fst,scnd):
    global centroidi
    global pedestrians
    global putanje
    global velocity

    print("Centroids length:",len(centroidi))
    nedozvoljene_putanja=[]            

    brzine_pesaka = nacrtaj_putanje(pedestrians, "red") # uredjen par (trenutna pozicija pesaka, brzina == sledeca pozicija)

    susedni_centroidi = triangulacija_temena() # lista listi susednih temena


    for i in susedni_centroidi: # susedna temena

        first = i[0] # prvo teme
        second = i[1] # drugo teme
        third = i[2] # trece teme

        #lista temena trougla
        lista=[list(first),list(second), list(third)]
        
        fst1=list(centroidi[int(fst)])
        scnd1=list(centroidi[int(scnd)])

        #ako 2 tacke koje obrazuju deo putanje su zapravo temena trougla
        if (fst1 in lista) and (scnd1 in lista):                

            for (trenutna_pozicija, putanja) in brzine_pesaka:
                # #### intersection between pedestrian and first, second centroid
                vektor_v = (second[0] - first[0], second[1] - first[1])
                vektor_u = (trenutna_pozicija[0] - first[0], trenutna_pozicija[1] - first[1])
                sledeca_pozicija_pesaka = (trenutna_pozicija[0] + putanja[0], trenutna_pozicija[1] + putanja[1])
                vektor_W = (sledeca_pozicija_pesaka[0] - first[0], sledeca_pozicija_pesaka[1] - first[1])



                # pygame.draw.line(screen, "yellow", first, second, 5)
                if angle(first, second, trenutna_pozicija):
                    if orijentacija(vektor_v, vektor_u) != orijentacija(vektor_v, vektor_W) :
                        pygame.draw.line(screen, "red", first, second, 5)
                        if (list(first),list(second)) not in nedozvoljene_putanja:
                            nedozvoljene_putanja.append((list(first),list(second)))
                        # print(nedozvoljene_putanja)
                        # print(orijentacija(vektor_v, vektor_u), orijentacija(vektor_v, vektor_W))
                        nacrtaj_krug(Krug(trenutna_pozicija[0], trenutna_pozicija[1]), "red")
                        nacrtaj_krug(Krug(sledeca_pozicija_pesaka[0], sledeca_pozicija_pesaka[1]), "red")
                        pygame.display.update()
                        time.sleep(0.6)

                # ##### end


                # #### intersection between pedestrian and first, third centroid
                vektor_v = (third[0] - first[0], third[1] - first[1])
                vektor_u = (trenutna_pozicija[0] - first[0], trenutna_pozicija[1] - first[1])
                sledeca_pozicija_pesaka = (trenutna_pozicija[0] + putanja[0], trenutna_pozicija[1] + putanja[1])
                vektor_W = (sledeca_pozicija_pesaka[0] - first[0], sledeca_pozicija_pesaka[1] - first[1])

                # pygame.draw.line(screen, "yellow", first, third, 5)

                if angle(first, third, trenutna_pozicija):
                    if orijentacija(vektor_v, vektor_u) != orijentacija(vektor_v, vektor_W) :
                        pygame.draw.line(screen, "red", first, third, 5)
                        
                        if (list(first),list(third)) not in nedozvoljene_putanja:
                            nedozvoljene_putanja.append((list(first),list(third)))
                        
                        # print(nedozvoljene_putanja)
                        # print(orijentacija(vektor_v, vektor_u), orijentacija(vektor_v, vektor_W))
                        nacrtaj_krug(Krug(trenutna_pozicija[0], trenutna_pozicija[1]), "red")
                        nacrtaj_krug(Krug(sledeca_pozicija_pesaka[0], sledeca_pozicija_pesaka[1]), "red")
                        pygame.display.update()
                        time.sleep(0.6)

                # ##### end


                #### intersection between pedestrian and second, third centroid
                vektor_v = (third[0] - second[0], third[1] - second[1])
                vektor_u = (trenutna_pozicija[0] - second[0], trenutna_pozicija[1] - second[1])
                sledeca_pozicija_pesaka = (trenutna_pozicija[0] + putanja[0], trenutna_pozicija[1] + putanja[1])
                vektor_W = (sledeca_pozicija_pesaka[0] - second[0], sledeca_pozicija_pesaka[1] - second[1])

                # pygame.draw.line(screen, "yellow", second, third, 5)

                if angle(second, third, trenutna_pozicija):
                    if orijentacija(vektor_v, vektor_u) != orijentacija(vektor_v, vektor_W) :
                        pygame.draw.line(screen, "red", third, second, 5)
                        
                        if (list(second),list(third)) not in nedozvoljene_putanja:
                            nedozvoljene_putanja.append((list(second),list(third)))
                        # print(orijentacija(vektor_v, vektor_u), orijentacija(vektor_v, vektor_W))
                        nacrtaj_krug(Krug(trenutna_pozicija[0], trenutna_pozicija[1]), "red")
                        nacrtaj_krug(Krug(sledeca_pozicija_pesaka[0], sledeca_pozicija_pesaka[1]), "red")
                        pygame.display.update()
                        time.sleep(0.6)


            # return nedozvoljene_putan-ja   

    # print("nedozvoljene putanje:",nedozvoljene_putanja)
    return nedozvoljene_putanja

def pomeranje_centroida():
    pass


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

    #dodata linija

    # centroidi=sorted(centroidi)

    for centroid in centroidi:
        font = pygame.font.Font(size=30)
        number_of_pedestrian = font.render(str(indeks_suseda(centroid,centroidi)), True, (255, 215, 0))
        screen.blit(number_of_pedestrian, (centroid[0]-20,centroid[1]-20,centroid[0]+20,centroid[1]+20))

    return povezi_centroide()

def povezi_centroide():
    lista_susednih_temena_triangulacije = []
    global centroidi
    triCentroid = Delaunay(centroidi)
    for i in triCentroid.simplices:
        tmp_lista =  spoji_centroide(centroidi[i[0]], centroidi[i[1]], centroidi[i[2]]) # fja vraca [prva, druga, treca]
        lista_susednih_temena_triangulacije.append(tmp_lista) # lista susednih temena centroida

    # for i in lista_susednih_temena_triangulacije:
    #     print(i)
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
    global end_indeks
    end_indeks=str(indeks_suseda(list(end),centroidi))
    ind=int(end_indeks)
    for i in range(len(centroidi)):
        H["{}".format(i)]=euclid_distance(list(centroidi[ind]),list(centroidi[i]))
    return H[n]

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

def h3(n):#heuristika udaljenosti od pocetka
    H={} 
    global centroidi

    for i,centroid in enumerate(centroidi):
        H["{}".format(i)]=euclid_distance(list(centroidi[0]),list(centroid))

        # H["{}".format(i)]=euclid_distance(list([centroidi[0][0], centroidi[0][1]]),list([pedestrians[i][0],pedestrians[i][1]]))
    # print(H)
    return H[n]

def astar( start, stop):
    global G
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
            if n == None or g[v] < g[n]  : 
                n = v
        if n == None:
            print("Ne postoji put!")
            s=parensts_astar.pop(m) #nisam siguran
            return [],[]
        
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
                return path,[path[0]]
            
            return path,[start,path[1]]
        

        # G=definisi_graf(centroidi)
        for m, weight in G[n]:
            print("a*:", n," : ",m)

            # screen.fill("black")
            nedozvoljene_putanje = provera_grane(n,m)
            # pygame.display.update()
            # time.sleep(1)

            ntmp=list(centroidi[int(n)])
            mtmp=list(centroidi[int(m)])
            edge1=(ntmp,mtmp)
            edge2=(mtmp,ntmp)
            #videti sad
            # print("Grana kroz koju prolazimo",edge1)
            # print("Zabrana:",nedozvoljene_putanje)
            if edge1 in nedozvoljene_putanje or edge2 in nedozvoljene_putanje:
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
         time.sleep(0.5)      





def heuristika(first, second):
    return math.dist(first, second)


def orijentacija(first, second):

    return np.linalg.det([first, second]) >= 0 



# def napravi_listu_od_krugova(lits_krugova)
def spoji_temena_redom(lista,color="orange"):
    for i in range(len(lista)-1):
         pygame.draw.line(screen, color, (lista[i][0], lista[i][1]),
                      (lista[i+1][0],lista[i+1][1]), 7) 
         pygame.display.update()
         time.sleep(0.5)      



def heuristika(first, second):
    return math.dist(first, second)


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
    # if len(bellow)>=4:
    #     for i in range(4):
    #         indeks=tmp_distance.index(distances1[i])
    #         bellow1.append(bellow[indeks])
    # else:
    below1=below



    for pesak in above:
        distances2.append(rastojanje_tacke_od_prave(pesak,a,b,c))

    distances2sorted=[]
    tmp_distance2=copy.deepcopy(distances2)
    distances2sorted=sorted(distances2,reverse=True)

    # above1=[]
    # if len(above)>=4:
    #     for i in range(4):
    #         indeks=tmp_distance2.index(distances2sorted[i])
    #         above1.append(above[indeks])
    # else:
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

        # above.append(above2)
        # bellow.append(bellow2)
        above=sorted(above)
        below=sorted(below)
        # print("ABOVE_:",above)
        # print("BELLOW_:",bellow)

        
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
            
            # print("ABOVE_RESULT:",above_result)
            # print("BELLOW_RESULT:",bellow_result)



    return above_result,below_result

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



def __main__():

    global velocity
    velocity = random.random() + 10 # constant speed for every pedestrian

    global trouglovi
    global putanje
    global centroidi
    nacrtaj_dugme()
    global start, end
    global start_indeks,end_indeks
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
                        for i in range(10):
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
                            # print(heuristika(start, end))
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
                    # astar_indikator=1

                    s=indeks_suseda(list(start),centroidi)
                    print("Pocetak",s)
                    start_indeks=str(s)

                    f=indeks_suseda(list(end),centroidi)
                    print('Kraj',f)
                    end_indeks=str(s)

                    lista_koordinata=kretanje() #"live" kretanje 

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
                    
                if event.key == pygame.K_d:
                    x=[i[0] for i in lista_koordinata]
                    y=[800-i[1] for i in lista_koordinata]
                
                    mymodel = np.poly1d(np.polyfit(x,y, 2))
                
                    myline = np.linspace(10, 1100 , 100)
                
                    plt.scatter(x, y)
                    plt.plot(myline, mymodel(myline))
                    plt.show()    


                # if event.key == pygame.K_a and astar_indikator==1:
                #     G=definisi_graf(centroidi)
                #     s=indeks_suseda(list(start),centroidi)
                #     print("Pocetak",s)

                #     f=indeks_suseda(list(end),centroidi)
                #     print('Kraj',f)

                #     l=astar(G,str(s),str(f))

                #     lista_indeksa=[int(s) for s in l]
                #     print("Lista temena kroz putanje",lista_indeksa)
                #     put=[list(centroidi[k]) for k in  lista_indeksa]
                #     # print(put)
                #     spoji_temena_redom(put,"orange")


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