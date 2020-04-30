import pygame
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()
BACKGROUND_DAY = pygame.image.load('background_day.png')
BACKGROUND_NIGHT = pygame.image.load('background_night.png')
WIDTH, HEIGHT = 576, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird by DINH XUAN HUNG")


class PIPE(object):


    def __init__(self, x):
        self.dis_bet_pipe = 50
        self.coefficient = random.randint(2, 5)
        self.safe_dis = 40
        self.width = 52
        self.height = 320
        self.x = x
        self.y = random.randint(- 3 * self.safe_dis, 0)

        self.pipe_up = pygame.image.load('assets/sprites/pipe-green_up.png')
        self.pipe_down = pygame.image.load('assets/sprites/pipe-green_down.png')
        self.vel = 5

    def display(self, trigger):
        global background_state
        WIN.blit(self.pipe_down, (self.x, self.y))
        WIN.blit(self.pipe_up, (self.x, self.y + self.height + 3 * self.safe_dis))

        self.x -= self.vel

        if trigger:
            self.x = random.randint(WIDTH - 200, WIDTH)
            background_state = -background_state


class BIRD(object):

    def __init__(self):
        self.width = 34
        self.height = 24
        self.x = random.randint(self.width, WIDTH // 2 - 2 * self.width)
        self.y = HEIGHT // 2
        self.bird_up = pygame.image.load('assets/sprites/yellowbird-upflap.png')
        self.bird_mid = pygame.image.load('assets/sprites/yellowbird-midflap.png')
        self.bird_down = pygame.image.load('assets/sprites/yellowbird-downflap.png')

        self.bird_img = self.bird_down
        self.vel = 5
        self.can_control = True

    def display_control(self):

        if self.can_control:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.bird_img = random.choice((self.bird_up, self.bird_mid))
                self.y -= 1.7 * self.vel

        WIN.blit(self.bird_img, (self.x, self.y))

        self.bird_img = self.bird_down

        self.y += self.vel


class SCORE(object):

    def __init__(self):
        self.width = 24
        self.height = 36
        self.score = 0
        self.x = self.width
        self.y = self.height
        self.score_img = {str(x): pygame.image.load('assets/sprites/{}.png'.format(x)) for x in range(10)}


    def displayScore(self):
        listScore = [str(_) for _ in list(str(self.score))]
        dis_bet = 0 if self.score < 10 else 20

        x = self.x
        for index in listScore:
            WIN.blit(self.score_img[index], (x, self.y))
            x += dis_bet


def isCollison(x1, y1, w1, h1, x2, y2, w2, h2):
    return x1 + w1 >= x2 and y1 + h1 >= y2 and x2 + w2 >= x1 and y2 + h2 >= y1


class FLAPPYBIRD(object):

    def __init__(self):
        self.SPEED_GAME = 5
        self.loc_bg = 0
        self.loc_bg_temp = WIDTH
        self.FPS = 30
        self.pipes = [PIPE(random.randint(WIDTH - 300, WIDTH)) for _ in range(100)]
        self.bird = BIRD()
        self.background_state = 1
        self.score = SCORE()
        self.Clock = pygame.time.Clock()


    def display(self):

        pygame.mixer.music.load('assets/audio/swoosh.wav')
        pygame.mixer.music.play(-1)

        background = BACKGROUND_DAY if self.background_state == 1 else BACKGROUND_NIGHT
        background_temp = background

        self.FPS += 0.04

        self.Clock.tick(self.FPS)

        WIN.blit(background, (self.loc_bg , 0))
        WIN.blit(background_temp, (self.loc_bg_temp, 0))

        #score
        self.score.displayScore()

        # control bird
        self.bird.display_control()
        trigger = False
        self.pipes[len(self.pipes) - 1].display(trigger)

        if self.pipes[len(self.pipes) - 1].x < 0:
            trigger = True
            self.pipes[len(self.pipes) - 1].x = random.randint(WIDTH - 200, WIDTH)
            random.shuffle(self.pipes)

        for index in range(len(self.pipes) - 1):

            self.pipes[index].display(trigger)
            # Update for distance next
            self.pipes[index + 1].x = self.pipes[index].x + self.pipes[index].coefficient * self.pipes[index].dis_bet_pipe

            if isCollison(self.bird.x, self.bird.y, self.bird.width, self.bird.height, self.pipes[index].x, self.pipes[index].y ,self.pipes[index].width, self.pipes[index].height) \
                or isCollison(self.bird.x, self.bird.y, self.bird.width, self.bird.height, self.pipes[index].x, self.pipes[index].y + self.pipes[index].height + 3 * self.pipes[index].safe_dis, self.pipes[index].width, self.pipes[index].height) \
                    or self.bird.y < 0:


                self.stopGame()
                break

            if self.pipes[index].x < self.bird.x and self.bird.x < self.pipes[index + 1].x:
                self.score.score += 1

        self.loc_bg -= self.SPEED_GAME
        self.loc_bg_temp -= self.SPEED_GAME

        if self.loc_bg < -WIDTH:
            self.loc_bg = WIDTH
        if self.loc_bg_temp < -WIDTH:
            self.loc_bg_temp = WIDTH

        pygame.display.update()


    def GamePlay(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            self.display()

    def ResetEverything(self):
        # Reset everything

        self.pipes = [PIPE(random.randint(WIDTH - 300, WIDTH)) for _ in range(100)]
        self.bird = BIRD()
        self.background_state = 1
        self.score = SCORE()

        self.loc_bg = 0
        self.loc_bg_temp = WIDTH
        self.FPS = 30

    def stopGame(self):
        
        pygame.mixer.music.load('assets/audio/hit.wav')
        pygame.mixer.music.play(1)

        icon = pygame.image.load('assets/sprites/gameover.png')

        self.bird.bird_img = pygame.image.load('assets/sprites/yellowbird-dropdown.png')
        self.bird.can_control = False

        background = BACKGROUND_DAY if self.background_state == 1 else BACKGROUND_NIGHT
        background_temp = background



        while True:

            WIN.blit(background, (self.loc_bg, 0))
            WIN.blit(background_temp, (self.loc_bg_temp, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    self.ResetEverything()
                    self.GamePlay()

            self.bird.display_control()
            WIN.blit(icon, (WIDTH // 2 - 50, HEIGHT // 2))
            pygame.display.update()


if __name__ == '__main__':
    FLAPPYBIRD().GamePlay()
