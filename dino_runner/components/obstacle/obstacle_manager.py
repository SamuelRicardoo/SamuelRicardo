import pygame
import random

from dino_runner.components.obstacle.cactus import Cactus
from dino_runner.components.obstacle.bird import Bird
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD,HAMMER_TYPE,DEFAULT_TYPE
from dino_runner.utils.constants_sound import COLISON_SOUND


class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        if len(self.obstacles) == 0:
            self.random_obstacle = random.randint(0,2)
            if self.random_obstacle == 0:
                self.obstacles.append(Bird(BIRD))
            elif self.random_obstacle == 1:
                self.obstacles.append(Cactus(SMALL_CACTUS))
            elif self.random_obstacle == 2:
                self.obstacles.append(Cactus(LARGE_CACTUS))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.has_power_up and game.life == 0:
                    COLISON_SOUND.play() #som de colisção adicionado
                    pygame.time.delay(500)
                    game.playing = False
                    game.death_count +=1
                    break
                elif game.player.type == DEFAULT_TYPE:
                    game.life -= 1
                    self.obstacles.remove(obstacle)
                elif game.player.type == HAMMER_TYPE: 
                    self.obstacles.remove(obstacle)
                    
    def reset_obstacles(self):
        self.obstacles = []

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)