import pygame

# Screen and Display
width = 1280
height = 720
# 1280 x 800 PERFECT FULL SCREEN (pls modify your display resolution :)
# width = 1920
# height = 1080
icon = pygame.image.load(r'assets\icons\miku.png')      
FPS = 60
clock = pygame.time.Clock()
# screen = pygame.display.set_mode((width, height))
# screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED, vsync=1)
# screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED | pygame.FULLSCREEN, vsync=1) # FULLSCREEN !!!

# display_size = pygame.display.get_desktop_sizes()
# width,height = display_size[0][0]-50, display_size[0][1]-50
# screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

# Colors
white = 'White' #reducing
red = 'Red' #damage/hp
black = 'Black' #blank
green = 'Green' #hp
cyan2 = 'Cyan2' #mana bar color
gold = 'Gold' #special

# special colors        
# 'purple'
# 'blue'
# 'yellow'

IMMEDIATE_RUN = False

HERO1_BOT = False
all_items = False #equip bot with all items
item_page


toggle_hero3 = False
random_pick_p1 = False 
random_pick_p2 = False 


MAIN_VOLUME = 0.05
TEXT_ANTI_ALIASING = False
SMOOTH_BG = False
MAX_ITEM = 4
# MAX DEFAULT ITEM = 4
x_gap = width * 0.078125
item_equip_hashmap = [(x*x_gap)-21 for x in range(2,MAX_ITEM+2)]


hitboxanddistance = False
show_bot_skills = False
show_bot_stats = True

SINGLE_MODE_ACTIVE = False # constant
MUTE = False # constant
SHOW_HITBOX = hitboxanddistance
DRAW_DISTANCE = hitboxanddistance
SHOW_GRID = False

# Pause tracking (used so UI/cooldowns stop while game is paused)
PAUSED = False
# Total milliseconds the game has been paused (accumulated)
PAUSED_TOTAL_DURATION = 0
# Timestamp when pause started (ms) - may be None when not paused
PAUSED_START = None

# Default Dimensions
DEFAULT_WIDTH = width
DEFAULT_HEIGHT = height

# Player Limit
ZERO_WIDTH = 0
TOTAL_WIDTH = width

# Game Settings
DISABLE_HEAL_REGEN = False
DISABLE_MANA_REGEN = False

DEFAULT_HEALTH_REGENERATION = 1.2 # 1.2/s (0.02)
DEFAULT_MANA_REGENERATION = 6.0 # 6.0/s (0.1)


DEFAULT_BASIC_ATK_DMG_BONUS = 1.2
DEFAULT_SPECIAL_SKILL_COOLDOWN = 2000 #120000

LOW_HP = 20
LITERAL_HEALTH_DEAD = 0
SPECIAL_MULTIPLIER = 1 # +dmg
# SPECIAL_MULTIPLIER = 2
MAX_SPECIAL = 200
SPECIAL_DURATION = 0.166667 # Lasts for 30 seconds (0.166666667 = 20s)
# 0.111111 = 30s
# 0.166667 = 20s
'''
Formula:
# Special Decrease Rate = MAX_SPECIAL / SPECIAL_DURATION / FPS
# Special Decrease Rate = 200 / 20 / 60 = 0.166
# I manually modified it

Note: MAX_SPECIAL and SPECIAL_DURATION may be modified by specific hero

'''

MANA_COST_INCREASE = 0.3

DISABLE_SPECIAL_REDUCE = False

# Character Settings
DEFAULT_CHAR_SIZE = 1.25
DEFAULT_CHAR_SIZE_2 = 1.9
DEFAULT_ANIMATION_SPEED = 120
DEFAULT_ANIMATION_SPEED_FOR_JUMPING = 2
JUMP_DELAY = 50
RUNNING_SPEED = 2.2

# Spacing and Positioning
X_POS_SPACING = 100
DEFAULT_X_POS = (int(width)) - 100

# This is the ground position
DEFAULT_Y_POS = ((int(height)) * 0.76) * 1.05 #145 left if height == 720 
'''
DEFAULT_Y_POS = (720 * 0.76) * 1.05
              = 547.2 * 1.05
              = 574.56

DEFAULT_Y_POS = 574

The screen size (gameplay screeen):
background_size = (width, int(height * 0.798))  # 0.798 = 574 / 720

Example: mountains_bg, size:
(main.width, int(main.height * 0.870)) -> 626.4 (accurate as possible) (ONLY IF HEIGHT-50 first)
'''

SPACING_X = int(width * 0.078)
START_OFFSET_X = int(width * 0.039)
SKILL_Y_OFFSET = int(height * 0.896)
ICON_WIDTH = int(width * 0.058)
ICON_HEIGHT = int(height * 0.104)

BASIC_ATK_POSX = int(width * 0.039)
BASIC_ATK_POSY = int(height * 0.896)

BASIC_ATK_POSX_END = width - (int(width * 0.039))


# Physics
DEFAULT_GRAVITY = 0.6
DEFAULT_JUMP_FORCE = -13
JUMP_LOGIC_EXECUTE_ANIMATION = 2

# Bar Settings
WHITE_BAR_SPEED_HP = 0.1
WHITE_BAR_SPEED_MANA = 1
TEXT_DISTANCE_BETWEEN_STATUS_AND_TEXT = 20

RUNNING_ANIMATION_SPEED = 6
# Player Selection
PLAYER_1 = 1
PLAYER_2 = 2
PLAYER_1_SELECTED_HERO = None
PLAYER_2_SELECTED_HERO = None
PLAYER_1_ICON = None
PLAYER_2_ICON = None

# Attack Display
attack_display = pygame.sprite.Group()

# Basic Attack
BASIC_SLASH_ANIMATION = 5
BASIC_SLASH_SIZE = 2
BASIC_SLASH_SIZE_BIG = 3
BASIC_ATK_COOLDOWN = 500
BASIC_FRAME_DURATION = 100

# BASIC_ATK_DAMAGE = 6.5/5 # slow atk
# BASIC_ATK_DAMAGE2 = 2.7/5 # medium 2 atks
# BASIC_ATK_DAMAGE3 = 1.2/5 #fast atk
# BASIC_ATK_DAMAGE4 = 3.2 # ranged

#this does not matter, pls ignore this
BASIC_ATK_DAMAGE = 6.5 # slow atk
BASIC_ATK_DAMAGE2 = 2.7 # medium 2 atks
BASIC_ATK_DAMAGE3 = 1.2 #fast atk
BASIC_ATK_DAMAGE4 = 3.2 # ranged


# Attack Speed Globals (DOTA 2-inspired)
# BASE_ATTACK_SPEED = 100  # Starting AS for all heroes
MIN_ATTACK_SPEED = 20    # Minimum cap (slowest)
MAX_ATTACK_SPEED = 700   # Maximum cap (fastest)
AGILITY_AS_BONUS = 1     # +1 AS per agility point
# BASE_BAT = 1000          # Base Attack Time in ms (1s); override per hero

# Miscellaneous
MULT = 0.7
dmg_mult = 0.05



hero1 = None
hero2 = None





#USER VARIABLE
username = None
user_id = None
user_bio = None









#loading screen
loading_screen_bg = pygame.transform.scale(
        pygame.image.load(r'assets\backgrounds\12.png').convert(), (width, height))

#hero icons
fire_wizard_icon = r'assets\hero profiles\fire wizard prof.png'
wanderer_magician_icon = r'assets\hero profiles\wanderer magician prof.png'
fire_knight_icon = r'assets\hero profiles\Fire Knight.png'
wind_hashashin_icon = r'assets\hero profiles\Wind Hashashin.png'
water_princess_icon = r'assets\hero profiles\Water Princess.png'
forest_ranger_icon = r'assets\hero profiles\Forest Ranger.png'
yurei_icon = r'assets\skill icons\onre\Yuriei.jpg'
chthulu_icon = r'assets\hero profiles\Chthulu.png'

#buttons
play_button_img = r'assets\UI\buttons\BTN PLAY.png'
text_box_img = r'assets\UI\buttons\Button BG.png'
loading_button_img = r'assets\UI\buttons\Loading icon.png'
menu_button_img = r'assets\UI\more\BTN MENU.png' 

#background icons
waterfall_icon = r'assets\backgrounds\map_icon\waterfall_icon.gif'
lava_icon = r'assets\backgrounds\map_icon\magma_chamber_icon.gif'
dark_forest_icon = r'assets\backgrounds\map_icon\dark_forest_icon.gif'
trees_icon = r'assets\backgrounds\map_icon\trees.gif'
mountains_icon = r'assets\backgrounds\map_icon\mountains_icon.gif'
sunset_icon = r'assets\backgrounds\map_icon\sunset_icon.gif'
city_icon = r'assets\backgrounds\map_icon\city icon.gif'

# button modifers

scale = 1
center_pos = (width / 2, height / 2)
# font_size = 100
font_size = int(height * 0.02)# = 14

# Font cache to avoid repeated font creation (expensive)
FONT_PATH = r'assets\\font\\slkscr.ttf'
FONT_PATH_2 = r'assets\\font\\slkscr.ttf'
_FONT_CACHE = {}

def get_font(size, font_path=FONT_PATH):
        """Return a cached pygame Font object for the given size.
        
        If font_path is not provided, uses the default font."""
        try:
                size = int(size)
        except Exception:
                size = 16
        font = _FONT_CACHE.get(size)
        if font is None:
                font = pygame.font.Font(font_path, size)
                _FONT_CACHE[size] = font
        return font

def load_font(font_path, size):
    """
    Load a font dynamically from the given path and size.

    Args:
        font_path: The file path to the font.
        size: The size of the font to load.

    Returns:
        A pygame.Font object.
    """
    try:
        return pygame.font.Font(font_path, size)
    except FileNotFoundError:
        print(f"Font file not found: {font_path}")
        return None

SHOW_MINI_HEALTH_BAR = True
SHOW_MINI_MANA_BAR = False
SHOW_MINI_SPECIAL_BAR = False



summon_display = pygame.sprite.Group()


no_swap = False

# import heroes as main
# def assign_summon_enemy(player_type):
#         for hero in (main.hero1_group if player_type == 2 else main.hero2_group):
#                 hero.enemy += list(summon_display)



















































# a = ['Learn', 'Quiz', 'Practice', 'Contribute'] 
# b = a 
# c = a[:] 

# b[0] = 'Code'
# c[1] = 'Mcq'

# count = 0
# for c in (a, b, c): 
# 	if c[0] == 'Code': 
# 		count += 1
# 	if c[1] == 'Mcq': 
# 		count += 10

# print (count) 
# print(c)
# li = range(100, 110) 
# for i in li:
#     print(i)

# a = [10, 20, 30, 40, 50] 
# b = [1, 2, 3, 4, 5] 
# subtracted = list()
# for a, b in zip(a, b):
#     item = a -b
#     subtracted.append(item)

# print(subtracted)


# li = [2, 3, 9] 
# li = [[x for x in[li]] for x in range(3)] 
# print (li) 


# a = [x for x in range(5)] 
# b = [x for x in range(7) if x in a and x%2==0] 
# print(b)

# a = []
# a.append([1, [2, 3], 4])
# a.extend([7, 8, 9])
# print(a[0][1][1] + a[2])



# a = 'kimhey'
# print(a[0:6:2])

# size = 30
# for i in range(size):
#     count = size - i
#     print(' '