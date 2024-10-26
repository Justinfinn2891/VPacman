import sys
sys.path.append("c:/Users/Justin Finn/Pacman/VPacman/pacman")
from boards import boards1
import pygame
import math 
pygame.init()

W_SCREEN = 900
H_SCREEN = 950
screen = pygame.display.set_mode([W_SCREEN, H_SCREEN])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = boards1
#COLOR OF BOARD
color = 'blue'
#USED FOR DRAWING THE ARCS OF THE BOARD
PI = math.pi 
player_images = []
for i in range(1,5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'pacman/Assets/player/{i}.png'), (45, 45)))
    print("yes")

blinky_img = pygame.transform.scale(pygame.image.load(f'pacman/Assets/ghost/red.png'), (45, 45))
pinky_img = pygame.transform.scale(pygame.image.load(f'pacman/Assets/ghost/pink.png'), (45, 45))
inky_img = pygame.transform.scale(pygame.image.load(f'pacman/Assets/ghost/blue.png'), (45, 45))
clyde_img = pygame.transform.scale(pygame.image.load(f'pacman/Assets/ghost/orange.png'), (45, 45))
spooked_img = pygame.transform.scale(pygame.image.load(f'pacman/Assets/ghost/powerup.png'), (45, 45))
dead_img = pygame.transform.scale(pygame.image.load(f'pacman/Assets/ghost/dead.png'), (45, 45))
player_x = 450
player_y = 663
direction = 0
#BLINKY
blinky_x = 56
blinky_y = 58
blinky_direction = 0
#INKY
inky_x = 440
inky_y = 438
inky_direction = 2

pinky_x = 440
pinky_y = 438
pinky_direction = 2

clyde_x = 480
clyde_y = 438
clyde_direction = 2

counter = 0 
flicker = False 
# RIGHT , LEFT, UP, DOWN
turns = [False, False, False, False]
direction_command = 0
player_speed = 2 
score = 0
powerup = False
power_counter = 0
eaten_ghost = [False, False, False, False]
targets = [(player_x, player_y),(player_x, player_y),(player_x, player_y),(player_x, player_y)]
blinky_dead = False
inky_dead = False
pinky_dead = False
clyde_dead = False

blinky_box = False
inky_box = False
pinky_box = False
clyde_box = False

ghost_speed = 2
startup_counter = 0 

moving = False 
lives = 3
#BUILDING THE BOARD


class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direction, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target 
        self.speed = speed
        self.img = img
        self.direction = direction
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()
    
    def draw(self):
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(spooked_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect
    
    def check_collisions(self):
        num1 = ((H_SCREEN-50) // 32)
        num2 = ((W_SCREEN//30))
        num3 = 15
        
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y-num3) // num1][self.center_x//num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][(self.center_x) // num2] < 3 \
                    or level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][(self.center_x) // num2] < 3 \
                    or level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead):
                self.turns[2] = True
            
            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                        or level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and self.in_box or self.dead:
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                        or level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and self.in_box or self.dead:
                        self.turns[2] = True
                if 12 <= self.center_x % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                        or level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and self.in_box or self.dead:
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                        or level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and self.in_box or self.dead:
                        self.turns[0] = True
                        
            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                        or level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and self.in_box or self.dead:
                        self.turns[3] = True
                    if level[(self.center_y - num1) // num1][self.center_x // num2] < 3 \
                        or level[(self.center_y - num1) // num1][self.center_x // num2] == 9 and self.in_box or self.dead:
                        self.turns[2] = True
                if 12 <= self.center_x % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                        or level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and self.in_box or self.dead:
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                        or level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and self.in_box or self.dead:
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
            
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 490:
            self.in_box = True
        else:
            self.in_box = False 
            
        return self.turns, self.in_box
    def move_clyde(self):
        # R L U D
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]: 
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.directions = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed 
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos += self.speed 
                else:
                    self.x_pos += self.speed
        elif self.direction == 1: 
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                    
                elif self.target[1] > self.y_pos and self.turns[2]:
                    self .direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]: 
                    self.direction = 0
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.directions = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed 
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos += self.speed 
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2: 
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                    
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self .direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]: 
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.directions = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                    
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self .direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed 
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
               
            
            
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                    
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self .direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction 
                    
        
    
def draw_board():
    
    num1 = ((H_SCREEN - 50) // 32)
    num2 = (W_SCREEN // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (.5*num1)),
                                 (j * num2 + num2, i * num1 + (.5*num1)), 3)
            
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j*num2 - (num2*.4)) - 2, (i * num1 + (.5*num1)), num2, num1], 0, PI/2, 3)
            
            if level[i][j] == 6:
                pygame.draw.arc(screen, color, [(j*num2 + (num2* .5)), (i * num1 + (.5*num1)), num2, num1], PI / 2, PI, 3)
                
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j*num2 + (num2* .5)), (i * num1 - (.4*num1)), num2, num1], PI, 3*PI/2, 3)
            
            if level[i][j] == 8:
                pygame.draw.arc(screen, color, [(j*num2 - (num2* .4)) - 2, (i * num1 - (.4*num1)), num2, num1], 3*PI/2, 2*PI, 3)
                
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (.5*num1)),
                                 (j * num2 + num2, i * num1 + (.5*num1)), 3)
            
def draw_player():
    #RIGHT
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    #LEFT
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    #UP
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter// 5],90), (player_x, player_y))
    #DOWN
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter// 5],270), (player_x, player_y))

def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (H_SCREEN-50) // 32
    num2 = (W_SCREEN//30)
    #CHECK COLLISIONS BASED ON CENTER X AND CENTER Y OF PLAYER
    num3 = 15
    
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery//num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery//num1][(centerx - num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery+num3)//num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery-num3) // num1 ][centerx // num2] < 3:
                turns[2] = True
        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True 
    return turns

def move_player(play_x, play_y):
    #r,l,u,d
    if direction == 0 and turns_allowed[0]: 
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    elif direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y

def get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y):
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:
        if not blinky.dead:
            blinky_target = (runaway_x, runaway_y)
        else:
            blinky_target = return_target
        if not inky.dead:
            inky_target = (runaway_x, player_y)
        else:
            inky_target = return_target 
        if not pinky.dead:
            pinky_target = (player_x, runaway_y)
        else:
            pinky_target = return_target 
        if not clyde.dead:
            clyde_target = (450, 450)
        else:
            clyde_target = return_target 
    else:
        if not blinky.dead:
            if 340 < blinky_x < 560 and 340 < blinky_y < 500:
                blinky_target = (400,100)
            else:
                blinky_target = (player_x, player_y)
        else:
            blinky_target = return_target
        if not inky.dead:
            if 340 < inky_x < 560 and 340 < inky_y < 500:
                inky_target = (400,100)
            else:
                inky_target = (player_x, player_y)
        else:
            inky_target = return_target 
        if not pinky.dead:
            if 340 < pinky_x < 560 and 340 < pinky_y < 500:
                pinky_target = (400,100)
            else:
                pinky_target = (player_x, player_y)
        else:
            pinky_target = return_target 
        if not clyde.dead:
            if 340 < clyde_x < 560 and 340 < clyde_y < 500:
                clyde_target = (400,100)
            else:
                clyde_target = (player_x, player_y)
        else:
            clyde_target = return_target
        
    return [blinky_target, inky_target, pinky_target, clyde_target]
def draw_misc():
    score_text = font.render(f'Score:  {score}', True, 'white')
    screen.blit(score_text, (10, 920))
    if powerup: 
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30,30)), (650 + i*40, 915))

def check_collisions(scor, power, power_count, eaten_ghosts):
    num1 = (H_SCREEN - 50) // 32
    num2 = W_SCREEN // 30
    if 0 < player_x < 870:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            scor += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            scor += 50
            #SETUPS POWER UP
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
    return scor, power, power_count, eaten_ghosts

run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter +=1
        if counter > 4:
            flicker = False
    else:
        counter = 0
        flicker = True
    if powerup and power_counter < 600: 
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]
    
    if startup_counter < 180:
        moving = False 
        startup_counter +=1
    else:
        moving = True; 
    #FILLS BACKGROUND BLACK
    screen.fill('black')
    draw_board()
    draw_player()
    draw_misc()
    blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speed, blinky_img, blinky_direction, blinky_dead, blinky_box, 0)
    inky = Ghost(inky_x, inky_y, targets[1], ghost_speed, inky_img, inky_direction, inky_dead, 
                 inky_box, 1)
    pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speed, pinky_img, pinky_direction, pinky_dead, 
                  pinky_box, 2) 
    clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speed, clyde_img, clyde_direction, clyde_dead, 
                  clyde_box, 3) 
    center_x = player_x + 23
    center_y = player_y + 24
    targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)
    turns_allowed = check_position(center_x, center_y)
    if moving:
        player_x, player_y = move_player(player_x, player_y)
        blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
        pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
        inky_x, inky_y, inky_direction = inky.move_clyde()
        clyde_x, clyde_y, clyde_direction = clyde.move_clyde()
    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost)
   
    #WHAT WE WILL USE FOR USING VOICE RECOGNITION
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = 0
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = 1
            if event.key == pygame.K_UP and direction_command == 2:
                direction_comand = 2
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = 3
        
    for i in range(4):
        if direction_command == i and turns_allowed[i]:
            direction = i
        if player_x > 900:
            player_x = -47
        elif player_x < -50:
            player_x = 897
        
    pygame.display.flip()
pygame.quit()
