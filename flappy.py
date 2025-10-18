import random
import pygame

pygame.init()

#This is a co-op Python flappy bird game where the goal is to work
#together to get as many points as possible

#Game size variables
GAME_WIDTH = 360
GAME_HEIGHT = 640

#bird class
bird_x = GAME_WIDTH/8
bird_y = GAME_HEIGHT/2
bird_width = 34
bird_height = 24

#Bird class
class Bird(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, bird_x, bird_y, bird_width, bird_height)
        self.img = img

#Pipe class
pipe_x = GAME_WIDTH
pipe_y = 0 #This is a default value make them random later
pipe_width = 64
pipe_height = 512

class Pipe(pygame.Rect):
    def __init__(self,img):
        pygame.Rect.__init__(self, pipe_x, pipe_y, pipe_width, pipe_height)
        self.img = img
        self.passed = False

#game images
background_image = pygame.image.load("flappybirdbg.bmp")
bird_image = pygame.image.load('flappybird.bmp')
bird_image = pygame.transform.scale(bird_image, (bird_width, bird_height))
top_pipe_image = pygame.image.load('toppipe.bmp')
top_pipe_image = pygame.transform.scale(top_pipe_image, (pipe_width, pipe_height))
bottom_pipe_image = pygame.image.load('bottompipe.bmp')
bottom_pipe_image = pygame.transform.scale(bottom_pipe_image, (pipe_width,pipe_height))

#Game logic
bird_1 = Bird(bird_image)
bird_2 = Bird(bird_image)

pipes = []
velocity_x = -2 #2 pixels to the left
velocity_y = 0
velocity_y1 = 0
gravity = 0.3
score = 0
game_over = False
start = True

#Draw the text, images, and background here
def draw():
    window.blit(background_image, (0,0))
    window.blit(bird_1.img, bird_1)
    window.blit(bird_2.img, bird_2)

    for pipe in pipes:
        window.blit(pipe.img, pipe)

    if start:
        text_str = "Co-Op"
        text_font = pygame.font.SysFont('Comic Sans MS', 45)
        text_render = text_font.render(text_str, True, 'white')
        window.blit(text_render, (5, 0))
    else:
        text_str = str(int(score))
        if game_over:
            text_str = "Game Over: " + text_str

        text_font = pygame.font.SysFont('Comic Sans MS', 45)
        text_render = text_font.render(text_str, True, 'white')

        window.blit(text_render, (5, 0))

#Make the calculations for the movement and the death cases
def move():
    global velocity_y, score, game_over, velocity_y1

    velocity_y += gravity
    velocity_y1 += gravity
    bird_1.y += velocity_y
    bird_2.y += velocity_y1

    bird_1.y = max(bird_1.y, 0)
    bird_2.y = max(bird_2.y, 0)

    if bird_1.y > GAME_HEIGHT or bird_2.y > GAME_HEIGHT:
        game_over = True
        return

    for pipe in pipes:
        pipe.x+=velocity_x

        if not pipe.passed and bird_1.x > pipe.x + pipe_width and bird_2.x > pipe.x + pipe.width:
            score += 1
            pipe.passed = True

        if bird_1.colliderect(pipe) or bird_2.colliderect(pipe):
            game_over = True
            return

    while len(pipes) > 0 and pipes[0].x + pipe_width < 0:
        pipes.pop(0) #removes the first element from the list

#Make the pipes, as well as move them to create the illusion of the bird moving
#The pipes are moving in the negative x direction
def create_pipes():
    random_pipe_y = pipe_y - pipe_height/4 - random.random() * (pipe_height/2)
    opening_space = GAME_HEIGHT/4

    top_pipe = Pipe(top_pipe_image)
    top_pipe.y = random_pipe_y

    bottom_pipe = Pipe(bottom_pipe_image)
    bottom_pipe.y = top_pipe.y + top_pipe.height + opening_space

    if not start:
        pipes.append(top_pipe)
        pipes.append(bottom_pipe)

    # print(len(pipes))
#Create the window and the title of the window
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

#Make an event for the pipes timer(every 1.5 seconds, new pipes will be created)
create_pipes_timer = pygame.USEREVENT + 0
pygame.time.set_timer(create_pipes_timer, 1500)

#This is the main game loop. The loop runs indefinitely until one of the 2 birds dies
while True: #This is the game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == create_pipes_timer and not game_over:
            create_pipes()

        #Get the key presses of the user
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                start = False
                velocity_y = -6
            if event.key == pygame.K_w:
                start = False
                velocity_y1 = -6

            #Reload the game when the r key is pressed
            if event.key == pygame.K_r:
                if game_over:
                    bird_1.y = bird_y
                    bird_2.y = bird_y
                    pipes.clear()
                    score = 0
                    game_over = False
                    velocity_y = 0
                    velocity_y1 = 0
    
    #When the game is not over, perform all of the game actions
    if not game_over:
        if not start:
            move()
        draw()
        pygame.display.update()
        clock.tick(60) #This is 60 fps