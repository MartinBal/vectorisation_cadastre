def delParcelles(layer):
    features=layer.getFeatures()
    idsToDelete=[f.id() for f in features if (f['surf']<100 and f['p2_a']<75)]
    layer.dataProvider().deleteFeatures(idsToDelete)
    