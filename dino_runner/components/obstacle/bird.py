import random

from dino_runner.components.obstacle.obstacle import Obstacle

Y_POS_BIRD = random.randrange(40, 250, 90)


class Bird(Obstacle):
    def __init__(self,image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = Y_POS_BIRD
        self.index = 0

    def draw(self, screen):
        global Y_POS_BIRD
        if self.index >= 9:
            self.index = 0
        screen.blit(self.image[self.index//5],(self.rect.x, self.rect.y))
        self.index +=1
        Y_POS_BIRD = random.randrange(40, 250, 90)     