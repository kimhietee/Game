import pygame
import random
import heroes as main
from pprint import pprint

# bg_paths = [ # Wrong path, recheck if using these.
#     (r'assets\backgrounds\animated_bg\Ocean_2\2.png', 'static', 0, 'left'),
#     (r'assets\backgrounds\animated_bg\Ocean_2\3.png', 'dynamic', 30, 'right'),
#     (r'assets\backgrounds\animated_bg\Ocean_2\4.png', 'dynamic', 30, 'right')
# ]
# (r'assets\backgrounds\animated_bg\Ocean_2\compiled img.png', 'dynamic', 500, 'right')
class BackgroundHandler: # moves images, very lag if hd image
    def __init__(self, img_paths: list):
        self.layers = []
        for image in img_paths:
            try:
                img = pygame.transform.scale(
                    pygame.image.load(image[0]).convert_alpha(),
                    (main.width, main.DEFAULT_Y_POS + int(720 * 0.1))
                )
                self.layers.append({
                    'img': img,
                    'type': image[1],
                    'interval': image[2],       # how often to move (in ms)
                    'direction': image[3],      # 'left' or 'right'
                    'x': 0,
                    'last_move_time': pygame.time.get_ticks()  # initialize timer
                })
            except Exception as e:
                pprint(f"Error loading background image {image[0]}: {e}")

    def update(self):
        current_time = pygame.time.get_ticks()
        for layer in self.layers:
            if layer['type'] == 'dynamic':
                if current_time - layer['last_move_time'] >= layer['interval']:
                    if layer['direction'] == 'left':
                        layer['x'] -= 1
                        if layer['x'] <= -main.width:
                            layer['x'] = 0
                    elif layer['direction'] == 'right':
                        layer['x'] += 1
                        if layer['x'] >= main.width:
                            layer['x'] = 0
                    layer['last_move_time'] = current_time  # reset timer

    def draw(self, screen):
        for layer in self.layers:
            x = layer['x']
            img = layer['img']

            screen.blit(img, (x, 0))
            if layer['type'] == 'dynamic':
                if layer['direction'] == 'left':
                    screen.blit(img, (x + main.width, 0))
                elif layer['direction'] == 'right':
                    screen.blit(img, (x - main.width, 0))

    
# main background preferred size:
# (main.width, main.DEFAULT_Y_POS + int(720 * 0.1))

class AnimatedBackground: # simple framed background animation (smooth)
    '''
    Make sure the name of frames starts at 1


    size may be:
    - "full"            → full screen
    - "game_bg"         → in-game aspect ratio
    - ["custom", (w,h)] → arbitrary dimensions

    '''
    def __init__(self, path, count, size="full", pos=(0,0), set_alpha=(False, 255), speed=150):  # 0.798 = 574 / 720):
        self.path = path if path.endswith(("\\", "/")) else path + "/"
        self.count = count
        self.pos = pos
        self.set_alpha = set_alpha
        self.frames = []
        self.current_frame = 0
        self.last_update_time = pygame.time.get_ticks()
        self.speed = speed


        if size == "full":
            self.size = (main.width, main.height)
        elif size == "game_bg":
            self.size = (main.width, int(main.height * 0.798)) 
        elif isinstance(size, (list, tuple)) and size[0] == "custom":
            self.size = size[1]
        else:
            raise ValueError(f"Invalid size input: {size!r}")
        


    def load_frames(self, extension=".gif") -> pygame.Surface:
        self.frames.clear()
        for i in range(self.count):
            img_path = f"{self.path}{i+1}{extension}"
            image = pygame.transform.scale(
                pygame.image.load(img_path).convert(),
                self.size
            )
            image.set_alpha(self.set_alpha[1]) if self.set_alpha[0] else None
            self.frames.append(image)

    def load_frames_type2(self, extension=".gif") -> pygame.Surface:
        self.frames.clear()
        for i in range(self.count):
            img_path = fr"{self.path}frame ({i+1}){extension}"
            image = pygame.transform.scale(
                pygame.image.load(img_path).convert(),
                self.size
            )
            image.set_alpha(self.set_alpha[1]) if self.set_alpha[0] else None
            self.frames.append(image)
# img_path = f"assets\backgrounds\animated_bg\Mountains\frame ({i+1}).gif
    def display(self, surface, speed=0):
        """
        surface: pygame.Surface to blit to
        speed: milliseconds per frame
        """
        self.speed=speed if speed>0 else self.speed
        now = pygame.time.get_ticks()
        if now - self.last_update_time > self.speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update_time = now

        surface.blit(self.frames[self.current_frame], (self.pos[0], self.pos[1]))




# background = main.pygame.transform.scale(
#     pygame.image.load(bg_list[random.randint(0, len(bg_list)-1)]).convert(), 
#     (main.width, main.DEFAULT_Y_POS + (720*1.1 - 720)))


# animated_bg = BackgroundHandler(bg_paths)


# ------------------------------------
# Game Backgrounds

waterfall_bg = AnimatedBackground(
    r"assets\backgrounds\animated_bg\Waterfall\\",
    8,
    size="game_bg"
)

lava_bg = AnimatedBackground(
    r"assets\backgrounds\animated_bg\Magma Chamber\\",
    8,
    size="game_bg"
)

dark_forest_bg = AnimatedBackground(
    r"assets\backgrounds\animated_bg\Dark Forest\\",
    8,
    size="game_bg"
)

trees_bg = AnimatedBackground(
    r"assets\backgrounds\animated_bg\Trees\\",
    40,
    size="full",
    pos=(0, -50)
)

mountains_bg = AnimatedBackground(
    r"assets\backgrounds\animated_bg\Mountains\\",
    40,
    size=["custom", (main.width, int(main.height * 0.870))],
    pos=(0, -50)
)

sunset_bg = AnimatedBackground(
    r"assets\backgrounds\animated_bg\Sunset\\",
    40,
    size=["custom", (main.width, main.height-100)]
)

city_bg = AnimatedBackground(
    r"assets\backgrounds\animated_bg\CIty\\",
    107,
    size="game_bg",
    speed=40
)

# ------------------------------------
# Main Menu Background

dragon_bg = AnimatedBackground(
    r"assets\backgrounds\animated_bg\Dragon\\",
    35,
    size=["custom", (main.width, main.height-100)],
    pos=(0,50)
)

# ------------------------------------
# Menu Backgrounds

waterfall_day_bg = AnimatedBackground(
    r"assets\backgrounds\animated_bg\Waterfall - Day\\",
    7,
    size="full"
)

waterfall_rainy_bg = AnimatedBackground(
    r"assets\backgrounds\animated_bg\Waterfall - Rainy\\",
    9,
    size="full"
)
smooth_waterfall_rainy_bg = AnimatedBackground(
    r"assets\backgrounds\animated_bg\Smooth Waterfall - Rainy\\",
    9,
    size="full"
)

waterfall_night_bg = AnimatedBackground(
    r"assets\backgrounds\animated_bg\Waterfall - Night\\",
    11,
    size="full"
)
smooth_waterfall_night_bg = AnimatedBackground(
    r"assets\backgrounds\animated_bg\Smooth Waterfall - Night\\",
    11,
    size="full"
)

green_bg = AnimatedBackground(
    r"assets\backgrounds\animated_bg\green_bg\\",
    192,
    size="full"
)

sword_login = AnimatedBackground(
    r"assets\backgrounds\animated_bg\blue_bg\\",
    250,
    size="full"
)





#Game Background
waterfall_bg.load_frames()
lava_bg.load_frames()
dark_forest_bg.load_frames()
trees_bg.load_frames()
mountains_bg.load_frames_type2()
sunset_bg.load_frames_type2()
city_bg.load_frames_type2()
# trees_bg = mountains_bg

# Main
dragon_bg.load_frames()

# UI
waterfall_day_bg.load_frames()
waterfall_rainy_bg.load_frames()
smooth_waterfall_rainy_bg.load_frames()
waterfall_night_bg.load_frames()
smooth_waterfall_night_bg.load_frames()
# green_bg.load_frames_type2()