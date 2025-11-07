import geopandas as gpd
from shapely.geometry import Polygon

def create_shapefile(coordinates, name, shapefile_path):
    coord = []
    for coordinate in coordinates:
        coord.append([coordinate['lng'], coordinate['lat']])
    coord.append([coordinates[0]['lng'], coordinates[0]['lat']])

    polygon = Polygon(coord)
    gdf = gpd.GeoDataFrame(crs={'init': 'epsg:4326'})
    gdf.loc[0, 'name'] = name
    gdf.loc[0, 'geometry'] = polygon

    # CORRIGIDO: Salva no caminho /tmp fornecido
    gdf.to_file(shapefile_path) 
    return gdf