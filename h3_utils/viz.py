import folium
import h3
from h3_utils import tools as h3_tools


def visualize_hexagons(hexagons, color="red", folium_map=None):
    """
    hexagons is a list of hexcluster. Each hexcluster is a list of hexagons. 
    eg. [[hex1, hex2], [hex3, hex4]]
    """
    polylines = []
    lat = []
    lng = []
    for hex in hexagons:
        polygons = h3.h3_set_to_multi_polygon([hex], geo_json=False)
        # flatten polygons into loops.
        outlines = [loop for polygon in polygons for loop in polygon]
        polyline = [outline + [outline[0]] for outline in outlines][0]
        lat.extend(map(lambda v: v[0], polyline))
        lng.extend(map(lambda v: v[1], polyline))
        polylines.append(polyline)

    if folium_map is None:
        m = folium.Map(location=[sum(lat)/len(lat), sum(lng) /
                       len(lng)], zoom_start=13, tiles='cartodbpositron')
    else:
        m = folium_map
    for polyline in polylines:
        my_PolyLine = folium.PolyLine(
            locations=polyline, weight=8, color=color)
        m.add_child(my_PolyLine)
    return m


def visualize_polygon(polyline, color):
    polyline.append(polyline[0])
    lat = [p[0] for p in polyline]
    lng = [p[1] for p in polyline]
    m = folium.Map(location=[sum(lat)/len(lat), sum(lng) /
                   len(lng)], zoom_start=13, tiles='cartodbpositron')
    my_PolyLine = folium.PolyLine(locations=polyline, weight=8, color=color)
    m.add_child(my_PolyLine)
    return m


def visualize_geojson_enclosing_cell(geojson, resolution=6):
    # Extract the coordinates from the GeoJSON feature and calculate the average center
    polyline = geojson['coordinates'][0]
    polyline = list(map(lambda v: [v[1], v[0]], polyline))
    polyline.append(polyline[0])
    lat = [p[0] for p in polyline]
    lng = [p[1] for p in polyline]
    avg_center = [sum(lat)/len(lat), sum(lng)/len(lng)]

    # Create a map centered on the feature
    m = folium.Map(location=avg_center, zoom_start=13, tiles='cartodbpositron')

    # Draw the original PolyLine on the map
    my_polyline = folium.PolyLine(locations=polyline, weight=8, color="green")
    m.add_child(my_polyline)

    # Find the hexagons that intersect with the GeoJSON feature
    found_hexagons, level = h3_tools.find_cells_for_geojson(geojson, 6)

    if level > 6:
        hexagons = [h3.h3_to_parent(h, 6) for h in found_hexagons]
    else:
        hexagons = found_hexagons

    # Draw the hexagons on the map
    for hex in hexagons:
        polygons = h3.h3_set_to_multi_polygon([hex], geo_json=False)
        outlines = [loop for polygon in polygons for loop in polygon]
        polyline = [outline + [outline[0]] for outline in outlines][0]
        my_polyline = folium.PolyLine(
            locations=polyline, weight=8, color='red')
        m.add_child(my_polyline)

    # Return the map object
    return m


def visualize_geojson_and_cells(geojson, cells):
    # extract polyline coordinates
    polyline = geojson['coordinates'][0]
    # reverse the coordinates to be [lat, lng] since geojson is [x, y] i.e [lng, lat] but folium likes [lat, lng]
    polyline = list(map(lambda v: [v[1], v[0]], polyline))
    polyline.append(polyline[0])
    lat = [p[0] for p in polyline]
    lng = [p[1] for p in polyline]
    avg_center = [sum(lat)/len(lat), sum(lng)/len(lng)]

    # create a map centered on the feature
    m = folium.Map(
        location=avg_center,
        zoom_start=16.4,
        tiles='cartodbpositron'
    )

    # add original polyline to the map
    my_PolyLine = folium.PolyLine(
        locations=polyline,
        weight=4,
        color="green"
    )
    m.add_child(my_PolyLine)

    # add hexagon boundaries to the map
    polylines = []
    lat = []
    lng = []
    for hex in cells:
        polygons = h3.h3_set_to_multi_polygon([hex], geo_json=False)
        # flatten polygons into loops.
        outlines = [loop for polygon in polygons for loop in polygon]
        polyline = [outline + [outline[0]] for outline in outlines][0]
        lat.extend(map(lambda v: v[0], polyline))
        lng.extend(map(lambda v: v[1], polyline))
        polylines.append(polyline)
    for polyline in polylines:
        my_PolyLine = folium.PolyLine(
            locations=polyline, weight=4, color='red')
        m.add_child(my_PolyLine)

    return m
