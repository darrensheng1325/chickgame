from time import sleep
sleep(1)
from chickgame import level
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
