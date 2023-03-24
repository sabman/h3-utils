from h3_utils import tools
import json
import pytest

# append the parent directory to the path so that we can import the h3_utils module
import sys
sys.path.append(".")


def test_find_cells_for_geojson():
    # Define a GeoJSON polygon to test with
    polygon = {
        "type": "Polygon",
        "coordinates": [
            [
                [-122.440902, 37.743008],
                [-122.439374, 37.743008],
                [-122.439374, 37.741414],
                [-122.440902, 37.741414],
                [-122.440902, 37.743008]
            ]
        ]
    }

    # Call the function with the polygon and a level of 10
    cells, level = tools.find_cells_for_geojson(polygon, 10)

    # Check that the function returns a non-empty list of cells and the correct level
    assert isinstance(cells, set)
    assert len(cells) > 0
    assert level == 10

# test when the polygon doesn't fit in the level
def test_find_cells_for_geojson_level_too_small():
    # load a geojson file
    with open("tests/data/councils/holdfastbay/jettyroad.geojson") as f:
        geojson = json.load(f)
        # get the geometry of the first feature
        geojson = geojson["features"][0]["geometry"]
    
    # Call the function with the polygon and a level of 6
    cells, level = tools.find_cells_for_geojson(geojson, 6)

    # Check that the function returns a non-empty list of cells and the correct level
    assert isinstance(cells, set)
    assert len(cells) > 0
    assert level == 9
