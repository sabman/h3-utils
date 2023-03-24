import h3


def find_cells_for_geojson(geojson, level):
    cells = h3.polyfill(geojson, level, geo_json_conformant=True)
    if len(cells):
        return cells, level
    level += 1
    return find_cells_for_geojson(geojson, level)

