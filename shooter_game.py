from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, image1, speed, x, y, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(image1), (size_x, size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= 5
        if keys_pressed[K_d] and self.rect.x < 620:
            self.rect.x += 5

    def fire(self):
        bullet = Bullet('bullet.png', 4, self.rect.centerx, self.rect.top, 15, 20)
        bullets.add(bullet)

lost = 0
count = 0
hp = 3
rel_time = False
num_fire = 0

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80, 620)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

        

width = 700
height = 500
window = display.set_mode((width, height))
background = transform.scale(image.load('galaxy.jpg'), (width, height))
display.set_caption('Шутер')
window.blit(background, (0, 0))

font.init()
font1 = font.SysFont('Arial', 120)
win = font1.render('YOU WIN!', 1, (28, 173, 12))
lose = font1.render('YOU LOSE!', 1, (173, 12, 12))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire = mixer.Sound('fire.ogg')

player = Player('rocket.png', 5, 300, 400, 80, 100)
monster1 = Enemy('ufo.png', 1, 400, 0, 80, 40)
monster2 = Enemy('ufo.png', 2, 300, 0, 80, 40)
monster3 = Enemy('ufo.png', 1, 200, 0, 80, 40)
monster4 = Enemy('ufo.png', 2, 80, 0, 80, 40)
monster5 = Enemy('ufo.png', 1, 500, 0, 80, 40)
monsters = sprite.Group()
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)
asteroid1 = Enemy('asteroid.png', 2, 250, 0, 50, 50)
asteroid2 = Enemy('asteroid.png', 2, 300, 0, 50, 50)
asteroid3 = Enemy('asteroid.png', 2, 350, 0, 50, 50)
asteroids = sprite.Group()
asteroids.add(asteroid1)
asteroids.add(asteroid2)
asteroids.add(asteroid3)

bullets = sprite.Group()

clock = time.Clock()
FPS = 60
finish = False
run = True
while run:
    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <  5 and rel_time == False:
                    fire.play()
                    player.fire()
                    num_fire += 1
                if num_fire == 5 and rel_time == False:
                    rel_time = True
                    last_time = timer()
        if e.type == QUIT:
            run = False
    if finish != True:
        window.blit(background, (0, 0))
        font.init()
        font1 = font.SysFont('Arial', 36)

        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for monster in sprites_list:
            count += 1
            monster6 = Enemy('ufo.png', 1, randint(80, 620), 0, 80, 40)
            monsters.add(monster6)

        asteroids.draw(window)
        asteroids.update()
        monsters.draw(window)
        monsters.update()

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                text_rel = font1.render('Wait, reload...', 1, (255, 255, 255))  
                window.blit(text_rel, (250, 400)) 
            else:
                rel_time = False
                num_fire = 0

        if count >= 10:
            finish = True
            window.blit(win, (150, 200))

        if sprite.spritecollide(player, monsters, False):
            finish = True
            window.blit(lose, (150, 200))

        if sprite.spritecollide(player, asteroids, True):
            asteroid4 = Enemy('asteroid.png', 2, 250, 0, 50, 50)
            asteroids.add(asteroid4)
            hp -= 1
            if hp == 0:
                finish = True
                window.blit(lose, (150, 200))

        text_hp = font1.render('Жизни: ' + str(hp), 1, (255, 255, 255))
        text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        text_count = font1.render("Счёт: " + str(count), 1, (255, 255, 255))
        window.blit(text_lose, (10, 60))
        window.blit(text_count, (10, 20))
        window.blit(text_hp, (550, 20))

        bullets.draw(window)
        bullets.update()
        player.update()
        player.reset()
        display.update()
        
    clock.tick(FPS)