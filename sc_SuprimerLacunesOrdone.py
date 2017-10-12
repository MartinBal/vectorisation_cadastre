# -*- coding: utf-8 -*-

import gdal

#vecteurCadastre=QgsMapLayerRegistry.instance().mapLayersByName("Aulan1_poly_DN0_plus75_p2a75_simp02_fh")[0]

def comblerLacunes(vecteurCadastre, distBuff=1):
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
