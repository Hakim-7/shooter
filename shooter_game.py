from pygame import *
from random import randint
from time import time as timer

# Initialize background music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

# Initialize fonts and captions
font.init()
font1 = font.Font(None, 80)
win_text = font1.render('YOU WIN!', True, (255, 255, 255))
lose_text = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.Font(None, 36)

# Load images
img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_bullet = "bullet.png"
img_enemy = "monsters.png"
img_enemy2 = "monsters2.png"
img_asteroids = "asteroid.png"

# Game window setup
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))

# Game variables
score = 0
lost = 0
goal = 10
max_lost = 3
life = 3

# Parent class for all sprites
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Main player class  
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

# Enemy class
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Enemy3(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

# Bullet class
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

# Create game objects
background = transform.scale(image.load(img_back), (win_width, win_height))
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

bullets = sprite.Group()
monsters = sprite.Group()
monsters2 = sprite.Group()
asteroids = sprite.Group()

for i in range(1, 4):
    monsters.add(Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 2)))
    monsters2.add(Enemy(img_enemy2, randint(80, win_width - 80), -40, 80, 50, randint(2, 4)))
    asteroids.add(Enemy3(img_asteroids, randint(80, win_width - 80), -40, 80, 50, randint(2, 4)))

# Game loop control variables
finish = False
run = True
FPS = 60
num_fire = 0
max_fire = 5
reload_time = False
last_time = 0

clock = time.Clock()

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < max_fire and not reload_time:
                    fire_sound.play()
                    ship.fire() 
                    num_fire += 1
                elif num_fire >= max_fire and not reload_time:
                    last_time = timer()
                    reload_time = True

    if not finish:
        window.blit(background, (0, 0))

        # Score and missed display
        text = font2.render(f"Score: {score}", True, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render(f"Missed: {lost}", True, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        
        # Update all sprites
        ship.update()
        bullets.update()
        monsters.update()
        monsters2.update()
        asteroids.update()

        # Draw everything
        ship.reset()
        bullets.draw(window)
        monsters.draw(window)
        monsters2.draw(window)
        asteroids.draw(window)

        # Collision detection
        sprite.groupcollide(asteroids, bullets, False, True)

        hits1 = sprite.groupcollide(monsters, bullets, True, True)
        for _ in hits1:
            score += 1
            monsters.add(Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 2)))

        hits2 = sprite.groupcollide(monsters2, bullets, True, True)
        for _ in hits2:
            score += 1
            monsters2.add(Enemy(img_enemy2, randint(80, win_width - 80), -40, 80, 50, randint(2, 4)))

        # Player collisions
        if sprite.spritecollide(ship, monsters, True) or \
           sprite.spritecollide(ship, monsters2, True) or \
           sprite.spritecollide(ship, asteroids, True):
            life -= 1

        # Reload handling
        if reload_time:
            now_time = timer()
            if now_time - last_time < 1.5:
                reload_text = font2.render("Wait... reloading...", True, (150, 0, 0))
                window.blit(reload_text, (260, 460))
            else:
                num_fire = 0
                reload_time = False

        # Life display
        if life == 3:
            life_color = (0, 150, 0)
        elif life == 2:
            life_color = (150, 150, 0)
        else:
            life_color = (150, 0, 0)
        life_text = font2.render(f"Life: {life}", True, life_color)
        window.blit(life_text, (600, 10))

        # Win/Lose check
        if score >= goal:
            finish = True
            window.blit(win_text, (200, 200))
        if life <= 0 or lost >= max_lost:
            finish = True
            window.blit(lose_text, (200, 200))

    display.update()
    clock.tick(50)
