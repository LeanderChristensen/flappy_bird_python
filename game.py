import sys
import pygame
import random

pygame.init()
pygame.display.set_caption("Flappy Bird")
size = width, height = 288, 512
menu = True
alive = False
falling = False
started = False
points = 0
best = 0
velocity = 0
jumpVelocity = 0
lowerPipes = []
upperPipes = []
spaceBetweenPipes = 150
lowerPipesY = 328
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)

background = pygame.image.load("data/sprites/background-day.png")
ground = pygame.image.load("data/sprites/base.png")
message = pygame.image.load("data/sprites/message.png")
gameover = pygame.image.load("data/sprites/gameover.png")
ok = pygame.image.load("data/sprites/ok.png")
title = pygame.image.load("data/sprites/message.png")
pipe_image = pygame.image.load("data/sprites/pipe-green.png")
bird_image = pygame.image.load("data/sprites/yellowbird-midflap.png")
pygame.display.set_icon(bird_image)
bird_image_up = pygame.image.load("data/sprites/yellowbird-upflap.png")
bird_image_down = pygame.image.load("data/sprites/yellowbird-downflap.png")
swoosh = pygame.mixer.Sound("data/audio/swoosh.wav")
wing = pygame.mixer.Sound("data/audio/wing.wav")
point = pygame.mixer.Sound("data/audio/point.wav")
hit = pygame.mixer.Sound("data/audio/hit.wav")
die = pygame.mixer.Sound("data/audio/die.wav")
font = pygame.font.Font('data/flappy-font.ttf', 48)
bird = pygame.sprite.Sprite()
bird.image = bird_image
bird.rect = bird_image.get_rect(center=(100,256))
points_text = font.render(f'{points}', True, (255, 255, 255))

for i in range(0,3):
	variance = random.randint(0, 143)
	lowerPipes.append(pygame.sprite.Sprite())
	lowerPipes[i].image = pipe_image
	lowerPipes[i].rect = pipe_image.get_rect()
	lowerPipes[i].rect.x = 350+(i*spaceBetweenPipes)
	lowerPipes[i].rect.y = lowerPipesY-variance
	upperPipes.append(pygame.sprite.Sprite())
	upperPipes[i].image = pipe_image
	upperPipes[i].image = pygame.transform.flip(upperPipes[i].image, False, True)
	upperPipes[i].rect = pipe_image.get_rect()
	upperPipes[i].rect.x = 350+(i*spaceBetweenPipes)
	upperPipes[i].rect.y = lowerPipesY-410-variance

def death():
	global best
	global points
	global alive
	global falling
	global started	
	global points_text
	best = max(best, points)
	font = pygame.font.Font('data/flappy-font.ttf', 32)
	while True:
		mouse = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN and mouse[0] >= 106 and mouse[0] <= 186 and mouse[1] >= 317 and mouse[1] <= 345:
				alive = True
				falling = False
				started = False
				points = 0
				font = pygame.font.Font('data/flappy-font.ttf', 48)
				points_text = font.render(f'{points}', True, (255, 255, 255))
				bird.rect = bird_image.get_rect(center=(100,256))
				for i in range(0,3):
					variance = random.randint(0, 143)
					lowerPipes.append(pygame.sprite.Sprite())
					lowerPipes[i].image = pipe_image
					lowerPipes[i].rect = pipe_image.get_rect()
					lowerPipes[i].rect.x = 350+(i*spaceBetweenPipes)
					lowerPipes[i].rect.y = lowerPipesY-variance
					upperPipes.append(pygame.sprite.Sprite())
					upperPipes[i].image = pipe_image
					upperPipes[i].image = pygame.transform.flip(upperPipes[i].image, False, True)
					upperPipes[i].rect = pipe_image.get_rect()
					upperPipes[i].rect.x = 350+(i*spaceBetweenPipes)
					upperPipes[i].rect.y = lowerPipesY-410-variance
				return
		screen.blit(background, (0, 0))
		screen.blit(ground, (0, 420))
		screen.blit(gameover, (50, 150))
		points_text = font.render('Score:', True, (255, 255, 255))
		screen.blit(points_text, (80, 220))
		points_text = font.render('Best:', True, (255, 255, 255))
		screen.blit(points_text, (80, 255))
		points_text = font.render(f'{points}', True, (255, 255, 255))
		screen.blit(points_text, (190, 220))
		points_text = font.render(f'{best}', True, (255, 255, 255))
		screen.blit(points_text, (190, 255))
		screen.blit(ok, (105, 315))
		pygame.display.flip()

while menu:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				pygame.mixer.Sound.play(swoosh)
				pygame.mixer.music.stop()
				menu = False
				alive = True
		if event.type == pygame.MOUSEBUTTONDOWN:
			menu = False
			alive = True
			pygame.mixer.Sound.play(swoosh)
			pygame.mixer.music.stop()
	screen.blit(background, (0, 0))
	screen.blit(ground, (0, 420))
	screen.blit(title, (50, 75))
	pygame.display.flip()

while alive:
	for i in range(0,3):
		if not falling:
			lowerPipes[i].rect.x -= 2
			if lowerPipes[i].rect.x <= -spaceBetweenPipes+50 and not started:
				start = True
				lowerPipes[i].rect.x = 350
				variance = random.randint(0, 143)
				lowerPipes[i].rect.y = lowerPipesY-variance
				upperPipes[i].rect.y = lowerPipesY-410-variance
			if lowerPipes[i].rect.x <= -spaceBetweenPipes and started:
				lowerPipes[i].rect.x = 350
				variance = random.randint(0, 143)
				lowerPipes[i].rect.y = lowerPipesY-variance
				upperPipes[i].rect.y = lowerPipesY-410-variance
			upperPipes[i].rect.x -= 2
			if upperPipes[i].rect.x <= -spaceBetweenPipes+50 and not started:
				start = True
				upperPipes[i].rect.x = 350
			if upperPipes[i].rect.x <= -spaceBetweenPipes and started:
				upperPipes[i].rect.x = 350
			if bird.rect.x <= lowerPipes[i].rect.x+52 and bird.rect.x+30 >= lowerPipes[i].rect.x and bird.rect.y >= lowerPipes[i].rect.y:
				pygame.mixer.Sound.play(hit)
				pygame.mixer.music.stop()
				falling = True
			if bird.rect.x <= upperPipes[i].rect.x+52 and bird.rect.x+30 >= upperPipes[i].rect.x and bird.rect.y <= upperPipes[i].rect.y+320:
				if bird.rect.y+12 < upperPipes[i].rect.y+320 and bird.rect.y+12 > upperPipes[i].rect.y+310:
					jumpVelocity = 0
				pygame.mixer.Sound.play(hit)
				pygame.mixer.music.stop()
				falling = True
			if lowerPipes[i].rect.x+26 == 100 or lowerPipes[i].rect.x+27 == 100:
				points += 1
				pygame.mixer.Sound.play(point)
				pygame.mixer.music.stop()
				points_text = font.render(f'{points}', True, (255, 255, 255))
		if bird.rect.x <= lowerPipes[i].rect.x+52 and bird.rect.x+20 >= lowerPipes[i].rect.x and bird.rect.y+24 >= lowerPipes[i].rect.y:
			if bird.rect.y+24 > lowerPipes[i].rect.y and bird.rect.y+24 < lowerPipes[i].rect.y+5:
				if not falling:
					pygame.mixer.Sound.play(hit)
					pygame.mixer.music.stop()
				alive = False
				death()
	if bird.rect.y < -10:
		bird.rect.y = -10
	if bird.rect.y > 400:
		pygame.mixer.Sound.play(die)
		pygame.mixer.music.stop()
		alive = False
		death()
	if velocity < 1:
		if velocity + 0.03 > 1:
			velocity = 1
		else:
			velocity += 0.03
	if jumpVelocity > 0:
		if jumpVelocity - 0.05 < 0:
			jumpVelocity = 0
		else:
			jumpVelocity -= 0.05
	if jumpVelocity < 0:
		jumpVelocity = 0
	if jumpVelocity > 0.3:
		bird.image = bird_image_down
	else:
		bird.image = bird_image_up
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.KEYDOWN and not falling:
			if event.key == pygame.K_SPACE:
				velocity = 0
				jumpVelocity = 1
				pygame.mixer.Sound.play(wing)
				pygame.mixer.music.stop()
		if event.type == pygame.MOUSEBUTTONDOWN and not falling:
			velocity = 0
			jumpVelocity = 1
			pygame.mixer.Sound.play(wing)
			pygame.mixer.music.stop()
	clock.tick(60)
	bird.rect.y -= 7*jumpVelocity
	bird.rect.y += 5*velocity
	screen.blit(background, (0, 0))
	for i in range(0,3):
		screen.blit(lowerPipes[i].image, lowerPipes[i].rect)
		screen.blit(upperPipes[i].image, upperPipes[i].rect)
	if points < 10:
		screen.blit(points_text, (120, 65))
	else:
		screen.blit(points_text, (108, 65))
	screen.blit(ground, (0, 420))
	screen.blit(bird.image, bird.rect)
	pygame.display.flip()