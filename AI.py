import random

class AI():

	def __init__(self, player, ball, blocks):
		self.player = player
		self.ball = ball 
		self.blocks = blocks

	# def get_next_move(self):
	# 	return random.randint(-4,4)

	# def follow_the_ball(self):
	# 	distance = -self.player.rect.x + self.ball.rect.x
	# 	return int(distance/6)

    # def get_random_next_move(self):
    #     return random.randint(0,5)

    def __init__(self):
        pass

    def get_random_next_move(self):
        return random.randint(0,5)

    def follow_ball(self,model):
        paddle_x = model.paddle.left + model.paddle_width/2
        ball_x = model.ball.left + model.ball_diameter/2
        dist_to_ball = ball_x - paddle_x
        paddle_x_vel = dist_to_ball/5
        model.paddle.left += paddle_x_vel
