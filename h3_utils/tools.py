import h3
import shapely
import json


def find_cells_for_geojson(geojson, level):
    """find the h3 cells for a given geojson polygon and level

    Args:
        geojson (dict): dict conforming to geojson geometry spec
        level (int): h3 resolution for which we want to find cells

    Returns:
        set, int: tuple with set of h3 cells and the level
    """

    cells = h3.polyfill(geojson, level, geo_json_conformant=True)
    if len(cells):
        return cells, level
    level += 1
    return find_cells_for_geojson(geojson, level)


def find_resolution_for_geojson(
        geojson, internal_area_ratio=0.9, starting_resolution=1):
    """find the resolution that given a geojson polygon, it will return hexagons that cover the polygon with an internal area to total area ratio.
    Args:
        geojson (dict): dict conforming to geojson geometry spec
        internal_area_ratio (float, optional): ratio of hexagons area that fall within the geojson. Defaults to 0.9.
        starting_resolution (int, optional): resolution at which to start searching for the required coverage. Defaults to 1.

    Returns:
        int, set: resolution and set of h3 cells 
    """
    # starting resolution for search
    cells, resolution = find_cells_for_geojson(geojson, starting_resolution)

    # h3_set_to_multi_polygon
    cells_polygon = h3.h3_set_to_multi_polygon(cells, geo_json=True)

    # convert the tuples in the cells_polygon to arrays
    cells_polygon = [[list(cell) for cell in cells_polygon[0][0]]]
    cells_polygon_geojson = {"type": "Polygon", "coordinates": cells_polygon}

    # convert cells_polygon to shapely polygon
    cells_polygon = shapely.from_geojson(
        json.dumps(cells_polygon_geojson)
    )

    # area_from_shapely = cells_polygon.area
    # print("cells area:", area_from_shapely * 1000000)

    shapely_geojson = shapely.from_geojson(json.dumps(geojson))
    # print("street area:", shapely_geojson.area * 1000000)

    intersection = cells_polygon.intersection(shapely_geojson)
    # print("intersection area:", intersection.area * 1000000)

    # print("intersection percentage:", intersection.area / shapely_geojson.area)

    # Area outside the polygon
    # external_area = cells_polygon.difference(shapely_geojson)
    # print("external area:", external_area.area * 1000000)
    # ratio of internal to external area
    ratio = intersection.area / cells_polygon.area
    # print("=====================================")
    # print("ratio:", ratio, "resolution:", resolution)

    if ratio > internal_area_ratio:
        return resolution, cells
    else:
        resolution += 1
        return find_resolution_for_geojson(
            geojson, internal_area_ratio, resolution
        )
