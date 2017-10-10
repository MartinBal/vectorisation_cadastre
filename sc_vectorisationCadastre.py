##Polyg_1=name
##cadastreraster=raster
##vect=output vector
import processing


def delParcelles(layer):
    features=layer.getFeatures()
    idsToDelete=[f.id() for f in features if (f['surf']<100 and f['p2_a']<75)]
    layer.dataProvider().deleteFeatures(idsToDelete)

def vectorisationCadastre(r_cadastre, ref_projection='EPSG:3945' ):
	'''fonction permettant de polygoniser le cadastre raster'''

	r_cadastreReprojete=processing.runalg('gdalogr:warpreproject', r_cadastre,ref_projection,'EPSG:2154',None,0.0,0,5,4,75.0,6.0,1.0,False,0,False,None,None)
	
	v_cadastreBrut=processing.runalg('gdalogr:polygonize', r_cadastreReprojete['OUTPUT'],'DN',None)
	
	v_Parcelles0=processing.runalg('qgis:extractbyattribute', v_cadastreBrut['OUTPUT'],'DN',0,'0',None)
	v_parcelles0=processing.runalg('qgis:fieldcalculator', v_Parcelles0['OUTPUT'],'surf',1,10.0,3.0,True,'$area',None)
	v_parcelles0=processing.runalg('qgis:fieldcalculator', v_parcelles0['OUTPUT_LAYER'],'p2_a',0,25.0,2.0,True,'($perimeter)^2/surf',None)
	v_parcellesSelectionnees=processing.runalg('qgis:extractbyattribute', v_parcelles0['OUTPUT_LAYER'],'surf',2,'75',None)
	##v_parcellesSelectionnees=delParcelles(v_parcellesSelectionnees['OUTPUT'])

	return v_parcellesSelectionnees

#parcelles = iface.addVectorLayer(v_parcellesSelectionnees'OUTPUT'], "Parcelles", "ogr")