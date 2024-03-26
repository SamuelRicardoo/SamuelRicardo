import random
import pygame

from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.extra_life import Heart
from dino_runner.components.power_ups.hammer import Hammer
from dino_runner.utils.constants import DEFAULT_TYPE


class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.when_appears = 0

    def generate_power_up(self, score):
        choose_appear = random.randint(0,2)
        if len(self.power_ups) == 0 and self.when_appears == score:
            self.when_appears += random.randint(200, 300)
            if choose_appear == 0:
                self.power_ups.append(Shield())
            elif choose_appear == 1:
                self.power_ups.append(Heart())
            elif choose_appear == 2:
                self.power_ups.append(Hammer())

    def update(self, game):
        self.generate_power_up(game.score)
        for power_up in self.power_ups:
            power_up.update(game.game_speed, self.power_ups)
            if game.player.dino_rect.colliderect(power_up.rect):
                if game.player.type == DEFAULT_TYPE and isinstance(power_up, Heart):
                    game.life +=1
                    game.player.has_power_up = False
                    self.power_ups.remove(power_up)
                else:
                    power_up.start_time = pygame.time.get_ticks()
                    game.player.has_power_up = True
                    game.player.type = power_up.type
                    game.player.power_up_time = power_up.start_time + (power_up.duration * 1000)
                    self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_ups(self):
        self.power_ups = []
        self.when_appears = random.randint(200, 300)