import gdal

layer=QgsMapLayerRegistry.instance().mapLayersByName("Aulan1_poly_DN0_plus75_p2a75_simp02_fh")[0]
features=layer.getFeatures()

orderedFeatures=[]
for f in features:
    i=0
    while i<len(orderedFeatures) and f['surf']<orderedFeatures[i]['surf']:
        i+=1
    orderedFeatures.insert(i,f)


for f in orderedFeatures:
    fid=f.id()
    print(fid)

    tmp_geom=f.geometry().buffer(5,5)
    gfeatures=layer.getFeatures()
    for g in gfeatures:
        if g.id() != fid:
            #print('in')
            g_geom=g.geometry()
            if tmp_geom.intersects(g_geom):
                tmp_geom = QgsGeometry(tmp_geom.difference(g_geom))
    layer.dataProvider().changeGeometryValues({ fid : tmp_geom })
