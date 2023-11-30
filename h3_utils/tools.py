import h3
import shapely
import json

MAX_RES = 15

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

    shapely_geojson = shapely.from_geojson(json.dumps(geojson))

    intersection = cells_polygon.intersection(shapely_geojson)
    # Area outside the polygon
    ratio = intersection.area / cells_polygon.area

    if ratio > internal_area_ratio:
        return resolution, cells
    else:
        resolution += 1
        if resolution > MAX_RES: # base case
            return MAX_RES, cells
        return find_resolution_for_geojson(
            geojson, internal_area_ratio, resolution
        )


def find_enclosing_cells(geo_json: dict, level: int) -> tuple:
    """find the h3 cells that enclose a given geojson polygon and level

    Args:
        geojson (dict): dict conforming to geojson geometry spec
        level (int): h3 resolution for which we want to find cells

    Returns:
        set, int: tuple with set of h3 cells and the level
    """
    # initial cells
    cells, _level = find_cells_for_geojson(geo_json, level)
    initial_cell = list(cells)[0]
    if _level > level:
        # get the parent cell at the level requested
        initial_cell = h3.h3_to_parent(list(cells)[0], level)
        # append the initial cell to the cells
        cells.add(initial_cell)

    cells_from_ring, ring_no = _find_ring_containing_geojson(
        initial_cell, geo_json)

    # remove cells that don't intersect the geo_json
    cells_from_ring = _remove_cells_not_intersecting_geojson(
        cells_from_ring, geo_json)

    return cells_from_ring, ring_no


def _find_ring_containing_geojson(cell: str, geo_json: dict) -> tuple:
    """Find the ring of cells containing the geo_json"""
    contained = False
    ring_no = 1
    # create a set to hold the cells with initial cell
    cells = set([cell])

    while not contained:
        # get the ring of cells at the ring_no
        ring = h3.k_ring(cell, ring_no)
        # add the ring to the cells
        cells = cells.union(ring)
        # get the merged boundary of the cells and check if it contains the geo_json
        merged_boundary = _cells2boundary(ring)
        # check if the merged boundary contains the geo_json
        if merged_boundary.contains(shapely.geometry.shape(geo_json)):
            contained = True
        else:
            ring_no += 1

    return cells, ring_no


def _cells2boundary(cells: set) -> shapely.geometry.Polygon:
    merged_boundary = h3.h3_set_to_multi_polygon(cells, geo_json=True)
    merged_boundary = [[list(cell) for cell in merged_boundary[0][0]]]
    merged_boundary_geojson = {
        "type": "Polygon", "coordinates": merged_boundary}
    # convert cells_polygon to shapely polygon
    merged_boundary = shapely.from_geojson(
        json.dumps(merged_boundary_geojson)
    )
    return merged_boundary


def _remove_cells_not_intersecting_geojson(cells: set, geo_json: dict) -> set:
    """Remove cells that don't intersect the geo_json"""
    cells_to_remove = set()
    for cell in cells:
        cell_polygon = _cells2boundary(set([cell]))
        if not cell_polygon.intersection(shapely.geometry.shape(geo_json)):
            cells_to_remove.add(cell)
    cells = cells.difference(cells_to_remove)
    return cells
