import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 300
GROUND_HEIGHT = 50
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dinosaur Game")

dinosaur_img = pygame.image.load("dino-pos1.png")
dinosaur_img = pygame.transform.scale(dinosaur_img, (50, 50))
cactus_img = pygame.image.load("cactus-single.png")
cactus_img = pygame.transform.scale(cactus_img, (30, 50))

font = pygame.font.Font(None, 36)

class DinoGame:
    def __init__(self):
        self.reset()
        self.high_score = self.load_high_score()
        self.play_again_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 30, 200, 50)
        self.button_text = font.render("Play Again", True, BLACK)

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
        self.dino_pos = [50, HEIGHT - GROUND_HEIGHT - 50]
        self.dino_speed = 0
        self.score = 0
        self.cactus_pos = [WIDTH, HEIGHT - GROUND_HEIGHT - 50]
        self.game_over = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.dino_pos[1] == HEIGHT - GROUND_HEIGHT - 50:
            self.dino_speed = -15

    def update(self):
        self.dino_pos[1] += self.dino_speed
        if self.dino_pos[1] >= HEIGHT - GROUND_HEIGHT - 50:
            self.dino_pos[1] = HEIGHT - GROUND_HEIGHT - 50
            self.dino_speed = 0
        else:
            self.dino_speed += 1

        self.cactus_pos[0] -= 5
        if self.cactus_pos[0] < 0:
            self.cactus_pos[0] = WIDTH
            self.score += 1

        if (self.dino_pos[0] + 50 > self.cactus_pos[0] and 
            self.dino_pos[0] < self.cactus_pos[0] + 30 and 
            self.dino_pos[1] + 50 > self.cactus_pos[1]):
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()

    def draw(self):
        screen.fill(WHITE)
        screen.blit(dinosaur_img, self.dino_pos)
        screen.blit(cactus_img, self.cactus_pos)
        pygame.draw.rect(screen, GRAY, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))
        
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        high_score_text = font.render(f"High Score: {self.high_score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 10, 10))

        if self.game_over:
            game_over_text = font.render("Game Over", True, BLACK)
            screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 18))
            pygame.draw.rect(screen, GRAY, self.play_again_button)
            screen.blit(self.button_text, (WIDTH // 2 - self.button_text.get_width() // 2, HEIGHT // 2 + 40))

    def check_play_again(self):
        mouse_pos = pygame.mouse.get_pos()
        if (pygame.mouse.get_pressed()[0] and 
            self.play_again_button.collidepoint(mouse_pos)):
            self.reset()
            pygame.time.delay(200)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_high_score()
                    pygame.quit()
                    sys.exit()

            if not self.game_over:
                self.handle_input()
                self.update()
            else:
                self.check_play_again()

            self.draw()
            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    game = DinoGame()
    game.run()