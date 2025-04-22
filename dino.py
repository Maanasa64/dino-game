import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 300
GROUND_HEIGHT = 50
WHITE = (255, 255, 255)
SKY_COLOR = (240, 240, 255)
GROUND_COLOR = (100, 100, 100)
BLACK = (0, 0, 0)
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Runner")

dinosaur_img = pygame.image.load("dino-pos1.png").convert_alpha()
dinosaur_img = pygame.transform.scale(dinosaur_img, (50, 50))
cactus_img = pygame.image.load("cactus-single.png").convert_alpha()
cactus_img = pygame.transform.scale(cactus_img, (30, 50))

font = pygame.font.Font(None, 36)

class DinoGame:
    def __init__(self):
        self.reset()
        self.high_score = self.load_high_score()
        self.play_again_button = pygame.Rect(WIDTH//2-100, HEIGHT//2+30, 200, 50)
        self.button_text = font.render("Play Again", True, BLACK)
        self.clouds = [{'x': random.randint(0, WIDTH), 'y': random.randint(30, 100), 
                      'speed': random.uniform(0.5, 1.5)} for _ in range(5)]
        
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
        self.game_speed = 5
        self.score_timer = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.dino_pos[1] == HEIGHT - GROUND_HEIGHT - 50:
            self.dino_speed = -15

    def update(self):
        # Update dinosaur
        self.dino_pos[1] += self.dino_speed
        if self.dino_pos[1] >= HEIGHT - GROUND_HEIGHT - 50:
            self.dino_pos[1] = HEIGHT - GROUND_HEIGHT - 50
            self.dino_speed = 0
        else:
            self.dino_speed += 0.8

        self.cactus_pos[0] -= self.game_speed
        if self.cactus_pos[0] < -30:
            self.cactus_pos[0] = WIDTH
            self.score += 1

        for cloud in self.clouds:
            cloud['x'] -= cloud['speed']
            if cloud['x'] < -50:
                cloud['x'] = WIDTH
                cloud['y'] = random.randint(30, 100)

        self.score_timer += 1
        if self.score_timer % 500 == 0:
            self.game_speed += 0.5

        dino_rect = pygame.Rect(self.dino_pos[0], self.dino_pos[1], 50, 50)
        cactus_rect = pygame.Rect(self.cactus_pos[0], self.cactus_pos[1], 30, 50)
        if dino_rect.colliderect(cactus_rect):
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()

    def draw(self):
        screen.fill(SKY_COLOR)

        for cloud in self.clouds:
            pygame.draw.circle(screen, WHITE, (int(cloud['x']), cloud['y']), 20)
            pygame.draw.circle(screen, WHITE, (int(cloud['x']+15), cloud['y']+5), 15)
            pygame.draw.circle(screen, WHITE, (int(cloud['x']-15), cloud['y']+5), 15)

        pygame.draw.rect(screen, GROUND_COLOR, (0, HEIGHT-GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

        pygame.draw.line(screen, (120, 120, 120), (0, HEIGHT-GROUND_HEIGHT), (WIDTH, HEIGHT-GROUND_HEIGHT), 2)

        screen.blit(dinosaur_img, self.dino_pos)
        screen.blit(cactus_img, self.cactus_pos)

        score_shadow = font.render(f"Score: {self.score}", True, (100, 100, 100))
        high_score_shadow = font.render(f"High Score: {self.high_score}", True, (100, 100, 100))
        screen.blit(score_shadow, (12, 12))
        screen.blit(high_score_shadow, (WIDTH - high_score_shadow.get_width() - 8, 12))
        
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        high_score_text = font.render(f"High Score: {self.high_score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 10, 10))

        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            
            game_over_text = font.render("GAME OVER", True, WHITE)
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
            
            pygame.draw.rect(screen, WHITE, self.play_again_button, 0, 5)
            pygame.draw.rect(screen, BLACK, self.play_again_button, 2, 5)
            screen.blit(self.button_text, (WIDTH//2 - self.button_text.get_width()//2, HEIGHT//2 + 45))

    def check_play_again(self):
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and self.play_again_button.collidepoint(mouse_pos):
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