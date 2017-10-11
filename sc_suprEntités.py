def delParcelles(layer):
    features=layer.getFeatures()
    idsToDelete=[f.id() for f in features if (f['surf']<75 or (f['surf']<150 and f['p2_a']<75))]
    layer.dataProvider().deleteFeatures(idsToDelete)
