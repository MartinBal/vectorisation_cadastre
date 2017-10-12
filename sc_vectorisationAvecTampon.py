# -*- coding: utf-8 -*-

import processing

def vectorisationTampon(rasterCadastre, ref_projection='EPSG:3945', distBuff=4, maxRing=250 ):
    '''fonction permettant de polygoniser le cadastre raster'''

    #reprojection du cadastre en RGF93 - Lambert93 (EPSG : 2154)
    ref_rasterCadastre=processing.runalg('gdalogr:warpreproject', rasterCadastre,ref_projection,'EPSG:2154',None,0.0,0,5,4,75.0,6.0,1.0,False,0,False,None,None)

    ref_rasterCadastre=processing.runalg('saga:gridbuffer', ref_rasterCadastre['OUTPUT'],distBuff,0,None)
    ref_rasterCadastre=processing.runalg('saga:invertdatanodata', ref_rasterCadastre['BUFFER'],None)
    ref_vecteurCadastre=processing.runalg('gdalogr:polygonize', ref_rasterCadastre['OUTPUT'],'DN',None)

    ref_vecteurCadastre=processing.runalg('qgis:fillholes', ref_vecteurCadastre['OUTPUT'],maxRing,None)
    ref_vecteurCadastre=processing.runalg('qgis:simplifygeometries', ref_vecteurCadastre['Results'],0.25,None)
    ref_vecteurCadastre=processing.runalg('qgis:fieldcalculator', ref_vecteurCadastre['OUTPUT'],'surf',0,10.0,2.0,True,'$area',None)
    ref_vecteurCadastre=processing.runalg('qgis:fieldcalculator', ref_vecteurCadastre['OUTPUT_LAYER'],'p2_a',0,25.0,2.0,True,'($perimeter)^2/surf',None)

    vecteurCadastreTampon = iface.addVectorLayer(ref_vecteurCadastre['OUTPUT_LAYER'], "ParcellesCadastrales", "ogr")

    netoyerParcelles(vecteurCadastreTampon)
