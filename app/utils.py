import rasterio
from rasterio import DatasetReader
from shapely.wkt import loads, dumps
from shapely.geometry import Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon, GeometryCollection


def add_z_coordinate(geo, z_function):
    if isinstance(geo, Point):
        return Point(geo.x, geo.y, z_function(geo.x, geo.y))
    elif isinstance(geo, LineString):
        new_coords = [(coord[0], coord[1], z_function(coord[0], coord[1])) for coord in geo.coords]
        return LineString(new_coords)
    elif isinstance(geo, Polygon):
        new_exterior_coords = [(coord[0], coord[1], z_function(coord[0], coord[1])) for coord in
                               geo.exterior.coords]
        new_interior_coords = [[(coord[0], coord[1], z_function(coord[0], coord[1])) for coord in int_coords] for
                               int_coords in geo.interiors]
        return Polygon(new_exterior_coords, new_interior_coords)
    elif isinstance(geo, MultiPoint):
        new_geoms = [Point(geom.x, geom.y, z_function(geom.x, geom.y)) for geom in geo.geoms]
        return MultiPoint(new_geoms)
    elif isinstance(geo, MultiLineString):
        new_geoms = [LineString([(coord[0], coord[1], z_function(coord[0], coord[1])) for coord in geom.coords]) for
                     geom in geo.geoms]
        return MultiLineString(new_geoms)
    elif isinstance(geo, MultiPolygon):
        new_geoms = []
        for polygon in geo.geoms:
            new_exterior_coords = [(coord[0], coord[1], z_function(coord[0], coord[1])) for coord in
                                   polygon.exterior.coords]
            new_interior_coords = [[(coord[0], coord[1], z_function(coord[0], coord[1])) for coord in int_coords]
                                   for int_coords in polygon.interiors]
            new_geoms.append(Polygon(new_exterior_coords, new_interior_coords))
        return MultiPolygon(new_geoms)
    elif isinstance(geo, GeometryCollection):
        new_geoms = [add_z_coordinate(g, z_function) for g in geo.geoms]
        return GeometryCollection(new_geoms)
    else:
        raise ValueError("Unsupported geometry type")


# (55-56 с.ш. и 160-161 в.д.)
def get_elevation_data(wkt_geometry, elevation_file):
    geom = loads(wkt_geometry)
    src: DatasetReader
    with rasterio.open(elevation_file, 'r') as src:
        def extropolate(x, y):
            return tuple(src.sample([(x, y)]))[0][0]

        geom = add_z_coordinate(geom, extropolate)

    return dumps(geom, trim=True)
