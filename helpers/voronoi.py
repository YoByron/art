from typing import List, Tuple
import numpy
from geovoronoi import voronoi_regions_from_coords
import shapely.geometry

import pygame


def rect_to_shapely_polygon(rect: pygame.Rect) -> shapely.geometry.Polygon:
    # Add a bit distance so that points are guaranteed to be removed before
    # exiting the rect.
    d = 1
    left = rect.left - d
    top = rect.top - d
    right = rect.right + d
    bottom = rect.bottom + d
    return shapely.geometry.Polygon((
        (left, top),
        (right, top),
        (right, bottom),
        (left, bottom)
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


import scipy.spatial


# def voronoi_new(points: List[Tuple[int, int]]) -> List[List[pygame.math.Vector2]]:
#     # # Does not work with less than 3 points.
#     if len(points) < 3:
#         return []
#
#     vor = scipy.spatial.Voronoi(numpy.array(points))
#

    # First calculate all lines where one end is at infinity (-1).
    # Then go through the regions and build one polygon for each region.
    # Then maybe sort the vertices in the polygons if they are not sorted?
    # Close the outer polygons? Repair polygons at the four corners of the window?

#     polygons = []
#     for region in vor.regions:
#         if region and -1 not in region:
#             polygons.append([vor.vertices[i] for i in region])
#
#     return polygons


# My first try at a voronoi function. Might become useful later.

# def generate_voronoi_polygons(points: List[Tuple[int, int]]) -> List[Tuple[float, float]]:
#     # see voronoi_plot_2d() in
#     # https://github.com/scipy/scipy/blob/master/scipy/spatial/_plotutils.py
#     # for how to plot the voronoi information
#     #
#     # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Voronoi.html
#
#     # scipy.spatial.Voronoi() does not work with less than 3 points.
#     if len(points) < 3:
#         return []
#     vor = scipy.spatial.Voronoi(numpy.array(points))
#
#     # FIXME: This is just copied from https://github.com/scipy/scipy/blob/master/scipy/spatial/_plotutils.py
#     #  Make it return the polygons surrounding the regions instead.
#     #  Test by filling the polygons in different colors.
#
#     center = vor.points.mean(axis=0)
#     segments = []
#     vor.ridge_vertices = numpy.asarray(vor.ridge_vertices)
#     for pointidx, simplex in zip(vor.ridge_points, vor.ridge_vertices):
#         if numpy.all(simplex >= 0):
#             segments.append(vor.vertices[simplex])
#         else:
#             i = simplex[simplex >= 0][0]  # finite end Voronoi vertex
#             near_point = vor.vertices[i]
#
#             t = vor.points[pointidx[1]] - vor.points[pointidx[0]]  # tangent
#             t /= numpy.linalg.norm(t)
#             n = numpy.array([-t[1], t[0]])  # normal
#
#             midpoint = vor.points[pointidx].mean(axis=0)
#             direction = numpy.sign(numpy.dot(midpoint - center, n)) * n
#             far_point = near_point + direction * WINDOW_DIAGONAL
#
#             segments.append((near_point, far_point))
#
#     return segments
