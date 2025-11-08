import pygame as pg
import sys, time
from bird import Bird
from pipe import Pipe
from characters import CHARACTERS
from progress import ProgressManager

pg.init()

SCORE_COLOR = (255, 0, 0)           
HIGH_SCORE_COLOR = (0, 0, 139)     
MENU_TITLE_COLOR = (255, 215, 0)   
MENU_UNLOCKED_COLOR = (34, 139, 34)  
MENU_LOCKED_COLOR = (120, 120, 120)  
MENU_SELECTED_COLOR = (255, 255, 0) 

class Game:
    def __init__(self):
        self.width = 600
        self.height = 768
        self.ground_y = 568  


        self.progress = ProgressManager("progress.json")

        self.selected_char = self.progress.get_selected()

        self.win = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Skybound Game")

        start_pos = (100, int(self.ground_y * 0.25))
        self.bird = Bird(self.selected_char, start_pos=start_pos)

        self.clock = pg.time.Clock()
        self.base_move_speed = 250
        self.move_speed = self.base_move_speed

        
        self.state = 'menu'

        self.pipes = []
        self.pipe_generate_counter = 71
        self.score = 0
        self.font = pg.font.Font(None, 36)

        self.setUpBgAndGround()

        print("Game initialized selected:", self.selected_char)
        self.gameLoop()

    def gameLoop(self):
        last_time = time.time()
        while True:
            new_time = time.time()
            dt = new_time - last_time
            last_time = new_time

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    
                    if self.state == 'menu':
                        if event.key == pg.K_1:
                            self.try_select("bird")
                        if event.key == pg.K_2:
                            self.try_select("eagle")
                        if event.key == pg.K_3:
                            self.try_select("plane")

                        if event.key == pg.K_RETURN:
                            
                            self.reset_round()
                            self.state = 'playing'
                            self.bird.update_on = True

                    elif self.state == 'playing':
                        
                        if event.key == pg.K_SPACE:
                            self.bird.flap()
                    elif self.state == 'falling':
                        
                        pass

            self.updateEverything(dt)
            self.checkCollisions()
            self.drawEverything()
            pg.display.update()
            self.clock.tick(60)

    def reset_round(self):
        
        self.pipes = []
        self.pipe_generate_counter = 71
        self.score = 0
        self.move_speed = self.base_move_speed
        start_pos = (100, int(self.ground_y * 0.25))
        self.bird = Bird(self.selected_char, start_pos=start_pos)
        self.bird.update_on = False

    def try_select(self, char_name):
    
        if self.progress.is_unlocked(char_name):
            self.selected_char = char_name
            self.progress.set_selected(char_name)
        
            start_pos = (100, int(self.ground_y * 0.25))
            self.bird = Bird(self.selected_char, start_pos=start_pos)
            self.bird.update_on = False

    def checkCollisions(self):
    
        if not self.pipes:
            if self.state == 'playing' and self.bird.rect.bottom >= self.ground_y:
                self.bird.rect.bottom = self.ground_y
                self.bird.y_pos = float(self.bird.rect.y)
                self.bird.update_on = False
                self.state = 'menu'
                self.progress.set_high_score(self.score)
            return

        
        if self.state == 'playing':
            for pipe in self.pipes:
                if self.bird.rect.colliderect(pipe.rect_down) or self.bird.rect.colliderect(pipe.rect_up):
                    
                    self.state = 'falling'
                    self.bird.update_on = True
                    if self.bird.y_velocity < 0:
                        self.bird.y_velocity = 0.0
                    
                    break

            
            if self.state == 'playing' and self.bird.rect.bottom >= self.ground_y:
                self.bird.rect.bottom = self.ground_y
                self.bird.y_pos = float(self.bird.rect.y)
                self.bird.update_on = False
                self.state = 'menu'
                self.progress.set_high_score(self.score)

        
        if self.state == 'falling':
            if self.bird.rect.bottom >= self.ground_y:
                self.bird.rect.bottom = self.ground_y
                self.bird.y_pos = float(self.bird.rect.y)
                self.bird.update_on = False
                self.state = 'menu'
                self.progress.set_high_score(self.score)

    def updateEverything(self, dt):
        target_move_speed = self.base_move_speed + min(150, int(self.score * 2))
        if self.state == 'playing':
            self.move_speed = target_move_speed

            self.ground1_rect.x -= int(self.move_speed * dt)
            self.ground2_rect.x -= int(self.move_speed * dt)

            if self.ground1_rect.right < 0:
                self.ground1_rect.x = self.ground2_rect.right
            if self.ground2_rect.right < 0:
                self.ground2_rect.x = self.ground1_rect.right

            spawn_threshold = max(45, 70 - self.score)
            if self.pipe_generate_counter > spawn_threshold:
                self.pipes.append(Pipe(self.scale_factor_pipe, self.move_speed, score=self.score, screen_width=self.width, ground_y=self.ground_y))
                self.pipe_generate_counter = 0

            self.pipe_generate_counter += 1

            for pipe in self.pipes:
                pipe.move_speed = self.move_speed
                pipe.update(dt)
                if not pipe.passed and self.bird.rect.left > pipe.rect_up.right:
                    self.score += 1
                    pipe.passed = True
                    self.check_for_unlocks()

            if len(self.pipes) != 0 and self.pipes[0].rect_up.right < 0:
                self.pipes.pop(0)

        elif self.state == 'falling':
            pass

        else:
            pass

        self.bird.update(dt, ground_y=self.ground_y)

    def check_for_unlocks(self):
        for name, props in CHARACTERS.items():
            if props.get("unlock_score", 0) <= self.score and not self.progress.is_unlocked(name):
                self.progress.unlock(name)

    def drawEverything(self):
        self.win.blit(self.bg_img, (0, 0))

        for pipe in self.pipes:
            pipe.drawPipe(self.win)

        self.win.blit(self.ground1_img, self.ground1_rect)
        self.win.blit(self.ground2_img, self.ground2_rect)
        self.win.blit(self.bird.image, self.bird.rect)

        score_text = self.font.render(f"Score: {self.score}", True, SCORE_COLOR)
        hs_text = self.font.render(f"High Score: {self.progress.get_high_score()}", True, HIGH_SCORE_COLOR)
        self.win.blit(score_text, (30, 30))
        self.win.blit(hs_text, (30, 66))

        if self.state == 'menu':
            menu_font = pg.font.Font(None, 28)
            text = menu_font.render("Character Menu (press number to select, ENTER to start)", True, MENU_TITLE_COLOR)
            self.win.blit(text, (30, 90))
            y = 130
            i = 1
            for name, props in CHARACTERS.items():
                unlocked = self.progress.is_unlocked(name)
                label = f"{i}. {props.get('display_name', name)}"
                if not unlocked:
                    color = MENU_LOCKED_COLOR
                    label += "  (Locked)"
                else:
                    if name == self.selected_char:
                        color = MENU_SELECTED_COLOR
                        label += "  <-- selected"
                    else:
                        color = MENU_UNLOCKED_COLOR
                line = menu_font.render(label, True, color)
                self.win.blit(line, (30, y))
                y += 34
                i += 1
            hint = menu_font.render("Press ENTER to start with selected character.", True, (180, 180, 180))
            self.win.blit(hint, (30, y + 10))

    def setUpBgAndGround(self):
        bg = pg.image.load("assets/bg.png").convert()
        self.bg_img = pg.transform.smoothscale(bg, (self.width, self.height))

        ground_src = pg.image.load("assets/ground.png").convert()
        ground_height = max(1, self.height - self.ground_y)
        
        self.ground1_img = pg.transform.smoothscale(ground_src, (self.width, ground_height))
        self.ground2_img = pg.transform.smoothscale(ground_src, (self.width, ground_height))

        self.ground1_rect = self.ground1_img.get_rect()
        self.ground2_rect = self.ground2_img.get_rect()

        self.ground1_rect.x = 0
        self.ground2_rect.x = self.ground1_rect.right
        self.ground1_rect.y = self.ground_y
        self.ground2_rect.y = self.ground_y

        
        self.scale_factor_pipe = 0.169

if __name__ == "__main__":
    game = Game()