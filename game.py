import pygame
import time
from pygame.locals import *
import os
import random

pygame.init()

W, H = 870, 520
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('Tamarun')

bg = pygame.image.load(os.path.join('images', 'bg.png')).convert()
bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()


class player(object):
    run = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(8, 16)]
    jump = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(1, 8)]
    slide = [pygame.image.load(os.path.join('images', 'S1.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S3.png')), pygame.image.load(os.path.join('images', 'S4.png')), pygame.image.load(os.path.join('images', 'S5.png'))]
    fall = pygame.image.load(os.path.join('images', '0.png'))
    jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.falling = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False

    def draw(self, win):
        if self.falling:
            win.blit(self.fall, (self.x, self.y + 30))
        elif self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.7
            win.blit(self.jump[self.jumpCount//18], (self.x, self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            self.hitbox = (self.x + 120, self.y + 35, self.width + 15, self.height - 10) # -- Jumping Hitbox
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
                self.hitbox = (self.x + 40, self.y + 20, self.width + 60, self.height + 20)
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            elif self.slideCount > 20 and self.slideCount < 80:
                self.hitbox = (self.x + 40, self.y + 30, self.width + 60, self.height + 20)

            if self.slideCount >= 110:
                self.slideCount = 0
                self.runCount = 0
                self.slideUp = False
                self.hitbox = (self.x + 40, self.y + 20, self.width + 60, self.height + 20)
            win.blit(self.slide[self.slideCount//10], (self.x, self.y))
            self.slideCount += 1

        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount//6], (self.x,self.y))
            self.runCount += 1
            self.hitbox = (self.x + 35, self.y + 25, self.width + 80, self.height + 30) # -- Walking Hitbox

        pygame.draw.rect(win, (255,0,0),self.hitbox, 2)

class saw(object):
    rotate = [pygame.image.load(os.path.join('images', 'SAW0.png')), pygame.image.load(os.path.join('images', 'SAW1.png')), pygame.image.load(os.path.join('images', 'SAW2.png')), pygame.image.load(os.path.join('images', 'SAW3.png'))]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotateCount = 0
        self.vel = 1.4

    def draw(self, win):
        self.hitbox = (self.x + 35, self.y + 15, self.width - 30, self.height - 30) # -- Mushroom Hitbox
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        if self.rotateCount >= 8:
            self.rotateCount = 0
        win.blit(pygame.transform.scale(self.rotate[self.rotateCount//2], (140,140)), (self.x,self.y))
        self.rotateCount += 1

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False


class log(saw):
    img = pygame.image.load(os.path.join('images', 'log.png'))

    def draw(self, win):
        self.hitbox = (self.x + 10, self.y, 28,315)
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        win.blit(self.img, (self.x, self.y))

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False

class coin(saw):
    img = pygame.image.load(os.path.join('images', 'gold.png'))

    def draw(self, win):
        self.hitbox = (self.x + 5, self.y + 5, 60, 60)
        pygame.draw.rect(win, (0,255,0), self.hitbox, 2)
        win.blit( pygame.transform.scale(self.img, (70, 70)), (self.x, self.y))

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False

class coinb(saw):
    img = pygame.image.load(os.path.join('images', 'bronze.png'))

    def draw(self, win):
        self.hitbox = (self.x + 5, self.y + 5, 60, 60)
        pygame.draw.rect(win, (0,255,0), self.hitbox, 2)
        win.blit( pygame.transform.scale(self.img, (70, 70)), (self.x, self.y))

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False

class bamboo(saw):
    img = pygame.image.load(os.path.join('images', 'bamboo.png'))

    def draw(self, win):
        self.hitbox = (self.x + 5, self.y + 5, 60, 60)
        pygame.draw.rect(win, (0,255,0), self.hitbox, 2)
        win.blit( pygame.transform.scale(self.img, (70, 70)), (self.x, self.y))

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False

class grass(saw):
    img = pygame.image.load(os.path.join('images', 'grass.png'))

    def draw(self, win):
        self.hitbox = (self.x + 5, self.y + 5, 60, 60)
        pygame.draw.rect(win, (0,255,0), self.hitbox, 2)
        win.blit( pygame.transform.scale(self.img, (70, 70)), (self.x, self.y))

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False

class tower(saw):
    img = pygame.image.load(os.path.join('images', 'tower.png'))

    def draw(self, win):
        self.hitbox = (self.x + 5, self.y + 5, 60, 60)
        pygame.draw.rect(win, (0,255,0), self.hitbox, 2)
        win.blit( pygame.transform.scale(self.img, (100, 250)), (self.x, self.y))

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False


def updateFile():
    f = open('scores.txt','r')
    file = f.readlines()
    last = int(file[0])

    if last < int(score):
        f.close()
        file = open('scores.txt', 'w')
        file.write(str(score))
        file.close()

        return score

    return last



def endScreen():
    global pause, score, speed, obstacles
    pause = 0
    speed = 60
    obstacles = []

    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                runner.falling = False
                runner.sliding = False
                runner.jumpin = False

        win.blit(bg, (0,0))
        largeFont = pygame.font.SysFont('comicsans', 80)
        lastScore = largeFont.render('Best Score: ' + str(updateFile()),1,(255,255,255))
        currentScore = largeFont.render('Score: '+ str(score),1,(255,255,255))
        win.blit(lastScore, (W/2 - lastScore.get_width()/2,150))
        win.blit(currentScore, (W/2 - currentScore.get_width()/2, 240))
        pygame.display.update()
    score = 0

def redrawWindow():
    largeFont = pygame.font.SysFont('comicsans', 30)
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2,0))
    text = largeFont.render('Score: ' + str(score), 1, (255,255,255))
    runner.draw(win)
    for obstacle in obstacles:
        obstacle.draw(win)

    win.blit(text, (700, 10))
    pygame.display.update()


pygame.time.set_timer(USEREVENT+1, 500)
pygame.time.set_timer(USEREVENT+2, 3000)
speed = 60

score = 0

run = True
runner = player(200, 270, 64, 64)

obstacles = []
pause = 0
fallSpeed = 40

while run:
    if pause > 0:
        pause += 1
        if pause > fallSpeed * 2:
            endScreen()

    score = speed//10 - 3

    for obstacle in obstacles:
        if obstacle.collide(runner.hitbox):
            runner.falling = True

            if pause == 0:
                pause = 1
                fallSpeed = speed
        if obstacle.x < -64:
            obstacles.pop(obstacles.index(obstacle))
        else:
            obstacle.x -= 3.4 # -- Obstacle Speed

    bgX -= 1.4
    bgX2 -= 1.4

    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False

        if event.type == USEREVENT+1: # -- Become Faster
            speed += 1

        if event.type == USEREVENT+2:
            r = random.randrange(0,6)
            c = time.time()
            if r == 0:
                obstacles.append(saw(990, 510, 64, 64))
            elif r == 1:
                obstacles.append(log(810, 0, 48, 310))
            elif r == 2:
                obstacles.append(coin(810, 160, 64, 64))
            elif r == 3:
                obstacles.append(coinb(810, 310, 64, 64))
            elif r == 4:
                obstacles.append(bamboo(810, 310, 64, 64))
            elif r == 5:
                obstacles.append(grass(810, 310, 64, 64))
            # while True:
            #    obstacles.append(tower(810, 140, 64, 64))
            #    time.sleep(60.0 - ((time.time() - c) % 60.0))

    if runner.falling == False:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if not(runner.jumping):
                runner.jumping = True

        if keys[pygame.K_DOWN]:
            if not(runner.sliding):
                runner.sliding = True

    clock.tick(speed)
    redrawWindow()
