def jogar():
    import pygame
    import random
    from sys import exit

    # Initialize Pygame
    pygame.init()

    # Set up the game window
    screen = pygame.display.set_mode((600, 640))
    pygame.display.set_caption("Snake")

    # Set up the game clock
    clock = pygame.time.Clock()

    # Initialize game variables
    game_active = True
    Right, Left, Up, Down = False, False, False, False
    apple_X, apple_Y = random.randrange(0, 581, 20), random.randrange(0, 581, 20)
    snake_body = [(300, 300)]
    snake_length = 1

    # Initialize game surfaces
    snake_surface = pygame.Surface((20,20))
    snake_surface.fill('White')
    snake_rect = snake_surface.get_rect(topleft=(300, 300))

    apple_surface = pygame.Surface((20,20))
    apple_surface.fill("Red")
    apple_rect = apple_surface.get_rect(topleft=(apple_X, apple_Y))

    score_font = pygame.font.Font(None, 40)
    score_surf = score_font.render("Score:", True, "Black")
    score_rect = score_surf.get_rect(center=(300, 620))

    bg_surface = pygame.Surface((600, 600))
    bg_surface.fill('Black')

    bg_Score = pygame.Surface((600, 50))
    bg_Score.fill((64, 64, 64))

    # Main game loop
    while True:
        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if game_active:
                if event.type == pygame.KEYDOWN:
                    # Update direction based on arrow key input
                    if event.key == pygame.K_RIGHT and not Left:
                        Right, Left, Up, Down = True, False, False, False
                    elif event.key == pygame.K_LEFT and not Right:
                        Right, Left, Up, Down = False, True, False, False
                    elif event.key == pygame.K_UP and not Down:
                        Right, Left, Up, Down = False, False, True, False
                    elif event.key == pygame.K_DOWN and not Up:
                        Right, Left, Up, Down = False, False, False, True
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Restart the game
                        # Reset game variables to their initial state
                        Right, Left, Up, Down = False, False, False, False
                        apple_X, apple_Y = random.randrange(0, 581, 20), random.randrange(0, 581, 20)
                        snake_body = [(300, 300)]
                        snake_length = 1
                        game_active = True
                        snake_rect.topleft = (300, 300)  # Reset the snake's position

        # Update game state
        if game_active:
            # Move the snake based on direction
            if Right:
                snake_rect.right += 20
            if Left:
                snake_rect.left -= 20
            if Up:
                snake_rect.top -= 20
            if Down:
                snake_rect.bottom += 20

            # Update the snake body and limit its length
            snake_body = [(snake_rect.x, snake_rect.y)] + snake_body
            snake_body = snake_body[:snake_length]

            # Check for collisions with walls
            if (
                snake_rect.left >= 600
                or snake_rect.right <= 0
                or snake_rect.top >= 600
                or snake_rect.bottom <= 0
            ):
                game_active = False

            # Draw game elements on the screen
            screen.blit(bg_surface, (0, 0))
            screen.blit(bg_Score, (0, 600))
            score_surf = score_font.render(f"Score: {len(snake_body) - 1}", True, "Black")
            screen.blit(score_surf, score_rect)

            for body_part in snake_body:
                rect = pygame.Rect(body_part[0], body_part[1], 20, 20)
                screen.blit(snake_surface, rect)
                pygame.draw.rect(screen, "Black", rect, 1)

            apple_rect = pygame.Rect(apple_X, apple_Y, 20, 20)
            screen.blit(apple_surface, apple_rect)
            pygame.draw.rect(screen, "Black", apple_rect, 1)

            # Check for collision with the apple and update score
            if snake_rect.colliderect(apple_rect):
                # Randomly place the apple while avoiding the snake's body
                while True:
                    apple_X = random.randrange(0, 581, 20)
                    apple_Y = random.randrange(0, 581, 20)
                    apple_rect.topleft = (apple_X, apple_Y)

                    # Check if the apple is not on the snake's body
                    if not any(part == apple_rect.topleft for part in snake_body):
                        break

                snake_length += 1

            # Check for self-collision
            if snake_body[0] in snake_body[1:]:
                game_active = False
        else:
            # If game over, fill the screen with black
            screen.blit(bg_surface, (0, 0))
            # Display game over message
            game_over_font = pygame.font.Font(None, 60)
            game_over_surf = game_over_font.render("Game Over", True, "Red")
            game_over_rect = game_over_surf.get_rect(center=(300, 300))
            screen.blit(game_over_surf, game_over_rect)

            # Display restart instructions
            restart_font = pygame.font.Font(None, 40)
            restart_surf = restart_font.render("Press SPACE to restart", True, "White")
            restart_rect = restart_surf.get_rect(center=(300, 400))
            screen.blit(restart_surf, restart_rect)

            # Check for space key press to restart the game
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                # Reset game variables to their initial state
                Right, Left, Up, Down = False, False, False, False
                apple_X, apple_Y = random.randrange(0, 581, 20), random.randrange(0, 581, 20)
                snake_body = [(300, 300)]
                snake_length = 1
                game_active = True
                snake_rect.topleft = (300, 300)  # Reset the snake's position

        # Update the display and set the game speed
        pygame.display.update()
        clock.tick(7)


if __name__ == '__main__':
    jogar()
