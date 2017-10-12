##vectorisation_cadastre=name
##cadastreraster=raster
##cadastrevecteur=output vector
outputs_GDALOGRWARPREPROJECT_1=processing.runalg('gdalogr:warpreproject', cadastreraster,'EPSG:3945','EPSG:2154',None,0.0,0,5,4,75.0,6.0,1.0,False,0,False,None,None)
outputs_SAGAGRIDBUFFER_1=processing.runalg('saga:gridbuffer', outputs_GDALOGRWARPREPROJECT_1['OUTPUT'],2.0,0,None)
outputs_SAGAINVERTDATANODATA_1=processing.runalg('saga:invertdatanodata', outputs_SAGAGRIDBUFFER_1['BUFFER'],None)
outputs_GDALOGRPOLYGONIZE_1=processing.runalg('gdalogr:polygonize', outputs_SAGAINVERTDATANODATA_1['OUTPUT'],'DN',cadastrevecteur)