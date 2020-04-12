import os,sys
import pygame
import time
from Breakout.paddle import Paddle
from Breakout.ball import Ball
from Breakout.brick import Brick

pygame.init()

white = (255,255,255)
black = (0,0,0)
darkblue = (36,90,190)
lightblue = (0,176,240)
red = (255,0,0)
orange = (255,100,0)
yellow = (255,255,0)

size = (800,600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Atari Breakout")

def breakoutGameLoop():

	score = 0
	lives = 3
	paddle = Paddle(white,100,10)
	paddle.rect.x = 350
	paddle.rect.y = 560

	ball = Ball(red,10,10)
	ball.rect.x = 345
	ball.rect.y = 195

	all_stuff = pygame.sprite.Group()
	all_bricks = pygame.sprite.Group()

	for i in range(7):
		brick = Brick(red,80,30)
		brick.rect.x = 60 + i*100
		brick.rect.y = 60
		all_stuff.add(brick)
		all_bricks.add(brick)

	for i in range(7):
		brick = Brick(red,80,30)
		brick.rect.x = 60 + i*100
		brick.rect.y = 100
		all_stuff.add(brick)
		all_bricks.add(brick)

	for i in range(7):
		brick = Brick(red,80,30)
		brick.rect.x = 60 + i*100
		brick.rect.y = 140
		all_stuff.add(brick)
		all_bricks.add(brick)

	all_stuff.add(paddle)
	all_stuff.add(ball)

	gameExit = False

	clock = pygame.time.Clock()

	while not gameExit:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					gameExit = True
		keys = pygame.key.get_pressed()
		if keys[pygame.K_a]:
			paddle.left(5)
		if keys[pygame.K_d]:
			paddle.right(5)

		all_stuff.update()

		if ball.rect.x >= 790:
			ball.velocity[0] = -ball.velocity[0]
		if ball.rect.x <= 0:
			ball.velocity[0] = -ball.velocity[0]
		if ball.rect.y > 590:
			ball.velocity[1] = -ball.velocity[1]
			lives -= 1
			if lives <= 0:
				font = pygame.font.Font(None,75)
				text = font.render("Game Over!",1,white)
				screen.blit(text,(200,300))
				pygame.display.flip()
				pygame.time.wait(5000)
				gameExit = True
		if ball.rect.y < 40:
			ball.velocity[1] = -ball.velocity[1]

		if pygame.sprite.collide_mask(ball, paddle):
			ball.rect.x -= ball.velocity[0]
			ball.rect.y -= ball.velocity[1]
			ball.bounce()

		brick_collision = pygame.sprite.spritecollide(ball,all_bricks,False)
		for b in brick_collision:
			ball.bounce()
			score += 1
			b.kill()
			if len(all_bricks) == 0:
				font = pygame.font.Font(None,75)
				text = font.render("Level complete!",1,white)
				screen.blit(text,(200,300))
				pygame.display.flip()
				pygame.time.wait(5000)
				gameExit = True

		screen.fill(darkblue)
		pygame.draw.line(screen,white,[0,38],[800,38],2)

		all_stuff.draw(screen)

		font = pygame.font.Font(None,34)
		text = font.render("Score: "+str(score),1,white)
		screen.blit(text,(20,10))
		text = font.render("Lives: "+str(lives),1,white)
		screen.blit(text,(650,10))

		pygame.display.flip()

		clock.tick(60)
	pygame.quit()