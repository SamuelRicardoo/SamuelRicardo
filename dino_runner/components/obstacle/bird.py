import random

from dino_runner.components.obstacle.obstacle import Obstacle


class Bird(Obstacle):
    def __init__(self,image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = self.generate_y_bird()
        self.index = 0

    def generate_y_bird(self):
        return random.randrange(50,250,90)    

    def draw(self, screen):
        if self.index >= 10:
            self.index = 0
        screen.blit(self.image[self.index//5],(self.rect.x, self.rect.y))
        self.index +=1