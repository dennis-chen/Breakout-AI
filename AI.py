import random
import numpy as np

MAX_X_VEL = 5

NUM_PADDLE_X_STATES = 8
NUM_BALL_X_STATES = 8
NUM_BALL_Y_STATES = 4
NUM_BRICK_STATES = 16
TOTAL_STATES = NUM_PADDLE_X_STATES*NUM_BALL_X_STATES*NUM_BALL_Y_STATES*NUM_BRICK_STATES*NUM_ACTIONS
TOTAL_ACTIONS = 11

class AI():

    def __init__(self, player, ball, blocks):
		self.player = player
		self.ball = ball 
		self.blocks = blocks

    def __init__(self):
        self.q_matrix = np.zeros(TOTAL_STATES+1,TOTAL_ACTIONS)
        self.q_matrix[TOTAL_STATES,:] = -10000

    def get_random_next_move(self):
        return random.randint(0,5)

    def follow_ball(self,model):
        paddle_x = model.paddle.left + model.paddle_width/2
        ball_x = model.ball.left + model.ball_diameter/2
        dist_to_ball = ball_x - paddle_x
        paddle_x_vel = dist_to_ball

        try: direction_to_ball = dist_to_ball/abs(dist_to_ball)
        except: direction_to_ball = 0 #catch divide by zero error
        paddle_x_magnitude = min(abs(dist_to_ball/5),MAX_X_VEL)
        paddle_x_vel = direction_to_ball*paddle_x_magnitude
        model.paddle.left += paddle_x_vel

    def get_qlearn_move(self,model):
        game_state = convert_model_info_to_state(model)
        q = self.q_matrix
        best_action = find_max_reward(q,game_state)
        best_paddle_vel = best_action - 5
        model.paddle.left += paddle_x_vel

    def find_max_reward(q,game_state):
        state_row = q[game_state,:]
        return state_row.argmax()

    def convert_model_info_to_state(self,model):
        if model.state = STATE_GAME_OVER:
            return TOTAL_STATES
        brick_state = self.get_brick_state(model)
        paddle_state = self.get_paddle_state(model)
        ball_state = self.get_paddle_state(model)
        brick_and_paddle_state = brick_state*NUM_PADDLE_X_STATES+paddle_state
        game_state = brick_and_paddle_state*NUM_BALL_X_STATES*NUM_BALL_Y_STATES + ball_state
        return game_state

    def get_paddle_state(self,model):
        """returns int between 0 and 7 that encodes location of paddle"""
        paddle_x = model.paddle.left + model.paddle_width/2
        screen_width,screen_height = model.SCREEN_SIZE
        divisions = NUM_PADDLE_X_STATES
        division_size = int((1.0*screen_width)/divisions)
        paddle_state = paddle_x/division_size
        return paddle_state

    def get_ball_state(self,model):
        """returns int between 0 and 31 that encodes location of the ball"""
        ball_x = model.ball.left + model.ball_diameter/2
        ball_y = model.ball.top + model.ball_diameter/2
        screen_width,screen_height = model.SCREEN_SIZE
        x_divisions = NUM_BALL_X_STATES
        y_divisions = NUM_BALL_Y_STATES
        x_division_size = int((1.0*screen_width)/x_divisions)
        y_division_size = int((1.0*screen_width)/y_divisions)
        ball_x_state = ball_x/x_division_size
        ball_y_state = ball_y/y_division_size
        ball_state = x_divisions*ball_y_state+ball_x_state
        return ball_state

    def get_brick_state(self,model):
        """returns int between 0 and 15 that encodes whether or not there
        are bricks present in one of the 4 discrete columns (2^4 is 16)"""
        brick_cols = model.brick_cols
        brick_col_binary = [None,None,None,None]
        for i, col in enumerate(brick_cols):
            brick_col_binary[i] = (len(brick_cols[i]) > 0)
        brick_state = 0
        for j, val in enumerate(brick_col_binary):
            brick_state += (2**j)*brick_col_binary[j]
        return brick_state


