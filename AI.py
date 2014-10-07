import random

class AI():
	def __init__(self, player, ball, blocks):
		self.player = player
		self.ball = ball 
		self.blocks = blocks

	# def get_next_move(self):
	# 	return random.randint(-4,4)

	def follow_the_ball(self):
		distance = -self.player.rect.x + self.ball.rect.x
		return int(distance/6)

    """AI for breakout game"""

    def __init__(self,player,ball,blocks):
        self.player = player
        self.ball = ball
        self.blocks = blocks

    def get_random_next_move(self):
        return random.randint(0,5)

    def follow_ball(self):
        dist_to_ball = self.ball.rect.x - self.player.rect.x
        return int(dist_to_ball)
