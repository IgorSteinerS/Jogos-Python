from sys import exit
import pygame

WIDTH, HEIGHT = 800, 600
FPS = 30

PADDLE_SPEED = 8
BALL_SPEED_X = 9
BALL_SPEED_Y = 9

WHITE = "White"
BLACK = "Black"

CENTER = (WIDTH // 2, HEIGHT // 2)


def init():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()
    return screen, clock


def create_assets():
    paddle = pygame.Surface((10, 75))
    paddle.fill(WHITE)

    ball = pygame.Surface((12, 12))
    ball.fill(WHITE)

    bg = pygame.Surface((WIDTH, HEIGHT))
    bg.fill(BLACK)

    return paddle, ball, bg


def create_fonts():
    return pygame.font.Font(None, 80)


def reset_state():
    return {
        "player": pygame.Rect(5, 300, 10, 75),
        "enemy": pygame.Rect(WIDTH - 15, 300, 10, 75),
        "ball": pygame.Rect(WIDTH // 2, HEIGHT // 2, 12, 12),
        "ball_dir": [BALL_SPEED_X, BALL_SPEED_Y],
        "player_score": 0,
        "enemy_score": 0,
        "player_speed": 0,
        "enemy_speed": 0,
    }


def handle_keydown(event, state):
    adjust_key_speed(event.key, state, 1)


def handle_keyup(event, state):
    adjust_key_speed(event.key, state, -1)


KEY_ACTIONS = {
    pygame.K_w: ("player_speed", -1),
    pygame.K_s: ("player_speed", 1),
    pygame.K_UP: ("enemy_speed", -1),
    pygame.K_DOWN: ("enemy_speed", 1),
}


def adjust_key_speed(key, state, factor):

    action = KEY_ACTIONS.get(key)
    if not action:
        return
    field, direction = action
    state[field] += direction * PADDLE_SPEED * factor


def move_objects(state):
    state["ball"].x += state["ball_dir"][0]
    state["ball"].y += state["ball_dir"][1]

    state["player"].y += state["player_speed"]
    state["enemy"].y += state["enemy_speed"]


def clamp_paddles(state):
    for paddle in ["player", "enemy"]:
        rect = state[paddle]
        rect.y = max(0, min(rect.y, HEIGHT - rect.height))


def handle_ball_collision(state):
    ball = state["ball"]

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        state["ball_dir"][1] *= -1

    if ball.left <= 0:
        state["enemy_score"] += 1
        reset_ball(state)

    if ball.right >= WIDTH:
        state["player_score"] += 1
        reset_ball(state)

    if ball.colliderect(state["player"]) or ball.colliderect(state["enemy"]):
        state["ball_dir"][0] *= -1


def reset_ball(state):
    state["ball"].center = CENTER
    state["ball_dir"] = [BALL_SPEED_X, BALL_SPEED_Y]


def render(screen, state, assets, font):
    paddle_surf, ball_surf, bg = assets

    screen.blit(bg, (0, 0))

    screen.blit(paddle_surf, state["player"])
    screen.blit(paddle_surf, state["enemy"])
    screen.blit(ball_surf, state["ball"])

    p_score = font.render(str(state["player_score"]), True, WHITE)
    e_score = font.render(str(state["enemy_score"]), True, WHITE)

    screen.blit(p_score, (200, 100))
    screen.blit(e_score, (600, 100))


def jogar():
    screen, clock = init()
    assets = create_assets()
    font = create_fonts()

    state = reset_state()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                handle_keydown(event, state)

            if event.type == pygame.KEYUP:
                handle_keyup(event, state)

        move_objects(state)
        clamp_paddles(state)
        handle_ball_collision(state)

        render(screen, state, assets, font)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    jogar()
