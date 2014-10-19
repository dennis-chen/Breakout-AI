import random

class AI():

    def __init__(self, player, ball, blocks):
		self.player = player
		self.ball = ball 
		self.blocks = blocks

    def __init__(self):
        self.MAX_X_VEL = 5

    def get_random_next_move(self):
        return random.randint(0,5)

    def follow_ball(self,model):
        paddle_x = model.paddle.left + model.paddle_width/2
        ball_x = model.ball.left + model.ball_diameter/2
        dist_to_ball = ball_x - paddle_x
        paddle_x_vel = dist_to_ball

        try: direction_to_ball = dist_to_ball/abs(dist_to_ball)
        except: direction_to_ball = 0
        paddle_x_magnitude = min(abs(dist_to_ball/5),self.MAX_X_VEL)
        paddle_x_vel = direction_to_ball*paddle_x_magnitude
        model.paddle.left += paddle_x_vel
