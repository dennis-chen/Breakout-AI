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