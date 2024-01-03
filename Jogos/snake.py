import pygame
import random
from sys import exit

class SnakeGame:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the game window
        self.screen = pygame.display.set_mode((600, 640))
        pygame.display.set_caption("Snake")

        # Set up the game clock
        self.clock = pygame.time.Clock()

        # Initialize game variables
        self.game_active = True
        self.Right, self.Left, self.Up, self.Down = False, False, False, False
        self.apple_X, self.apple_Y = random.randrange(0, 581, 20), random.randrange(0, 581, 20)
        self.snake_body = [(300, 300)]
        self.snake_length = 1

        # Initialize game surfaces
        self.initialize_surfaces()

    def initialize_surfaces(self):
        # Load and scale snake image
        self.snake_surface = pygame.Surface((20,20))
        self.snake_surface.fill('White')
        self.snake_rect = self.snake_surface.get_rect(topleft=(300, 300))
        

        # Load and scale apple image
        self.apple_surface = pygame.Surface((20,20))
        self.apple_surface.fill("Red")
        self.apple_rect = self.apple_surface.get_rect(topleft=(self.apple_X, self.apple_Y))

        # Set up score display
        self.score_font = pygame.font.Font(None, 40)
        self.score_surf = self.score_font.render("Score:", True, "Black")
        self.score_rect = self.score_surf.get_rect(center=(300, 620))

        # Set up background surfaces
        self.bg_surface = pygame.Surface((600, 600))
        self.bg_surface.fill('Black')

        self.bg_Score = pygame.Surface((600, 50))
        self.bg_Score.fill((64, 64, 64))

    def place_apple(self):
        # Randomly place the apple while avoiding the snake's body
        while True:
            self.apple_X = random.randrange(0, 581, 20)
            self.apple_Y = random.randrange(0, 581, 20)
            self.apple_rect.topleft = (self.apple_X, self.apple_Y)

            # Check if the apple is not on the snake's body
            if not any(part == self.apple_rect.topleft for part in self.snake_body):
                break

    def restart_game(self):
        # Reset game variables to their initial state
        self.Right, self.Left, self.Up, self.Down = False, False, False, False
        self.apple_X, self.apple_Y = random.randrange(0, 581, 20), random.randrange(0, 581, 20)
        self.snake_body = [(300, 300)]
        self.snake_length = 1
        self.game_active = True
        self.snake_rect.topleft = (300, 300)  # Reset the snake's position

    def handle_events(self):
        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if self.game_active:
                if event.type == pygame.KEYDOWN:
                    # Update direction based on arrow key input
                    if event.key == pygame.K_RIGHT and not self.Left:
                        self.Right, self.Left, self.Up, self.Down = True, False, False, False
                    elif event.key == pygame.K_LEFT and not self.Right:
                        self.Right, self.Left, self.Up, self.Down = False, True, False, False
                    elif event.key == pygame.K_UP and not self.Down:
                        self.Right, self.Left, self.Up, self.Down = False, False, True, False
                    elif event.key == pygame.K_DOWN and not self.Up:
                        self.Right, self.Left, self.Up, self.Down = False, False, False, True
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Restart the game
                        self.restart_game()

    def update_game_state(self):
        # Update game state
        if self.game_active:
            # Move the snake based on direction
            if self.Right:
                self.snake_rect.right += 20
            if self.Left:
                self.snake_rect.left -= 20
            if self.Up:
                self.snake_rect.top -= 20
            if self.Down:
                self.snake_rect.bottom += 20

            # Update the snake body and limit its length
            self.snake_body = [(self.snake_rect.x, self.snake_rect.y)] + self.snake_body
            self.snake_body = self.snake_body[:self.snake_length]

            # Check for collisions with walls
            if (
                self.snake_rect.left >= 600
                or self.snake_rect.right <= 0
                or self.snake_rect.top >= 600
                or self.snake_rect.bottom <= 0
            ):
                self.game_active = False

            # Draw game elements on the screen
            self.screen.blit(self.bg_surface, (0, 0))
            self.screen.blit(self.bg_Score, (0, 600))
            self.score_surf = self.score_font.render(f"Score: {len(self.snake_body) - 1}", True, "Black")
            self.screen.blit(self.score_surf, self.score_rect)

            for body_part in self.snake_body:
                rect = pygame.Rect(body_part[0], body_part[1], 20, 20)
                self.screen.blit(self.snake_surface, rect)
                pygame.draw.rect(self.screen, "Black", rect, 1)

            apple_rect = pygame.Rect(self.apple_X, self.apple_Y, 20, 20)
            self.screen.blit(self.apple_surface, apple_rect)
            pygame.draw.rect(self.screen, "Black", apple_rect, 1)

            

            # Check for collision with the apple and update score
            if self.snake_rect.colliderect(self.apple_rect):
                self.place_apple()  # Call the method to place the apple in a valid position
                self.snake_length += 1

            # Check for self-collision
            if self.snake_body[0] in self.snake_body[1:]:
                self.game_active = False
        else:
            # If game over, fill the screen with black
            self.screen.blit(self.bg_surface, (0, 0))
            # Display game over message
            game_over_font = pygame.font.Font(None, 60)
            game_over_surf = game_over_font.render("Game Over", True, "Red")
            game_over_rect = game_over_surf.get_rect(center=(300, 300))
            self.screen.blit(game_over_surf, game_over_rect)

            # Display restart instructions
            restart_font = pygame.font.Font(None, 40)
            restart_surf = restart_font.render("Press SPACE to restart", True, "White")
            restart_rect = restart_surf.get_rect(center=(300, 400))
            self.screen.blit(restart_surf, restart_rect)

            # Check for space key press to restart the game
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.restart_game()

        # Update the display and set the game speed
        pygame.display.update()
        self.clock.tick(7)

if __name__ == "__main__":
    # Create an instance of the SnakeGame class
    game = SnakeGame()

    # Main game loop
    while True:
        game.handle_events()
        game.update_game_state()
