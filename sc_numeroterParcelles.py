# -*- coding: utf-8 -*-

import os
import pickle
from PyQt4.QtCore import *

## Décallage dans les numéro de parcelles
##  --> essayer en CC45?
##  --> essayer par numpy?
##  --> essayer par indexage

from PyQt4.QtCore import *

#rasterReprojete=QgsMapLayerRegistry.instance().mapLayersByName("Reprojet")[0]

def numeroterParcelles(rasterReprojete, fichier='Feuille CL0180000A01 AULAN - 026/26041010180000A01.LOC', dossier='/home/martin/Documents/Permagro/Mission1_PALUD/donnees'):
    os.chdir(dossier)
    fichierLoc=open(fichier,'r')

    chaine=fichierLoc.read()
    listeChaines=chaine.split('\r\n')[:-1]

    tabLoc=[c.split(',') for c in listeChaines]

    emprise=rasterReprojete.extent().toString()
    largeur = rasterReprojete.width()
    hauteur = rasterReprojete.height()
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
>>>>>>> 60ec34743644ca7910b10d5ea4b43a61186b5711

    #pbl de callage
    indexCalageX=0.99
    indexCalageY=1
    largeur = largeur * indexCalageX
    hauteur = hauteur * indexCalageY
<<<<<<< HEAD
=======
>>>>>>> 78f5b1ce9416396adaa33ca6d4c031e73f247c8f
>>>>>>> 60ec34743644ca7910b10d5ea4b43a61186b5711


    tabEmprise=[angle.split(',') for angle in emprise.split(' : ')]

    Coordonnees=[[((int(x) * (float(tabEmprise[1][0])-float(tabEmprise[0][0])))/largeur + float(tabEmprise[0][0])),\
    ((int(y) * (float(tabEmprise[1][1])-float(tabEmprise[0][1])))/hauteur + float(tabEmprise[0][1])),\
    n] \
    for x,y,n in tabLoc]

    ##Creation d'une couche de points
    #Creation du champ:
    fields = QgsFields()
    fields.append(QgsField("NumParcelle", QVariant.String))

    #Creation du writer de la couche
    writer = QgsVectorFileWriter("ptsNumParcelles.shp", "UTF-8", fields, QGis.WKBPoint, QgsCoordinateReferenceSystem(2154), "ESRI Shapefile")

    if writer.hasError() != QgsVectorFileWriter.NoError:
        print "Error when creating shapefile: ",  w.errorMessage()

<<<<<<< HEAD
    # Ajout des entitees:
=======
<<<<<<< HEAD
    # Ajout des entitees:
=======
    # Ajout des entitÃ©es:
>>>>>>> 78f5b1ce9416396adaa33ca6d4c031e73f247c8f
>>>>>>> 60ec34743644ca7910b10d5ea4b43a61186b5711
    for p in Coordonnees:
        fet = QgsFeature()
        fet.setGeometry(QgsGeometry.fromPoint(QgsPoint(p[0],p[1])))
        fet.setAttributes([p[2]])
        writer.addFeature(fet)
<<<<<<< HEAD

    # delete the writer to flush features to disk
=======
<<<<<<< HEAD
=======

    # delete the writer to flush features to disk
>>>>>>> 78f5b1ce9416396adaa33ca6d4c031e73f247c8f
>>>>>>> 60ec34743644ca7910b10d5ea4b43a61186b5711
    del writer

    #layer.dataProvider().addAttributes([QgsField("mytext", QVariant.String), QgsField("myint", QVariant.Int)])
