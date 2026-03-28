import pygame
from random import choice, randint
#credit to https://www.soundjay.com/beep-sounds-1.html for the sound effects
pygame.mixer.init()
speed = float(input("How fast do you want the paddles to be? 0.2-0.4 is recommended. "))
if speed < 0:
    print("I will not allow you to break the game. Try again with a positive number.")
    exit()
elif speed < 0.2:
    print("Warning: The game may be boring with this slow speed, as whoever serves will likely score.")
elif speed > 0.4:
    print("Warning: The game may be too difficult with this fast speed, as it may be hard to react in time.")
    print("Plus, the AI may be difficult or impossible to beat at this speed.")
collect = pygame.mixer.Sound("Downloads/powerup_collect.wav")
beep1 = pygame.mixer.Sound("Downloads/wall_beep_1.wav")
beep2 = pygame.mixer.Sound("Downloads/wall_beep_2.wav")
beep3 = pygame.mixer.Sound("Downloads/wall_beep_3.wav")
beep4 = pygame.mixer.Sound("Downloads/wall_beep_4.wav")
lose1 = pygame.mixer.Sound("Downloads/lose_sound.wav")
lose2 = pygame.mixer.Sound("Downloads/lose_sound_2.wav")
pygame.font.init()
#soundvar.play() to play a sound
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Powerup Pong")
player_ypos = 250
ball_xpos = 390
ball_ypos = 290
player_height = 100
AI_height = 100
ball_xvel = 0
ball_yvel = 0
AI_ypos = 250
player_boost = 1
ai_boost = 1
ball_boost = 1
player_score = False
player_points = 0
AI_points = 0
turn_start = False
bounces = 0
powerup_exists = False
powerup_xpos = -100 #off the screen, invisible to the player
powerup_ypos = -100
font = pygame.font.SysFont("Arial", 100)
score = font.render(str(player_points) + " - " + str(AI_points), False, "White")
text_rect = score.get_rect()
text_rect.center = (400, 50)
class powerup:
    def __init__(self, color, positive_effect, effect):
        self.color = color
        self.positive_effect = positive_effect
        self.effect = effect
    def effect_apply(self):
        #looking back i probably could've just had it check for color and did the effect based on that
        global player_height, AI_height, player_boost, ai_boost, ball_boost
        if self.effect == "ball_boost":
            ball_boost = randint(5, 20)/10 #changes ball speed by a random amount, regardless of who collected it
        elif self.positive_effect == True:
            if self.effect == "boost": #speed boost
                if ball_xvel > 0: #ball moving right, player gets powerup
                    player_boost *= 1.2
                else:
                    ai_boost *= 1.2 #i decided to make powerups stack (except ball boost)
            elif self.effect == "size":
                if ball_xvel > 0:
                    player_height *= 1.2
                else:
                    AI_height *= 1.2
        else:
            if self.effect == "boost":
                if ball_xvel > 0:
                    ai_boost *= 0.83
                else:
                    player_boost *= 0.83
            elif self.effect == "size":
                if ball_xvel > 0:
                    AI_height *= 0.83
                else:
                    player_height *= 0.83
def P1collision(xpos_ball, ypos_ball, ypos_obj):
    if ypos_ball + 20 > ypos_obj and ypos_ball < ypos_obj + player_height:
        if abs(xpos_ball - 40) <= 1: #prevents phasing through with enough speed 
            return True
    return False
def P2collision(xpos_ball, ypos_ball, ypos_obj):
    if ypos_ball + 20 > ypos_obj and ypos_ball < ypos_obj + AI_height:
        if abs(xpos_ball - 740) <= 1:
            return True
    return False 

def Powerupcollision(xpos_ball, ypos_ball, xpos_obj, ypos_obj): #both objects are 20x20, top right corner is considered the position
    if ypos_ball + 20 > ypos_obj and ypos_ball < ypos_obj + 20:
        if xpos_ball + 20 > xpos_obj and xpos_ball < xpos_obj + 20:
            return True
    return False

def score_update():
    global score, bounces, powerup_exists, powerup_xpos, player_height, AI_height, player_boost, ai_boost, ball_boost
    bounces = 0
    powerup_exists = False
    powerup_xpos = -100 #off screen so it's not visible to the player
    player_height = 100
    AI_height = 100
    player_boost = 1 #resets all powerups
    ai_boost = 1
    ball_boost = 1
    score = font.render(str(player_points) + " - " + str(AI_points), False, "White")
while True:
    screen.fill("black")
    if turn_start == False and ball_xpos != 390:
        if player_score == True:
            ball_xpos = 739
            ball_ypos = AI_ypos + 40
        else:
            ball_xpos = 41
            ball_ypos = player_ypos + 40
    screen.fill("black")
    key = pygame.key.get_pressed()
    player = pygame.Rect((10, player_ypos), (30, player_height))
    AI = pygame.Rect((760, AI_ypos), (30, AI_height))
    ball = pygame.Rect((ball_xpos, ball_ypos), (20, 20))
    pygame.draw.rect(screen, (255, 255, 255), player)
    pygame.draw.rect(screen, (255, 255, 255), AI)
    pygame.draw.rect(screen, (255, 255, 255), ball)

    if ball_ypos < 0 or ball_ypos > 580:
        ball_yvel = -ball_yvel
    if key[pygame.K_UP] and player_ypos >= 0:
        player_ypos -= speed * player_boost
    if key[pygame.K_DOWN] and player_ypos <= 600 - player_height: #continuous movement
        player_ypos += speed * player_boost
    if ball_ypos < AI_ypos + 50 and turn_start == True and AI_ypos >= 0:
        AI_ypos -= speed * ai_boost
    if ball_ypos > AI_ypos + 50 and turn_start == True and AI_ypos <= 600 - AI_height: #so you don't go off the screen
        AI_ypos += speed * ai_boost

    ball_ypos += ball_yvel * ball_boost
    ball_xpos += ball_xvel * ball_boost
    if P2collision(ball_xpos, ball_ypos, AI_ypos) or P1collision(ball_xpos, ball_ypos, player_ypos) and turn_start == True:
        ball_xvel = -ball_xvel
        if turn_start == True:
            bounces += 1
            choice([beep1,  beep2, beep3, beep4]).play()
        if bounces >= 7:
            if powerup_exists == False: #I do not want it changing every single bounce
                green = ["Green", True, "boost"] #makes your paddle faster
                blue = ["Blue", True, "size"] #makes your paddle bigger
                red = ["Red", False, "boost"] #makes opponent paddle slower
                yellow = ["Yellow", False, "size"] #makes opponent paddle smaller
                grey = ["Grey", False, "ball_boost"] #changes speed of ball, second var is irrelevant
                choose = choice([red, blue, yellow, green, grey])
                power = powerup(choose[0], choose[1], choose[2])
                [powerup_xpos, powerup_ypos] = [randint(300, 500), randint(100, 500)]
            powerup_exists = True
        if ball_xpos < 400: #player collision
            dist_from_center = (player_ypos - ball_ypos + (player_height-20)/2) #negative value means below, positive above
        else: #ai collision
            dist_from_center = (AI_ypos - ball_ypos + (AI_height-20)/2)
        ball_yvel -= dist_from_center/250
    if powerup_exists == True:
        powerup_rect = pygame.Rect((powerup_xpos, powerup_ypos), (20, 20))
        pygame.draw.rect(screen, power.color, powerup_rect)
        if Powerupcollision(ball_xpos, ball_ypos, powerup_xpos, powerup_ypos):
            power.effect_apply()
            bounces = 0
            collect.set_volume(0.5) #protect's the players ears from a high pitched sound
            collect.play()
            powerup_exists = False
    if ball_xpos <= 0:
        player_score = False
        AI_points += 1
        ball_xpos =  10
        ball_xvel = 0
        ball_yvel = 0
        turn_start = False
        lose1.play()
        score_update()
    elif ball_xpos >= 800:
        player_points += 1
        player_score = True
        ball_xpos = 740
        ball_xvel = 0
        ball_yvel = 0
        turn_start = False
        lose2.play()
        score_update()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and turn_start == False:
                ball_yvel = -0.2
                if player_score:
                    ball_xvel = -0.2
                else:
                    ball_xvel = 0.2
                turn_start = True
    screen.blit(score, text_rect)
    pygame.display.update()

    #it's K_UP/DOWN/LEFT/RIGHT for arrow keys