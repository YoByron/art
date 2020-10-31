from typing import List

import pygame


def cut(
        points: List[pygame.math.Vector2],
        ratio: float,
        iterations: int = 1,
        is_open: bool = False
) -> List[pygame.math.Vector2]:
    """ Chaikin's corner cutting algorithm.
    ratio: Ratio (between 0 and 1) of the edge length which
        determines how close to the corner the cut should be made.
    iterations: Number of iterations of the cutting algorithm.
    """
    # Avoid cutting over the line midpoint:
    if ratio > 0.5:
        ratio = 1 - ratio

    for _ in range(iterations):
        new_points = []
        n = len(points)
        if is_open:
            n -= 1
        for i in range(n):
            a = points[i]
            b = points[(i + 1) % len(points)]
            new_points.append(a.lerp(b, ratio))
            new_points.append(b.lerp(a, ratio))

        # For open polygons keep the original endpoints:
        if is_open:
            new_points[0] = points[0]
            new_points[-1] = points[-1]

        points = new_points

    return points
