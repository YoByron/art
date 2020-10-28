import numpy
from typing import List, Tuple
import scipy.spatial


import pygame


WINDOW_SIZE = (1200, 800)
WINDOW_DIAGONAL = numpy.hypot(*WINDOW_SIZE)
WINDOW_RECT = pygame.Rect((0, 0), WINDOW_SIZE)
FPS = 60
BACKGROUND_COLOR = pygame.Color(0, 32, 0)
CIRCLE_COLOR = pygame.Color(0, 96, 255)
CIRCLE_RADIUS = 5
POLYGON_COLOR = pygame.Color(255, 128, 0)


def generate_voronoi_polygons(points: List[Tuple[int, int]]) -> List[Tuple[float, float]]:
    # see voronoi_plot_2d() in
    # https://github.com/scipy/scipy/blob/master/scipy/spatial/_plotutils.py
    # for how to plot the voronoi information
    #
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Voronoi.html

    # scipy.spatial.Voronoi() does not work with less than 3 points.
    if len(points) < 3:
        return []
    vor = scipy.spatial.Voronoi(numpy.array(points))

    # FIXME: This is just copied from https://github.com/scipy/scipy/blob/master/scipy/spatial/_plotutils.py
    #  Make it return the polygons surrounding the regions instead.
    #  Test by filling the polygons in different colors.

    center = vor.points.mean(axis=0)
    segments = []
    vor.ridge_vertices = numpy.asarray(vor.ridge_vertices)
    for pointidx, simplex in zip(vor.ridge_points, vor.ridge_vertices):
        if numpy.all(simplex >= 0):
            segments.append(vor.vertices[simplex])
        else:
            i = simplex[simplex >= 0][0]  # finite end Voronoi vertex
            near_point = vor.vertices[i]

            t = vor.points[pointidx[1]] - vor.points[pointidx[0]]  # tangent
            t /= numpy.linalg.norm(t)
            n = numpy.array([-t[1], t[0]])  # normal

            midpoint = vor.points[pointidx].mean(axis=0)
            direction = numpy.sign(numpy.dot(midpoint - center, n)) * n
            far_point = near_point + direction * WINDOW_DIAGONAL

            segments.append((near_point, far_point))

    return segments


def run() -> None:
    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("art: round voronoi")
    clock = pygame.time.Clock()
    points = []

    # DEBUG
    debug_points = [(300, 200), (800, 100), (800, 700), (200, 600), (600, 400)]
    for p in debug_points:
        points.append(p)
    polygons = generate_voronoi_polygons(points)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    points.append(event.pos)
                    polygons = generate_voronoi_polygons(points)

        window.fill(BACKGROUND_COLOR)

        for point in points:
            pygame.draw.circle(
                window,
                CIRCLE_COLOR,
                point,
                CIRCLE_RADIUS
            )

        for polygon in polygons:
            pygame.draw.line(window, POLYGON_COLOR, polygon[0], polygon[1])
        # NOTE: The polygons at the screen edges will be open.
        #     pygame.draw.aalines(
        #         window,
        #         POLYGON_COLOR,
        #         True,
        #         polygon
        #     )

        pygame.display.flip()


if __name__ == "__main__":
    run()
