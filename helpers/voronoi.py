from typing import List, Tuple
import numpy
from geovoronoi import voronoi_regions_from_coords
import shapely.geometry

import pygame


# TODO: Make a version that returns open polygons for points at the outer edge.
# TODO: Use scipy to get the voronoi and then calculate the poygons yourself.
#  See if that is more performant.


def rect_to_shapely_polygon(rect: pygame.Rect) -> shapely.geometry.Polygon:
    return shapely.geometry.Polygon((
        rect.topleft,
        rect.topright,
        rect.bottomright,
        rect.bottomleft
    ))


def generate_voronoi_polygons(
        points: List[Tuple[int, int]],
        outer_polygon: shapely.geometry.Polygon
) -> List[List[pygame.math.Vector2]]:
    """Convert a list of points into a list of polygons. Points at
    the outer edge of the point cloud result in closed polygons.
    """
    # Does not work with less than 3 points.
    if len(points) < 3:
        return []

    poly_shapes = voronoi_regions_from_coords(
        numpy.asarray(points),
        outer_polygon
    )[0]
    polygons = [ps.exterior.coords[:-1] for ps in poly_shapes]
    for i, polygon in enumerate(polygons):
        polygons[i] = [pygame.Vector2(p) for p in polygon]

    return polygons
