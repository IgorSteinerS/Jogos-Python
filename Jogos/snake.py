import random
from sys import exit
import pygame

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 640
GAME_AREA = 600
GRID_SIZE = 20
FPS = 7

BLACK = "Black"
WHITE = "White"
RED = "Red"

INITIAL_POS = (300, 300)

DIRECTIONS = {
    pygame.K_RIGHT: (1, 0),
    pygame.K_LEFT: (-1, 0),
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
}

def init():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    return screen, clock


def reset():
    return {
        "direction": (1, 0), 
        "snake": [INITIAL_POS],
        "length": 1,
        "apple": spawn_apple([INITIAL_POS]),
        "active": True,
    }

def spawn_apple(snake):
    while True:
        pos = (
            random.randrange(0, GAME_AREA, GRID_SIZE),
            random.randrange(0, GAME_AREA, GRID_SIZE),
        )
        if pos not in snake:
            return pos

def handle_input(event, state):
    if event.key not in DIRECTIONS:
        return

    new_dir = DIRECTIONS[event.key]
    current = state["direction"]

    # impede reversão direta
    if (new_dir[0] * -1, new_dir[1] * -1) != current:
        state["direction"] = new_dir


def move_snake(state, rect):
    dx, dy = state["direction"]

    rect.x += dx * GRID_SIZE
    rect.y += dy * GRID_SIZE

    return rect


def update_body(state, rect):
    state["snake"] = [(rect.x, rect.y)] + state["snake"]
    state["snake"] = state["snake"][: state["length"]]


def hit_wall(rect):
    return not (0 <= rect.x < GAME_AREA and 0 <= rect.y < GAME_AREA)


def hit_self(body):
    return body[0] in body[1:]


def hit_apple(rect, apple_rect):
    return rect.colliderect(apple_rect)


def draw(screen, state, assets, fonts, apple_pos):
    snake_surf, apple_surf, bg, bg_score = assets
    score_font = fonts

    screen.blit(bg, (0, 0))
    screen.blit(bg_score, (0, GAME_AREA))

    score = len(state["snake"]) - 1
    text = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (250, 610))

    for part in state["snake"]:
        rect = pygame.Rect(part[0], part[1], GRID_SIZE, GRID_SIZE)
        screen.blit(snake_surf, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)

    apple_rect = pygame.Rect(apple_pos[0], apple_pos[1], GRID_SIZE, GRID_SIZE)
    screen.blit(apple_surf, apple_rect)
    pygame.draw.rect(screen, BLACK, apple_rect, 1)

    return apple_rect


def game_over(screen, assets):
    _, _, bg, _ = assets

    font_big = pygame.font.Font(None, 60)
    font_small = pygame.font.Font(None, 40)

    screen.blit(bg, (0, 0))

    title = font_big.render("Game Over", True, RED)
    msg = font_small.render("Press SPACE to restart", True, WHITE)

    screen.blit(title, title.get_rect(center=(300, 300)))
    screen.blit(msg, msg.get_rect(center=(300, 400)))


def load_assets():
    snake = pygame.Surface((GRID_SIZE, GRID_SIZE))
    snake.fill(WHITE)

    apple = pygame.Surface((GRID_SIZE, GRID_SIZE))
    apple.fill(RED)

    bg = pygame.Surface((GAME_AREA, GAME_AREA))
    bg.fill(BLACK)

    bg_score = pygame.Surface((SCREEN_WIDTH, 40))
    bg_score.fill((60, 60, 60))

    return snake, apple, bg, bg_score


def load_fonts():
    return pygame.font.Font(None, 40)


def jogar():
    screen, clock = init()
    assets = load_assets()
    font = load_fonts()

    state = reset()

    snake_rect = pygame.Rect(*INITIAL_POS, GRID_SIZE, GRID_SIZE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if state["active"]:
                    handle_input(event, state)
                elif event.key == pygame.K_SPACE:
                    state = reset()
                    snake_rect.topleft = INITIAL_POS

        if state["active"]:
            snake_rect = move_snake(state, snake_rect)
            update_body(state, snake_rect)

            if hit_wall(snake_rect) or hit_self(state["snake"]):
                state["active"] = False

            apple_rect = draw(screen, state, assets, font, state["apple"])

            if hit_apple(snake_rect, apple_rect):
                state["length"] += 1
                state["apple"] = spawn_apple(state["snake"])

        else:
            game_over(screen, assets)

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                state = reset()
                snake_rect.topleft = INITIAL_POS

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    jogar()