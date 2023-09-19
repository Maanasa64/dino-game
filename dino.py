import pygame
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 300
GROUND_HEIGHT = 50
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
FPS = 60

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dinosaur Game")

# Load images
dinosaur = pygame.image.load("dino-pos1.png")
dinosaur = pygame.transform.scale(dinosaur, (50, 50))
cactus = pygame.image.load("cactus-single.png")
cactus = pygame.transform.scale(cactus, (30, 50))

font = pygame.font.Font(None, 36)

class DinoGame:
    def __init__(self):
        self.dino_x, self.dino_y = 50, HEIGHT - GROUND_HEIGHT - 50
        self.dino_speed = 0  # Change in vertical speed
        self.gravity = 1     # Gravity force
        self.score = 0
        self.high_score = self.load_high_score()  # Load high score from file
        self.cactus_x, self.cactus_y = WIDTH, HEIGHT - GROUND_HEIGHT - 50
        self.game_over = False

        # Create "Play Again" button
        self.play_again_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 30, 200, 50)
        self.button_color = GRAY
        self.text_color = BLACK
        self.button_font = pygame.font.Font(None, 36)
        self.button_text = self.button_font.render("Play Again", True, self.text_color)

    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def save_high_score(self):
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))

    def reset(self):
        # Only reset game state variables, not the high score
        self.dino_x, self.dino_y = 50, HEIGHT - GROUND_HEIGHT - 50
        self.dino_speed = 0
        self.score = 0
        self.cactus_x, self.cactus_y = WIDTH, HEIGHT - GROUND_HEIGHT - 50
        self.game_over = False

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if not self.game_over:
                # Check for user input
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE] and self.dino_y == HEIGHT - GROUND_HEIGHT - 50:
                    self.dino_speed = -15  # Jump when on the ground

                # Update game elements
                self.dino_y += self.dino_speed
                if self.dino_y >= HEIGHT - GROUND_HEIGHT - 50:
                    self.dino_y = HEIGHT - GROUND_HEIGHT - 50
                    self.dino_speed = 0
                else:
                    self.dino_speed += self.gravity  # Apply gravity when in the air

                self.cactus_x -= 5
                if self.cactus_x < 0:
                    self.cactus_x = WIDTH
                    self.score += 1

                # Check for collisions
                if self.dino_x + 50 > self.cactus_x and self.dino_x < self.cactus_x + 30 and self.dino_y + 50 > self.cactus_y:
                    self.game_over = True

                    # Update high score if the current score is higher
                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.save_high_score()  # Save the new high score

            # Draw everything
            screen.fill(WHITE)
            screen.blit(dinosaur, (self.dino_x, self.dino_y))
            screen.blit(cactus, (self.cactus_x, self.cactus_y))
            pygame.draw.rect(screen, GRAY, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))
            
            # Display the score and high score
            score_text = font.render(f"Score: {self.score}", True, BLACK)
            high_score_text = font.render(f"High Score: {self.high_score}", True, BLACK)
            screen.blit(score_text, (10, 10))
            screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 10, 10))

            if self.game_over:
                # Display "Game Over" and the enhanced "Play Again" button
                game_over_text = font.render("Game Over", True, BLACK)
                screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 18))
                
                # Draw the enhanced "Play Again" button
                pygame.draw.rect(screen, self.button_color, self.play_again_button)
                screen.blit(self.button_text, (WIDTH // 2 - self.button_text.get_width() // 2, HEIGHT // 2 + 30 + 10))

                # Check for mouse click on "Play Again" button
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0] and self.play_again_button.collidepoint(mouse_x, mouse_y):
                    self.reset()
                    pygame.time.delay(200)  # Delay to prevent instant restart

            pygame.display.flip()
            clock.tick(FPS)

game = DinoGame()
game.run()

# Save the high score when the game ends or when a new high score is achieved
game.save_high_score()

pygame.quit()
sys.exit()
