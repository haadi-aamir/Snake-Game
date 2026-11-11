import pygame
import random
from pygame import mixer

ball_wall_timer = 0
ball_corner_timer = 0
ball_size = 10

# LOADING MUSIC

pygame.mixer.pre_init()
mixer.init()
eating_fx = pygame.mixer.Sound(r'D:\PROGRAMMING\PYTHON\crash_projects\snake_game\music\food.mp3')
eating_fx.set_volume(1.3)
pygame.mixer.music.load(r'D:\PROGRAMMING\PYTHON\crash_projects\snake_game\music\music.mp3')
pygame.mixer.music.play(-1 , 0 , 5000)
pygame.mixer.music.set_volume(0.3)
game_over_fx = pygame.mixer.Sound(r'D:\PROGRAMMING\PYTHON\crash_projects\snake_game\music\gameover.mp3')



class Ball():
    def __init__(self , x , y , screen):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.ball_rect = pygame.Rect(self.x , self.y , self.width , self.height)
        self.screen = screen
  
    def draw(self):
        pygame.draw.rect(self.screen , 'white', self.ball_rect , border_radius=20)
        
class Snake():  
    def __init__(self , screen , screen_widht , screen_height):
        self.snake = pygame.Rect(0 , 0 , 20, 20)
        self.snake_segments = []
        self.timer = 0
        self.direction = 'Right'
        self.ball = Ball(50 , 50 , screen)
        self.body_color = 'white'
        self.head_movement = []
        self.screen = screen
        self.WIDHT = screen_widht
        self.HEIGHT = screen_height
    
    def snake_movement(self):
        # KEY PRESSES
        key = pygame.key.get_pressed()
        if key[pygame.K_s] and self.direction != 'Up':
            self.direction = 'Down'
        elif key[pygame.K_w] and self.direction != 'Down':
            self.direction = 'Up'
        elif key[pygame.K_a] and self.direction != 'Right':
            self.direction = 'Left'  
        elif key[pygame.K_d] and self.direction != 'Left':
            self.direction = 'Right'
    
        # LIMITING THE TIMER SO THE SNAKE IS NOT MOVING AT LIGHT SPEED
        if self.timer > 10: 
            self.head_movement.append((self.snake.x , self.snake.y))
            
            self.timer = 0
            if self.direction == 'Right':
                self.snake.x += 20
            elif self.direction == 'Left':
                self.snake.x -= 20
            elif self.direction == 'Up':
                self.snake.y -= 20
            elif self.direction == 'Down':
                self.snake.y += 20
        self.timer += 1 
        
        if len(self.head_movement) > len(self.snake_segments):
                self.head_movement.pop(0)
        if len(self.snake_segments) > 0:
            for head_movement , segment in zip(self.head_movement , self.snake_segments):
                segment.x = head_movement[0]
                segment.y = head_movement[1]
                pygame.draw.rect(self.screen , self.body_color , segment)

        
        pygame.draw.rect(self.screen, 'red', self.snake)
        
        
        
    def make_sanke_body(self):
        if len(self.snake_segments) > 0:
            last_segment = self.snake_segments[-1]
            snake_body_rect = pygame.Rect(last_segment.x , last_segment.y , 20, 20)
            self.snake_segments.append(snake_body_rect)
        else: 
            snake_body_rect = pygame.Rect(self.snake.x , self.snake.y , 20 , 20)
            self.snake_segments.append(snake_body_rect)
        
        
    def snake_collision_eating(self):
        global ball_wall_timer
        global ball_corner_timer
        global ball_size
        if self.snake.colliderect(self.ball.ball_rect):
            self.ball = None
            eating_fx.play()
            # FOR WALL 
            if ball_wall_timer > 2:
                print('now')
                ball_wall_timer = 0
                wall = random.choice(['Top', 'Bottom', 'Left' , 'Right'])
                if wall == 'Top':
                    x = random.randrange(0, self.WIDHT - ball_size)
                    y = 0
                elif wall == 'Bottom':
                    x = random.randrange(0, self.WIDHT - ball_size)
                    y = self.HEIGHT - ball_size
                elif wall == 'Left':
                    x = 0
                    y = random.randrange(0, self.HEIGHT - ball_size)
                elif wall == 'Right':
                    x = self.WIDHT - ball_size
                    y = random.randrange(0, self.HEIGHT - ball_size)
                self.ball = Ball(x , y, self.screen)
                ball_corner_timer += 1
                
            # FOR CORNER
            elif ball_corner_timer > 6:
                ball_corner_timer = 0
                corners = [(0, 0) , (0 , self.HEIGHT - ball_size) , (self.WIDHT - ball_size , 0) , (self.WIDHT - ball_size , self.HEIGHT - ball_size)]
                x , y = random.choice(corners)
                self.ball = Ball(x , y , self.screen)
                ball_wall_timer += 1
                
            # NORMAL
            else:
                x = random.randrange(0 , self.WIDHT - 20)
                y = random.randrange(0 , self.HEIGHT - 20)
                self.ball = Ball(x , y , self.screen)
                ball_wall_timer += 1
                ball_corner_timer += 1
            self.make_sanke_body()
            
    def snake_collision_boundry(self):
        game_over = False
        # DRAWING BOUNDRY LINES
        pygame.draw.line(self.screen , 'White' , (0,0) , (0 , self.HEIGHT) , 3) #left line
        pygame.draw.line(self.screen , 'White' , (self.WIDHT - 1 , 0) , (self.WIDHT - 1 , self.HEIGHT) , 3) #right line
        pygame.draw.line(self.screen , 'White' , (0,0) , (self.WIDHT - 1 , 0) , 3) #top line
        pygame.draw.line(self.screen , 'White' , (0 , self.HEIGHT - 1) , (self.WIDHT - 1 , self.HEIGHT) , 3) #bottom line
        
        # COLLISION
        if self.snake.x >= self.WIDHT or self.snake.x < 0:
            game_over = True
            return game_over
        if self.snake.y < 0 or self.snake.y >= self.HEIGHT:
            game_over = True
            return game_over
        else:
            game_over = False
            return game_over
        
    def snake_body_collision(self):
        game_over = False
        # SNAKE HEAD IS IN THE LIST SO EXCLUDING THAT:
        if self.snake.collidelist(self.snake_segments[:-1]) != -1:
            game_over = True
            return game_over
        else:
            game_over = False
            return game_over
        
class Button():
    def __init__(self , img ,  x , y , scale , screen):
        img_width = img.get_width()
        img_height = img.get_height()
        self.scale = scale
        self.img = pygame.transform.scale(img, (int(img_width * self.scale) , int(img_height * self.scale)))
        self.rect = img.get_rect()
        self.rect.topleft = (x , y)
        self.x = x
        self.y = y
        self.screen = screen
        self.clicked = False
        
    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                self.clicked = True
                return True     
        if pygame.mouse.get_pressed()[0] == False:
            self.clicked = False
            
        self.screen.blit(self.img , (self.rect.x , self.rect.y))