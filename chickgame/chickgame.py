import pgzrun
import math
from time import sleep
import pygame
from threading import Thread
from tqdm import tqdm
from random import *

HEIGHT = 720
WIDTH = 1280
GRAVITY = 10
chick_image = "chick-a"
chick = Actor(chick_image)
green = Actor("block_green")
red = Actor("block_red")
pipe = Actor("pipe_level")
game_over = Actor("game_over")
fixed_blocks = [Actor("block_blue") for i in range(10)]
enemy1 = Actor("enemy1")
global chick_health
chick_health = 3

level = 0
background = pygame.image.load("images/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_ = pygame.image.load("images/background2.jpg")
globaljumping = 0
chick.pos = WIDTH, 0
green.pos = 320, 570
pipe.pos = -10, 100
red.pos = 89, 150
global horizon
horizon = 260
for setblocks in fixed_blocks:
    setblocks.pos = -10000, -10000
game_over.pos = WIDTH / 2, HEIGHT / 2
DEBUG = True
update_levels = True
game_over.image = "null_blank"


def calculate_gravity(gravity=GRAVITY):
    return math.ceil(math.sqrt(gravity))
def draw():
    screen.clear()
    try:
        screen.blit(background,(0, 0))
    except Exception:
        pass
    chick.draw()
    green.draw()
    pipe.draw()
    red.draw()
    enemy1.draw()
    for render_blocks in fixed_blocks:
        render_blocks.draw()
def jump(actor):
    for distance in range(30-calculate_gravity()):
        actor.y -= 30-calculate_gravity()/2-distance
        sleep(0.0071289754892652893546724543)
def game_over_():
    game_over.image = "game_over"
def reset_positions(red_={0:0,1:0}, green_={0:0,1:0}, chick_={0:0,1:0}, pipe_={0:100,1:120}, blocks_=[{},{},{},{},{},{},{},{},{},{}]):
    red.pos = red_[0], red_[1]
    green.pos = green_[0], green_[1]
    chick.pos = chick_[0], chick_[1]
    pipe.pos = pipe_[0], pipe_[1]
    try:
        global fixed_blocks
        for i_block in tqdm(range(len(blocks_)-1)):
            fixed_blocks[i_block].pos = blocks_[i_block][0], blocks_[i_block][1]
    except Exception:
        pass
def update_level(amount=1):
    global level
    level_old = level
    if level < 0:
        level = math.ceil(level_old)
    else:
        level = math.floor(level_old)
    level += amount
def blockbarrier():
    touch_block = []
    for i in fixed_blocks:
        touch_block.append(chick.colliderect(i))
    print(True in touch_block)
    return True in touch_block
def on_key_down(key):
    if key == keys.DOWN:
        chick.y += 10
    if key == keys.RIGHT:
        chick.x += 10
    if key == keys.LEFT:
        chick.x -= 10
    if key == keys.UP:
        if chick.y <= horizon:
            chick.y -= 50
        else:
            print("-")
            chick.y -= 10
            global jumping
            jumping=True
    if key == keys.W and chick.colliderect(green):
        green.y -= 10
    if key == keys.S and chick.colliderect(green):
        green.y += 10
    if key == keys.A and chick.colliderect(green):
        green.x -= 10
    if key == keys.D and chick.colliderect(green):
        green.x += 10
def update():
    try:
        if not chick.y >= horizon and not chick.colliderect(green) and not chick.colliderect(red) and not blockbarrier():
            chick.y += 25
        elif chick.colliderect(red):
            game_over_()
        if chick.colliderect(pipe):
            global level
            update_level()
            
    except KeyboardInterrupt:
        DEBUG = False
        update_levels = False
        quit()
def jumphandelerthread():
    global jumping
    jumping = False
    while True:
        if jumping:
            jump(chick)
            sleep(0.9)
            jumping = False
        if update_levels == False:
            break
def debug_info_thread():
    while True:
        if DEBUG == False:
            break
        print(chick.pos)
        print(jumping)
        print(background)
        print(level)
        sleep(1)
def commandInterface():
    while True:
        command = input()
        if command == "level+":
            global update_level
            update_level()
        if command == "level-":
            update_levels(-1)
        if command == "chgravity":
            global GRAVITY
            GRAVITY += int(input())
        if command == "closegame":
            global DEBUG
            DEBUG = False
            global levels
            update_level()
            update_levels = False
            break
def level_updator_thread():
    while True:
        global level
        if level == 1:
            global background
            background = pygame.image.load("images/background2.jpg")
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            reset_positions(red_={0:380,1:20}, green_={0:400,1:400},chick_={0:1280,1:0})
            level += 0.00001
        if level == 2:
            background = pygame.image.load("images/background.jpeg")
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            reset_positions(red_={0:50,1:60}, green_={0:700,1:550}, chick_={0:560,1:0}, blocks_=[{0:300,1:300},{0:500,1:550}])
            level += 0.00001
        if update_levels == False:
            break
        sleep(0.1)
def enemyAI():
    enemies = [enemy1]
    enemydata = {1:{"enemytype":"1","datanumber":1,"linkedenemy":enemy1,"state":0}}
    for i in enemies:
        i.pos = randint(0,1000), randint(0, 720)
    while True:
        for enemynumber, i in enumerate(enemies):
            if i.y <= horizon and not "1" in enemydata[enemynumber+1]["enemytype"]:
                i.y += 1
                sleep(0.000031923382119392749)
            if i.pos == chick.pos:
                global chick_health
                chick_health -= 1
                if "2" in enemydata[enemynumber+1]["enemytype"]:
                    enemydata[enemynumber+1]["state"] = 1
                i.x -= 500
            if chick.x > i.x:
                i.x += 1
            elif chick.x < i.x:
                i.x -= 1
            elif chick.y > i.y:
                i.y += 1
            elif chick.y < i.y:
                i.y -= 1
            sleep(0.008792346742386572564817642367854)

threads = [Thread(target=jumphandelerthread), Thread(target=debug_info_thread), Thread(target=level_updator_thread), Thread(target=commandInterface), Thread(target=enemyAI)]

if __name__ == 'pgzero.builtins':
    for thread in threads:
        thread.start()
    pgzrun.go()