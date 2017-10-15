# -*- coding: utf-8 -*-

#Pre-requis : qgis et SAGA

import processing
import gdal
import os
import pickle
from PyQt4.QtCore import *


#rasterCadastre=QgsMapLayerRegistry.instance().mapLayersByName("26041010180000A010250002")[0]

def vectorisationCadastre(rasterCadastre, ref_projection='EPSG:3945' ):
    '''fonction permettant de polygoniser le cadastre raster'''

    #reprojection du cadastre en RGF93 - Lambert93 (EPSG : 2154)
    ref_rasterCadastre_reproj=processing.runalg('gdalogr:warpreproject', rasterCadastre,ref_projection,'EPSG:2154',None,0.0,0,5,4,75.0,6.0,1.0,False,0,False,None,None)
    fileName = ref_rasterCadastre_reproj['OUTPUT']
    fileInfo = QFileInfo('rasterReproj')
    baseName = fileInfo.baseName()
    rasterCadastre_reproj = QgsRasterLayer(fileName, baseName)

    #### Polygonisation finne
    ref_vecteurCadastre=processing.runalg('gdalogr:polygonize', ref_rasterCadastre_reproj['OUTPUT'],'DN',None)
    ref_vecteurCadastre=processing.runalg('qgis:extractbyattribute', ref_vecteurCadastre['OUTPUT'],'DN',0,'0',None)

    # Affinage
    ref_vecteurCadastre=processing.runalg('qgis:fillholes', ref_vecteurCadastre['OUTPUT'],150.0,None)
    ref_vecteurCadastre=processing.runalg('qgis:simplifygeometries', ref_vecteurCadastre['Results'],0.25,None)

    #calcul des champs surface et p2_a
    ref_vecteurCadastre=processing.runalg('qgis:fieldcalculator', ref_vecteurCadastre['OUTPUT'],'surf',1,10.0,3.0,True,'$area',None)
    ref_vecteurCadastre=processing.runalg('qgis:fieldcalculator', ref_vecteurCadastre['OUTPUT_LAYER'],'p2_a',0,25.0,2.0,True,'($perimeter)^2/surf',None)

    #Affichage de la couche
    vecteurCadastre = iface.addVectorLayer(ref_vecteurCadastre['OUTPUT_LAYER'], "ParcellesCadastrales", "ogr")

    #Suppression des artéfactes (traces de lettres et symboles)
    netoyerParcelles(vecteurCadastre)

    #Comblement lacunes
    comblerLacunes(vecteurCadastre)

    #Suppression de la parcelle cadre
    supprimerCadre(vecteurCadastre)

    ####Extraction des parcelles tampon (polygonisation grossière)
    ref_vecteurCadastreTampon=vectorisationTampon(ref_rasterCadastre_reproj)

    vecteurCadastreTampon = iface.addVectorLayer(ref_vecteurCadastreTampon['OUTPUT_LAYER'], "ParcellesCadastralesTampon", "ogr")
    netoyerParcelles(vecteurCadastreTampon)

    #Comblement du polygonne fin avec parcelle tampon

    ajoutParcellesManquantes(vecteurCadastre, vecteurCadastreTampon)

    supprimerCadre(vecteurCadastre)

    #affectation des numéros
    ###########
    #Pour trouver le Loc on peut utiliser
    #rasterCadastre.source()
    ##################

    ptsNumParcelles=numeroterParcelles(rasterCadastre_reproj)
    affecterNum(vecteurCadastre, ptsNumParcelles)
    #ref_vecteurCadastre=processing.runalg('qgis:joinattributesbylocation', vecteurCadastre,pointsNum,['contains'],0.0,0,None,1,None)

    #vecteurCadastreNumerote = iface.addVectorLayer(ref_vecteurCadastreTampon['OUTPUT_LAYER'], "ParcellesCadastralesNumerotees", "ogr")


def netoyerParcelles(coucheParcelles, surfMax1=75, surfMax2=100, p2_aMax=75):
    '''Fonction permettant de supprimer sur une couche vecteur les atéfactes liés à
    la polygonisation des lettres et symboles.
    Attention la couche en entrée est modifiée.
    Critères : surf < surfMax1 OU (surf<surfMax2 ET p2_aMax<75)'''

    features=coucheParcelles.getFeatures()
    idsToDelete=[f.id() for f in features if f['surf']<surfMax1 or (f['surf']<surfMax2 and f['p2_a']<p2_aMax)]
    coucheParcelles.dataProvider().deleteFeatures(idsToDelete)

def comblerLacunes(vecteurCadastre, distBuff=0.75):
    '''Comble les lacunes entre les parcelles par iteration d'un tampon puis différenciation'''
    features=vecteurCadastre.getFeatures()

    #Ordonner les entités de la plus grande à la plus petite
    #N.B. Ordonner les entités permet de faire ressortir les petites entités incluses et recouvertes par fillholes
    orderedFeatures=[]
    for f in features:
        i=0
        while i<len(orderedFeatures) and f['surf']<orderedFeatures[i]['surf']:
            i+=1
        orderedFeatures.insert(i,f)


    for f in orderedFeatures:
        fid=f.id()

        tmp_geom=f.geometry().buffer(distBuff,5)
        gfeatures=vecteurCadastre.getFeatures()
        for g in gfeatures:
            if g.id() != fid:
                g_geom=g.geometry()
                if tmp_geom.intersects(g_geom):
                    tmp_geom = QgsGeometry(tmp_geom.difference(g_geom))
        #Des geometries peuvent disparaitre complètement
        if tmp_geom == None :
            vecteurCadastre.dataProvider().deleteFeatures([fid])
        else:
            vecteurCadastre.dataProvider().changeGeometryValues({ fid : tmp_geom })

def vectorisationTampon(ref_rasterCadastre_reproj, distBuff=4, maxRing=1000 ):
    '''fonction permettant de polygoniser le cadastre raster'''

    ref_rasterCadastre=processing.runalg('saga:gridbuffer', ref_rasterCadastre_reproj['OUTPUT'],distBuff,0,None)
    ref_rasterCadastre=processing.runalg('saga:invertdatanodata', ref_rasterCadastre['BUFFER'],None)
    ref_vecteurCadastre=processing.runalg('gdalogr:polygonize', ref_rasterCadastre['OUTPUT'],'DN',None)

    ref_vecteurCadastre=processing.runalg('qgis:fillholes', ref_vecteurCadastre['OUTPUT'],maxRing,None)
    ref_vecteurCadastre=processing.runalg('qgis:simplifygeometries', ref_vecteurCadastre['Results'],0.25,None)
    ref_vecteurCadastre=processing.runalg('qgis:fieldcalculator', ref_vecteurCadastre['OUTPUT'],'surf',0,10.0,2.0,True,'$area',None)
    ref_vecteurCadastre=processing.runalg('qgis:fieldcalculator', ref_vecteurCadastre['OUTPUT_LAYER'],'p2_a',0,25.0,2.0,True,'($perimeter)^2/surf',None)

    return ref_vecteurCadastre
    vecteurCadastreTampon = iface.addVectorLayer(ref_vecteurCadastre['OUTPUT_LAYER'], "ParcellesTampon", "ogr")

    netoyerParcelles(vecteurCadastreTampon)

def ajoutParcellesManquantes(cadastreIncomplet, parcellesTampon):
    '''Complete le cadastre avec les parcelles issues du traitement grossier du raster'''

    parcellesTampon.setSelectedFeatures([])
    selections=[]

    for f in parcellesTampon.getFeatures():
        for c in cadastreIncomplet.getFeatures():
            if c.geometry().intersects(f.geometry()) :
                selections.append( f.id() )
                break
    parcellesTampon.setSelectedFeatures(selections)
    parcellesTampon.invertSelection()

    for f in parcellesTampon.selectedFeatures():
        tmp_geom=f.geometry().buffer(5,5)
        cfeatures=cadastreIncomplet.getFeatures()
        for c in cfeatures:
            if c.geometry().intersects(tmp_geom):
                tmp_geom = QgsGeometry(tmp_geom.difference(c.geometry()))
    #Des geometries peuvent disparaitre completement
        if tmp_geom != None :
            #parcellesTampon.dataProvider().changeGeometryValues({ f.id() : tmp_geom })
            f.setGeometry(tmp_geom)
            cadastreIncomplet.dataProvider().addFeatures([f])

def supprimerCadre(vecteurCadastre):
    features=vecteurCadastre.getFeatures()
    featCadre=features.next()
    for f in features:
        if f['surf']>featCadre['surf']: featCadre=f
    vecteurCadastre.dataProvider().deleteFeatures([featCadre.id()])

def numeroterParcelles(rasterReprojete, fichier='Feuille CL0180000A01 AULAN - 026/26041010180000A01.LOC', dossier='/home/martin/Documents/Permagro/Mission1_PALUD/donnees'):
    os.chdir(dossier)
    fichierLoc=open(fichier,'r')

    chaine=fichierLoc.read()
    listeChaines=chaine.split('\r\n')[:-1]

    tabLoc=[c.split(',') for c in listeChaines]

    emprise=rasterReprojete.extent().toString()
    largeur = rasterReprojete.width()
    hauteur = rasterReprojete.height()

    #pbl de callage
    indexCalageX=0.99
    indexCalageY=1
    largeur = largeur * indexCalageX
    hauteur = hauteur * indexCalageY

    tabEmprise=[angle.split(',') for angle in emprise.split(' : ')]

    Coordonnees=[[((int(x) * (float(tabEmprise[1][0])-float(tabEmprise[0][0])))/largeur + float(tabEmprise[0][0])),\
    ((int(y) * (float(tabEmprise[1][1])-float(tabEmprise[0][1])))/hauteur + float(tabEmprise[0][1])),\
    n] \
    for x,y,n in tabLoc]

    ##Creation d'une couche de points
    #Creation du champ:
    fields = QgsFields()
    fields.append(QgsField("NumPar", QVariant.String))

    #Creation du writer de la couche
    ptsNumParcelles=QgsVectorLayer("Point", "ptsNumParcelles", "memory")
    ptsNumParcelles.startEditing()
    ptsNumParcelles.dataProvider().addAttributes(fields)
    ptsNumParcelles.commitChanges()

    # Ajout des entitees:
    for p in Coordonnees:
        feat = QgsFeature()
        feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(p[0],p[1])))
        feat.setAttributes([p[2]])
        ptsNumParcelles.dataProvider().addFeatures([feat])
    return ptsNumParcelles

def affecterNum(vecteurCadastre, ptsNumParcelles):
    NumChamp=vecteurCadastre.pendingFields().count()

    vecteurCadastre.startEditing()
    vecteurCadastre.dataProvider().addAttributes([QgsField("NumPar", QVariant.String)])
    vecteurCadastre.commitChanges()
    dict={}

    for f in ptsNumParcelles.getFeatures():
        for g in vecteurCadastre.getFeatures():
            if g.geometry().contains(f.geometry()):
                dict[g.id()]={NumChamp : f["NumPar"] }
                break
                break
    vecteurCadastre.startEditing()
    vecteurCadastre.dataProvider().changeAttributeValues(dict)
    vecteurCadastre.commitChanges()
