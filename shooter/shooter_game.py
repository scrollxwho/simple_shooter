from pygame import *
from random import randint

class GameSprite(sprite.Sprite):

    def __init__(self, player_image, player_x, player_y, width,height,player_speed):
        super().__init__()
 
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.width = width
        self.height = height

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx-7, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		pos = mouse.get_pos()

		if self.rect.collidepoint(pos):
			if mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if mouse.get_pressed()[0] == 0:
			self.clicked = False

		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

class Enemy(GameSprite):
    def update(self):
        global score_2
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(50, 650)
            self.rect.y = 0
            score_2 += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

shans = 0
FPS = 60
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
display.set_caption('Шутер')
clock = time.Clock()

start_img = image.load('start_btn.png').convert_alpha()
exit_img = image.load('exit_btn.png').convert_alpha()
start_btn = Button(180, 280, start_img, 0.5)
exit_btn = Button(360, 280, exit_img, 0.5)

font.init()
font = font.SysFont(None, 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))

finish = False
game = True

ship = Player('rocket.png', 350, 400, 80, 100, 10)

monsters = sprite.Group()
asteroids = sprite.Group()
bullets = sprite.Group()

for i in range(10):
    monster = Enemy('ufo.png', randint(50, 650), 0, 80, 50, randint(2, 5))
    monsters.add(monster)

asteroid_object = Enemy('asteroidv2.png', randint(50, 550), 0, 150, 150, randint(1, 3))
asteroids.add(asteroid_object)

score = 0
score_2 = 0

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
        if start_btn.draw(window):
            start = False
            finish = False
            asteroids.empty()
            monsters.empty()
            bullets.empty()
            ship.rect.x = 350
            ship.rect.y = 400
            for i in range(6):
                monster = Enemy('ufo.png', randint(50, 650), 0, 80, 50, randint(2, 5))
                monsters.add(monster)
            for i in range(1):
                asteroid_object = Enemy('asteroidv2.png', randint(50, 550), 0, 150, 150, randint(1, 3))
                asteroids.add(asteroid_object)
            score = 0
            score_2 = 0
        if exit_btn.draw(window):
            game = False

    if finish != True:
        window.blit(background, (0, 0))

        ship.reset()
        asteroids.update()
        bullets.draw(window)
        monsters.draw(window)
        asteroids.draw(window)
        bullets.update()
        ship.update()
        monsters.update()

        collides = sprite.groupcollide(monsters, bullets, True, True)
        collides_2 = sprite.groupcollide(asteroids, monsters, False, True)

        score_label = font.render("Score: "+str(score), True, (255, 255, 255))
        score_label_2 = font.render("Omitted: "+str(score_2), True, (255, 255, 255))
        window.blit(score_label, (0, 0))
        window.blit(score_label_2, (400, 0))

        for monster in collides:
            monster = Enemy('ufo.png', randint(50, 650), 0, 80, 50, randint(2, 6))
            monsters.add(monster)
            score += 1 
        
        sprite_list = sprite.spritecollide(ship, monsters, False)
        sprite_list_2 = sprite.spritecollide(ship, asteroids, False)

        if sprite_list:
            finish = True
            window.blit(lose, (200, 200))

        if sprite_list_2:
            finish = True
            window.blit(lose, (200, 200))

        if score == 30:
            finish = True
            window.blit(win, (200, 200))
        
        if score_2 == 10:
            finish = True
            window.blit(lose, (200, 200))
            
    #обновление экрана
    display.update()
    clock.tick(FPS)