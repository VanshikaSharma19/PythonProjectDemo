import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GROUND_HEIGHT = HEIGHT - 100

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Run")

# Load assets
player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (50, 80))
coin_img = pygame.image.load("coin.png")
coin_img = pygame.transform.scale(coin_img, (30, 30))

# Player class
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = GROUND_HEIGHT - 80
        self.width = 50
        self.height = 80
        self.velocity = 5
        self.is_jumping = False
        self.jump_count = 10
    
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.velocity
    
    def jump(self):
        if self.is_jumping:
            if self.jump_count >= -10:
                neg = 1 if self.jump_count > 0 else -1
                self.y -= (self.jump_count ** 2) * 0.3 * neg
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = 10
    
    def draw(self):
        screen.blit(player_img, (self.x, self.y))

# Obstacle class
class Obstacle:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 50)
        self.y = 0
        self.width = 50
        self.height = 50
        self.velocity = 7
    
    def move(self):
        self.y += self.velocity
    
    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

# Coin class
class Coin:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 30)
        self.y = 0
        self.width = 30
        self.height = 30
        self.velocity = 5
    
    def move(self):
        self.y += self.velocity
    
    def draw(self):
        screen.blit(coin_img, (self.x, self.y))

# Game loop
player = Player()
obstacles = []
coins = []
clock = pygame.time.Clock()
score = 0
running = True

while running:
    clock.tick(30)
    screen.fill(WHITE)
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not player.is_jumping:
                player.is_jumping = True
    
    player.move(keys)
    player.jump()
    player.draw()
    
    if random.randint(1, 50) == 1:
        obstacles.append(Obstacle())
    if random.randint(1, 70) == 1:
        coins.append(Coin())
    
    for obstacle in obstacles[:]:
        obstacle.move()
        obstacle.draw()
        if obstacle.y > HEIGHT:
            obstacles.remove(obstacle)
        if player.x < obstacle.x + obstacle.width and player.x + player.width > obstacle.x and player.y < obstacle.y + obstacle.height and player.y + player.height > obstacle.y:
            print("Game Over! Final Score:", score)
            running = False
    
    for coin in coins[:]:
        coin.move()
        coin.draw()
        if coin.y > HEIGHT:
            coins.remove(coin)
        if player.x < coin.x + coin.width and player.x + player.width > coin.x and player.y < coin.y + coin.height and player.y + player.height > coin.y:
            coins.remove(coin)
            score += 10
    
    pygame.display.update()

pygame.quit()
