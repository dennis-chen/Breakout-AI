"""
 bricka (a breakout clone)
 Developed by Leonel Machava <leonelmachava@gmail.com>
 Super heavily modified and put into MVC by Dennis & Fillippos

 http://codeNtronix.com
"""
import pygame
from AI import AI

SCREEN_SIZE   = 480,480

# Object dimensions
BRICK_WIDTH   = 120
BRICK_HEIGHT  = 20
PADDLE_WIDTH  = 60
PADDLE_HEIGHT = 12
BALL_DIAMETER = 16
BALL_RADIUS   = BALL_DIAMETER / 2

MAX_PADDLE_X = SCREEN_SIZE[0] - PADDLE_WIDTH
MAX_BALL_X   = SCREEN_SIZE[0] - BALL_DIAMETER
MAX_BALL_Y   = SCREEN_SIZE[1] - BALL_DIAMETER

# Paddle Y coordinate
PADDLE_Y = SCREEN_SIZE[1] - PADDLE_HEIGHT - 10

# Color constants
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE  = (0,0,255)
BRICK_COLOR = (200,200,0)

# State constants
STATE_BALL_IN_PADDLE = 0
STATE_PLAYING = 1
STATE_WON = 2
STATE_GAME_OVER = 3

class BrickView:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("bricka (a breakout clone by codeNtronix.com)")
        if pygame.font:
            self.font = pygame.font.Font(None,30)
        else:
            self.font = None

    def show_stats(self,model):
        if self.font:
            font_surface = self.font.render("SCORE: " + str(model.score) + " LIVES: " + str(model.lives), False, WHITE)
            self.screen.blit(font_surface, (150,5))

    def show_message(self,message):
        if message is None:
            return
        if self.font:
            size = self.font.size(message)
            font_surface = self.font.render(message,False, WHITE)
            x = (SCREEN_SIZE[0] - size[0]) / 2
            y = (SCREEN_SIZE[1] - size[1]) / 2
            self.screen.blit(font_surface, (x,y))

    def fill_screen(self,color):
        self.screen.fill(color)

    def draw_brick_paddle_ball(self,model):
        # Draw paddle
        pygame.draw.rect(self.screen, BLUE, model.paddle)
        # Draw ball
        pygame.draw.circle(self.screen, WHITE, (model.ball.left + BALL_RADIUS, model.ball.top + BALL_RADIUS), BALL_RADIUS)
        # Draw bricks
        for brick in model.bricks:
            pygame.draw.rect(self.screen, BRICK_COLOR, brick)

        self.show_stats(model)
        pygame.display.flip()

    def kill_game(self):
        pygame.quit()

class BrickModel:

    def __init__(self):
        self.lives = 1
        self.score = 0
        self.state = STATE_PLAYING
        self.paddle   = pygame.Rect(300,PADDLE_Y,PADDLE_WIDTH,PADDLE_HEIGHT)
        self.ball     = pygame.Rect(300,PADDLE_Y - BALL_DIAMETER,BALL_DIAMETER,BALL_DIAMETER)
        self.ball_vel = [5,5]
        self.x_num_bricks = 4
        self.y_num_bricks = 4
        self.create_bricks(0,0,1,1,self.y_num_bricks,self.x_num_bricks)
        self.brick_width = BRICK_WIDTH
        self.brick_height = BRICK_HEIGHT
        self.paddle_width = PADDLE_WIDTH
        self.paddle_height = PADDLE_HEIGHT
        self.ball_diameter = BALL_DIAMETER
        self.SCREEN_SIZE = SCREEN_SIZE

    def create_bricks(self,i_x_ofs,i_y_ofs,x_spacing,y_spacing,y_num_bricks,x_num_bricks):
        y_ofs = i_y_ofs
        self.bricks = []
        self.brick_cols = [[],[],[],[]]
        for i in range(y_num_bricks):
            x_ofs = i_x_ofs
            for j in range(x_num_bricks):
                brick = pygame.Rect(x_ofs,y_ofs,BRICK_WIDTH,BRICK_HEIGHT)
                self.bricks.append(brick)
                self.brick_cols[j].append(brick)
                x_ofs += BRICK_WIDTH + x_spacing
            y_ofs += BRICK_HEIGHT + y_spacing

    def move_ball(self):
        self.ball.left += self.ball_vel[0]
        self.ball.top  += self.ball_vel[1]
        #check left and right wall collisions
        if self.ball.left <= 0:
            self.ball.left = 0
            self.ball_vel[0] = -self.ball_vel[0]
        elif self.ball.left >= MAX_BALL_X:
            self.ball.left = MAX_BALL_X
            self.ball_vel[0] = -self.ball_vel[0]
        #check top and bottom collisions? is the bottom collision check useless?
        if self.ball.top < 0:
            self.ball.top = 0
            self.ball_vel[1] = -self.ball_vel[1]

    def check_paddle_collisions(self):
        if self.paddle.left < 0:
            self.paddle.left = 0
        if self.paddle.left > MAX_PADDLE_X:
            self.paddle.left = MAX_PADDLE_X

    def handle_collisions(self):
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                self.score += 3
                self.ball_vel[1] = -self.ball_vel[1]
                self.bricks.remove(brick)
                self.brick_cols.remove(brick)
                break

        if len(self.bricks) == 0:
            self.state = STATE_WON

        if self.ball.colliderect(self.paddle):
            ball_x = self.ball.left + BALL_DIAMETER/2
            paddle_x = self.paddle.left + PADDLE_WIDTH/2
            dist_along_paddle = ball_x - paddle_x
            self.ball.top = PADDLE_Y - BALL_DIAMETER
            self.ball_vel[1] = -self.ball_vel[1]
            self.ball_vel[0] = dist_along_paddle/3
        elif self.ball.top > self.paddle.top:
            self.lives -= 1
            if self.lives > 0:
                self.state = STATE_BALL_IN_PADDLE
            else:
                self.state = STATE_GAME_OVER
        self.check_paddle_collisions()

    def check_states(self):
        display_msg = None
        if self.state == STATE_PLAYING:
            self.move_ball()
            self.handle_collisions()
        elif self.state == STATE_BALL_IN_PADDLE:
            self.ball.left = self.paddle.left + self.paddle.width / 2
            self.ball.top  = self.paddle.top - self.ball.height
            display_msg = "PRESS SPACE TO LAUNCH THE BALL"
        elif self.state == STATE_GAME_OVER:
            display_msg = "GAME OVER. PRESS ENTER TO PLAY AGAIN"
        elif self.state == STATE_WON:
            display_msg = "YOU WON! PRESS ENTER TO PLAY AGAIN"
        return display_msg, self.state == STATE_GAME_OVER

class BrickController():

    def __init__(self):
        self.ai = AI()

    def ai_update_model(self,model):
        self.ai.follow_ball(model)

    def controller_update_model(self,model):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            model.paddle.left -= 5
            if model.paddle.left < 0:
                model.paddle.left = 0

        if keys[pygame.K_RIGHT]:
            model.paddle.left += 5
            if model.paddle.left > MAX_PADDLE_X:
                model.paddle.left = MAX_PADDLE_X

        if keys[pygame.K_SPACE] and model.state == STATE_BALL_IN_PADDLE:
            model.ball_vel = [5,-5]
            model.state = STATE_PLAYING
        elif keys[pygame.K_RETURN] and (model.state == STATE_GAME_OVER or model.state == STATE_WON):
            self.init_game()

class BrickGame():

    def __init__(self):
        self.m = BrickModel()
        self.v = BrickView()
        self.c = BrickController()
        self.clock = pygame.time.Clock()

    def run_game(self):
        game_over = False
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.v.kill_game()

            self.clock.tick(50)
            self.v.fill_screen(BLACK)
            self.c.ai_update_model(self.m)
            display_msg,game_over = self.m.check_states()
            self.v.show_message(display_msg)
            self.v.draw_brick_paddle_ball(self.m)
        self.v.kill_game()

if __name__ == "__main__":
    b = BrickGame()
    b.run_game()
