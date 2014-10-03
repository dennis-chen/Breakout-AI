import random

class AI():
    """AI for breakout game"""
    def __init__(self,player,ball,blocks):
        self.player = player
        self.ball = ball
        self.blocks = blocks
        self.max_speed = 1

    def get_next_move(self):
        return random.randint(-1*self.max_speed,self.max_speed)
