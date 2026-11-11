import pygame
import sys
import random
from pygame import mixer
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_SIZE = 10
FPS = 60


# TEXT ON MENU SCREEN
font = pygame.font.SysFont('Arial', 24)
line1 = font.render('Controls: W - Up | A - Left | S - Down | D - Right', True, (255, 255, 255))
line2 = font.render(' THANK U FROM MY HEART TO SIR DAVID MALAN AND THE WHOLE CS50 TEAM', True , (255,255,255))
text_x1 = WIDTH // 2 - line1.get_width() // 2
text_y1 = HEIGHT // 2 + 100
text_x2 = WIDTH// 2 - line2.get_width()// 2
text_y2 = HEIGHT // 2 + 150

# Load Sounds
def load_sounds():
    pygame.mixer.pre_init()
    mixer.init()
    eating_fx = pygame.mixer.Sound(
        r"D:\PROGRAMMING\PYTHON\crash_projects\snake_game\music\food.mp3"
    )
    eating_fx.set_volume(1.3)
    pygame.mixer.music.load(r"D:\PRORAMMING\PYTHON\crash_projects\snake_game\music\music.mp3")
    pygame.mixer.music.play(-1, 0, 5000)
    pygame.mixer.music.set_volume(0.3)
    game_over_fx = pygame.mixer.Sound(
        r"D:PROGRAMMING\\PYTHON\crash_projects\snake_game\music\gameover.mp3"
    )
    return eating_fx, game_over_fx


# Ball Class
class Ball:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.width = BALL_SIZE
        self.height = BALL_SIZE
        self.ball_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen, "white", self.ball_rect, border_radius=20)


# Snake Class
class Snake:
    def __init__(self, screen, screen_width, screen_height):
        self.snake = pygame.Rect(0, 0, 20, 20)
        self.snake_segments = []
        self.timer = 0
        self.direction = "Right"
        self.ball = Ball(50, 50, screen)
        self.body_color = "white"
        self.head_movement = []
        self.screen = screen
        self.WIDTH = screen_width
        self.HEIGHT = screen_height

    def snake_movement(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_s] and self.direction != "Up":
            self.direction = "Down"
        elif key[pygame.K_w] and self.direction != "Down":
            self.direction = "Up"
        elif key[pygame.K_a] and self.direction != "Right":
            self.direction = "Left"
        elif key[pygame.K_d] and self.direction != "Left":
            self.direction = "Right"

        if self.timer > 10:
            self.head_movement.append((self.snake.x, self.snake.y))
            self.timer = 0

            if self.direction == "Right":
                self.snake.x += 20
            elif self.direction == "Left":
                self.snake.x -= 20
            elif self.direction == "Up":
                self.snake.y -= 20
            elif self.direction == "Down":
                self.snake.y += 20

        self.timer += 1
        if len(self.head_movement) > len(self.snake_segments):
            self.head_movement.pop(0)

        if len(self.snake_segments) > 0:
            for head_movement, segment in zip(self.head_movement, self.snake_segments):
                segment.x = head_movement[0]
                segment.y = head_movement[1]
                pygame.draw.rect(self.screen, self.body_color, segment)

        pygame.draw.rect(self.screen, "red", self.snake)

    def make_sanke_body(self):
        if len(self.snake_segments) > 0:
            last_segment = self.snake_segments[-1]
            snake_body_rect = pygame.Rect(last_segment.x, last_segment.y, 20, 20)
            self.snake_segments.append(snake_body_rect)
        else:
            snake_body_rect = pygame.Rect(self.snake.x, self.snake.y, 20, 20)
            self.snake_segments.append(snake_body_rect)

    def snake_collision_eating(self, eating_fx):
        if self.snake.colliderect(self.ball.ball_rect):
            self.ball = None
            eating_fx.play()
            self.make_new_ball()
            self.make_sanke_body()

    def make_new_ball(self):
        x = random.randrange(0, self.WIDTH - BALL_SIZE)
        y = random.randrange(0, self.HEIGHT - BALL_SIZE)
        self.ball = Ball(x, y, self.screen)

    def snake_collision_boundry(self):
        game_over = False
        # DRAWING BOUNDRY LINES
        pygame.draw.line(self.screen , 'White' , (0,0) , (0 , self.HEIGHT) , 3) #left line
        pygame.draw.line(self.screen , 'White' , (self.WIDTH - 1 , 0) , (self.WIDTH - 1 , self.HEIGHT) , 3) #right line
        pygame.draw.line(self.screen , 'White' , (0,0) , (self.WIDTH - 1 , 0) , 3) #top line
        pygame.draw.line(self.screen , 'White' , (0 , self.HEIGHT - 1) , (self.WIDTH - 1 , self.HEIGHT) , 3) #bottom line
        
        # COLLISION
        if self.snake.x >= self.WIDTH or self.snake.x < 0:
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


# Button Class
class Button:
    def __init__(self, img, x, y, scale, screen):
        img_width = img.get_width()
        img_height = img.get_height()
        self.scale = scale
        self.img = pygame.transform.scale(
            img, (int(img_width * self.scale), int(img_height * self.scale))
        )
        self.rect = img.get_rect()
        self.rect.topleft = (x, y)
        self.screen = screen
        self.clicked = False

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                return True
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        self.screen.blit(self.img, (self.rect.x, self.rect.y))


# Additional Functions
def display_menu(screen, start_button, exit_button):
    # Draw Menu Screen
    screen.fill((104, 98, 99))
    if start_button.draw():
        return False  # Start the game
    if exit_button.draw():
        pygame.quit()
        sys.exit()
    return True  # Stay in menu


def handle_game_over(screen, restart_button, exit_button, snake):
    screen.fill((104, 98, 99))
    if restart_button.draw():
        snake.__init__(screen, WIDTH, HEIGHT)  # Reset the snake
        return False  # Not game over
    elif exit_button.draw():
        pygame.quit()
        sys.exit()
    return True  # Still game over


def main():
    should_music_play = True
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    menu_screen = True
    game_over = False

    # Load Sounds
    eating_fx, game_over_fx = load_sounds()

    # Load Buttons
    start_button_img = pygame.image.load(
        r"D:\PROGRAMMING\PYTHON\crash_projects\snake_game\Resources\start_btn.png"
    )
    exit_button_img = pygame.image.load(
        r"D:\PROGRAMMING\PYTHON\crash_projects\snake_game\Resources\exit_btn.png"
    )
    restart_button_img = pygame.image.load(
        r"D:\PROGRAMMING\PYTHON\crash_projects\snake_game\Resources\restart_btn.png"
    )

    start_button = Button(start_button_img, 200, HEIGHT // 2 - 50, 0.5, screen)
    exit_button = Button(exit_button_img, 410, HEIGHT // 2 - 50, 0.5, screen)
    restart_button = Button(restart_button_img, 180, HEIGHT // 2 - 50, 1.5, screen)

    snake = Snake(screen, WIDTH, HEIGHT)

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
                snake.snake_collision_eating(eating_fx)
                if snake.ball:
                    snake.ball.draw()
        else:
            if should_music_play:
                game_over_fx.play()
            should_music_play = False
            if restart_button.draw():
                should_music_play = True
                snake = Snake(screen , WIDTH , HEIGHT)
                game_over = False
            elif exit_button.draw():
                pygame.quit()
                sys.exit()
                
        # FPS CONTROL
        clock.tick(FPS)
        pygame.display.update()


if __name__ == "__main__":
    main()
