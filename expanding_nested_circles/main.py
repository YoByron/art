# inspiration: https://www.reddit.com/r/generative/comments/kyb93x/genuary_16_circles_i_contain_multitudes

# Ideas:
# - Let the small circles grow faster, eventually becoming bigger than their parents?
# - Fix the circles edges becoming slower over time. Maybe the idea above will
#   help with this?
# - Calculate growth rate and/or new radius once and then pass the values into
#   the circle tree as a list. Because all circles of the same depth have the
#   same radius.


import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import pygame.freetype


DEBUG = True
WINDOW_SIZE = (800, 800)
FPS = 60
BACKGROUND_COLOR = pygame.Color(32, 32, 32)
CIRCLE_COLOR = pygame.Color(255, 200, 30)
N_CIRCLE_CHILDREN = 5
MAX_DEPTH = 5
GROWTH_RATE = 30  # pixels per second
CHILD_DIRECTIONS = []
up = pygame.Vector2(0, -1)
for i in range(N_CIRCLE_CHILDREN):
    CHILD_DIRECTIONS.append(up.rotate(360 / N_CIRCLE_CHILDREN * i))
RADIUS_SHRINKAGE = 1 / 3


class Circle:
    def __init__(self, center, radius, depth, direction):
        self.radius = radius
        self.center = center
        self.direction = direction
        self.depth = depth
        self.children = []
        if depth < MAX_DEPTH:
            for cd in CHILD_DIRECTIONS:
                self.children.append(Circle(
                    self.center + self.radius * cd,
                    radius * RADIUS_SHRINKAGE,
                    depth + 1,
                    cd
                ))
                # print(cd * self.radius)

    def update(self, dt):
        self.radius += GROWTH_RATE * dt
        for child in self.children:
            child.center = self.center + self.radius * child.direction
            child.update(dt)

    def draw(self, target_surface):
        pygame.draw.circle(
            target_surface,
            CIRCLE_COLOR,
            self.center,
            self.radius,
            1
        )
        for child in self.children:
            child.draw(target_surface)


def run() -> None:
    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("art: expanding nested circles")
    clock = pygame.time.Clock()
    is_paused = True
    is_reversed = False

    font = pygame.freetype.SysFont("inconsolate, consolas, monospace", 16)
    font.fgcolor = pygame.Color(255, 255, 255)
    font.bgcolor = BACKGROUND_COLOR

    circles = Circle(
        pygame.Vector2(window.get_rect().center),
        window.get_width() // 5,
        1,
        pygame.Vector2()
    )
    relative_radii = [1]
    for i in range(1, N_CIRCLE_CHILDREN):
        relative_radii.append(1 / N_CIRCLE_CHILDREN**i)
    print(relative_radii)

    while True:
        dt = clock.tick(FPS) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_SPACE:
                    is_paused = not is_paused
                elif event.key == pygame.K_BACKSPACE:
                    is_reversed = not is_reversed
        if not is_paused:
            if is_reversed:
                dt *= -1
            circles.update(dt)
        window.fill(BACKGROUND_COLOR)
        circles.draw(window)
        if DEBUG:
            font.render_to(
                window,
                (5, 5),
                f"fps: {clock.get_fps():.0f}"
            )
        pygame.display.flip()


if __name__ == "__main__":
    run()
