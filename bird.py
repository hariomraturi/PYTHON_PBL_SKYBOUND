import pygame as pg
from characters import CHARACTERS

def safe_load_image(path):
    try:
        return pg.image.load(path).convert_alpha()
    except Exception:
        return None

class Bird(pg.sprite.Sprite):
    def __init__(self, char_name="bird", start_pos=(100, 100)):
        super(Bird, self).__init__()
        self.char_name = char_name if char_name in CHARACTERS else "bird"
        char = CHARACTERS[self.char_name]

        base_target_height = 40
        scale_mult = char.get("scale", 1.0)
        target_height = max(12, int(base_target_height * scale_mult))

        up_path = char.get("img_up", "")
        down_path = char.get("img_down", "")

        img_up = safe_load_image(up_path) if up_path else None
        img_down = safe_load_image(down_path) if down_path else None

        if img_up is None:
            img_up = safe_load_image(f"assets/{self.char_name}up.png") or safe_load_image(f"assets/{self.char_name}_up.png")
        if img_down is None:
            img_down = safe_load_image(f"assets/{self.char_name}down.png") or safe_load_image(f"assets/{self.char_name}_down.png")

        if img_up is None:
            img_up = safe_load_image("assets/birdup.png")
        if img_down is None:
            img_down = safe_load_image("assets/birddown.png")

        if img_up is None:
            img_up = pg.Surface((34, 24), pg.SRCALPHA)
            img_up.fill((255, 200, 0))
        if img_down is None:
            img_down = pg.Surface((34, 24), pg.SRCALPHA)
            img_down.fill((255, 120, 0))

        def scale_to_height(img, desired_h):
            w, h = img.get_width(), img.get_height()
            if h == 0:
                return pg.transform.smoothscale(img, (desired_h, desired_h))
            new_w = max(1, int(w * (desired_h / h)))
            return pg.transform.smoothscale(img, (new_w, desired_h))

        img_up = scale_to_height(img_up, target_height)
        img_down = scale_to_height(img_down, max(12, int(target_height * 0.85)))

        self.img_list = [img_up, img_down]
        self.image_index = 0
        self.image = self.img_list[self.image_index]

        self.rect = self.image.get_rect(center=start_pos)

        self.y_pos = float(self.rect.y)
        self.y_velocity = 0.0 
        self.gravity = float(char.get("gravity", 900.0))
        self.flap_speed = float(char.get("flap_speed", 300.0))

        self.anim_counter = 0
        self.update_on = False

    def update(self, dt, ground_y=568):
        if self.update_on:
            self.playAnimation()
            self.applyGravity(dt)

            if self.y_pos < 0:
                self.y_pos = 0.0
                if self.y_velocity < 0:
                    self.y_velocity = 0.0
            self.rect.y = int(self.y_pos)

        
        if self.rect.top < 0:
            self.rect.top = 0
            self.y_pos = float(self.rect.y)

    def applyGravity(self, dt):
        
        self.y_velocity += self.gravity * dt
        self.y_pos += self.y_velocity * dt
        self.rect.y = int(self.y_pos)

    def flap(self):
        self.y_velocity = -self.flap_speed

    def playAnimation(self):
        self.anim_counter += 1
        if self.anim_counter >= 6:
            self.image = self.img_list[self.image_index]
            self.image_index = 1 - self.image_index
            self.anim_counter = 0