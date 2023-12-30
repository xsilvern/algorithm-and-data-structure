import pygame
import time
from graph import dijkstra_for_tile_map, a_star_for_tile_map
import queue
import random


def bfs_for_set_merge(graph, x, y, target, change):
    if target == change:
        return False
    q = queue.Queue()
    height = len(graph)
    width = len(graph[0])
    q.put((x, y))
    direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while not q.empty():
        x, y = q.get()
        for dx, dy in direction:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if graph[ny][nx] == target:
                    graph[ny][nx] = change
                    q.put((nx, ny))
    return True


def generate_eller_maze(width, height):
    maze = [[-1 for _ in range(width * 2)] for _ in range(height * 2)]

    sets = [[x for x in range(width)]]
    for i in range(height * 2 - 1):
        for j in range(width * 2 - 1):
            if i % 2 == 0 and j % 2 == 0:
                maze[i][j] = 0

    next_set_num = width
    for y in range(height - 1):
        vertical_dict = dict()
        for x in range(width - 1):
            if random.randint(0, 1) == 0:
                target = max(sets[y][x+1], sets[y][x])
                change = min(sets[y][x+1], sets[y][x])
                if bfs_for_set_merge(sets, x, y, target, change) == False:
                    continue
                if x * 2 + 1 < height * 2 - 1:
                    maze[y * 2][x * 2 + 1] = 0

        for x in range(width):
            if vertical_dict.get(sets[y][x]) == None:
                vertical_dict[sets[y][x]] = 0
            vertical_dict[sets[y][x]] += 1
        sets.append([-1 for _ in range(width)])
        for x in range(width):
            count = vertical_dict[sets[y][x]]
            if count > 0 and random.randint(0, count-1) == 0:
                sets[y + 1][x] = sets[y][x]
                maze[(y + 1) * 2 - 1][x * 2] = 0
                vertical_dict[sets[y][x]] = 0
            else:
                sets[y + 1][x] = next_set_num
                next_set_num += 1

            vertical_dict[sets[y][x]] -= 1
    y += 1
    for x in range(width-1):
        maze[y * 2][x * 2 + 1] = 0
    return maze


class Button:
    y = 50

    def __init__(self, x, y, text, font, padding=10):
        self.text = text
        self.font = font
        text_render = font.render(text, True, BLACK)
        self.rect = pygame.Rect(x, Button.y, text_render.get_width(
        ) + 2 * padding, text_render.get_height() + 2 * padding)
        Button.y += 60

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)
        text_render = self.font.render(self.text, True, BLACK)
        screen.blit(text_render, (self.rect.x + (self.rect.width - text_render.get_width()) // 2,
                                  self.rect.y + (self.rect.height - text_render.get_height()) // 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


pygame.init()


# 창 크기 및 타일 설정
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 20
map_rows, map_cols = 20, 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# 색상 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (200, 200, 200)

tile_map = generate_eller_maze(map_cols//2, map_rows//2)
start = (0, 0)
end = (map_rows-2, map_cols-2)
# 버튼 설정
font = pygame.font.SysFont("malgungothic", 30)
buttons = {
    'dijkstra': Button(500, 50, '다익스트라로 변경', font),
    'astar_manhattan': Button(500, 110, 'A스타(맨해튼)로 변경', font),
    'run': Button(500, 170, '실행', font),
    'remap': Button(500, 230, '맵 재생성', font)
}
selected_algorithm = None


def draw_map():
    for i in range(map_rows):
        for j in range(map_cols):
            rect = pygame.Rect(j * TILE_SIZE, i * TILE_SIZE,
                               TILE_SIZE, TILE_SIZE)
            if tile_map[i][j] == -1:
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, GREY, rect, 1)


def draw_path(path):
    global is_path_drawn
    if is_path_drawn:
        for x, y in path:
            rect = pygame.Rect(y * TILE_SIZE, x * TILE_SIZE,
                               TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, RED, rect)
    else:
        for x, y in path:
            rect = pygame.Rect(y * TILE_SIZE, x * TILE_SIZE,
                               TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, RED, rect)
            pygame.display.flip()
            pygame.time.delay(100)
        is_path_drawn = True


class Button:
    def __init__(self, x, y, text, font, padding=10):
        self.text = text
        self.font = font
        text_render = font.render(text, True, BLACK)
        self.rect = pygame.Rect(x, y, text_render.get_width(
        ) + 2 * padding, text_render.get_height() + 2 * padding)

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)
        text_render = self.font.render(self.text, True, BLACK)
        screen.blit(text_render, (self.rect.x + (self.rect.width - text_render.get_width()) // 2,
                                  self.rect.y + (self.rect.height - text_render.get_height()) // 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


is_running = True
is_path_drawn = False
path = []
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for key, button in buttons.items():
                if button.is_clicked(event.pos):
                    if key == 'dijkstra':
                        selected_algorithm = 'dijkstra'
                    elif key == 'astar_manhattan':
                        selected_algorithm = 'astar_manhattan'
                    elif key == 'run' and selected_algorithm:
                        path = []
                        is_path_drawn = False
                        if selected_algorithm == 'dijkstra':
                            distance, path = dijkstra_for_tile_map(
                                tile_map, start, end)

                        elif selected_algorithm == 'astar_manhattan':
                            distance, path = a_star_for_tile_map(
                                tile_map, start, end)
                    elif key == 'remap':
                        path = []
                        is_path_drawn = False
                        tile_map = generate_eller_maze(
                            map_cols//2, map_rows//2)

    screen.fill(WHITE)
    draw_map()
    for button in buttons.values():
        button.draw(screen)
    if path:
        draw_path(path)
    pygame.display.flip()

pygame.quit()
