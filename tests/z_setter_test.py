import unittest
from shapely.geometry import Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon, GeometryCollection

from app.utils import add_z_coordinate


def z_function(x, y):
    return x + y


class TestAddZCoordinate(unittest.TestCase):
    def test_point(self):
        geo = Point(1, 2)
        expected = Point(1, 2, 3)
        self.assertEqual(add_z_coordinate(geo, z_function), expected)

    def test_line_string(self):
        geo = LineString([(1, 2), (3, 4), (5, 6)])
        expected = LineString([(1, 2, 3), (3, 4, 7), (5, 6, 11)])
        self.assertEqual(add_z_coordinate(geo, z_function), expected)

    def test_polygon(self):
        geo = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
        expected = Polygon([(0, 0, 0), (1, 0, 1), (1, 1, 2), (0, 1, 1)])
        self.assertEqual(add_z_coordinate(geo, z_function), expected)

    def test_multi_point(self):
        geo = MultiPoint([(1, 2), (3, 4), (5, 6)])
        expected = MultiPoint([Point(1, 2, 3), Point(3, 4, 7), Point(5, 6, 11)])
        self.assertEqual(add_z_coordinate(geo, z_function), expected)

    def test_multi_line_string(self):
        geo = MultiLineString([[(1, 2), (3, 4)], [(5, 6), (7, 8)]])
        expected = MultiLineString([[(1, 2, 3), (3, 4, 7)], [(5, 6, 11), (7, 8, 15)]])
        self.assertEqual(add_z_coordinate(geo, z_function), expected)

    def test_multi_polygon(self):
        geo = MultiPolygon([Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]), Polygon([(2, 2), (3, 2), (3, 3), (2, 3)])])
        expected = MultiPolygon([Polygon([(0, 0, 0), (1, 0, 1), (1, 1, 2), (0, 1, 1)]),
                                 Polygon([(2, 2, 4), (3, 2, 5), (3, 3, 6), (2, 3, 5)])])
        self.assertEqual(add_z_coordinate(geo, z_function), expected)

    def test_geometry_collection(self):
        geo = GeometryCollection([Point(1, 2), LineString([(3, 4), (5, 6)])])
        expected = GeometryCollection([Point(1, 2, 3), LineString([(3, 4, 7), (5, 6, 11)])])
        self.assertEqual(add_z_coordinate(geo, z_function), expected)


if __name__ == '__main__':
    unittest.main()
