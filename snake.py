import pygame
import sys
from  CLass import Snake , Button , game_over_fx

pygame.init() 
WIDHT , HEIGHT = 800 , 600
screen = pygame.display.set_mode((WIDHT,HEIGHT))
fps = 60
clock = pygame.time.Clock()
menu_screen = True
game_over = False
should_music_play = True

# LOADING AND INTIALINZING BUTTONS

start_button_img = pygame.image.load(r'D:\PROGRAMMING\PYTHON\crash_projects\snake_game\Resources\start_btn.png')
exit_button_img = pygame.image.load(r'D:\PROGRAMMING\PYTHON\crash_projects\snake_game\Resources\exit_btn.png')
restart_button_img = pygame.image.load(r'D:\PROGRAMMING\PYTHON\crash_projects\snake_game\Resources\restart_btn.png')  
start_button = Button(start_button_img , 200 , HEIGHT//2 - 50 , 0.5 , screen)
exit_button = Button(exit_button_img , 410 , HEIGHT//2 - 50 , 0.5 , screen)
restart_button = Button(restart_button_img , 180 , HEIGHT//2 - 50 , 1.5 , screen)

# TEXT ON MENU SCREEN
font = pygame.font.SysFont('Arial', 24)
line1 = font.render('Controls: W - Up | A - Left | S - Down | D - Right', True, (255, 255, 255))
line2 = font.render(' THANK U FROM MY HEART TO SIR DAVID MALAN AND THE WHOLE CS50 TEAM', True , (255,255,255))
text_x1 = WIDHT // 2 - line1.get_width() // 2
text_y1 = HEIGHT // 2 + 100
text_x2 = WIDHT// 2 - line2.get_width()// 2
text_y2 = HEIGHT // 2 + 150



# CREATING FIRST INSTANCE
snake = Snake(screen , WIDHT , HEIGHT)
# MAIN GAME LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    # BACKGROUND COLOR
    screen.fill((104 , 98 , 99)) 
    
    if game_over == False:
        # MENU SCREEN 
        if menu_screen:
            if start_button.draw():
                menu_screen = False
            if exit_button.draw():
                pygame.quit()
                sys.exit()
            screen.blit(line1 , (text_x1, text_y1)) 
            screen.blit(line2 , (text_x2, text_y2)) 
        else:
            snake.snake_movement()
            game_over = snake.snake_collision_boundry()   
            game_over = snake.snake_body_collision()
            snake.snake_collision_eating()
            if snake.ball:
                snake.ball.draw()
    else:
        if should_music_play:
            game_over_fx.play()
        should_music_play = False
        if restart_button.draw():
            should_music_play = True
            snake = Snake(screen , WIDHT , HEIGHT)
            game_over = False
        elif exit_button.draw():
            pygame.quit()
            sys.exit()
            
    # FPS CONTROL
    clock.tick(fps)
    pygame.display.update()