# -*- coding: utf-8 -*-

def ajoutParcellesManquantes(cadastreIncomplet, parcellesTampon):
    '''ComplÃ¨te le cadastre avec les parcelles issues du traitement grossier du raster'''
    parcellesTampon.setSelectedFeatures([])
    selections=[]
    for f in parcellesTampon.getFeatures():
        for c in cadastreIncomplet.getFeatures():
            print c.id()
            print c.geometry()
            ##TEMPORAIRE###
            if not c.geometry() == None:
            ##TEMPORAIRE###
                if c.geometry().intersects(f.geometry()):
                    selections.append( f.id() )
                    break
    parcellesTampon.setSelectedFeatures(selections)
    parcellesTampon.invertSelection()

    for f in parcellesTampon.selectedFeatures():
        cadastre.addFeature([f])
