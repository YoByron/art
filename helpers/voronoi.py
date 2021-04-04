from typing import List, Tuple

import scipy.spatial
import numpy as np
import pygame


def get_voronoi_polygons(points: List[Tuple[int, int]]) -> List[List[pygame.math.Vector2]]:
    vor = scipy.spatial.Voronoi(np.asarray(points))
    vertices = [pygame.Vector2(*v) for v in vor.vertices]
    polygons = []
    for region in vor.regions:
        if region and -1 not in region:
            polygons.append([vertices[i] for i in region])
    return polygons


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
