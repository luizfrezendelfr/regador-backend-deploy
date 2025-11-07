import rasterio
import uuid
from rasterio.mask import mask
import os
from datetime import datetime
from rasterio.windows import Window

def crop_image(fields, date):
    """
    Recorta uma imagem raster (mapa) com base nas coordenadas de um polígono (campo).
    Salva o resultado num ficheiro temporário em /tmp e retorna o caminho.
    """
    geoms = []
    for field in fields:
        field_coordinate = field['coordinates']
        coord = []
        for coordinate in field_coordinate:
            coord.append([coordinate['lng'], coordinate['lat']])
        coord.append([field_coordinate[0]['lng'], field_coordinate[0]['lat']])
        geoms.append({"type": "Polygon", "coordinates": [coord]})

    with rasterio.open(f"images/STA_NDVI_{date}.tif") as src:
        out_image, out_transform = mask(src, geoms, crop=True)

    out_meta = src.meta.copy()
    out_meta.update({"driver": "GTiff",
                       "height": out_image.shape[1],
                       "width": out_image.shape[2],
                       "transform": out_transform})

    # CORRIGIDO: Salva na pasta /tmp permitida pelo Render
    filename = str(uuid.uuid4())
    temp_file_path = f"/tmp/{filename}.tif"

    with rasterio.open(temp_file_path, "w", **out_meta) as dest:
        dest.write(out_image)
        
    return temp_file_path


def getPixelHistory(lon, lat):
    """
    Obtém o histórico de valores de um único pixel (baseado em lon/lat)
    em todas as imagens de mapa disponíveis.
    (Esta era a função em falta)
    """
    values_history = []
    directory = r'images/'
    for filename in os.listdir(directory):
        if filename.startswith("STA_NDVI_"):
            
            date_str = filename.removeprefix('STA_NDVI_').removesuffix('.tif')
            date_obj = datetime.strptime(date_str, "%d_%m_%Y")
            f_date = date_obj.strftime("%d/%m/%Y")
            
            with rasterio.open(f"images/{filename}") as dataset:
                # Converte lon/lat para a linha/coluna do pixel
                py, px = dataset.index(lon, lat)
                
                # Cria uma janela 1x1 para ler esse pixel
                window = Window(px, py, 1, 1)
                
                # Lê o valor da banda 1
                clip = dataset.read(1, window=window)
            
            values_history.append(
                {"f_date": f_date, "date": date_obj, "value": clip[0][0]})

    return sorted(values_history, key=lambda i: i['date'])