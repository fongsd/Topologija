#!/usr/bin/python3
import json

br_pesaka = 20

pozicije = {}

import random

for i in range(br_pesaka):
    poz_x = random.random() * 1000 + 100
    poz_y = random.random() * 700 +  80
    vx = random.random() * 3 
    vy = random.random() * 3 
    pozicija = (poz_x, poz_y)
    brzina = (vx, vy)
    pozicije[i] = (pozicija, brzina)

fajl = open("podaci.json", "w")

json.dump(pozicije, fajl)

