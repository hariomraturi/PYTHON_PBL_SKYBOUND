import pygame as pg
from random import randint

class Pipe:
    def __init__(self, scale_factor, move_speed, score=0, screen_width=600, ground_y=568):
        base_img_up = pg.image.load("assets/pipeup.png").convert_alpha()
        base_img_down = pg.image.load("assets/pipedown.png").convert_alpha()

        self.scale_factor = scale_factor
        self.move_speed = move_speed
        self.screen_width = screen_width
        self.ground_y = ground_y

        # Gap reduces as score grows
        max_gap_start = 250
        min_gap = 100
        gap_center = max(min_gap, max_gap_start - score * 3)

        low = max(min_gap, gap_center - 30)
        high = min(max_gap_start, gap_center + 20)
        if low > high:
            low, high = min_gap, max_gap_start

        self.pipe_gap = randint(low, high)

        # Choose bottom pipe height (space constraints)
        total_space = self.ground_y
        self.pipe_height = randint(120, int(total_space * 0.6))

        if self.pipe_height + self.pipe_gap > total_space - 40:
            self.pipe_height = total_space - self.pipe_gap - 40
            if self.pipe_height < 40:
                self.pipe_height = 40

        # scale images by scale_factor (explicit)
        w_down, h_down = base_img_down.get_width(), base_img_down.get_height()
        w_up, h_up = base_img_up.get_width(), base_img_up.get_height()

        # target widths keep relative size, heights adjusted
        target_width = max(10, int(w_down * scale_factor * 1.75))
        # For down image scale width to target_width and height to pipe_height
        self.img_down = pg.transform.smoothscale(base_img_down, (target_width, self.pipe_height))
        # For up image height based on top space
        top_height = max(30, self.ground_y - self.pipe_gap - self.pipe_height)
        self.img_up = pg.transform.smoothscale(base_img_up, (target_width, top_height))

        self.rect_down = self.img_down.get_rect()
        self.rect_down.bottom = self.ground_y

        self.rect_up = self.img_up.get_rect()
        self.rect_up.bottom = self.rect_down.top - self.pipe_gap

        # both start at right edge
        self.rect_up.x = self.screen_width
        self.rect_down.x = self.screen_width

        self.passed = False

    def drawPipe(self, win):
        win.blit(self.img_up, self.rect_up)
        win.blit(self.img_down, self.rect_down)

    def update(self, dt):
        move_x = int(self.move_speed * dt)
        self.rect_up.x -= move_x
        self.rect_down.x -= move_x