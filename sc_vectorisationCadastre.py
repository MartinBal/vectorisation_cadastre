# -*- coding: utf-8 -*-

#Pre-requis : qgis et SAGA

import processing
import gdal


#rasterCadastre=QgsMapLayerRegistry.instance().mapLayersByName("26041010180000A010250002")[0]

def vectorisationCadastre(rasterCadastre, ref_projection='EPSG:3945' ):
    '''fonction permettant de polygoniser le cadastre raster'''

    #reprojection du cadastre en RGF93 - Lambert93 (EPSG : 2154)
    ref_rasterCadastre=processing.runalg('gdalogr:warpreproject', rasterCadastre,ref_projection,'EPSG:2154',None,0.0,0,5,4,75.0,6.0,1.0,False,0,False,None,None)

    #### Polygonisation finne
    ref_vecteurCadastre=processing.runalg('gdalogr:polygonize', ref_rasterCadastre['OUTPUT'],'DN',None)
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
    features=vecteurCadastre.getFeatures()
    featCadre=features.next()
    for f in features:
        if f['surf']>featCadre['surf']: featCadre=f
    vecteurCadastre.dataProvider().deleteFeatures([featCadre.id()])

    #Comblement des parcelles avec les parcelles Tampon

    ####Extraction des parcelles tampon (polygonisation grossière)
    # RasterBuffer 4m
    # Invert data/noData
    # Polygonisation
    # Fill holes 200?
    # simplification 0,25
    # Calcul des indexs
    #Suppression des artéfactes (s<75 ou s<100 et p2_a<75)

    #Comblement du polygonne fin
    #Affinage

    #affectation des numéros

    #verification des erreurs



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
        print(fid)

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
