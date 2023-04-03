from h3_utils import tools
import json
import pytest
import requests
import fixtures

# append the parent directory to the path so that we can import the h3_utils module
import sys
sys.path.append(".")


def test_find_resolution_for_geojson():
    # url for geojson
    url = "https://gist.githubusercontent.com/sabman/f1aee8de222c263fb0aa4d40409404e7/raw/118150c1d402d5a998a5b180731a98ac33983dad/jettyroad.geojson"
    # load the geojson
    geojson = requests.get(url).json()
    # get the geometry of the first feature
    geojson = geojson["features"][0]["geometry"]
    # call the function
    resolution, cells = tools.find_resolution_for_geojson(geojson, 0.85, 1)
    # check that the resolution is 12
    assert resolution == 12
    assert cells == fixtures.get_cells()


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


def test_find_enclosing_cells():
    with open("tests/data/councils/Maribyrnong-polygon.geojson") as f:
        geo_json = json.load(f)
        geo_json = geo_json["features"][0]["geometry"]

    expected_cells = {'86be6356fffffff', '86be630b7ffffff', '86be6354fffffff'}

    cells, rings = tools.find_enclosing_cells(geo_json, 6)
    assert cells == expected_cells

    # TODO: test the case where the geojson is more than one ring
