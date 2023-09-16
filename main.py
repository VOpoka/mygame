import random

import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

HEIGTH=800
WIDTH=1200

FPS=pygame.time.Clock()

COLOR_WHITE=(255, 255, 255)
COLOR_BLACK=(0, 0, 0)
COLOR_BLUE=(0, 0, 255)
COLOR_GREEN=(0, 255, 0)

main_display=pygame.display.set_mode((WIDTH, HEIGTH))

player_size=(20, 20)
player=pygame.Surface(player_size)
player.fill((COLOR_WHITE))
player_rect=player.get_rect()
#player_speed=[1, 1]
player_move_down=[0, 1]
player_move_left=[-1, 0]
player_move_up=[0, -1]
player_move_right=[1, 0]

def create_enemy():
    enemy_size=(30, 30)
    enemy=pygame.Surface(enemy_size)
    enemy.fill(COLOR_BLUE)
    enemy_rect=pygame.Rect(WIDTH, random.randint(0, HEIGTH), *enemy_size)
    enemy_move=[random.randint(-6, -1), 0]
    return [enemy, enemy_rect, enemy_move]

CREATE_ENEMY=pygame.USEREVENT+1
pygame.time.set_timer(CREATE_ENEMY, 1500)
enemies=[]
def create_prize():
    prize_size=(35, 35)
    prize=pygame.Surface(prize_size)
    prize.fill(COLOR_GREEN)
    prize_rect=pygame.Rect(random.randint(0, WIDTH), 0, *prize_size)
    prize_move=[0, random.randint(1,6)]
    return [prize, prize_rect, prize_move]

CREATE_PRIZE=pygame.USEREVENT+2
pygame.time.set_timer(CREATE_PRIZE, 1900)
prizeies=[]

playing=True
while playing:
    FPS.tick(240)    
    for event in pygame.event.get():
        if event.type==QUIT:
            playing=False
        if event.type==CREATE_ENEMY:
            enemies.append(create_enemy())
                     
        if event.type==CREATE_PRIZE:
            prizeies.append(create_prize())                      
    
    main_display.fill(COLOR_BLACK) 
    keys=pygame.key.get_pressed()
    
    if keys[K_DOWN]and player_rect.bottom<HEIGTH:
        player_rect=player_rect.move(player_move_down)
        
    if keys[K_UP]and player_rect.top>0:
        player_rect=player_rect.move(player_move_up)
        
    if keys[K_LEFT]and player_rect.left>0:
        player_rect=player_rect.move(player_move_left)
        
    if keys[K_RIGHT]and player_rect.right<WIDTH:
        player_rect=player_rect.move(player_move_right)
        
    main_display.blit(player, player_rect)
        
    for enemy in enemies:
        enemy[1]=enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])
        
    for prize in prizeies:
        prize[1]=prize[1].move(prize[2])
        main_display.blit(prize[0], prize[1])
          
    pygame.display.flip() 
    
    for enemy in enemies:
        if enemy[1].left<0:
            enemies.pop(enemies.index(enemy))
            
    for prize in prizeies:
        if prize[1].bottom<0:
            prizeies.pop(prizeies.index(prize))
        
         
        
    
