# -*- coding: utf-8 -*-

def ajoutParcellesManquantes(cadastreIncomplet, parcellesTampon):
    '''Complete le cadastre avec les parcelles issues du traitement grossier du raster'''
    parcellesTampon.setSelectedFeatures([])
    selections=[]
    for f in parcellesTampon.getFeatures():
        for c in cadastreIncomplet.getFeatures():
            ##TEMPORAIRE###
            if not c.geometry() == None:
            ##TEMPORAIRE###
                if c.geometry().intersects(f.geometry()) or f.geometry().contains(c.geometry()):
                    print f.id()
                    selections.append( f.id() )
                    break
    parcellesTampon.setSelectedFeatures(selections)
    parcellesTampon.invertSelection()

    for f in parcellesTampon.selectedFeatures():
        print(f.id())
        tmp_geom=f.geometry().buffer(4,5)
        cfeatures=cadastreIncomplet.getFeatures()
        for c in cfeatures:
            if c.geometry() != None and c.geometry().intersects(tmp_geom):
                print(f.id())
                tmp_geom = QgsGeometry(tmp_geom.difference(c.geometry()))
    #Des geometries peuvent disparaitre completement
        if tmp_geom != None :
            #parcellesTampon.dataProvider().changeGeometryValues({ f.id() : tmp_geom })
            f.setGeometry(tmp_geom)
            cadastreIncomplet.dataProvider().addFeatures([f])
            print(cadastreIncomplet.featureCount())


    #cadastreComplet = cadastreIncomplet
    #cadastreComplet.dataProvider().addFeatures(parcellesTampon.selectedFeatures())
    #cadastreComplet = iface.addVectorLayer(cadastreIncomplet, "Parcelles_cadastrales", "ogr")

    #QgsMapLayerRegistry.instance().addMapLayer(cadastreInomplet)

    return cadastreIncomplet
