import rasterio
import uuid
from rasterio.mask import mask

def crop_image(fields, date):
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

    # CORRIGIDO: Define o caminho temporário
    filename = str(uuid.uuid4())
    temp_file_path = f"/tmp/{filename}.tif"

    # CORRIGIDO: Escreve no caminho /tmp
    with rasterio.open(temp_file_path, "w", **out_meta) as dest:
        dest.write(out_image)

    # CORRIGIDO: Retorna o caminho completo
    return temp_file_path