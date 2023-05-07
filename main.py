import pygame
from ground import Ground
from bird import Bird
from pipes_ import Pipe
from random import randint
import json

pygame.init()

score = 0

def updateScore():
    global score
    score = 0

def getScore():
    global score
    return score

#Screen
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Frames
clock = pygame.time.Clock()

#Sounds
flap_sound = pygame.mixer.Sound(r'assets\audio\wing.wav')
point_sound = pygame.mixer.Sound(r'assets\audio\point.wav')
dead_sound = pygame.mixer.Sound(r'assets\audio\die.wav')
hit_sound = pygame.mixer.Sound(r'assets\audio\hit.wav')
swoosh_sound = pygame.mixer.Sound(r'assets\audio\swoosh.wav')

#Assets
yellow_bird_images = [pygame.image.load(r'assets\sprites\yellowbird-downflap.png'),
            pygame.image.load(r'assets\sprites\yellowbird-midflap.png'),
            pygame.image.load(r'assets\sprites\yellowbird-upflap.png')]

blue_bird_images = [pygame.image.load(r'assets\sprites\bluebird-downflap.png'),
            pygame.image.load(r'assets\sprites\bluebird-midflap.png'),
            pygame.image.load(r'assets\sprites\bluebird-upflap.png')]

red_bird_images = [pygame.image.load(r'assets\sprites\redbird-downflap.png'),
            pygame.image.load(r'assets\sprites\redbird-midflap.png'),
            pygame.image.load(r'assets\sprites\redbird-upflap.png')]

bird_images = [yellow_bird_images, blue_bird_images, red_bird_images]

day_background = pygame.image.load(r"assets\sprites\background-day.png")
night_background = pygame.image.load(r"assets\sprites\background-night.png")

backgrounds = [day_background, night_background]

gameover = pygame.image.load(r"assets\sprites\gameover.png")

start_image = pygame.image.load(r'assets\sprites\message.png')

green_pipe_down = pygame.image.load(r'assets\sprites\pipe-green-down.png')
green_pipe_up = pygame.image.load(r'assets\sprites\pipe-green-up.png')

red_pipe_down = pygame.image.load(r'assets\sprites\pipe-red-down.png')
red_pipe_up = pygame.image.load(r'assets\sprites\pipe-red-up.png')

pipe_images = [[green_pipe_down, green_pipe_up], [red_pipe_down, red_pipe_up]]



score_images = [pygame.image.load(f'assets\sprites\{i}.png') for i in range(0, 10)]

#fonts
font = pygame.font.SysFont('couriernew', 28, True)
font2 = pygame.font.SysFont('couriernew', 24, True)

#RESTART TEXT
restart_text = font.render('PRESS SPACE', True, (255,255,255))
restart_text1 = font.render('TO RESTART', True, (255,255,255))

#CHANGE SKIN TEXT
change_skin_text = font2.render('C-change bird', True, (255, 128, 0))
change_time_text = font2.render('T-change time', True, (255, 128, 0))
change_pipe_text = font2.render('P-change pipes', True, (255, 128, 0))

#SHOW RESULT
best = ''
last = ''
with open('scores.json', 'r') as file:
    dict = json.load(file)
    best = dict["BEST"]
    last = dict['LAST']


best_score = font2.render(f'Best:{best}', True, (255, 255, 255))
last_score = font2.render(f'Last:{last}', True, (255, 255, 255))



class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = type

        self.entered = False
        self.passed = False


    def update(self, speed, bird_x):
        self.rect.x -= speed
        if self.rect.x <= -288:
            self.kill() 

        if self.type == 'bot':
            if bird_x > self.rect.topleft[0]:
                self.entered = True
            if bird_x > self.rect.topright[0] and not self.passed:
                self.passed = True
                global score
                score += 1
                pygame.mixer.Sound.play(point_sound)

    def check(self, bird_x):
        if bird_x > self.rect.topleft[0] and not self.passed:
            self.entered = True
        if bird_x > self.rect.topright[0] and self.entered:
            self.passed = True



def createPipes(pipe_image):
    top_coordinate = randint(-260, -100) # Создаем рандомную координату для верхней пайпы
    up_pipe = Pipe(288, top_coordinate, pipe_image[1], 'top')
    down_pipe = Pipe(288, top_coordinate + 96 + up_pipe.image.get_height(), pipe_image[0], 'bot') # Нижнюю создаем относительно верхней

    return [down_pipe, up_pipe]


def displayScore():
    total_length = 0    #Суммарная длина(по ширине на экране) счётчика
    for i in str(score):
        total_length += score_images[int(i)].get_width() #У каждой пнгшки разная ширина
    start_x = 144 - total_length//2 # Стартовая координата - центр по иксу минус половина ширины счётчика
    previous_width = 0 # Переменная для хранения ширины предыдущих цифр
    for num in str(score):
        screen.blit(score_images[int(num)], (start_x+previous_width, 80)) #Здесь мы отступаем от стартовой координаты ровно на сумму ширин предшествующих цифр
        previous_width += score_images[int(num)].get_width() # Обновляем ширину предшествующих цифр
        


def game(menu):
    current_bird_image_index = 0
    current_background_index = 0
    current_background = backgrounds[current_background_index]
    current_pipe_image = pipe_images[0]
    current_pipe_image_index = 0

    score = 0

    wasHit = False

    pipes = pygame.sprite.Group()
    # pipes.add(createPipes(current_pipe_image))

    ground = pygame.sprite.Group()
    ground.add(Ground(0, 400))

    bird = pygame.sprite.GroupSingle()
    bird.add(Bird((SCREEN_WIDTH//2 - 4, SCREEN_HEIGHT//2 + 10), yellow_bird_images, menu))

    pipeTimer = randint(200, 300)

    speed = 1

    running = True
    while running:

        input = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and menu:
                    menu = False
                    bird.sprite.menu = False
                    bird.sprite.jump()
                elif event.key == pygame.K_SPACE and not menu:
                    bird.sprite.jump()
                    pygame.mixer.Sound.play(flap_sound)

                elif event.key == pygame.K_c and menu:
                    current_bird_image_index += 1
                    bird.sprite.images = bird_images[(current_bird_image_index)%3]
                
                elif event.key == pygame.K_t and menu:
                    current_background_index += 1
                    current_background = backgrounds[(current_background_index)%2]

                elif event.key == pygame.K_p and menu:
                    current_pipe_image_index += 1
                    current_pipe_image = pipe_images[(current_pipe_image_index)%2]

        #Background sky
        screen.blit(current_background, (0, 0))

        if not menu:
            #Pipes
            pipes.draw(screen)
            pipes.update(speed, bird.sprite.rect.centerx)

        if menu:
            screen.blit(start_image, (SCREEN_WIDTH//6, SCREEN_HEIGHT//6))

        #Bird
        bird.update()
        bird.draw(screen)

        #Ground
        ground.draw(screen)
        ground.update(speed)

        if menu:
            screen.blit(change_skin_text, (10, SCREEN_HEIGHT-90))
            screen.blit(change_pipe_text, (10, SCREEN_HEIGHT-65))
            screen.blit(change_time_text, (10, SCREEN_HEIGHT-40))

            screen.blit(best_score, (10, 10))
            screen.blit(last_score, (10, 30))

        #To make the ground move continuously
        if len(ground) <= 3: 
            ground.add(Ground(SCREEN_WIDTH, 400))


        #Create pipes with different timing
        if not menu:
            if pipeTimer < 0:
                pipes.add(createPipes(current_pipe_image))
                pipeTimer = randint(200, 260)
            pipeTimer -= 1

        #Collisions
        collision_pipes = pygame.sprite.spritecollide(bird.sprite, pipes, False)
        collision_ground = pygame.sprite.spritecollide(bird.sprite, ground, False)

        if collision_ground or collision_pipes:
            bird.sprite.isAlive = False

        if not bird.sprite.isAlive:
            if not wasHit:
                wasHit = True
                pygame.mixer.Sound.play(hit_sound)
                pygame.mixer.Sound.play(dead_sound)
            speed = 0
            screen.blit(gameover, (SCREEN_WIDTH//6, SCREEN_HEIGHT//3))
            screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT-90))
            screen.blit(restart_text1, (SCREEN_WIDTH//2 - restart_text1.get_width()//2, SCREEN_HEIGHT-60))

            result = getScore()

            with open('scores.json', 'r') as file:
                dict = json.load(file)
                if int(dict['BEST']) < result:
                    with open ('scores.json', 'w') as w_file:
                        json.dump({"BEST":f"{result}", "LAST":f"{result}"}, w_file)
                else:
                    with open ('scores.json', 'w') as w_file:
                        json.dump({"BEST":f"{dict['BEST']}", "LAST":f"{result}"}, w_file)


            if input[pygame.K_SPACE]:
                pygame.mixer.Sound.play(swoosh_sound)
                updateScore()
                game(True)

        #Score
        if not menu:
            displayScore()

    
        clock.tick(60)
        pygame.display.update()

def main():
    game(True)

if __name__ == '__main__':
    main()