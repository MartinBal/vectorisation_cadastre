# -*- coding: utf-8 -*-

import os
import pickle

#rasterReprojete=QgsMapLayerRegistry.instance().mapLayersByName("Reprojet")[0]

def numeroterParcelles(rasterReprojete, fichier='Feuille CL0180000A01 AULAN - 026/26041010180000A01.LOC', dossier='/home/martin/Documents/Permagro/Mission1_PALUD/donnees'):
    os.chdir(dossier)
    fichierLoc=open(fichier,r)

    chaine=fichierLoc.read(fichierLoc)
    listeChaines=chaine.split('\r\n')[:-1]

    tabLoc=[c.split(',') for c in listeChaines]

    emprise=rasterReprojete.extent().toString()
    largeur = rasterReprojete.width()
    hauteur = rasterReprojete.heigth()

    tabEmprise=[angle.split(',') for angle in emprise.split(' : ')]


    Coordonnees=[[((int(x) * (float(tabEmprise[1][0])-float(tabEmprise[0][0])))/largeur + float(tabEmprise[0][0])),\
    ((int(y) * (float(tabEmprise[1][1])-float(tabEmprise[0][1])))/hauteur + float(tabEmprise[0][1])),\
    n] \
    for x,y,n in tabLoc]
