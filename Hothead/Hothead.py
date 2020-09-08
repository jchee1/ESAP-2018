import pygame,math,sys,random
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((960,540))
clock = pygame.time.Clock()


#game constants
BOUNDARIES = (110,445)

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Hothead(pygame.sprite.Sprite):
	SPEED = 40
	TIMEBOUND = 5

	def __init__(self,images,position):
		pygame.sprite.Sprite.__init__(self)
		self.position = position
		self.idle1 = pygame.image.load(images[0])
		self.idle2 = pygame.image.load(images[1])
		self.upim = pygame.image.load(images[2])
		self.downim = pygame.image.load(images[3])
		self.up = self.down = 0
		self.whichidle = 0
		self.timer = 0


	def update(self,deltat):
		x,y = self.position
		oldy = y
		y += self.down - self.up

		if self.whichidle < self.TIMEBOUND:
			idle = self.idle1
			self.whichidle += 1
		else:
			idle = self.idle2
			self.whichidle += 1
			if self.whichidle > 2*self.TIMEBOUND:
				self.whichidle = 0
		if self.down > 0 or self.up > 0:
			if self.up > self.down:
				self.image = self.upim
			elif self.up == self.down:
				self.image = idle
			else:
				self.image = self.downim
		else:
			self.image = idle

		if y > BOUNDARIES[1] or y < BOUNDARIES[0]:
			y = oldy
		self.position = (x,y)
		self.rect = self.image.get_rect()
		self.rect.center = self.position
		self.collide = Rect(self.rect.left+20,self.rect.top+20,self.rect.width-40,self.rect.height-40)

class Screen(pygame.sprite.Sprite):
	CAP = 55
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.position = (960,320)
		self.image = pygame.image.load('empty.png')
		self.rect = self.image.get_rect()
		self.speed = 30
		self.scrolls = 0
		self.limit = 4

	def update(self,deltat,water,fire,water2):
		x,y = self.position
		if x <= 50:
			x = 960
			self.scrolls += 1
			self.randomize(water,fire,water2)
			water.image = water.im
			fire.image = fire.im
			water2.image = water2.im
		else:
			x -= self.speed
		if self.scrolls > self.limit and self.speed < self.CAP:
			self.speed += 1
			self.limit += 4

		self.position = (x,y)
		self.rect.center = self.position

	def randomize(self,water,fire,water2):
		ordering = random.randint(0,8)
		wat2pos = 0
		if ordering == 0:
			watpos = 1
			firepos = 0
		elif ordering == 1:
			watpos = 2
			firepos = 0
		elif ordering == 2:
			watpos = 3
			firepos = 0
		elif ordering == 3:
			firepos = 1
			watpos = 0
		elif ordering == 4:
			firepos = 2
			watpos = 0
		elif ordering == 5:
			firepos = 3
			watpos = 0
		elif ordering == 6:
			watpos = 1
			wat2pos = 2
			firepos = 0
		elif ordering == 7:
			watpos = 2
			wat2pos = 3
			firepos = 0
		elif ordering == 8:
			watpos = 3
			wat2pos = 1
			firepos = 0
		water.where = watpos
		fire.where = firepos
		water2.where = wat2pos

class Scroller(pygame.sprite.Sprite):
	def __init__(self,image):
		pygame.sprite.Sprite.__init__(self)
		self.im = pygame.image.load(image)
		self.image = self.im
		self.ys = [1200,160,280,400]
		self.position = (0,self.ys[0])
		self.emptyimage = pygame.image.load('empty.png')
		self.where = 0

	def update(self,deltat,screen):
		x,y= self.position
		if self.where == 0:
			self.position = (0,self.ys[0])
			self.rect = self.image.get_rect()
			self.rect.center = self.position
		else:
			y = self.ys[self.where]
			x = screen.position[0]  
			self.position = (x,y)
			self.rect = self.image.get_rect()
			self.rect.center = self.position
		self.collide = Rect(self.rect.left+20,self.rect.top+20,self.rect.width-40,self.rect.height-40)

class Fire(Scroller):
	def __init__(self,image):
		Scroller.__init__(self,image)


class Water(Scroller):
	def __init__(self,image):
		Scroller.__init__(self,image)

class Score(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.font = pygame.font.SysFont("impact",40)
		self.color = Color('red')
		self.scor = 0
		self.lastscore = -1
		self.update()
		self.rect = self.image.get_rect().move(440,50)

	def update(self):
		if self.scor != self.lastscore:
			self.lastscore = self.scor
			msg = "%d" % self.scor
			self.image = self.font.render(msg,0,self.color)

	def lose(self,hs):
			msg = "YOUR SCORE: %d" % self.scor + "                HIGH SCORE: %d" % hs.hs
			self.image = self.font.render(msg,0,self.color)
			self.rect = self.image.get_rect().move(200,300)

class HighScore(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.font = pygame.font.SysFont("impact",40)
		self.color = Color('red')
		with open("hs.txt","r") as f:
			self.hs = int(f.readlines()[0])


	def lose(self,score):
		if score.scor > self.hs:
			with open("hs.txt","w") as f:
				self.hs = score.scor
				f.writelines(str(self.hs))



def main():
	rect = screen.get_rect()
	sc = Score()
	background = Background('bg.png', [0,0])
	losebackground = Background('loser.png',[0,0])
	lose = False
	score_group = pygame.sprite.RenderPlain(sc)
	hothead = Hothead(['hothead0.png','hothead1.png','hhup.png','hhdown.png'],(100,300))
	hot_group = pygame.sprite.RenderPlain(hothead)
	scrn = Screen()
	scrn_group = pygame.sprite.RenderPlain(scrn)
	fire = Fire('fire.png')
	fire_group = pygame.sprite.RenderPlain(fire)
	wat = Water('water.png')
	wat_group = pygame.sprite.RenderPlain(wat)
	wat2 = Water('water.png')
	wat2_group = pygame.sprite.RenderPlain(wat2)
	hs = HighScore()
	hs_group = pygame.sprite.RenderPlain(hs)
	collide = False
	while True:
		deltat = clock.tick(30)
		for ev in pygame.event.get():
			if not hasattr(ev,'key'): continue
			keypress = ev.type == KEYDOWN
			if ev.key == K_UP or ev.key == K_LEFT or ev.key == K_w or ev.key == K_d:
				hothead.up = keypress*hothead.SPEED
			elif ev.key == K_DOWN or ev.key == K_RIGHT or ev.key == K_s or ev.key == K_a:
				hothead.down = keypress*hothead.SPEED
			elif ev.key == K_ESCAPE:
				sys.exit(0)
			elif ev.key == K_RETURN and lose:
				main()
		if lose:
			screen.blit(losebackground.image,losebackground.rect)
			sc.lose(hs)
			hs.lose(sc)
			score_group.update()
			score_group.draw(screen)
		else:
			#rendering
			screen.fill((255,255,255))
			screen.blit(background.image,background.rect)
			scrn_group.update(deltat,wat,fire,wat2)
			scrn_group.draw(screen)
			wat_group.update(deltat,scrn)
			wat_group.draw(screen)
			wat2_group.update(deltat,scrn)
			wat2_group.draw(screen)
			fire_group.update(deltat,scrn)
			fire_group.draw(screen)
			hot_group.update(deltat)
			hot_group.draw(screen)
			if hothead.collide.colliderect(wat.collide) and not collide:
				lose = True
			elif hothead.collide.colliderect(wat2.collide) and not collide:
				lose = True
			elif hothead.collide.colliderect(fire.collide) and not collide:
				sc.scor += 1
				collide =True
				fire.image = fire.emptyimage
			elif not hothead.collide.colliderect(wat.collide) and not hothead.collide.colliderect(fire.collide) and not hothead.collide.colliderect(wat2.collide):
				collide = False
			score_group.update()
			score_group.draw(screen)
		pygame.display.flip()


main()