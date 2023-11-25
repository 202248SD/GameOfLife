import pygame
import random

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIDTH, HEIGHT = 800, 800
TILE_SIZE = 10
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 120
REFRESH_RATE = 0.5
LINES = False

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def gen(num):
    return set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)])


def draw_grid(positions):
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, WHITE, (*top_left, TILE_SIZE, TILE_SIZE))

    if LINES:
        for row in range(GRID_HEIGHT):
            pygame.draw.line(screen, WHITE, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))
        for col in range(GRID_WIDTH):
            pygame.draw.line(screen, WHITE, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))


def refresh(positions):
    all_neighbors = set()
    new_positions = set()

    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) in [2, 3]:
            new_positions.add(position)

    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) == 3:
            new_positions.add(position)

    return new_positions


def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx > GRID_WIDTH:
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy > GRID_HEIGHT:
                continue
            if dx == 0 and dy == 0:
                continue

            neighbors.append((x + dx, y + dy))
    return neighbors


def main():
    running = True
    playing = False
    drag = False
    count = 0
    life_cycle = 0
    count_freq = int(FPS * REFRESH_RATE)

    positions = set()
    while running:
        clock.tick(FPS)

        if playing:
            count += 1
            life_cycle += 1
        else:
            life_cycle = 0
        if count >= count_freq:
            count = 0
            positions = refresh(positions)

        pygame.display.set_caption(f"Playing  Cycle:{life_cycle // count_freq}" if playing else "Edit")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                drag = True
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)

            if event.type == pygame.MOUSEBUTTONUP:
                drag = False

            if event.type == pygame.MOUSEMOTION and drag:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)

                if pos not in positions:
                    positions.add(pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing
                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0
                if event.key == pygame.K_r:
                    positions = gen(random.randrange(2, 5) * GRID_WIDTH)

        screen.fill(BLACK)
        draw_grid(positions)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
