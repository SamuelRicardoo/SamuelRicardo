import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, RESET, PLAY, SCORE
from dino_runner.utils.constants_sound import SCORE_SOUND,RESET_SOUND,START_SOUND
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacle.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

FONT_STYLE = 'freesansbold.ttf'


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.score = 0
        self.death_count = 0
        self.life = 1
        self.font_style = FONT_STYLE
        self.sound_played = False

        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

    def render_text(self,font_style, text, size=22, color=(0, 0, 0), x=0 , y=0):
        font = pygame.font.Font(font_style, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x , y)
        self.screen.blit(text_surface, text_rect)
    
    def play_sound(self):
        if not self.sound_played: 
            if self.death_count == 0:   
                START_SOUND.play()
            else:
                RESET_SOUND.play() 
            self.sound_played = True

    def restart_game(self): 
        self.score = 0
        self.sound_played = False
        self.game_speed = 20
        self.life = 1

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
                
        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.restart_game()
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        while self.playing:
            self.events()
            self.update()
            self.draw()
       
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self)
    
    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            SCORE_SOUND.play()
            self.game_speed += 5
        
    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((0, 255, 255))
        self.draw_background()
        self.draw_score()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.draw_power_up_time()
        self.draw_life()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        score_text = f"      {self.score}"
        x = 1000
        y = 50
        self.render_text(self.font_style, score_text,x = x+10 , y = y+1)
        self.screen.blit(SCORE, (x- SCORE.get_width(),y - SCORE.get_height() // 2))

    def draw_life(self):
        text_life = "Life: {}".format(self.life)
        self.render_text(self.font_style, text_life, x = 50, y = 51)


    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                self.render_text(self.font_style, f"{self.player.type.capitalize()} enabled for {time_to_show} seconds", x=500, y=50)
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE
                
    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.check_button_click(mouse_pos):
                    self.run()

    def check_button_click(self, mouse_pos):   
        button_width = RESET.get_width()
        button_height = RESET.get_height()
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        button_y = SCREEN_HEIGHT // 2 - button_height // 2
        if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
            return True   
        return False

    def show_menu(self):
        self.screen.fill((0,255,255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        x_reset = half_screen_width - RESET.get_width() // 2
        y_reset = half_screen_height - RESET.get_height() // 2

        if self.death_count == 0:
            self.screen.blit(PLAY, (x_reset, y_reset))
            text_start = "Press to start"
            self.render_text(self.font_style, text_start, x = half_screen_width, y = half_screen_height+100)
            self.play_sound()
        else:
            self.screen.blit(RESET, (x_reset, y_reset))
            text_restart = "Press to Restart"
            text_death_count = "Death Count: {}".format(self.death_count)
            self.render_text(self.font_style, text_restart, x=half_screen_width, y=y_reset + RESET.get_height() + 5)
            self.render_text(self.font_style, text_death_count, x=half_screen_width, y=y_reset + RESET.get_height() + 35)
            self.draw_score()
            self.play_sound()
           
        pygame.display.flip()

        self.handle_events_on_menu()