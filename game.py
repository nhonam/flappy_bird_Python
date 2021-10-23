import pygame, sys, random

from pygame.sprite import RenderUpdates

#tạo funtion cho game
def draw_floor():
    screen.blit(floor,(floor_x_pos,650))
    screen.blit(floor,(floor_x_pos+432,650))

def create_pipe():
    random_pipe_pos  = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos - 700))
    return bottom_pipe, top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -=5
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top < -75 or bird_rect.bottom >= 650:
        return False
    return True

def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement*3,1)
    return new_bird

def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)), True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)

        hight_score_surface = game_font.render(f'High Score: {int(high__score)}', True,(255,255,255))
        hight_score_rect = score_surface.get_rect(center = (170,630))
        screen.blit(hight_score_surface,hight_score_rect)

def update_score(score, high__score):
    if score > high__score:
        high__score = score
    return high__score
pygame.mixer.pre_init()
pygame.init()
screen  = pygame.display.set_mode((432,768))
clock  =pygame.time.Clock()
game_font = pygame.font.Font('FileGame/04B_19.TTF',40)

 
#tạo cái variable cho trò chơi
gravity = 0.2
bird_movement = 0
game_activity = True
#chèn backgrounf
bg = pygame.image.load('FileGame/assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)
score = 0
high__score =0
#chèn cái sàn ở dưới 
floor = pygame.image.load('FileGame\\assets\\floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

#tạo chim
bird_down = pygame.image.load('FileGame\\assets\\yellowbird-downflap.png').convert_alpha()
bird_down = pygame.transform.scale2x(bird_down)

bird_mid = pygame.image.load('FileGame\\assets\\yellowbird-midflap.png').convert_alpha()
bird_mid = pygame.transform.scale2x(bird_mid)

bird_up = pygame.image.load('FileGame\\assets\\yellowbird-upflap.png').convert_alpha()
bird_up = pygame.transform.scale2x(bird_up)
bird_list = [bird_down,bird_mid,bird_up]
bird_index =0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (100,384))

#tao timer cho bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap,200)

#tạo ống
pipe_surface = pygame.image.load('FileGame\\assets\\pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
#tạo timer
spaewnpipe = pygame.USEREVENT
pygame.time.set_timer(spaewnpipe, 1200)

pipe_height = [200,300,400]
#manf  hình kết thúc
end_game = pygame.image.load('FileGame\\assets\\message.png').convert_alpha()
end_game = pygame.transform.scale2x(end_game)
end_game_rect = end_game.get_rect(center =(216, 384))
#aam thanh
flap_sound = pygame.mixer.Sound('FileGame\sound\sfx_wing.wav')
hit_sound = pygame.mixer.Sound('FileGame\sound\sfx_hit.wav')
score_sound = pygame.mixer.Sound('FileGame\sound\sfx_point.wav')
score_sound_countdown =100
#GAME
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_activity:
                bird_movement = 0
                bird_movement = -6 # độ nhảy của chim
                flap_sound.play()
            if event.key == pygame.K_LCTRL and game_activity == False:
                game_activity = True
                pipe_list.clear()
                bird_rect.center = (100,384)
                bird_movement = 0
                score =0
        if event.type == spaewnpipe:
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index =0
            bird, bird_rect = bird_animation()

    screen.blit(bg,(0,0))
    if game_activity:
         #chim
        bird_movement +=gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_activity = check_collision(pipe_list)
        #ống
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display('main game')
        score_sound_countdown -=1
        if score_sound_countdown <=0:
            score_sound.play()
            score_sound_countdown =100
    else:
        screen.blit(end_game, end_game_rect)
        high__score = update_score(score,high__score)
        score_display('game_over')
    
    #sàn
    floor_x_pos -= 1
    draw_floor()
    if  floor_x_pos <= -432:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)