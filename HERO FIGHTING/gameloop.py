import pygame
import json
import os
import sys
import time

# --- iOS / cross-platform CWD fix (Approach A safety net) ---
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from path_helper import resource_path




import random
from global_vars import (IMMEDIATE_RUN, FONT_PATH,
    width, height, icon, FPS, clock, screen, hero1, hero2, fire_wizard_icon, wanderer_magician_icon, fire_knight_icon, wind_hashashin_icon,
    white, red, black, green, cyan2, gold, play_button_img, text_box_img, loading_button_img, menu_button_img, SPECIAL_DURATION, DISABLE_SPECIAL_REDUCE,
    DEFAULT_WIDTH, DEFAULT_HEIGHT, scale, center_pos, font_size,
    DISABLE_HEAL_REGEN, DEFAULT_HEALTH_REGENERATION, DEFAULT_MANA_REGENERATION,
    LOW_HP, LITERAL_HEALTH_DEAD,
    DEFAULT_CHAR_SIZE, DEFAULT_CHAR_SIZE_2, DEFAULT_ANIMATION_SPEED, DEFAULT_ANIMATION_SPEED_FOR_JUMPING,
    JUMP_DELAY, RUNNING_SPEED,
    X_POS_SPACING, DEFAULT_X_POS, DEFAULT_Y_POS, SPACING_X, START_OFFSET_X, SKILL_Y_OFFSET,
    ICON_WIDTH, ICON_HEIGHT,
    DEFAULT_GRAVITY, DEFAULT_JUMP_FORCE, JUMP_LOGIC_EXECUTE_ANIMATION,
    WHITE_BAR_SPEED_HP, WHITE_BAR_SPEED_MANA, TEXT_DISTANCE_BETWEEN_STATUS_AND_TEXT,
    PLAYER_1, PLAYER_2, PLAYER_1_SELECTED_HERO, PLAYER_2_SELECTED_HERO, PLAYER_1_ICON, PLAYER_2_ICON,
    attack_display, MULT, dmg_mult, loading_screen_bg, no_swap
)
from global_vars import SHOW_HITBOX

import global_vars


from button import ImageButton, ImageInfo, ModalObject, draw_black_screen, create_title, RectButton, create_bordered_title, create_timed_title
import heroes as main
import global_vars




# from Animate_BG import BackgroundHandler

import Animate_BG

import key
from player import display_inputs
import loader as Save

# Keybinds will be loaded after user login


# LEADERBOARD CLASS
# LEADERBOARD CLASS (now draws ONLY the leaderboard table/panel itself)
class Leaderboard:
    def __init__(self):
        # ================================================================
        # LAYOUT CONSTANTS (still fully adjustable here)
        # ================================================================
        self.LEADERBOARD_WIDTH = 450
        self.LEADERBOARD_HEIGHT = 600

        # Column offsets from panel_left (no overlap, WR% removed)
        self.col_rank_offset = 30
        self.col_name_offset = 100
        self.col_games_offset = 235
        self.col_wins_offset = 280 + 50
        self.col_loss_offset = 345 + 50

        self.font_title = global_vars.get_font(48)
        self.font_header = global_vars.get_font(20)
        self.font_data = global_vars.get_font(22)
        self.font_helper = global_vars.get_font(18)   # smallest font for bottom texts

        self.sort_mode = "wins"
        self.sort_order = "desc"

        self.ITEMS_PER_PAGE = global_vars.LEADERBOARD_PER_PAGE  # you will set this to 5

        self.leaderboard_page = 1

        # Fetch data ONCE (snapshot - never changes while the leaderboard is open)
        self.raw_data = Save.get_leaderboard_data()

    def update(self, screen, x, y, mouse_pos, mouse_press, events):
        """
        Call this every frame from your game loop.
        Draws ONLY the leaderboard panel/table (no background).
        
        - x, y = top-left position of the entire leaderboard panel
        - mouse_pos, mouse_press = current pygame.mouse.get_pos() and get_pressed()
        - events = the list returned by pygame.event.get() in your main loop
        
        Returns:
            "back" if ESC or menu_button was clicked
            None otherwise
        """
        # ====================== LAYOUT (now driven by passed x, y) ======================
        # print(x, y)
        panel_left = x
        panel_top = y

        # Vertical layout inside the panel
        title_y = panel_top + 30
        header_y = panel_top + 65
        row_start_y = header_y + 35
        row_height = 45

        # Buttons positioned exactly as before (just before the 8th player + 75 px down)
        button_y = row_start_y + 7 * row_height + 50

        # Create buttons every frame with current position
        leaderboard_prev_button = RectButton(
            panel_left + 40, button_y,
            global_vars.FONT_PATH, int(height * 0.025), (0, 255, 0), "<", height_position=0
        )
        leaderboard_next_button = RectButton(
            panel_left + self.LEADERBOARD_WIDTH - 80, button_y,
            global_vars.FONT_PATH, int(height * 0.025), (0, 255, 0), ">", height_position=0
        )

        # ====================== SORTING ======================
        if self.sort_mode == "wins":
            key_func = lambda user: user[3]  # games_won
        else:
            key_func = lambda user: user[2]  # games_played

        reverse = self.sort_order == "desc"
        data = sorted(self.raw_data, key=key_func, reverse=reverse)

        total_leaderboard_pages = ((len(data) - 1) // self.ITEMS_PER_PAGE) + 1 if len(data) > 0 else 1

        # ====================== EVENT HANDLING ======================
        back_requested = False

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # print(x, y)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    back_requested = True
                elif event.key == pygame.K_w:
                    self.sort_mode = "wins"
                elif event.key == pygame.K_g:
                    self.sort_mode = "games"
                elif event.key == pygame.K_UP:
                    self.sort_order = "asc"
                elif event.key == pygame.K_DOWN:
                    self.sort_order = "desc"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.is_clicked(event.pos):
                    back_requested = True
                    main_menu()
                if leaderboard_next_button.is_clicked(event.pos):
                    if self.leaderboard_page < total_leaderboard_pages:
                        self.leaderboard_page += 1
                if leaderboard_prev_button.is_clicked(event.pos):
                    if self.leaderboard_page > 1:
                        self.leaderboard_page -= 1

        # ====================== PANEL (the leaderboard table itself) ======================
        panel_surface = pygame.Surface((self.LEADERBOARD_WIDTH, self.LEADERBOARD_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (20, 20, 30, 150), (0, 0, self.LEADERBOARD_WIDTH, self.LEADERBOARD_HEIGHT), border_radius=-1)
        pygame.draw.rect(panel_surface, (180, 140, 40, 150), (0, 0, self.LEADERBOARD_WIDTH, self.LEADERBOARD_HEIGHT), 3, border_radius=-1)
        screen.blit(panel_surface, (panel_left, panel_top))
        # panel_rect = pygame.Rect(panel_left, panel_top, self.LEADERBOARD_WIDTH, self.LEADERBOARD_HEIGHT)
        # pygame.draw.rect(screen, (20, 20, 30), panel_rect, border_radius=-1) # 12
        # pygame.draw.rect(screen, (180, 140, 40), panel_rect, 3, border_radius=-1)

        # ====================== TITLE ======================
        title_surf = self.font_title.render(" LEADERBOARD ", True, (255, 220, 120))
        title_rect = title_surf.get_rect(center=(10 + panel_left + self.LEADERBOARD_WIDTH // 2, title_y))
        screen.blit(title_surf, title_rect)

        # ====================== HEADERS ======================
        headers = [
            ("RANK", panel_left + self.col_rank_offset),
            ("PLAYER", panel_left + self.col_name_offset),
            ("GAMES", panel_left + self.col_games_offset),
            ("W", panel_left + self.col_wins_offset),
            ("L", panel_left + self.col_loss_offset),
        ]
        for text, x_pos in headers:
            surf = self.font_header.render(text, True, (255, 255, 200))
            screen.blit(surf, (x_pos, header_y))

        # Header separator line
        pygame.draw.line(screen, (150, 120, 80),
                         (panel_left + 15, header_y + 25),
                         (panel_left + self.LEADERBOARD_WIDTH - 15, header_y + 25), 2)

        # ====================== ROWS ======================
        if len(data) == 0:
            no_user = self.font_data.render("No warriors found...", True, (255, 120, 120))
            screen.blit(no_user, no_user.get_rect(center=(panel_left + self.LEADERBOARD_WIDTH // 2, panel_top + 280)))
        else:
            start_idx = (self.leaderboard_page - 1) * self.ITEMS_PER_PAGE
            end_idx = start_idx + self.ITEMS_PER_PAGE
            page_data = data[start_idx:end_idx]

            for idx, user in enumerate(page_data):
                uid, name, gp, gw, gl = user
                actual_rank = start_idx + idx + 1

                # Limit name to 10 characters + "..."
                display_name = (name[:10] + "...") if len(name) > 10 else name

                row_y = row_start_y + (idx * row_height)
                row_rect = pygame.Rect(panel_left + 15, row_y - 4, self.LEADERBOARD_WIDTH - 30, row_height - 8)

                # Row background
                pygame.draw.rect(screen, (35, 35, 50), row_rect, border_radius=6)

                # Top 3 medal borders
                if idx == 0:
                    rank_color = (255, 215, 0)
                    # pygame.draw.rect(screen, rank_color, row_rect, 2, border_radius=6)
                elif idx == 1:
                    rank_color = (192, 192, 192)
                    # pygame.draw.rect(screen, rank_color, row_rect, 2, border_radius=6)
                elif idx == 2:
                    rank_color = (205, 127, 50)
                    # pygame.draw.rect(screen, rank_color, row_rect, 2, border_radius=6)
                else:
                    rank_color = (220, 220, 220)

                # Current user highlight
                if global_vars.username and global_vars.username == name:
                    pygame.draw.rect(screen, (100, 150, 255), row_rect, 3, border_radius=6)

                row_values = [
                    str(actual_rank),
                    display_name,
                    str(gp),
                    str(gw),
                    str(gl),
                ]

                row_colors = [
                    rank_color,
                    (120, 255, 255),
                    (200, 200, 200),
                    (100, 255, 100),
                    (255, 120, 120),
                ]

                row_positions = [
                    panel_left + self.col_rank_offset,
                    panel_left + self.col_name_offset,
                    panel_left + self.col_games_offset,
                    panel_left + self.col_wins_offset,
                    panel_left + self.col_loss_offset,
                ]

                for value, x_pos, color in zip(row_values, row_positions, row_colors):
                    surf = self.font_data.render(str(value), True, color)
                    screen.blit(surf, (x_pos, row_y))

        # ====================== BOTTOM UI ======================
        # Buttons visual update + draw
        prev_pressed = leaderboard_prev_button.is_clicked(mouse_pos) and mouse_press[0]
        leaderboard_prev_button.update(mouse_pos, prev_pressed)
        leaderboard_prev_button.draw(screen, global_vars.TEXT_ANTI_ALIASING)

        next_pressed = leaderboard_next_button.is_clicked(mouse_pos) and mouse_press[0]
        leaderboard_next_button.update(mouse_pos, next_pressed)
        leaderboard_next_button.draw(screen, global_vars.TEXT_ANTI_ALIASING)

        # Sort indicator and helper text
        sort_y = button_y + 50
        # sort_indicator = self.font_helper.render(f"Sorting: {self.sort_mode.upper()} ({self.sort_order.upper()})", True, (180, 220, 100))
        # screen.blit(sort_indicator, (panel_left + 15, sort_y))

        # info_text = f"[W] Wins  [G] Games  [^] Asc  [v] Desc"
        # info = self.font_helper.render(info_text, True, (200, 200, 150))
        # info_rect = info.get_rect(center=(panel_left + self.LEADERBOARD_WIDTH // 2, sort_y + 23))
        # screen.blit(info, info_rect)

        # Page indicator
        page_y = panel_top + self.LEADERBOARD_HEIGHT - 28
        page_indicator = self.font_helper.render(f"Page {self.leaderboard_page}/{total_leaderboard_pages}", True, (200, 200, 150))
        screen.blit(page_indicator, page_indicator.get_rect(center=(panel_left + self.LEADERBOARD_WIDTH // 2, page_y)))

        # Global menu button
        menu_button.draw(screen, mouse_pos)

        # Return signal
        if back_requested:
            return "back"
        return None


# from heroes import player_selection, p1_select, p2_select, hero1_group, hero2_group
# from heroes import Fire_Wizard, Wanderer_Magician, Fire_Knight, Wind_Hashashin
# from player_selector import PlayerSelector
# # from global_vars import (
#     width, height, icon, FPS, clock, screen, hero1, hero2,
#     white, red, black, green, cyan2, gold,
#     DEFAULT_WIDTH, DEFAULT_HEIGHT,
#     DISABLE_HEAL_REGEN, DEFAULT_HEALTH_REGENERATION, DEFAULT_MANA_REGENERATION,
#     LOW_HP, LITERAL_HEALTH_DEAD,
#     DEFAULT_CHAR_SIZE, DEFAULT_CHAR_SIZE_2, DEFAULT_ANIMATION_SPEED, DEFAULT_ANIMATION_SPEED_FOR_JUMPING,
#     JUMP_DELAY, RUNNING_SPEED,
#     X_POS_SPACING, DEFAULT_X_POS, DEFAULT_Y_POS, SPACING_X, START_OFFSET_X, SKILL_Y_OFFSET,
#     ICON_WIDTH, ICON_HEIGHT,
#     DEFAULT_GRAVITY, DEFAULT_JUMP_FORCE, JUMP_LOGIC_EXECUTE_ANIMATION,
#     WHITE_BAR_SPEED_HP, WHITE_BAR_SPEED_MANA, TEXT_DISTANCE_BETWEEN_STATUS_AND_TEXT,
#     PLAYER_1, PLAYER_2, PLAYER_1_SELECTED_HERO, PLAYER_2_SELECTED_HERO, PLAYER_1_ICON, PLAYER_2_ICON,
#     attack_display, MULT, dmg_mult
# )



# from heroes import Fire_Wizard, Wanderer_Magicianoo

# The hero selection logic need to be at the main file :))d


# # Declaration of the eobject sprites (Single instance)
# fire_wizard = main.Fire_Wizard(PLAYER_2)
# wanderer_magician = main.Wanderer_Magician(PLAYER_1)

# # Group of objects sprites (Multiple instances)
# fire_wizard_group = main.pygame.sprite.Group()
# fire_wizard_group.add(fire_wizard)

# wanderer_magician_group = main.pygame.sprite.Group()
# wanderer_magician_group.add(wanderer_magician)
    
#basic attack
#ultimate regen
#increase mana every attack
#hook       

pygame.font.init()

MENU_MUSIC = resource_path('assets/audios/price-of-freedom-33106.mp3')
GAME_MUSIC_1 = resource_path('assets/audios/intense-battle-scene-115478.mp3')
GAME_MUSIC_2 = resource_path('assets/audios/z-battle-227609.mp3')

MENU_FADE_DURATION = 1000  # in milliseconds
GAME_FADE_IN = 1500

winner = None
battle_result_recorded = False  # Flag to prevent recording win multiple times per battle
paused = False

# Add a global variable to track the pause state
is_paused = False
xaxa = pygame.time.Clock()





w_gap = 0.1
h_gap = 0.133
base_width = 0.1
base_height = 0.33

button_width = width * 0.046875
button_height = button_width
width_half = width*0.45











#BUTTONS SHEEEEEEEESH 


# fade()
loading = ImageButton(
    image_path=loading_button_img,
    pos=center_pos,
    scale=0.8,
    text='',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

# Menu button to return to menu()
menu_button = ImageButton(
    image_path=menu_button_img,
    pos=(60, 25),
    scale=0.9,
    text='',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)



register_button = ImageButton(
    image_path=text_box_img,
    pos=(width * 0.4, height * 0.85),
    scale=0.9,
    text='REGISTER',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

ingame_menu_button = ImageButton(
    image_path=menu_button_img,
    pos=(50, 15),
    scale=0.9,
    text='',
    font_path=global_vars.FONT_PATH,  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

# main_menu()
play_button = ImageButton(
    image_path=play_button_img,
    pos=center_pos,
    scale=scale,
    text='',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)
central_offset = 270

# menu()
campaign_button = ImageButton(
    image_path=text_box_img,
    pos=(center_pos[0], center_pos[1]-60),
    scale=scale,
    text='Campaign',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING,
    hover_move=0
)

#_____ for campaign
coming_soon_button = ImageButton(
    image_path=text_box_img,
    pos=(center_pos[0], center_pos[1]-60),
    scale=scale*0.95,
    text='Coming Soon',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING,
    hover_move=0,
    alpha=(0.75, 1)
)


single_button = ImageButton(
    image_path=text_box_img,
    pos=(center_pos[0], center_pos[1]),
    scale=scale,
    text='Single Player',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

multiplayer_button = ImageButton(
    image_path=text_box_img,
    pos=(center_pos[0], center_pos[1]+60),
    scale=scale,
    text='Multiplayer',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

# --------------------------


# Login Button from menu page
login_button = ImageButton(
    image_path=text_box_img,
    pos=(width - 100, height - 50),
    scale=scale*0.8,
    text='LOGIN',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)
control_button = ImageButton(
    image_path=text_box_img,
    pos=(300, height - 50),
    scale=scale*0.8,
    text='Controls',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

settings_button = ImageButton(
    image_path=text_box_img,
    pos=(100, height - 50),
    scale=scale*0.8,
    text='Settings',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

# ---------------



leaderboard_button = ImageButton(
    image_path=text_box_img,
    pos=(width - 300, height - 50),
    scale=scale * 0.8,
    text='LEADERBOARD',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size*0.95,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

# info_button = ImageButton(
#     image_path=text_box_img,
#     pos=(width - 100, height - 100),
#     scale=scale*0.8,
#     text='Game Info',
#     font_path=r'assets\font\slkscr.ttf',  # or any other font path
#     font_size=font_size*0.8,  # dynamic size ~29 at 720p
#     text_color='white',
#     text_anti_alias=global_vars.TEXT_ANTI_ALIASING
# )


has_changes = False
def show_confirmation_modals(font=None):
    # Use cached font if not provided
    if font is None:
        font = global_vars.get_font(60)

    if no_swap:
        create_title('(The existing key will be leave empty)', font, 0.5, height * 0.5)
    else:
        create_title('(The existing key will be swapped)', font, 0.5, height * 0.5)
    # create_title('Key already in use', font, 1, height * 0.40, color=(150,150,150))
    # create_title('Key already in use', font, 1, height * 0.40, color=(150,10,10))
    color=(150,150,150)
    
    create_title('Key already in use', font, 1, height * 0.40, color)
        
def save_before_exiting_modal(font=None):
    if font is None:
        font = global_vars.get_font(60)
    create_title('Save before exiting!', font, 0.5, height * 0.95, x_offset=width*0.35)
   
    



def show_controls(font=None):
    # Display controls title
    draw_black_screen(0.2,size=(width*0.05, height * 0.2, width*0.44, height*0.65))
    draw_black_screen(0.2,size=(width*0.45 + width*0.05, height * 0.2,  width*0.44, height*0.65))
    if font is None:
        font = global_vars.get_font(40)
    create_title('CONTROLS', global_vars.get_font(60), 1, height * 0.1)
    
    # Player 1 Controls
    create_title('Player 1:', font, 1, height * 0.25, angle=0, x_offset=width *0.33)

    # Player 2 Controls
    create_title('Player 2:', font, 1, height * 0.25, angle=0, x_offset=((width *0.33) + (width * 0.9)))
    


    w_margin = 0.143
    h_margin = 0.02

    # width_half = width*0.5
    
    create_title("Attack", font, 0.5, height * (base_height - h_margin), color=white, angle=0, x_offset=width*(base_width + w_margin))
    create_title("Special", font, 0.5, height * ((base_height + h_gap) - h_margin), color=white, angle=0, x_offset=width*(base_width + w_margin))
    

    create_title("Move", font, 0.5, height * ((base_height + h_gap) - h_margin - 0.03), color=white, angle=0, x_offset=width*((base_width + 2*w_gap) + w_margin))
    create_title("Left", font, 0.5, height * ((base_height + h_gap) - h_margin), color=white, angle=0, x_offset=width*((base_width + 2*w_gap) + w_margin))
    

    create_title("Jump", font, 0.5, height * ((base_height - h_margin)), color=white, angle=0, x_offset=width*((base_width + 4*w_gap) + w_margin))

    create_title("Move", font, 0.5, height * ((base_height + h_gap) - h_margin - 0.03), color=white, angle=0, x_offset=width*((base_width + 6*w_gap) + w_margin))
    create_title("Right", font, 0.5, height * ((base_height + h_gap) - h_margin), color=white, angle=0, x_offset=width*((base_width + 6*w_gap) + w_margin))
    
    
    create_title("Skill 1", font, 0.5, height * ((base_height + 2.5*h_gap) - h_margin), color=white, angle=0, x_offset=width*((base_width) + w_margin))
    create_title("Skill 2", font, 0.5, height * ((base_height + 2.5*h_gap) - h_margin), color=white, angle=0, x_offset=width*((base_width + 2*w_gap) + w_margin))
    create_title("Skill 3", font, 0.5, height * ((base_height + 2.5*h_gap) - h_margin), color=white, angle=0, x_offset=width*((base_width + 4*w_gap) + w_margin))
    create_title("Skill 4", font, 0.5, height * ((base_height + 2.5*h_gap) - h_margin), color=white, angle=0, x_offset=width*((base_width + 6*w_gap) + w_margin))




    create_title("Attack", font, 0.5, height * (base_height - h_margin), color=white, angle=0, x_offset=width*(base_width + w_margin) + width_half*2)
    create_title("Special", font, 0.5, height * ((base_height + h_gap) - h_margin), color=white, angle=0, x_offset=width*(base_width + w_margin) + width_half*2)
    

    create_title("Move", font, 0.5, height * ((base_height + h_gap) - h_margin - 0.03), color=white, angle=0, x_offset=width*((base_width + 2*w_gap) + w_margin) + width_half*2)
    create_title("Left", font, 0.5, height * ((base_height + h_gap) - h_margin), color=white, angle=0, x_offset=width*((base_width + 2*w_gap) + w_margin) + width_half*2)
    

    create_title("Jump", font, 0.5, height * ((base_height - h_margin)), color=white, angle=0, x_offset=width*((base_width + 4*w_gap) + w_margin) + width_half*2)

    create_title("Move", font, 0.5, height * ((base_height + h_gap) - h_margin - 0.03), color=white, angle=0, x_offset=width*((base_width + 6*w_gap) + w_margin) + width_half*2)
    create_title("Right", font, 0.5, height * ((base_height + h_gap) - h_margin), color=white, angle=0, x_offset=width*((base_width + 6*w_gap) + w_margin) + width_half*2)
    
    
    create_title("Skill 1", font, 0.5, height * ((base_height + 2.5*h_gap) - h_margin), color=white, angle=0, x_offset=width*((base_width) + w_margin) + width_half*2)
    create_title("Skill 2", font, 0.5, height * ((base_height + 2.5*h_gap) - h_margin), color=white, angle=0, x_offset=width*((base_width + 2*w_gap) + w_margin) + width_half*2)
    create_title("Skill 3", font, 0.5, height * ((base_height + 2.5*h_gap) - h_margin), color=white, angle=0, x_offset=width*((base_width + 4*w_gap) + w_margin) + width_half*2)
    create_title("Skill 4", font, 0.5, height * ((base_height + 2.5*h_gap) - h_margin), color=white, angle=0, x_offset=width*((base_width + 6*w_gap) + w_margin) + width_half*2)








import loader as Save

from typing import Callable, Any

def fade(background:pygame.Surface, action:Callable[[Any], Any], fade_duration=MENU_FADE_DURATION, immediate_load=False):
    '''Uses current single background frame to cover the current screen with current background,
    displays loading image and fading into provided function.

    - background: Single background image (must be a surface).

    - action: Function to be called after fade

    - fade_duration: How long to turn screen black.

    - immediate_load: If True, calls the assigned function immediately (displays loading, no black fade).'''
    # background = pygame.transform.scale(
    #     pygame.image.load(r'assets\backgrounds\12.png').convert(), (width, height))

    fade_overlay = pygame.Surface((width, height))
    fade_overlay.fill((0, 0, 0))
    fade_alpha = 0
    fading = True
    fade_start_time = pygame.time.get_ticks()

    while True:
        for event in main.pygame.event.get():
            if event.type == main.pygame.QUIT:
                main.pygame.quit()
                exit()

        if fading:
            screen.blit(background, (0, 0))
            loading.draw(screen, pygame.mouse.get_pos())
            current_time = pygame.time.get_ticks()
            # pygame.time.get_ticks()
            fade_elapsed = current_time - fade_start_time
            fade_alpha = min(255, int((fade_elapsed / fade_duration) * 255))
            fade_overlay.set_alpha(fade_alpha)
            screen.blit(fade_overlay, (0, 0)) if not immediate_load else None
            # print(fade_alpha, not immediate_load)
            if fade_alpha >= 255 and not immediate_load:
                end_result = action()
                fading = False
                return end_result
            if fade_alpha >= 10 and immediate_load: # load function immediately (just displaying first frame)
                end_result = action()
                fading = False
                return end_result
            
        pygame.display.update()
        main.clock.tick(main.FPS)

# def counter(itemlist): # this one is a dud
#     count = 0
#     for item in itemlist:
#         if item.is_selected():
#             count += 1
#     # print(count)
#     return count



def item_list(itemlist): # at least it works, not reusable tho
    value_list = []
    for i, item in enumerate(itemlist):
        if item.is_selected():
            value_list.append(item)
    return value_list


def draw_grid(screen, width=1280, height=720, grid_size=35, color=(100, 100, 100)):
    cell_width = width // grid_size
    cell_height = height // grid_size

    font = global_vars.get_font(20, None)

    for i in range(grid_size + 1):
        # Vertical lines
        x = i * cell_width
        # pygame.draw.line(screen, color, (x, 0), (x, height), 1)

        # Horizontal lines
        y = i * cell_height
        pygame.draw.line(screen, color, (0, y), (width, y), 1)

    for row in range(grid_size):
        for col in range(grid_size):
            x = (col + 1) * cell_width
            y = row * cell_height

            # Reverse Y: higher numbers at the top
            reversed_y = height - y
            # pos_text = f"{x}, {reversed_y}"
            pos_text = f"{reversed_y}"

            text_surface = font.render(pos_text, global_vars.TEXT_ANTI_ALIASING, (150, 150, 255))
            screen.blit(text_surface, (x - 5, y + 2))


        
# def map_selection():

#     font = pygame.font.Font(fr'assets\font\slkscr.ttf', 100)
#     default_size = ((main.width * main.DEFAULT_HEIGHT) / (main.height * main.DEFAULT_WIDTH))

#     while True:
#         keys = pygame.key.get_pressed()
#         mouse_pos = pygame.mouse.get_pos()
#         mouse_press = pygame.mouse.get_pressed()
#         key_press = pygame.key.get_pressed()

#         main.screen.fill((0, 0, 0))
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 exit()   

#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if play_button.is_clicked(event.pos):
#                     # fade(background, menu)
#                     return
#             if keys[pygame.K_RETURN]:
#                 return

        # main.screen.blit(background, (0, 0))
        # Animate_BG.waterfall_night_bg.display(screen, speed=50) if not global_vars.SMOOTH_BG else Animate_BG.smooth_waterfall_night_bg.display(screen, speed=50)
        # create_title('Map Selection', font, default_size, height * 0.1)
        # menu_button.draw(screen, mouse_pos)

        # pygame.display.update()
        # xaxa.tick(main.FPS)
def run_background(bg):
    bg.display(screen)
import time

# ── Phase D: host-authoritative state sync ──
# Render runs at 60 FPS; this is only how often the host SENDS snapshots over the
# socket. 30Hz halves bandwidth/CPU and is gentler on a slow (WiFi) client; bump
# to 60 to A/B test tighter sync on a fast link.
NET_STATE_TICK_HZ = global_vars.FPS
NET_STATE_TICK_MS = NET_STATE_TICK_HZ#1000 / NET_STATE_TICK_HZ

def serialize_hero(h):

    """Snapshot the crucial, host-authoritative state of one hero.
    
    Synced variables (see serialize_hero_guide.md for full breakdown):
    - Core resources: health, mana, special, temp_hp, max_health, max_mana
    - Position/movement: x, y, y_velocity, jumping, facing_right, running, speed
    - Status effects: frozen, rooted, slowed, slow_speed, silenced, stunned, hasted, flying, invisible
    - Attacking states: attacking1-3, sp_attacking, basic_attacking, special_active
    - Items/abilities: immortality_activated, immortality_duration
    - Cooldowns: skills_cd, special_skills_cd
    
    NOT serialized (and why):
    - enemy (list of Player objects — not JSON-serializable, already set on both clients)
    - animation indices (computed locally from state)
    - sprites/sounds/rects (pygame objects, loaded locally)
    - damage_numbers, white bars (cosmetic, computed locally)
    """
    return {
        # ─────────────────────────────
        # Core Resources
        # ─────────────────────────────
        'health': h.health,
        'mana': h.mana,
        'special': h.special,
        'temp_hp': h.temp_hp,

        'max_health': h.max_health,
        'max_mana': h.max_mana,
        'max_temp_hp': getattr(h, 'max_temp_hp', 0),

        # smooth UI bars
        # white_health/mana chase-bar values are cosmetic and re-derived locally
        # on each client from health/mana each frame. No need to sync over network.

        # ─────────────────────────────
        # Position & Movement
        # ─────────────────────────────
        'x': h.x_pos,
        'y': h.y_pos,
        'yv': h.y_velocity,

        'jump': h.jumping,
        'running': h.running,
        'facing_right': h.facing_right,

        'speed': h.speed,
        'speed_multiplier': getattr(h, 'speed_multiplier', 1.0),

        # ─────────────────────────────
        # Status Effects
        # ─────────────────────────────
        'frozen': h.frozen,
        'rooted': h.rooted,

        'slowed': h.slowed,
        'slow_speed': h.slow_speed,

        'silenced': h.silenced,
        'stunned': h.stunned,

        'hasted': getattr(h, 'hasted', False),
        'flying': getattr(h, 'flying', False),
        'invisible': getattr(h, 'invisible', False),

        # ─────────────────────────────
        # Attack States
        # ─────────────────────────────
        'attacking1': h.attacking1,
        'attacking2': h.attacking2,
        'attacking3': h.attacking3,

        'attacking4': h.sp_attacking,
        'basic_attacking': h.basic_attacking,

        'special_active': h.special_active,

        # # animation sync
        # Animation indices are intentionally NOT serialized.
        # P2 drives all animation frames locally from the attacking-state flags
        # (attacking1-4, basic_attacking, running, jumping) that are already synced.
        # Serializing raw index values caused "stuck frame" bugs because last_atk_time
        # is an absolute host clock value that mismatches P2's independent clock.

        # death sync
        'dead': h.is_dead() if hasattr(h, 'is_dead') else False,

        # ─────────────────────────────
        # Immortality
        # ─────────────────────────────
        'immortality_activated': h.immortality_activated,
        'immortality_duration': h.immortality_duration,

        # ─────────────────────────────
        # Cooldowns
        # ─────────────────────────────
        'skills_cd': [
            skill.get_skill_cooldown()
            for skill in h.attacks
        ],

        'special_skills_cd': [
            skill.get_skill_cooldown()
            for skill in h.attacks_special
        ],
    }

def apply_hero_state(h, s, x=None, y=None):
    """Apply a serialized hero state snapshot to a live hero object."""
    
    """owner's note:
    - sets the hero (h) its current state and position based on what its current state as
    seen on the host client.
    - These includes updated:
        - x and y position
        - health, mana, special, max_health, max_mana, etc...
        - statuses/effects (frozen, rooted, slowed + slow_speed, etc..)
        - player states (jumping, facing, attacking, running, special_active, speed, etc...)
    
    ai note >:(
    - Overwrite a hero with an authoritative snapshot (used on the non-host client).
    x/y override the snapshot position with an interpolated value when provided."""
    if h is None or s is None:
        return

    # NOTE: every field is read with s.get(..., <current value>) so a partial or
    # version-mismatched snapshot degrades gracefully (keeps the last known value)
    # instead of raising KeyError and desyncing/crashing the non-host client.

    # ── Core Resources ──
    h.health = s['health']
    h.mana = s['mana']
    h.special = s['special']
    h.temp_hp = s['temp_hp']
    h.max_health = s['max_health']
    h.max_mana = s['max_mana']
    if hasattr(h, 'max_temp_hp'):
        h.max_temp_hp = s.get('max_temp_hp', 0)
    # smooth UI bars: re-derived locally each frame from health/mana, not synced.

    # ── Position & Movement ──
    h.x_pos = x if x is not None else s['x']
    h.y_pos = y if y is not None else s['y']
    h.y_velocity = s['yv']
    h.jumping = s['jump']
    h.facing_right = s['facing_right']
    h.running = s['running']
    h.speed = s['speed']
    if hasattr(h, 'speed_multiplier'):
        h.speed_multiplier = s.get('speed_multiplier', 1.0)

    # ── Status Effects ──
    h.frozen = s['frozen']
    h.rooted = s['rooted']
    h.slowed = s['slowed']
    h.slow_speed = s['slow_speed']
    h.silenced = s['silenced']
    h.stunned = s['stunned']
    if hasattr(h, 'hasted'):
        h.hasted = s.get('hasted', None)
    if hasattr(h, 'flying'):
        h.flying = s.get('flying', None)
    if hasattr(h, 'invisible'):
        h.invisible = s.get('invisible', None)

    # ── Attacking States ──
    # Store host-authoritative attack flags so _reconcile_p2_attack_flag()
    # can keep animations alive while the host still reports the attack active.
    h._host_attacking1      = s['attacking1']
    h._host_attacking2      = s['attacking2']
    h._host_attacking3      = s['attacking3']
    h._host_sp_attacking    = s['attacking4']
    h._host_basic_attacking = s['basic_attacking']

    # Reset animation indices when a new attack cycle starts on the host but
    # the local animation already finished (flag is False, index stuck at last
    # frame).  Without this, the animation visually freezes on repeat attacks.
    if s['attacking1'] and not h.attacking1:
        h.player_atk1_index = 0
        h.player_atk1_index_flipped = 0
    if s['attacking2'] and not h.attacking2:
        h.player_atk2_index = 0
        h.player_atk2_index_flipped = 0
    if s['attacking3'] and not h.attacking3:
        h.player_atk3_index = 0
        h.player_atk3_index_flipped = 0
    if s['attacking4'] and not h.sp_attacking:
        h.player_sp_index = 0
        h.player_sp_index_flipped = 0
    if s['basic_attacking'] and not h.basic_attacking:
        h.player_basic_index = 0
        h.player_basic_index_flipped = 0

    h.attacking1      = s['attacking1']
    h.attacking2      = s['attacking2']
    h.attacking3      = s['attacking3']
    h.sp_attacking    = s['attacking4']
    h.basic_attacking = s['basic_attacking']
    h.special_active  = s['special_active']

    # Animation indices are NOT applied here — P2 animates locally from the
    # state flags above. See serialize_hero() for the full rationale.

    # ── Items/Abilities ──
    h.immortality_activated = s['immortality_activated']
    h.immortality_duration = s['immortality_duration']

    # ── Cooldowns ──
    now = pygame.time.get_ticks()

    for i, cooldown in enumerate(s['skills_cd']):
        if i < len(h.attacks):
            h.attacks[i]

    for i, cd in enumerate(s.get('skills_cd', [])):
        if i < len(h.attacks):
            skill = h.attacks[i]

            elapsed = max(0, skill.cooldown - int(cd))

            skill.last_used_time = now - elapsed
            skill.remaining_ms = cd

    for i, cd in enumerate(s.get('special_skills_cd', [])):
        if i < len(h.attacks_special):
            skill = h.attacks_special[i]

            elapsed = max(0, skill.cooldown - int(cd))

            skill.last_used_time = now - elapsed
            skill.remaining_ms = cd

def apply_hero_game_state(h, s):
    """Apply ONLY the authoritative game-state fields (HP / mana / status / cooldowns)
    to a live hero — intentionally skipping position, movement, and attacking flags.

    Used for P2's OWN hero in multiplayer so that:
    - HP damage dealt by P1 (the damage authority) is visible on P2.
    - Positions and animation state remain under P2's local control, preventing the
      position-rollback and attacking-flag deadlock that blocked player_movement().
    """
    if h is None or s is None:
        return
    # ── Core resources (authoritative from host) ──
    h.health     = s['health']
    h.mana       = s['mana']
    h.special    = s['special']
    h.temp_hp    = s['temp_hp']
    h.max_health = s['max_health']
    h.max_mana   = s['max_mana']
    if hasattr(h, 'max_temp_hp'):
        h.max_temp_hp = s.get('max_temp_hp', 0)
    # ── Status effects ──
    h.frozen    = s['frozen']
    h.rooted    = s['rooted']
    h.slowed    = s['slowed']
    h.slow_speed = s['slow_speed']
    h.silenced  = s['silenced']
    h.stunned   = s['stunned']
    if hasattr(h, 'hasted'):    h.hasted    = s.get('hasted',    None)
    if hasattr(h, 'flying'):    h.flying    = s.get('flying',    None)
    if hasattr(h, 'invisible'): h.invisible = s.get('invisible', None)
    # ── Items / abilities ──
    h.immortality_activated = s['immortality_activated']
    h.immortality_duration  = s['immortality_duration']
    # ── Cooldowns ──
    now = pygame.time.get_ticks()
    for i, cd in enumerate(s.get('skills_cd', [])):
        if i < len(h.attacks):
            skill = h.attacks[i]
            elapsed = max(0, skill.cooldown - int(cd))
            skill.last_used_time = now - elapsed
            skill.remaining_ms   = cd
    for i, cd in enumerate(s.get('special_skills_cd', [])):
        if i < len(h.attacks_special):
            skill = h.attacks_special[i]
            elapsed = max(0, skill.cooldown - int(cd))
            skill.last_used_time = now - elapsed
            skill.remaining_ms   = cd

def emit_skill_events_for_host(net_client, heroes):
    """Host (P1) only: detect each hero's attacking-flag rising edge this frame
    and emit a fire-once skill_event. Runs every frame (not throttled like the
    state snapshot) so no cast is ever missed to network jitter.

    heroes is an iterable of (hero_id, hero) where hero_id is 1 or 2.
    skill ids: 1=atk1, 2=atk2, 3=atk3, 4=sp, 5=basic.
    """
    for hero_id, h in heroes:
        if h is None:
            continue
        prev = getattr(h, '_host_prev_atk_flags', None)
        cur = (h.attacking1, h.attacking2, h.attacking3,
               h.sp_attacking, h.basic_attacking)
        if prev is not None:
            for i, skill in enumerate((1, 2, 3, 4, 5)):
                if (not prev[i]) and cur[i]:
                    net_client.send_skill_event(hero_id, skill)
        h._host_prev_atk_flags = cur


# def consume_skill_events_for_p2(net_client, hero1, hero2):
#     """P2 only: drain queued skill_events and spawn the matching Attack_Display
#     visual via the hero's _trigger_attack_display_for_p2(). Lossless: every
#     event fires exactly once regardless of state-snapshot timing."""
#     now = pygame.time.get_ticks()
#     for ev in net_client.pop_skill_events():
#         h = hero1 if ev.get('hero') == 1 else hero2
#         skill = ev.get('skill')
#         if h is None or skill is None:
#             continue
#         if not hasattr(h, '_trigger_attack_display_for_p2'):
#             continue
#         h._p2_atk_just_triggered = skill
#         h._trigger_attack_display_for_p2()
#         h._p2_atk_just_triggered = 0
#         # Mark so the snapshot-based rising-edge path in apply_hero_state()
#         # won't double-spawn the same cast within a short window.
#         h._p2_last_event_skill = skill
#         h._p2_last_event_time = now


def interp_xy(prev, latest, t0, t1, hero_key, render_time):
    """Lerp a hero's (x, y) between the prev and latest snapshots at render_time.
    Falls back to the latest position when there's no prior snapshot. Clamped so a
    late snapshot just holds the latest position rather than overshooting."""
    ls = latest.get(hero_key)
    if ls is None:
        return None, None
    ps = prev.get(hero_key) if prev else None
    if ps is not None and t1 > t0:
        a = (render_time - t0) / (t1 - t0)
        a = 0.0 if a < 0 else 1.0 if a > 1 else a
        return ps['x'] + (ls['x'] - ps['x']) * a, ps['y'] + (ls['y'] - ps['y']) * a
    return ls['x'], ls['y']

def game(bg=None, net_client=None):
    global winner, paused, is_paused, battle_result_recorded
    if global_vars.active_net_client is not None:
        global_vars.active_net_client.phase = 'playing'
        global_vars.active_net_client.declared_winner = None  # reset from any previous game

    _last_state_send_1 = 0   # Phase D: throttle host -> client state snapshots (30Hz)
    _last_state_send_2 = 0

    
    game_music_started = False
    second_track_played = False
    battle_result_recorded = False  # Reset for new game
    # bg_list = [
    #     r'assets\backgrounds\1.png',
    #     r'assets\backgrounds\2.png',
    #     r'assets\backgrounds\3.png',
    #     r'assets\backgrounds\4.jpg',
    #     r'assets\backgrounds\13.jpg',
    #     r'assets\backgrounds\14.png',
    #     r'assets\backgrounds\15.png',
    #     r'assets\backgrounds\16.png',
    #     r'assets\backgrounds\17.png'
    # ]
    # print(f'hahahahaa [{random.randint(0, len(bg_list)-1)}')
    # background = main.pygame.transform.scale(
    #     pygame.image.load(bg_list[random.randint(0, len(bg_list)-1)]).convert(), (main.width, main.DEFAULT_Y_POS + (720*1.1 - 720)))
    # ground = main.pygame.transform.scale(
    #     main.pygame.image.load(r'assets\backgrounds\10.jpg').convert(), (main.width, main.height))
    ground = pygame.Rect(0, main.DEFAULT_Y_POS, 2121, 1111)
    
    start_time = pygame.time.get_ticks()
    timer_font = global_vars.get_font(50)  # Timer font

    cube_sound = pygame.mixer.Sound(resource_path('assets/sound effects/wanderer_magician/shine-8-268901 1.mp3'))
    cube_sound.set_volume(0.8 * global_vars.MAIN_VOLUME) 

    cubes = [
        {'fall': -500, 'x': random.randint(20, int(main.width - 20)), 'color': 'Green', 'image': pygame.image.load(resource_path('assets/icons/hp bonus.png')).convert_alpha(), 'bonus_type': 'health', 'bonus_amount': 10, 'sound': cube_sound},
        {'fall': -300, 'x': random.randint(20, int(main.width - 20)), 'color': 'Blue', 'image': pygame.image.load(resource_path('assets/icons/mana bonus.png')).convert_alpha(), 'bonus_type': 'mana', 'bonus_amount': 30, 'sound': cube_sound},
        {'fall': -700, 'x': random.randint(20, int(main.width - 20)), 'color': 'Yellow', 'image': pygame.image.load(resource_path('assets/icons/special bonus.png')).convert_alpha(), 'bonus_type': 'special', 'bonus_amount': 15, 'sound': cube_sound},
    ]
    
    # In LAN mode, use the shared seed from the server so both clients generate
    # identical initial cube X positions — no broadcast needed, no race condition.
    if global_vars.active_net_client is not None and global_vars.active_net_client.cube_seed is not None:
        _cube_rng = random.Random(global_vars.active_net_client.cube_seed)
        _cube_x = [_cube_rng.randint(20, int(main.width - 20)) for _ in cubes]
        print(f"[CUBE SYNC] Using shared seed {global_vars.active_net_client.cube_seed}, X positions: {_cube_x}")
        for i, cube in enumerate(cubes):
            cube['x'] = _cube_x[i]
    else:
        print("[CUBE SYNC] No shared seed — using local random (local/offline mode)")
    
    if game_music_started and not second_track_played:
        if not pygame.mixer.music.get_busy():
            pygame.event.post(pygame.event.Event(pygame.USEREVENT))
            
            
    FREEZE_SPECIAL = False
    freeze_toggled = True

    final_elapsed_time = None
    paused_start_time = None
    total_paused_duration = 0
    global_vars.PAUSED = False
    global_vars.PAUSED_TOTAL_DURATION = 0
    global_vars.PAUSED_START = None

    #testing purposes
    #testing
    # main.hero1.x_pos += 250
    # main.hero2.x_pos -= 150

    

    # Import keybinds as data from json
    
    bot_pos = 200

    for p1 in main.hero1_group:
        # p1.x_pos = random.randint(50, 100)
        p1.x_pos = 300
    for p2 in main.hero2_group:
        # p2.x_pos = random.randint(width-100, width-50)
        p2.x_pos = width-300


    disable_debug = False
    while True:
        # print(main.hero1.mana)
        
            
        
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        key_press = pygame.key.get_pressed()

        current_time = pygame.time.get_ticks()

        # Handle pause timing correctly by accumulating paused durations.
        if not paused or global_vars.active_net_client is not None:
            # If we have a paused_start_time it means we just resumed; accumulate the paused duration (local only)
            if not global_vars.active_net_client and paused_start_time is not None :
                total_paused_duration += (current_time - paused_start_time)
                paused_start_time = None

            # Update global_vars so other modules (like heroes) can read paused totals
            global_vars.PAUSED = False
            global_vars.PAUSED_TOTAL_DURATION = total_paused_duration
            global_vars.PAUSED_START = None

            if winner is None:
                # Elapsed time excludes total paused duration
                elapsed_time = (current_time - start_time - total_paused_duration) // 1000
            else:
                # Freeze final elapsed time when a winner is determined
                if final_elapsed_time is None:
                    final_elapsed_time = (current_time - start_time - total_paused_duration) // 1000
                elapsed_time = final_elapsed_time
        else:
            # When entering paused state, record when pause started (local mode only))
            if paused_start_time is None:
                paused_start_time = current_time
                global_vars.PAUSED = True
                global_vars.PAUSED_START = paused_start_time
        
        # if not paused:
        #     main.screen.fill((0, 0, 0))
        # print(global_vars.MAIN_VOLUME)
        
        if global_vars.active_net_client is not None:
            if global_vars.active_net_client.opponent_left:
                print("Opponent left detected in player_selection")
                return 'opponent_left'
                
            if global_vars.active_net_client.rematch_confirmed:
                global_vars.active_net_client.rematch_confirmed = False
                global_vars.active_net_client.my_rematch_sent = False
                global_vars.active_net_client.opponent_rematch_sent = False
                global_vars.active_net_client.declared_winner = None
                reset_all()
                return 'rematch'

        for event in main.pygame.event.get():
            if event.type == main.pygame.QUIT:
                if global_vars.active_net_client is not None:
                    global_vars.active_net_client.disconnect()
                main.pygame.quit()
                exit()

            if event.type == pygame.USEREVENT + 1 and not game_music_started:
                pygame.mixer.music.load(GAME_MUSIC_1)
                pygame.mixer.music.set_volume(0 if global_vars.MUTE else global_vars.MAIN_VOLUME * 0.5)  # Apply mute logic
                pygame.mixer.music.play(1, fade_ms=1500)
                game_music_started = True

            elif event.type == pygame.USEREVENT and game_music_started and not second_track_played:
                pygame.mixer.music.load(GAME_MUSIC_2)
                pygame.mixer.music.set_volume(0 if global_vars.MUTE else global_vars.MAIN_VOLUME * 0.5)  # Apply mute logic
                pygame.mixer.music.play(loops=-1, fade_ms=1500)
                second_track_played = True

            # if keys[pygame.K_ESCAPE]:
            #     return

            if keys[pygame.K_ESCAPE]:
                paused = True
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if menu_button.is_clicked(event.pos):
            #         return    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ingame_menu_button.is_clicked(event.pos):
                    paused = True 
                
            # Toggle pause state when the pause key is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                is_paused = not is_paused
            if not disable_debug:
                if keys[main.pygame.K_6]:
                    main.hero1.health += 20
                    main.hero2.health += 20 
                    main.hero1.mana += 20
                    main.hero2.mana += 20
                    if hasattr(main.bot, 'mana'):
                        main.bot.mana += 20
                    if hasattr(main.bot, 'health'):
                        main.bot.health += 20

                # if keys[main.pygame.K_SPACE]: # reset
                #     main.hero1.health += 500
                #     main.hero2.health += 500
                #     main.hero1.mana += 500
                #     main.hero2.mana += 500
                #     main.hero1.special -= 500
                #     main.hero2.special -= 500

                if keys[main.pygame.K_1] and not keys[main.pygame.K_LALT]: # reset
                    main.hero1.special += 500
                    main.hero2.special += 500
                    

                # if keys[main.pygame.K_2] and not keys[main.pygame.K_LALT] and not FREEZE_SPECIAL: # freeze
                #     FREEZE_SPECIAL = True
                #     # freeze_toggled = False
                #     if event.type == pygame.USEREVENT:
                #         print('freeze special toggled')
                    

                # if keys[main.pygame.K_2] and keys[main.pygame.K_LALT]: # unfreeze (alt)
                #     FREEZE_SPECIAL = False
                #     # freeze_toggled = True
                #     if event.type == pygame.USEREVENT:
                #         print('unfreeze special toggled') 

                if keys[main.pygame.K_3] and not keys[main.pygame.K_LALT]: # special to 1
                    main.hero1.special = 0.01   
                    main.hero2.special = 0.01
                    

                if keys[main.pygame.K_4] and not keys[main.pygame.K_LALT]: # disable special
                    global_vars.DISABLE_SPECIAL_REDUCE = False
                elif keys[main.pygame.K_4] and keys[main.pygame.K_LALT]: # special on (alt)
                    global_vars.DISABLE_SPECIAL_REDUCE = True

                if keys[main.pygame.K_2] and not keys[main.pygame.K_LALT]:
                    global_vars.DISABLE_SPECIAL_REDUCE = True
                    main.hero1.special = 0.01
                    main.hero2.special = 0.01

                if keys[main.pygame.K_5] and not keys[main.pygame.K_LALT]: # disable hp regen
                    main.DISABLE_HEAL_REGEN = True
                if keys[main.pygame.K_5] and keys[main.pygame.K_LALT]: # hp regen (alt)
                    main.DISABLE_HEAL_REGEN = False
                    
                #'''add another flag which also disables random unstuck direction, but in this case, it is the core flag, which is specific for the hero, not just on a skill, eg fire wizard escapes random direction, while also other hero escapes depends on where the player is. (this is for the skill, if the hero has escape, and that skill has specific flag(assuming that skill forcefully move the bot, or an escape skill, then it also behaves the same)'''

            # if FREEZE_SPECIAL: 
            #     main.hero1.special_active = True
            #     main.hero2.special_active = True
            #     main.hero1.special += 0.001
            #     main.hero2.special += 0.001
            # elsed:
            #     pass

        # print(FREEZE_SPECIAL)
                
# -------------------------------------------------------------------------------------
        
        
        if not paused or global_vars.active_net_client is not None:
            # Background
            # Animate_BG.waterfall_bg.display(screen)
            # Animate_BG.lava_bg.display(screen)
            # Animate_BG.dark_forest_bg.display(screen)
            
            run_background(main.map_selected)
            draw_black_screen(0.4,size=(0, 0, width, height*0.165))
            # main.screen.blit(background, (0, -(720*1.05 - 720)))

            draw_grid(screen) if global_vars.SHOW_GRID else None

            # print(main.hero1.health, main.hero1.max_health)
            # draws animated cloud background (lag)
            # animated_bg.update()
            # animated_bg.draw(screen)
            
            # main.screen.blit(ground, (0,main.DEFAULT_Y_POS))

            # Ground
            pygame.draw.rect(main.screen, main.black, ground)


            # Draw selected hero icons in-game (top corners)
            for selector in main.p1_select:
                if selector.is_selected():
                    selector.draw_icon(center_pos=(75, 75), hero_sp=main.hero1.is_special_active())  # Top-left
                    # main.hero1.draw_profile(center_pos=(75, 75), hero_sp=main.hero1.is_special_active())

            for selector in main.p2_select:
                if selector.is_selected():
                    selector.draw_icon(center_pos=(width - 75, 75), hero_sp=main.hero2.is_special_active())  # Top-right
                    # main.hero2.draw_profile(center_pos=(width - 75, 75), hero_sp=main.hero2.is_special_active())

            for i, item in enumerate(main.hero1.items):
                item.draw_icon((150+(50*i), 100), small='smallest')
            for i, item in enumerate(main.hero2.items):
                item.draw_icon((main.width-(150+(50*i)), 100), small='smallest')
        
            # ── Phase 2: apply pending cube updates from server ──
            if global_vars.active_net_client is not None:
                for update in global_vars.active_net_client.pop_cube_updates():
                    ci = update['index']
                    cubes[ci]['fall'] = update['fall']
                    cubes[ci]['x'] = update['x']
                    
                    if global_vars.active_net_client.my_player_type == 2 and update.get('hero_hit') is not None:
                        target = main.hero1 if update['hero_hit'] == 1 else main.hero2
                        btype = update.get('bonus_type')
                        bamount = update.get('bonus_amount')
                        if btype == 'health':
                            target.health = min(target.max_health, target.health + bamount)
                        elif btype == 'mana':
                            target.mana = min(target.max_mana, target.mana + bamount)
                        elif btype == 'special':
                            target.special = min(target.max_special, target.special + bamount)

            for i, cube in enumerate(cubes):
                cube['fall'], cube['x'] = handle_cube(
                    pygame.Rect(cube['x'], cube['fall'], 25, 25),
                    cube['fall'],
                    cube['x'],
                    cube['color'],
                    cube['image'],
                    main.hero1,
                    main.hero2,
                    cube['bonus_type'],
                    cube['bonus_amount'],
                    cube['sound'],
                    cube_index=i,
                    net_client=global_vars.active_net_client
                )




            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            timer_text = timer_font.render(f"[{minutes:02d}:{seconds:02d}]", global_vars.TEXT_ANTI_ALIASING, main.white)

            main.screen.blit(timer_text, (main.width / 2.3, 30))  # Display timer at the top-left corner
            
            ingame_menu_button.draw(main.screen, mouse_pos)
            
            #drawing the hp and mana icon
            main.draw_hp_mana_icons()

            #drawing the damage display
            x = 0

            
            

            
            # ── NETWORK INPUT INJECTION ──────────────────────────────
            if global_vars.active_net_client is not None and global_vars.active_net_client.phase == 'playing':
                p1_keys, p2_keys = global_vars.active_net_client.get_inputs()
                my_type = global_vars.active_net_client.my_player_type

                # Both hero1 and hero2 get their inputs from the server
                main.hero1._net_keys = p1_keys
                main.hero2._net_keys = p2_keys

                # Send MY keys to server this frame
                keybinds = key.read_settings()
                raw_keys = pygame.key.get_pressed()
                if my_type == 1:
                    my_keys = {
                        'left':    bool(raw_keys[keybinds['left_move_p1'][0]]),
                        'right':   bool(raw_keys[keybinds['right_move_p1'][0]]),
                        'up':      bool(raw_keys[keybinds['jump_p1'][0]]),
                        'basic':   bool(raw_keys[keybinds['basic_atk_p1'][0]]),
                        'skill1':  bool(raw_keys[keybinds['skill_1_p1'][0]]),
                        'skill2':  bool(raw_keys[keybinds['skill_2_p1'][0]]),
                        'skill3':  bool(raw_keys[keybinds['skill_3_p1'][0]]),
                        'skill4':  bool(raw_keys[keybinds['skill_4_p1'][0]]),
                        'special': bool(raw_keys[keybinds['sp_skill_p1'][0]]),
                    }
                else:
                    my_keys = {
                        'left':    bool(raw_keys[keybinds['left_move_p1'][0]]),
                        'right':   bool(raw_keys[keybinds['right_move_p1'][0]]),
                        'up':      bool(raw_keys[keybinds['jump_p1'][0]]),
                        'basic':   bool(raw_keys[keybinds['basic_atk_p1'][0]]),
                        'skill1':  bool(raw_keys[keybinds['skill_1_p1'][0]]),
                        'skill2':  bool(raw_keys[keybinds['skill_2_p1'][0]]),
                        'skill3':  bool(raw_keys[keybinds['skill_3_p1'][0]]),
                        'skill4':  bool(raw_keys[keybinds['skill_4_p1'][0]]),
                        'special': bool(raw_keys[keybinds['sp_skill_p1'][0]]),
                    }
                    # my_keys = {
                    #     'left':    bool(raw_keys[keybinds['left_move_p2'][0]]),
                    #     'right':   bool(raw_keys[keybinds['right_move_p2'][0]]),
                    #     'up':      bool(raw_keys[keybinds['jump_p2'][0]]),
                    #     'basic':   bool(raw_keys[keybinds['basic_atk_p2'][0]]),
                    #     'skill1':  bool(raw_keys[keybinds['skill_1_p2'][0]]),
                    #     'skill2':  bool(raw_keys[keybinds['skill_2_p2'][0]]),
                    #     'skill3':  bool(raw_keys[keybinds['skill_3_p2'][0]]),
                    #     'skill4':  bool(raw_keys[keybinds['skill_4_p2'][0]]),
                    #     'special': bool(raw_keys[keybinds['sp_skill_p2'][0]]),
                    # }
                global_vars.active_net_client.send_input(my_keys)
                # P1 is the HP authority — report hero HPs to server every frame
                if global_vars.active_net_client.my_player_type == 1: # must use the hero_group, not individual (will work for now)
                    global_vars.active_net_client.send_report_hp(main.hero1.health, main.hero2.health)
                    
            else:
                # Normal local mode — clear net_keys so keyboard works
                if hasattr(main, 'hero1') and main.hero1 is not None: main.hero1._net_keys = None
                if hasattr(main, 'hero2') and main.hero2 is not None: main.hero2._net_keys = None
                # for skill in enumerate(main.hero1.attacks):
                #     print(f'skill {skill[0]+1} [{round(skill[1].get_skill_cooldown(), 2)}]', end="")
                #     print()
                # if main.hero1.special_active:
                #     for skill in enumerate(main.hero1.attacks_special):
                #         print(f'special skill {skill[0]+1} [{round(skill[1].get_skill_cooldown(), 2)}]', end="")
                #         print()
                # print('-------')

                # skill 1 [0]
                # skill 2 [17048]
                # skill 3 [0]
                # skill 4 [0]
                # skill 5 [0]
                # skill 6 [0]
                # special skill 1 [6614]
                # special skill 2 [0]
                # special skill 3 [0]
                # special skill 4 [0]
                # special skill 5 [662.19]

                
            # ── END NETWORK INPUT INJECTION ──────────────────────────

            # detect if anyone left
            if global_vars.active_net_client is not None and global_vars.active_net_client.opponent_left:
                global_vars.active_net_client.opponent_left = False
                global_vars.active_net_client.disconnect()
                global_vars.active_net_client = None
                # lobby('disconnected') 
                return 'opponent_left'

            # Safety net: detect silent disconnection (connection dropped without
            # opponent_left message — e.g. host process killed, network failure)
            if global_vars.active_net_client is not None and global_vars.active_net_client.phase == 'disconnected':
                global_vars.active_net_client.disconnect()
                global_vars.active_net_client = None
                return 'opponent_left'
            
            if global_vars.active_net_client is not None and global_vars.active_net_client.phase == 'playing':
                # ── Receive and apply opponent / authoritative state ──────────────
                #
                # P1 (host) is the DAMAGE AUTHORITY:
                #   • It runs input() for both heroes (h1 via keyboard, h2 via p2_keys).
                #   • _apply_damage() only mutates HP on P1.
                #   • It sends BOTH h1 and h2 states so P2 sees authoritative HP.
                #
                # P2 (client) receives P1's full snapshot (h1 + h2) and applies both.
                #   • Its own input() runs locally for instant visual feedback.
                #   • apply_hero_state() corrects any drift each frame.
                #
                prev_st, latest_st, prev_t, latest_t = global_vars.active_net_client.get_states_for_render()

                if latest_st is not None:
                    render_time = time.monotonic() - 0.050  # 50 ms buffer for jitter

                    if global_vars.active_net_client.my_player_type == 1:
                        # P1 receives P2's packet which contains 'h2'.
                        # Apply to local hero2 (position sync from P2's self-report).
                        # P1 is damage-authoritative so we only sync movement/facing from P2's data.
                        h2_recv = latest_st.get('h2')
                        if h2_recv and main.hero2 is not None:
                            x2, y2 = interp_xy(prev_st, latest_st, prev_t, latest_t, 'h2', render_time)
                            # Sync position/movement from P2's self-reported state.
                            # HP/cooldowns are NOT overwritten here — P1 is authoritative for those.
                            if x2 is not None: main.hero2.x_pos = x2
                            if y2 is not None: main.hero2.y_pos = y2
                            main.hero2.y_velocity   = h2_recv.get('yv',          main.hero2.y_velocity)
                            main.hero2.facing_right  = h2_recv.get('facing_right', main.hero2.facing_right)
                            main.hero2.running       = h2_recv.get('running',      main.hero2.running)

                    if global_vars.active_net_client.my_player_type == 2:
                        # P2 receives P1's packet which contains BOTH 'h1' and 'h2'.
                        #
                        # hero1 (opponent): apply fully — position, HP, animation, everything.
                        x1, y1 = interp_xy(prev_st, latest_st, prev_t, latest_t, 'h1', render_time)
                        apply_hero_state(main.hero1, latest_st.get('h1'), x1, y1)
                        #
                        # hero2 (own hero): apply GAME-STATE ONLY (HP / mana / status / cooldowns).
                        # Position and attacking flags are managed locally via keyboard input.
                        # This prevents P1's attacking flags from blocking player_movement() on P2
                        # and stops the position-rollback that made hero2 appear stuck.
                        apply_hero_game_state(main.hero2, latest_st.get('h2'))

                # ── Send own-hero state to server ─────────────────────────────────
                _now_ms = pygame.time.get_ticks()
                if global_vars.active_net_client.my_player_type == 1:
                    if _now_ms - _last_state_send_1 >= NET_STATE_TICK_MS:
                        # Send BOTH heroes: h1 is P1's own hero; h2 is P1's authoritative
                        # view of hero2 (including all HP changes from damage applied on P1).
                        global_vars.active_net_client.send_state({
                            'h1': serialize_hero(main.hero1),
                            'h2': serialize_hero(main.hero2),
                        })
                        _last_state_send_1 = _now_ms

                if global_vars.active_net_client.my_player_type == 2:
                    if _now_ms - _last_state_send_2 >= NET_STATE_TICK_MS:
                        # P2 sends its own hero2 state so P1 can sync position on P1's display.
                        global_vars.active_net_client.send_state({'h2': serialize_hero(main.hero2),})
                        _last_state_send_2 = _now_ms


            # ── Phase D: host broadcasts authoritative hero state (~30Hz) ──
            # if global_vars.active_net_client is not None and global_vars.active_net_client.my_player_type == 1 and global_vars.active_net_client.phase == 'playing':
            #     _now_ms = pygame.time.get_ticks()
            #     if _now_ms - _last_state_send >= NET_STATE_TICK_MS:
            #         global_vars.active_net_client.send_state({
            #             'h1': serialize_hero(main.hero1),
            #             'h2': serialize_hero(main.hero2),
            #         })
            #         _last_state_send = _now_ms

            # Update and draw Fire Wizard
            main.hero2_group.draw(main.screen)
            main.hero2_group.update()
            

            main.hero1_group.draw(main.screen)
            main.hero1_group.update()
            for hero in main.hero1_group:
                hero.show_skill_info(main.screen, mouse_pos)
            for hero in main.hero2_group:
                hero.show_skill_info(main.screen, mouse_pos)


            #draw summon
            # global_vars.summon_display.draw(main.screen)
            # global_vars.summon_display.update()

            # Update anddddddddddddd draw attacks
            attack_display.update()
            attack_display.draw(main.screen)

            
            

            # Update and draw Wanderer Magician
            # main.hero3_group.draw(main.screen)
            # main.hero3_group.update()
            # if not main.hero2.is_dead():
            if hero2 is not None:
                if hero2.target is not None:
                    print(hero2.target.name, hero2.target.player_type, 'hero2')
            # {("Burner"), ("damage") ("$damage", "red")}

            
            # Bot logic: only in single-player mode AND not in a LAN session.
            # The active_net_client guard prevents bot AI from overriding hero2
            # on the non-host client where hero2 is a real remote player.
            if global_vars.SINGLE_MODE_ACTIVE and global_vars.active_net_client is None:
                if global_vars.HERO1_BOT:
                    main.hero1.bot_logic()  # Add bot logic for hero1
                main.hero2.bot_logic()
                if hasattr(main, 'hero3') and main.hero3 is not None:
                    main.hero3.bot_logic()


            if winner is None:
                if global_vars.active_net_client is not None:
                    # LAN: server declares winner, not local logic
                    if global_vars.active_net_client.declared_winner is not None:
                        winner = global_vars.active_net_client.declared_winner
                else:
                    # Local mode: unchanged logic
                    if main.hero1.is_dead() and main.hero2.is_dead():
                        if global_vars.SINGLE_MODE_ACTIVE and hasattr(main, 'hero3') and main.hero3 is not None:
                            if main.hero3.is_dead():
                                winner = 'hero1'
                            else:
                                winner = None
                        else:
                            winner = 'hero1'
                    elif main.hero1.is_dead():
                        winner = 'hero2'
                    elif main.hero2.is_dead():
                        # In single player mode, check if all enemies are dead
                        if global_vars.SINGLE_MODE_ACTIVE and hasattr(main, 'hero3') and main.hero3 is not None:
                            if main.hero3.is_dead():
                                winner = 'hero1'
                            else:
                                winner = None
                        else:
                            winner = 'hero1'
                    elif global_vars.SINGLE_MODE_ACTIVE and hasattr(main, 'hero3') and main.hero3 is not None:
                        # In single player mode with 2 enemies, player wins only if both enemies are dead
                        if main.hero2.is_dead() and main.hero3.is_dead():
                            winner = 'hero1'
                        else:
                            winner = None
                    else:
                        winner = None
                

            # For displaying mana and special bonus (already on player class)
            # main.hero1.update_damage_numbers(main.screen)
            # main.hero2.update_damage_numbers(main.screen)
            # main.hero3.update_damage_numbers(main.screen)

            # main.hero2.health = 1 if not main.hero2.is_dead() else 0
            battle_end_result = battle_end(mouse_pos, mouse_press)
            pause_result = pause(mouse_pos, mouse_press)
            if pause_result == 'opponent_left' or battle_end_result == 'opponent_left':
                return 'opponent_left'
            if pause_result == 'back_to_menu' or battle_end_result == 'back_to_menu':
                return 'back_to_menu'
            if pause_result == 'restart':
                return 'restart'
            
            # print(FPS)

            

        else: # completely pause if only offline
            pause_result = pause(mouse_pos, mouse_press)
            if pause_result == 'opponent_left' or battle_end_result == 'opponent_left':
                return 'opponent_left'
            if pause_result == 'back_to_menu' or battle_end_result == 'back_to_menu':
                return 'back_to_menu'
            if pause_result == 'restart':
                return 'restart'

        
        




        #draw distance
        # main.hero2.draw_distance(main.hero1_group)
        # hero1.draw_hitbox(screen)
        # Save.update_user_win(global_vars.user_id)
        main.pygame.display.update()
        main.clock.tick(main.FPS)
        # xaxa.tick(10000)



def leaderboard():

    leaderboard_ui = Leaderboard()
    load_sword_login_bg = False
    
    # leaderboard_ui.update()
    while True:
        events = pygame.event.get()

        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        key_press = pygame.key.get_pressed()

        current_time = pygame.time.get_ticks()
        for event in events:
            if event.type == main.pygame.QUIT:
                main.pygame.quit()
                exit()

            if keys[pygame.K_ESCAPE]:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.is_clicked(event.pos):
                    return


        if not load_sword_login_bg:
            Animate_BG.sword_login.load_frames_type2()
            load_sword_login_bg = True
        Animate_BG.sword_login.display(screen, speed=10)


        leaderboard_ui.update(
            screen=main.screen,
            x=width // 2 + 100,
            y=75,
            # x=mouse_pos[0],
            # y=mouse_pos[1],
            mouse_pos=mouse_pos,
            mouse_press=mouse_press,
            events=events
        )




        main.pygame.display.update()
        main.clock.tick(main.FPS)

def handle_cube(cube, cube_fall, cube_x, cube_color, cube_image, hero1, hero2, bonus_type, bonus_amount, sound, cube_index=0, net_client=None):
    """
    Handles the logic for a single cube.

    Args:
        cube: The `pygame.Rect` object representing the cube.
        cube_fall: The current y-position of the cube.
        cube_x: The current x-position of the cube.
        cube_color: The color of the cube (for debugging purposes).
        cube_image: The image to render for the cube.
        hero1: The first hero object.
        hero2: The second hero object.
        bonus_type: The type of bonus ('health', 'mana', 'special').
        bonus_amount: The amount of the bonus to apply.

    Returns:
        Updated cube_fall and cube_x values.
    """
    if cube_fall < main.DEFAULT_Y_POS - 20:
        cube_fall += 1
        cube = pygame.Rect(cube_x, cube_fall, 25, 25)
        cube_hitbox = pygame.rect.Rect(cube.x, cube.y, cube.width * (cube.width * .07), cube.height * (cube.height * .07))

        scaled_image = pygame.transform.scale(cube_image, (cube.width * (cube.width * .07), cube.height * (cube.height * .07)))
        main.screen.blit(scaled_image, cube)
        if SHOW_HITBOX:
            pygame.draw.rect(main.screen, 'Red', cube_hitbox, 1)


        # Collision detection — only P1 (authority) or local games apply bonuses and reset
        if cube_hitbox.colliderect(hero1.hitbox_rect):
            if global_vars.active_net_client is None or global_vars.active_net_client.my_player_type == 1:
                sound.play()
                if bonus_type == 'health':
                    hero1.health = min(hero1.max_health, hero1.health + bonus_amount)
                elif bonus_type == 'mana':
                    prev = hero1.mana
                    hero1.mana = min(hero1.max_mana, hero1.mana + bonus_amount)
                    actual = hero1.mana - prev
                    if actual > 0:
                        hero1.display_damage(actual, interval=30, color=cyan2, size=50)
                elif bonus_type == 'special':
                    prev = hero1.special
                    hero1.special = min(hero1.max_special, hero1.special + bonus_amount)
                    actual = hero1.special - prev
                    if actual > 0:
                        hero1.display_damage(actual, interval=30, color=gold, size=50)

                cube_x = random.randint(20, int(main.width - 20))
                cube_fall = random.randint(-2000, -500)
                if global_vars.active_net_client is not None:
                    global_vars.active_net_client.send_cube_reset(cube_index, cube_fall, cube_x, hero_hit=1, bonus_type=bonus_type, bonus_amount=bonus_amount)

        elif cube_hitbox.colliderect(hero2.hitbox_rect):
            if global_vars.active_net_client is None or global_vars.active_net_client.my_player_type == 1:
                sound.play()
                if bonus_type == 'health':
                    hero2.health = min(hero2.max_health, hero2.health + bonus_amount)
                elif bonus_type == 'mana':
                    prev = hero2.mana
                    hero2.mana = min(hero2.max_mana, hero2.mana + bonus_amount)
                    actual = hero2.mana - prev
                    if actual > 0:
                        hero2.display_damage(actual, interval=30, color=cyan2, size=50)
                elif bonus_type == 'special':
                    prev = hero2.special
                    hero2.special = min(hero2.max_special, hero2.special + bonus_amount)
                    actual = hero2.special - prev
                    if actual > 0:
                        hero2.display_damage(actual, interval=30, color=gold, size=50)

                cube_x = random.randint(20, int(main.width - 20))
                cube_fall = random.randint(-2000, -500)
                if global_vars.active_net_client is not None:
                    global_vars.active_net_client.send_cube_reset(cube_index, cube_fall, cube_x, hero_hit=2, bonus_type=bonus_type, bonus_amount=bonus_amount)
    else:
        if global_vars.active_net_client is not None:
            if global_vars.active_net_client.my_player_type == 1:
                cube_x = random.randint(20, int(main.width - 20))
                cube_fall = -150
                global_vars.active_net_client.send_cube_reset(cube_index, cube_fall, cube_x, hero_hit=None, bonus_type=None, bonus_amount=None)
        else:
            cube_x = random.randint(20, int(main.width - 20))
            cube_fall = -150

    return cube_fall, cube_x

menu_game = ImageButton(
    image_path=text_box_img,
    pos=(width/2-(width*0.075), height*0.475),
    scale=0.8,
    text='menu',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)
rematch_game = ImageButton(
    image_path=text_box_img,
    pos=(width/2+(width*0.075), height*0.475),
    scale=0.8,
    text='rematch',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

resume_game = ImageButton(
    image_path=text_box_img,
    pos=(width/2+(width*0.075), height*0.475),
    scale=0.8,
    text='resume',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

restart_game = ImageButton(
    image_path=text_box_img,
    pos=(width/2+(width*0.075), height*0.575),
    scale=0.8,
    text='restart',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

in_game_settings_button = ImageButton(
    image_path=text_box_img,
    pos=(width/2-(width*0.075), height*0.575),
    scale=0.8,
    text='Settings',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size*0.8,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)
def battle_end(mouse_pos, mouse_press, font=None, default_size = ((width * DEFAULT_HEIGHT) / (height * DEFAULT_WIDTH)),):
    global paused, battle_result_recorded
    if font is None:
        font = global_vars.get_font(100)
    if winner is not None:
        if winner == 'hero1':
            create_title('PLAYER 1 WINS!!!', font, default_size - 0.55, height * 0.40)
            # Track win for player 1 if logged in and multiplayer (only record ONCE)
            if not global_vars.SINGLE_MODE_ACTIVE and global_vars.logged_in and global_vars.user_id is not None and not battle_result_recorded:
                Save.update_user_win(global_vars.user_id)
                # Track loss for player 2 if logged in and multiplayer
                if global_vars.logged_in2 and global_vars.user_id2 is not None:
                    Save.update_user_loss(global_vars.user_id2)
                battle_result_recorded = True
        elif winner == 'hero2':
            create_title('PLAYER 2 WINS!!!', font, default_size - 0.55, height * 0.40)
            # Track loss for player 1 if logged in and multiplayer (only record ONCE)
            if not global_vars.SINGLE_MODE_ACTIVE and global_vars.logged_in and global_vars.user_id is not None and not battle_result_recorded:
                Save.update_user_loss(global_vars.user_id)
                # Track win for player 2 if logged in and multiplayer
                if global_vars.logged_in2 and global_vars.user_id2 is not None:
                    Save.update_user_win(global_vars.user_id2)
                battle_result_recorded = True
    
        menu_game.draw(screen, mouse_pos)
        rematch_game.draw(screen, mouse_pos)
        if mouse_press[0] and menu_game.is_clicked(mouse_pos):
            paused = False
            if global_vars.active_net_client is not None and global_vars.active_net_client.opponent_left:
                print(f'I am leaving good luck everybody')
                print("Opponent left detected in player_selection")
                return 'opponent_left'
            else:
                print('going back to menu?')
                return 'back_to_menu'

        if mouse_press[0] and rematch_game.is_clicked(mouse_pos):
            paused = False
            if global_vars.active_net_client is not None:
                if not global_vars.active_net_client.my_rematch_sent:
                    global_vars.active_net_client.send_rematch_request()
            else:
                reset_all()
                return "rematch"
            
        if global_vars.active_net_client is not None:
            status_font = global_vars.get_font(30)
            if global_vars.active_net_client.my_rematch_sent:
                t = status_font.render("Rematch request sent!", True, (100, 255, 100))
                screen.blit(t, (width // 2 - t.get_width() // 2, int(height * 0.55)))
            if global_vars.active_net_client.opponent_rematch_sent:
                t = status_font.render("Opponent requested a rematch!", True, (255, 200, 100))
                screen.blit(t, (width // 2 - t.get_width() // 2, int(height * 0.60)))

def pause(mouse_pos, mouse_press, font=None, default_size = ((width * DEFAULT_HEIGHT) / (height * DEFAULT_WIDTH)),):
    global paused
    #'''problem: skills can go negative numbers while paused, lan multiplayer and local multiplayer must both working, when pausing in multiplayer, skills and other cooldowns and times won't be paused if on lan multiplayer, in local, if paused, all related timings such as skill cooldowns must be paused, but the total pause duration adds more cooldown to skills, which is a bug that needs to be fixed.'''
    if font is None:
        font = global_vars.get_font(100)
    if paused:
        create_title('PAUSED', font, default_size - 0.55, height * 0.40)

        menu_game.draw(screen, mouse_pos)
        resume_game.draw(screen, mouse_pos)
        if global_vars.active_net_client is None:
            restart_game.draw(screen, mouse_pos)
            in_game_settings_button.draw(screen, mouse_pos)
        if mouse_press[0] and menu_game.is_clicked(mouse_pos):
            paused = False
            if global_vars.active_net_client is not None:
                global_vars.active_net_client.disconnect()
                global_vars.active_net_client = None
                return 'opponent_left'
            return 'back_to_menu'
            

        if mouse_press[0] and resume_game.is_clicked(mouse_pos):
            paused = False

        if global_vars.active_net_client is None:
            if mouse_press[0] and restart_game.is_clicked(mouse_pos):
                paused = False
                reset_all()
                return 'restart'
                # fade(loading_screen_bg, game)
                

            if mouse_press[0] and in_game_settings_button.is_clicked(mouse_pos):
                settings(in_game=True)


            

pygame.mixer.music.set_volume(0.8 * global_vars.MAIN_VOLUME)



def menu():
    
    pygame.mixer.music.fadeout(1000)
    pygame.time.set_timer(pygame.USEREVENT + 3, 1000)

    pygame.mixer.music.stop()
    pygame.mixer.music.load(MENU_MUSIC)
    # Set volume based on mute state
    if global_vars.MUTE:
        pygame.mixer.music.set_volume(0)
    else:
        pygame.mixer.music.set_volume(global_vars.MAIN_VOLUME)
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(loops=-1, fade_ms=1500)  # Loop indefinitely
    # print('playing music')

    # background = main.pygame.transform.scale(
    #     pygame.image.load(r'assets\backgrounds\9.png').convert(), (main.width, main.height))

    font = global_vars.get_font(100)
    default_size = ((main.width * main.DEFAULT_HEIGHT) / (main.height * main.DEFAULT_WIDTH))

    _lan_connecting = False

    while True:
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        key_press = pygame.key.get_pressed()

        main.screen.fill((0, 0, 0))
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()   
                pass

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
                if not _lan_connecting and global_vars.active_net_client is None:
                    _lan_connecting = True
                    # multiplayer_menu keeps the survivor in the lobby and shows
                    # its own 'Opponent Left' banner; it only returns when the
                    # player chooses to leave the lobby.
                    main.multiplayer_menu()   # Minecraft-style Host / Join
                    _lan_connecting = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if single_button.is_clicked(event.pos):
                    global_vars.SINGLE_MODE_ACTIVE = True
                    main.player_selection()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.is_clicked(event.pos):
                    main_menu()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if multiplayer_button.is_clicked(event.pos):
                    _lan_connecting = True
                    main.multiplayer_menu()
                    _lan_connecting = False
                                 
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                if control_button.is_clicked(event.pos):
                    fade(Animate_BG.waterfall_day_bg.frames[0], controls, 300, True)
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if settings_button.is_clicked(event.pos):
                    settings()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if campaign_button.is_clicked(event.pos):
                    fade(Animate_BG.waterfall_day_bg.frames[0], campaign, 300, True)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if login_button.is_clicked(event.pos):
                    fade(Animate_BG.waterfall_day_bg.frames[0], login, 300, True)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # pass
                if leaderboard_button.is_clicked(event.pos):
                    fade(Animate_BG.waterfall_day_bg.frames[0], leaderboard, 300, True)      

            if keys[pygame.K_SPACE]:
                main.player_selection()

            if keys[pygame.K_KP_ENTER]:
                main.multiplayer_menu()
                
            if keys[pygame.K_r]:
                main.player_selection()
                
            if keys[pygame.K_e]:
                controls()
        
        Animate_BG.waterfall_day_bg.display(screen, speed=50)
        create_bordered_title('Maine Menu', font, default_size, main.height * 0.2)
        single_button.draw(main.screen, mouse_pos)
        multiplayer_button.draw(main.screen, mouse_pos)

        login_button.draw(main.screen,mouse_pos)
        control_button.draw(main.screen,mouse_pos)

        settings_button.draw(main.screen,mouse_pos)
        login_button.draw(main.screen, mouse_pos)
        leaderboard_button.draw(main.screen, mouse_pos)

        menu_button.draw(main.screen, mouse_pos)
        

        if campaign_button.is_hovered(mouse_pos):
            coming_soon_button.draw(main.screen, mouse_pos)
        else:
            campaign_button.draw(main.screen, mouse_pos)


        # result = leaderboard_ui.update(
        #                     screen=main.screen,
        #                     x=50,
        #                     y=75,
        #                     # x=mouse_pos[0],
        #                     # y=mouse_pos[1],
        #                     mouse_pos=mouse_pos,
        #                     mouse_press=mouse_press,
        #                     events=events
        #                 )


        

        # print(global_vars.MAIN_VOLUME)
        pygame.display.update()
        main.clock.tick(main.FPS)

def campaign():
    pass


load_sword_login_bg = False

def login():

    #variables
    global load_sword_login_bg
    username_input = ""
    password_input = ""
    usernamereg_input = ""
    passwordreg_input = ""
    username_clicked = False
    password_clicked = False
    usernamereg_clicked = False
    passwordreg_clicked = False
    
    # Player 2 login variables
    username_input_p2 = ""
    password_input_p2 = ""
    username_clicked_p2 = False
    password_clicked_p2 = False
    p2_login_field_offset = 80
    p2_label_y_offset = 20  # Offset to position label above the field

    login_button_width = width * 0.4
    login_button_height = 50
    username_limit_char = [1, 20]
    password_limit_char = [8, 20]
    typing_gap = 1500
    typing = False
    font = global_vars.get_font(60)
    
    # Popup message tracking
    popup_message = ""
    popup_type = ""  # "success", "error", "info"
    popup_show_time = 0
    popup_duration = 3500  # 3.5 seconds - increased duration for better visibility

    userreg = RectButton(width*0.5 - int(login_button_width/2), 
                            height*2, 
                            r'assets\font\slkscr.ttf', int(height * 0.05), 

                            (50, 255, 255), username_input + (("|" if typing else "") if username_clicked and len(username_input) <= username_limit_char[1] else ""), 
                            
                            login_button_width, 
                            login_button_height, 
                            0)
    passreg = RectButton(width*0.5 - int(login_button_width/2), 
                            height*2, 
                            r'assets\font\slkscr.ttf', int(height * 0.05), 

                            (50, 255, 255), username_input + (("|" if typing else "") if username_clicked and len(username_input) <= username_limit_char[1] else ""), 
                            
                            login_button_width, 
                            login_button_height, 
                            0)
    

    userreg_but1 = RectButton(width*0.5 - int(login_button_width/2), 
                            height*2, 
                            r'assets\font\slkscr.ttf', int(height * 0.05), 

                            (50, 255, 255), username_input + (("|" if typing else "") if username_clicked and len(username_input) <= username_limit_char[1] else ""), 
                            
                            80, 
                            40, 
                            0)
    

    userreg_but2 = RectButton(width*0.8 - int(login_button_width/2), 
                            height*2, 
                            r'assets\font\slkscr.ttf', int(height * 0.05), 

                            (50, 255, 255), username_input + (("|" if typing else "") if username_clicked and len(username_input) <= username_limit_char[1] else ""), 
                            
                            80, 
                            40, 
                            0)

    register_modal = ModalObject((width * 0.5, height * 1.5),(width*0.7,height*0.7),   inputobject=[userreg, passreg], buttons = [reg_back, reg_register], button_gap = 0.5, button_bottom_gap= 0, Title = "Register")
    
    Username = RectButton(width*0.5 - int(login_button_width/2), 
                            height*0.4, 
                            r'assets\font\slkscr.ttf', int(height * 0.05), 

                            (50, 255, 255), username_input + (("|" if typing else "") if username_clicked and len(username_input) <= username_limit_char[1] else ""), 
                            
                            login_button_width, 
                            login_button_height, 
                            0)
        
    Password = RectButton(width*0.5 - int(login_button_width/2), 
                            height*0.6, 
                            r'assets\font\slkscr.ttf', int(height * 0.05), 
                            (50, 255, 255), ("*" * len(password_input)) + (("|" if typing else "") if password_clicked and len(password_input) <= password_limit_char[1] else ""), 
                            login_button_width, 
                            login_button_height, 
                            0)
    register_opacity = 0
    
    login_option = ImageButton(
        image_path=text_box_img,
        pos=(width * 0.6, height * 0.85),
        scale=0.9,
        text='LOGIN',
        font_path=r'assets\font\slkscr.ttf',
        font_size=font_size,
        text_color='white',
        text_anti_alias=global_vars.TEXT_ANTI_ALIASING
    )
    # Logout button (only visible when logged in)
    logout_button = ImageButton(
        image_path=text_box_img,
        pos=(width * 0.4, height * 0.85),
        scale=0.9,
        text='LOGOUT',
        font_path=r'assets\font\slkscr.ttf',
        font_size=font_size,
        text_color='white',
        text_anti_alias=global_vars.TEXT_ANTI_ALIASING
    )
    
    # Login button for Player 2 (only visible when Player 1 is logged in and Player 2 is not)
    login_button_p2 = ImageButton(
        image_path=text_box_img,
        pos=(width * 0.6, height * 0.85),
        scale=0.9,
        text='LOGIN',
        font_path=r'assets\font\slkscr.ttf',
        font_size=font_size,
        text_color='white',
        text_anti_alias=global_vars.TEXT_ANTI_ALIASING
    )
    
    # Logout button for Player 2 (only visible when Player 2 is logged in)
    logout_button_p2 = ImageButton(
        image_path=text_box_img,
        pos=(width * 0.6, height * 0.85),
        scale=0.9,
        text='LOGOUT',
        font_path=r'assets\font\slkscr.ttf',
        font_size=font_size,
        text_color='white',
        text_anti_alias=global_vars.TEXT_ANTI_ALIASING
    )
    
    while True:
        
        Username = RectButton(width*0.5 - int(login_button_width/2), 
                            height*0.4, 
                            r'assets\font\slkscr.ttf', int(height * 0.05), 

                            (50, 255, 255), username_input + (("|" if typing else "") if username_clicked and len(username_input) <= username_limit_char[1] else ""), 
                            
                            login_button_width, 
                            login_button_height, 
                            0)
        Password = RectButton(width*0.5 - int(login_button_width/2), 
                            height*0.6, 
                            r'assets\font\slkscr.ttf', int(height * 0.05), 
                            (50, 255, 255), ("*" * len(password_input)) + (("|" if typing else "") if password_clicked and len(password_input) <= password_limit_char[1] else ""), 
                            login_button_width, 
                            login_button_height, 
                            0)
        
        # Player 2 Input Fields (for P2 login)
        Username_p2 = RectButton(
                            width*0.5 - int(login_button_width/2),
                            height*0.4 + p2_login_field_offset,   # SAME as P1 + offset
                            r'assets\font\slkscr.ttf',
                            int(height * 0.05),
                            (50, 255, 255),
                            username_input_p2 + (("|" if typing else "") if username_clicked_p2 and len(username_input_p2) <= username_limit_char[1] else ""),
                            login_button_width,
                            login_button_height,
                            0)

        Password_p2 = RectButton(
                            width*0.5 - int(login_button_width/2),
                            height*0.55 + p2_login_field_offset,   # SAME as P1 + offset
                            r'assets\font\slkscr.ttf',
                            int(height * 0.05),
                            (50, 255, 255),
                            ("*" * len(password_input_p2)) + (("|" if typing else "") if password_clicked_p2 and len(password_input_p2) <= password_limit_char[1] else ""),
                            login_button_width,
                            login_button_height,
                            0)

        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        

        if not load_sword_login_bg:
            Animate_BG.sword_login.load_frames_type2()
            load_sword_login_bg = True
        Animate_BG.sword_login.display(screen, speed=10)
        

        #typing indicator
        if (pygame.time.get_ticks() % typing_gap) > typing_gap/2:
            typing = True
        else: 
            typing = False

        # Check if popup should still be shown
        if popup_message and (pygame.time.get_ticks() - popup_show_time) > popup_duration:
            popup_message = ""
            popup_type = ""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  
            if keys[pygame.K_ESCAPE]:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.is_clicked(event.pos):
                    return
                
                # Logout button handling for Player 1
                if global_vars.logged_in and logout_button.is_clicked(event.pos):
                    global_vars.logged_in = False
                    global_vars.username = None
                    global_vars.user_id = None
                    global_vars.current_user_controls = None
                    username_input = ""
                    password_input = ""
                    popup_message = "Player 1 logged out successfully!"
                    popup_type = "success"
                    popup_show_time = pygame.time.get_ticks()
                    continue
                
                # Logout button handling for Player 2
                if global_vars.logged_in2 and logout_button_p2.is_clicked(event.pos):
                    global_vars.logged_in2 = False
                    global_vars.username2 = None
                    global_vars.user_id2 = None
                    global_vars.current_user_controls2 = None
                    username_input_p2 = ""
                    password_input_p2 = ""
                    popup_message = "Player 2 logged out successfully!"
                    popup_type = "success"
                    popup_show_time = pygame.time.get_ticks()
                    continue
                
                # Login button for Player 2 (only clickable when P1 is logged in and P2 is not)
                if global_vars.logged_in and not global_vars.logged_in2 and login_button_p2.is_clicked(event.pos):
                    # Check if we're already in the login fields (try to login)
                    if username_clicked_p2 or password_clicked_p2 or len(username_input_p2) > 0:
                        # Processing login credentials for Player 2
                        if len(username_input_p2) == 0:
                            popup_message = "Please enter Player 2 username"
                            popup_type = "error"
                            popup_show_time = pygame.time.get_ticks()
                        else:
                            user = Save.login_check(username_input_p2)
                            if user == None:
                                popup_message = "Player 2: No account found"
                                popup_type = "error"
                                popup_show_time = pygame.time.get_ticks()
                            else:
                                if user[2] == Save.hash_pw(password_input_p2):
                                    # Login successful for Player 2
                                    global_vars.logged_in2 = True
                                    global_vars.username2 = user[1]
                                    global_vars.user_id2 = user[0]
                                    # Load user-specific keybinds for Player 2
                                    global_vars.current_user_controls2 = key.read_settings()
                                    popup_message = f"Welcome {global_vars.username2}! (Player 2)"
                                    popup_type = "success"
                                    popup_show_time = pygame.time.get_ticks()
                                    username_input_p2 = ""
                                    password_input_p2 = ""
                                    username_clicked_p2 = False
                                    password_clicked_p2 = False
                                else:
                                    popup_message = "Player 2: Wrong password"
                                    popup_type = "error"
                                    popup_show_time = pygame.time.get_ticks()
                    else:
                        # First click on login button - activate fields
                        username_clicked_p2 = True
                        password_clicked_p2 = False
                        continue
                
                if Username.is_clicked(event.pos) and not register_modal.selected and not global_vars.logged_in:
                    username_clicked = not username_clicked
                    password_clicked = False
                if Password.is_clicked(event.pos) and not register_modal.selected and not global_vars.logged_in:
                    password_clicked = not password_clicked
                    username_clicked = False
                
                # Player 2 input field handling (when P1 is logged in and P2 is not, and username_clicked_p2 is True)
                if Username_p2.is_clicked(event.pos) and global_vars.logged_in and not global_vars.logged_in2 and not register_modal.selected:
                    username_clicked_p2 = not username_clicked_p2
                    password_clicked_p2 = False
                if Password_p2.is_clicked(event.pos) and global_vars.logged_in and not global_vars.logged_in2 and not register_modal.selected:
                    password_clicked_p2 = not password_clicked_p2
                    username_clicked_p2 = False

                if userreg.is_clicked(event.pos) and register_modal.selected:
                    usernamereg_clicked = not usernamereg_clicked
                    passwordreg_clicked = False
                if passreg.is_clicked(event.pos) and register_modal.selected:
                    passwordreg_clicked = not passwordreg_clicked
                    usernamereg_clicked = False

                if reg_register.is_clicked(event.pos) and register_modal.selected:

                    error_message = None

                    # --- Validate username ---
                    if not (username_limit_char[0] <= len(usernamereg_input) <= username_limit_char[1]):
                        error_message = "Username length must be 1-20 chars"

                    # --- Validate password ---
                    elif not (password_limit_char[0] <= len(passwordreg_input) <= password_limit_char[1]):
                        error_message = "Password too short (min 8 chars)"

                    # --- Attempt registration ---
                    else:
                        success = Save.register(usernamereg_input, Save.hash_pw(passwordreg_input))
                        if not success:
                            error_message = "Username already exists!"

                    # --- Handle result ---
                    if error_message:
                        popup_message = error_message
                        popup_type = "error"
                        popup_show_time = pygame.time.get_ticks()
                        register_modal.close_modal()

                        # Reset inputs safely
                        usernamereg_clicked = False
                        passwordreg_clicked = False
                        typing = False  # prevents freeze bug

                        usernamereg_input = ""
                        passwordreg_input = ""

                    else:
                        popup_message = "User registered successfully!"
                        popup_type = "success"
                        popup_show_time = pygame.time.get_ticks()

                        register_modal.close_modal()

                        # Reset inputs safely
                        usernamereg_clicked = False
                        passwordreg_clicked = False
                        typing = False  # prevents freeze bug

                        usernamereg_input = ""
                        passwordreg_input = ""

                        
                if login_option.is_clicked(event.pos) and not register_modal.selected and not global_vars.logged_in:
                    if len(username_input) == 0:
                        popup_message = "Please enter username"
                        popup_type = "error"
                        popup_show_time = pygame.time.get_ticks()
                    else:
                        user = Save.login_check(username_input)
                        if user == None:
                            popup_message = "No account found"
                            popup_type = "error"
                            popup_show_time = pygame.time.get_ticks()
                        else:
                            if user[2] == Save.hash_pw(password_input):
                                # Login successful
                                global_vars.logged_in = True
                                global_vars.username = user[1]
                                global_vars.user_id = user[0]
                                # Load user-specific keybinds
                                global_vars.current_user_controls = key.read_settings()
                                popup_message = f"Welcome {global_vars.username}! (Player 1)"
                                popup_type = "success"
                                popup_show_time = pygame.time.get_ticks()
                                username_input = ""
                                password_input = ""
                            else:
                                popup_message = "Wrong password"
                                popup_type = "error"
                                popup_show_time = pygame.time.get_ticks()

                if register_button.is_clicked(event.pos) and not register_modal.selected and not global_vars.logged_in:
                    Save.show_all_user()
                    # Animate register modal to center
                    register_modal.open_modal()
                    usernamereg_clicked = False
                    passwordreg_clicked = False
                    password_clicked = False
                    username_clicked = False
                    password_input = ""
                    username_input = ""
                    usernamereg_input = ""
                    passwordreg_input = ""
                    continue  # Skip rest of event processing for this frame

            if username_clicked and not register_modal.selected:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        username_input = username_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        pass
                    elif len(username_input) <= username_limit_char[1]:
                        username_input += event.unicode
                    else:
                        popup_message = "Max username length reached"
                        popup_type = "error"
                        popup_show_time = pygame.time.get_ticks()

            if password_clicked and not register_modal.selected:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        password_input = password_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        pass
                    elif len(password_input) <= password_limit_char[1]:
                        password_input += event.unicode
                    else:
                        popup_message = "Max password length reached"
                        popup_type = "error"
                        popup_show_time = pygame.time.get_ticks()

            if usernamereg_clicked and register_modal.selected:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        usernamereg_input = usernamereg_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        pass
                    elif len(usernamereg_input) <= username_limit_char[1]:
                        usernamereg_input += event.unicode
                    else:
                        popup_message = "Max username length reached"
                        popup_type = "error"
                        popup_show_time = pygame.time.get_ticks()

            if passwordreg_clicked and register_modal.selected:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        passwordreg_input = passwordreg_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        pass
                    elif len(passwordreg_input) <= password_limit_char[1]:
                        passwordreg_input += event.unicode
                    else:
                        popup_message = "Max password length reached"
                        popup_type = "error"
                        popup_show_time = pygame.time.get_ticks()
            
            # Player 2 keyboard input handling
            if username_clicked_p2 and global_vars.logged_in and not global_vars.logged_in2:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        username_input_p2 = username_input_p2[:-1]
                    elif event.key == pygame.K_RETURN:
                        pass
                    elif len(username_input_p2) <= username_limit_char[1]:
                        username_input_p2 += event.unicode
                    else:
                        popup_message = "Max username length reached"
                        popup_type = "error"
                        popup_show_time = pygame.time.get_ticks()

            if password_clicked_p2 and global_vars.logged_in and not global_vars.logged_in2:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        password_input_p2 = password_input_p2[:-1]
                    elif event.key == pygame.K_RETURN:
                        pass
                    elif len(password_input_p2) <= password_limit_char[1]:
                        password_input_p2 += event.unicode
                    else:
                        popup_message = "Max password length reached"
                        popup_type = "error"
                        popup_show_time = pygame.time.get_ticks()
        

        Username.text = username_input + (("|" if typing else "") if username_clicked and len(username_input) <= username_limit_char[1] else "")
        
        Password.text = ("*" * len(password_input)) + (("|" if typing else "") if password_clicked and len(password_input) <= password_limit_char[1] else "")
        
        userreg.text = usernamereg_input + (("|" if typing else "") if usernamereg_clicked and len(usernamereg_input) <= username_limit_char[1] else "")
        
        passreg.text = ("*" * len(passwordreg_input)) + (("|" if typing else "") if passwordreg_clicked and len(passwordreg_input) <= password_limit_char[1] else "")
        
        # Player 2 input text updates
        Username_p2.text = username_input_p2 + (("|" if typing else "") if username_clicked_p2 and len(username_input_p2) <= username_limit_char[1] else "")
        Password_p2.text = ("*" * len(password_input_p2)) + (("|" if typing else "") if password_clicked_p2 and len(password_input_p2) <= password_limit_char[1] else "")
        

        
        draw_black_screen(0.5,size=(width*0.2, height * 0.2, width*0.6, height*0.6))

        create_title('FIGHTING KIMHIEE', font , 1, height * 0.1, angle=0, x_offset=width)

        # Show different UI based on login status for Player 1
        if global_vars.logged_in:
            # Show Player 1 logged in status with success color
            create_title(f'P1 Logged In: Welcome, {global_vars.username}!', font , 0.45, height * 0.32, angle=0, x_offset=width, color=green)
            logout_button.draw(screen, mouse_pos)
            
            # Show Player 2 login fields immediately when Player 1 is logged in
            if global_vars.logged_in2:
                # Both players logged in - show Player 2 info
                create_title(f'P2 Logged In: Welcome, {global_vars.username2}!', font , 0.45, height * 0.42, angle=0, x_offset=width, color=green)
                logout_button_p2.draw(screen, mouse_pos)
            else:
                # Player 1 logged in, showing Player 2 login fields
                create_title('Player 2 Login:', font , 0.5, height * 0.36, angle=0, x_offset=width)
                create_title('Username', font , 0.5, height * 0.4 + p2_login_field_offset - p2_label_y_offset, angle=0, x_offset=width*0.74)
                create_title('Password', font , 0.5, height * 0.55 + p2_login_field_offset - p2_label_y_offset, angle=0, x_offset=width*0.74)
                
                Username_p2.update(mouse_pos, username_clicked_p2)
                Username_p2.draw(screen, global_vars.TEXT_ANTI_ALIASING)
                
                Password_p2.update(mouse_pos, password_clicked_p2)
                Password_p2.draw(screen, global_vars.TEXT_ANTI_ALIASING)
                
                # Show LOGIN button for Player 2 login submission (not LOGIN P2)
                login_button_p2.text = 'LOGIN'
                login_button_p2.draw(screen, mouse_pos)
        else:
            # Player 1 not logged in - show login fields
            create_title('Username', font , 0.5, height * 0.35, angle=0, x_offset=width*0.74)
            create_title('Password', font , 0.5, height * 0.55, angle=0, x_offset=width*0.74)

            Password.update(mouse_pos, password_clicked)
            Password.draw(screen, global_vars.TEXT_ANTI_ALIASING)

            Username.update(mouse_pos, username_clicked)
            Username.draw(screen, global_vars.TEXT_ANTI_ALIASING)

            userreg.update(mouse_pos, usernamereg_clicked)
            passreg.update(mouse_pos, passwordreg_clicked)

            login_option.draw(screen, mouse_pos)
            register_button.draw(screen, mouse_pos)
        
        menu_button.draw(screen, mouse_pos)
        
        # Calculate opacity based on modal state AFTER event processing
        if register_modal.selected:
            register_opacity = 0.5
        else:
            register_opacity = 0
        
        draw_black_screen(register_opacity)
        register_modal.update(mouse_pos, mouse_press, None, max_selected=1)

        # Draw popup message if active
        if popup_message:
            if popup_type == "success":
                popup_color = green
            elif popup_type == "error":
                popup_color = red
            else:
                popup_color = white
            
            # Make popup message larger and more visible for success
            if popup_type == "success":
                create_title(popup_message, font, 0.6, height * 0.5, color=popup_color, angle=0, x_offset=width)
            else:
                create_title(popup_message, font, 0.5, height * 0.5, color=popup_color, angle=0, x_offset=width)
        
        pygame.display.update()
        main.clock.tick(main.FPS)
        



#-------------------------------------START-----------------------------------------

keybinds = ImageButton(
    image_path=text_box_img,
    pos=(width/2 + width*0.08, height*0.9),
    scale=0.8 * (width/1280),
    text='Save Keys',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)


reset_keybinds = ImageButton(
    image_path=text_box_img,
    pos=(width/2 - width*0.08, height*0.9),
    scale = 0.8 * (width/1280),
    text='Default Keys',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)


swapconfirm_yes = ImageButton(
    image_path=text_box_img,
    pos=(width/2 + width*0.08, height*1.2),
    scale=0.8,
    text='Replace Key',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

swapconfirm_no = ImageButton(
    image_path=text_box_img,
    pos=(width/2 - width*0.08, height*1.2),
    scale=0.8,
    text='Back',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p,
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

reg_back = ImageButton(
            image_path=text_box_img,
            pos=(center_pos[0] * 0.8, height * 3),
            scale=1,
            text="Back",
            font_path=FONT_PATH,
            font_size=font_size,
            text_color='white',
            text_anti_alias=global_vars.TEXT_ANTI_ALIASING
        )

reg_register = ImageButton(
            image_path=text_box_img,
            pos=(center_pos[0] * 1.2, height * 3),
            scale=1,
            text="Register",
            font_path=FONT_PATH,
            font_size=font_size,
            text_color='white',
            text_anti_alias=global_vars.TEXT_ANTI_ALIASING
        )
        








#-------------------------------------END-----------------------------------------

can_click = True
opacity = 0
display_confirmation = False
load_green_bg = False
def controls(can_click = can_click, opacity=opacity, display_confirmation = display_confirmation, has_changes = has_changes):
    global load_green_bg
#-------------------------------------START-----------------------------------------
    # command_img = main.pygame.transform.scale(
    #     pygame.image.load(r'assets\command image.png').convert(), (main.width/2, main.height))
    # control_img = main.pygame.transform.scale(
    #     pygame.image.load(r'assets\control image.png').convert(), (main.width/2, main.height))
    # (text, font=None, scale=1, y_offset=100, color=white, angle=0)
   
    
    Keybinds_keys = key.read_settings()    
 
    new_key = [Keybinds_keys[x] for x in Keybinds_keys]

    
   

    basic_atk_btn_p1 = RectButton(width*base_width, height*base_height, r'assets\font\slkscr.ttf', int(height * 0.05), (0, 255, 0), display_inputs(new_key[4][1]),button_width,button_height,0)
    sp_skill_btn_p1 = RectButton(width*base_width, height*(base_height + h_gap) , r'assets\font\slkscr.ttf', int(height * 0.05), (0, 255, 0), display_inputs(new_key[5][1]),button_width,button_height,0)


   
    skill_1_btn_p1 = RectButton(width*base_width,               height*(base_height + 2.5*h_gap), r'assets\font\slkscr.ttf', int(height * 0.05), (0, 255, 0), display_inputs(new_key[0][1]),button_width,button_height,0)
    skill_2_btn_p1 = RectButton(width*(base_width + w_gap),       height*(base_height + 2.5*h_gap), r'assets\font\slkscr.ttf', int(height * 0.05), (0, 255, 0), display_inputs(new_key[1][1]),button_width,button_height,0)
    skill_3_btn_p1 = RectButton(width*(base_width + (w_gap *2)),  height*(base_height + 2.5*h_gap), r'assets\font\slkscr.ttf', int(height * 0.05), (0, 255, 0), display_inputs(new_key[2][1]),button_width,button_height,0)
    skill_4_btn_p1 = RectButton(width*(base_width + (w_gap *3)),  height*(base_height + 2.5*h_gap), r'assets\font\slkscr.ttf', int(height * 0.05), (0, 255, 0), display_inputs(new_key[3][1]),button_width,button_height,0)

    
    left_move_btn_p1 = RectButton(width*(base_width + w_gap), height*(base_height + h_gap), r'assets\font\slkscr.ttf', int(height * 0.05), (0, 255, 0), display_inputs(new_key[7][1]),button_width,button_height,0)
    jump_btn_p1 = RectButton(width*(base_width + 2*w_gap), height*(base_height), r'assets\font\slkscr.ttf', int(height * 0.05), (0, 255, 0), display_inputs(new_key[6][1]),button_width,button_height,0)
    right_move_btn_p1 = RectButton(width*(base_width + 3*w_gap) , height*(base_height + h_gap), r'assets\font\slkscr.ttf', int(height * 0.05), (0, 255, 0), display_inputs(new_key[8][1]),button_width,button_height,0)


    # w_gap = 0.1
    # h_gap = 0.133
    # base_width = 0.1
    # base_height = 0.33

    # button_width = 60
    # button_height = 60
    
    skill_1_btn_p2 = RectButton(width*base_width + width_half,               height*(base_height + 2.5*h_gap), r'assets\font\slkscr.ttf', int(height * 0.05), (0, 255, 0), display_inputs(new_key[9][1]),button_width,button_height,0)
    skill_2_btn_p2 = RectButton(width*(base_width + w_gap) + width_half,       height*(base_height + 2.5*h_gap), r'assets\font\slkscr.ttf', int(height * 0.05), (0, 255, 0), display_inputs(new_key[10][1]),button_width,button_height,0)
    skill_3_btn_p2 = RectButton(width*(base_width + (w_gap *2)) + width_half,  height*(base_height + 2.5*h_gap), r'assets\font\slkscr.ttf', int(height * 0.05), (0, 255, 0), display_inputs(new_key[11][1]),button_width,button_height,0)
    skill_4_btn_p2 = RectButton(width*(base_width + (w_gap *3)) + width_half,  height*(base_height + 2.5*h_gap), r'assets\font\slkscr.ttf', int(height * 0.05), (0, 255, 0), display_inputs(new_key[12][1]),button_width,button_height,0)


    basic_atk_btn_p2 = RectButton(width*base_width + width_half, height*base_height, r'assets\font\slkscr.ttf', int(height * 0.05), (0, 255, 0), display_inputs(new_key[13][1]),button_width,button_height,0)
    sp_skill_btn_p2 = RectButton(width*base_width + width_half, height*(base_height + h_gap) , r'assets\font\slkscr.ttf', int(height * 0.05), (0, 255, 0), display_inputs(new_key[14][1]),button_width,button_height,0)


    left_move_btn_p2 = RectButton(width*(base_width + w_gap) + width_half, height*(base_height + h_gap), r'assets\font\slkscr.ttf', int(height * 0.05), (0, 255, 0), display_inputs(new_key[16][1]),button_width,button_height,0)
    jump_btn_p2 = RectButton(width*(base_width + 2*w_gap)+ width_half, height*(base_height), r'assets\font\slkscr.ttf', int(height * 0.05), (0, 255, 0), display_inputs(new_key[15][1]),button_width,button_height,0)
    right_move_btn_p2 = RectButton(width*(base_width + 3*w_gap) + width_half, height*(base_height + h_gap), r'assets\font\slkscr.ttf', int(height * 0.05), (0, 255, 0), display_inputs(new_key[17][1]),button_width,button_height,0)

    temp_button = RectButton(width*(base_width + 2*w_gap)+ width_half, height*(base_height + h_gap), r'assets\font\slkscr.ttf', int(height * 0.05), (0, 255, 0), "UwU",button_width,button_height,0)
    
   



    key_list = [
    skill_1_btn_p1,
    skill_2_btn_p1,
    skill_3_btn_p1, 
    skill_4_btn_p1, 
    basic_atk_btn_p1,
    sp_skill_btn_p1, 
    jump_btn_p1, 
    left_move_btn_p1,
    right_move_btn_p1, 
    skill_1_btn_p2, 
    skill_2_btn_p2,
    skill_3_btn_p2, 
    skill_4_btn_p2, 
    basic_atk_btn_p2, 
    sp_skill_btn_p2,
    jump_btn_p2,
    left_move_btn_p2,
    right_move_btn_p2
    ]

# ---------------------END--------------------------------------------------


    

    

    keyswap_cancel = RectButton(width*0.5 - int(80/2), 
                            height*2, 
                            r'assets\font\slkscr.ttf', int(height * 0.05), 

                                (255, 50, 50), "Cancel",    
                            button_width * 3, 
                            button_height, 
                            0)
    

    keyswap_replace = RectButton(width*0.8 - int(80/2), 
                            height*2, 
                            r'assets\font\slkscr.ttf', int(height * 0.05), 

                            (50, 255, 50), "Confirm", 
                            
                            button_height * 3, 
                            button_height, 
                            0)


    keyswap_modal = ModalObject((width * 0.5, height * 1.5),(width*0.7,height*0.7), buttons = [keyswap_cancel, keyswap_replace], button_gap = 0.5, Title = "Key Already in Use", opacity = 0.8, description = "Bind Hotkey?")
    
    
    while True:
        # print(keyswap_modal.disable_action)

        draw_black_screen(opacity)
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        key_press = pygame.key.get_pressed()
        
        
        main.screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  
            if keys[pygame.K_ESCAPE]:
                key_list = keybind_select_reset(key_list)
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.is_clicked(event.pos):
                    return
                







# Added
#--------------------------------------------------------------------------------------------------
            #onClick, 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if keybinds.is_clicked(mouse_pos):
                    keybinds_filename = key.get_keybinds_filename()
                    if os.path.exists(keybinds_filename):
                        # with open(keybinds_filename, "r") as f:
                        #     try:
                        data = Save.loadFile(keybinds_filename)
                        #     data = json.load(f)
                        # except json.JSONDecodeError:
                        #     print("Error")
                        
                        for count,i in enumerate(data):
                            # print(i)
                            # print(tuple(new_key[count]))
                            data[i] = tuple(new_key[count])

                        Save.saveFile(keybinds_filename, data)
                        # with open(keybinds_filename, "w") as f:
                        #     # print(data, "Data type")
                        #     json.dump(data, f, indent=4)

                        # f.close()
                    
                    else:
                        data = key.data
                        Save.saveFile(keybinds_filename, data)

                    has_changes = False
                    # print('Save keybinds') 

            if event.type == pygame.MOUSEBUTTONDOWN:
                if reset_keybinds.is_clicked(mouse_pos):
                    # print("Reset Key")
                    
                    temporary_list = []
                    for i in key.data:
                        temporary_list.append(key.data[i])
                    update_key_display(key_list, temporary_list)
                    new_key = temporary_list

            if event.type == pygame.MOUSEBUTTONDOWN:

                if keyswap_replace.is_clicked(mouse_pos):
                                # Check if True exists in detect and modal is open before proceeding
                                if True in detect and keyswap_modal.selected:
                                    display_keyswap_confirmation(False)
                                    indexed = key_store.index(key_name)
                                    detect_index = detect.index(True)
                                    temp = new_key[detect_index]
                                    new_key[detect_index] = (pygame.key.key_code(key_name), key_name)
                                    # Close the confirmation modal after successful key swap
                                    keyswap_modal.close_modal()

                                    if no_swap:
                                        new_key[indexed] = (200, " ")
                                    else:
                                        new_key[indexed] = temp
                                    for i in key_list:
                                        # print(i)
                                        i.is_switched(False, False)
                                    # Reset detect flags
                                    for idx in range(len(detect)):
                                        detect[idx] = False
                                    keybind_select_reset()
                                    has_changes = True
                                    update_key_display(key_list, new_key)
                                    can_click = True
                                    opacity = 0
                                    display_confirmation = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if keyswap_cancel.is_clicked(mouse_pos):
                    can_click = True
                    display_keyswap_confirmation(False)
                    opacity = 0
                    display_confirmation = False
                            



            detect = ([x for x in key.detect_key_skill.values()])
            if event.type == pygame.MOUSEBUTTONDOWN:
                # ([x for i,x in enumerate(key.detect_key_skill.values()) if i!= 0 ])
                
                if skill_1_btn_p1.is_clicked(event.pos) and can_click:
                    temp_value = not key.detect_key_skill['read_skill_1_p1']
                    refresh_key(key.detect_key_skill)
                    key.detect_key_skill['read_skill_1_p1'] = temp_value

                if skill_2_btn_p1.is_clicked(event.pos) and can_click:
                    temp_value = not key.detect_key_skill['read_skill_2_p1']
                    refresh_key(key.detect_key_skill)
                    key.detect_key_skill['read_skill_2_p1'] = temp_value

                if skill_3_btn_p1.is_clicked(event.pos) and can_click:
                    temp_value = not key.detect_key_skill['read_skill_3_p1']
                    refresh_key(key.detect_key_skill)
                    key.detect_key_skill['read_skill_3_p1'] = temp_value

                if skill_4_btn_p1.is_clicked(event.pos)and can_click:
                    temp_value = not key.detect_key_skill['read_skill_4_p1']
                    refresh_key(key.detect_key_skill)
                    key.detect_key_skill['read_skill_4_p1'] = temp_value

               


                if basic_atk_btn_p1.is_clicked(event.pos) and can_click:
                    temp_value = not key.detect_key_skill['read_basic_atk_p1']
                    refresh_key(key.detect_key_skill)
                    key.detect_key_skill['read_basic_atk_p1'] = temp_value

                if sp_skill_btn_p1.is_clicked(event.pos)and can_click:  
                    temp_value = not key.detect_key_skill['read_sp_skill_p1']  
                    refresh_key(key.detect_key_skill)            
                    key.detect_key_skill['read_sp_skill_p1'] = temp_value

                if jump_btn_p1.is_clicked(event.pos)and can_click:
                    temp_value = not key.detect_key_skill['read_jump_p1']
                    refresh_key(key.detect_key_skill)
                    key.detect_key_skill['read_jump_p1'] = temp_value
                if left_move_btn_p1.is_clicked(event.pos)and can_click:
                    temp_value = not key.detect_key_skill['read_left_move_p1']
                    refresh_key(key.detect_key_skill)
                    key.detect_key_skill['read_left_move_p1'] = temp_value

                if right_move_btn_p1.is_clicked(event.pos)and can_click:  
                    temp_value = not key.detect_key_skill['read_right_move_p1']     
                    refresh_key(key.detect_key_skill)           
                    key.detect_key_skill['read_right_move_p1'] = temp_value
                             #Player 2 settings

                if skill_1_btn_p2.is_clicked(event.pos)and can_click:
                    temp_value = not key.detect_key_skill['read_skill_1_p2']
                    refresh_key(key.detect_key_skill)
                    key.detect_key_skill['read_skill_1_p2'] = temp_value
                if skill_2_btn_p2.is_clicked(event.pos) and can_click:
                    temp_value = not key.detect_key_skill['read_skill_2_p2']
                    refresh_key(key.detect_key_skill)
                    key.detect_key_skill['read_skill_2_p2'] = temp_value
                if skill_3_btn_p2.is_clicked(event.pos) and can_click:
                    temp_value = not key.detect_key_skill['read_skill_3_p2']
                    refresh_key(key.detect_key_skill)
                    key.detect_key_skill['read_skill_3_p2'] = temp_value
                if skill_4_btn_p2.is_clicked(event.pos) and can_click:
                    temp_value = not key.detect_key_skill['read_skill_4_p2']
                    refresh_key(key.detect_key_skill)
                    key.detect_key_skill['read_skill_4_p2'] = temp_value
                if basic_atk_btn_p2.is_clicked(event.pos) and can_click:
                    temp_value = not key.detect_key_skill['read_basic_atk_p2']
                    refresh_key(key.detect_key_skill)
                    key.detect_key_skill['read_basic_atk_p2'] = temp_value

                if sp_skill_btn_p2.is_clicked(event.pos)and can_click:
                    temp_value = not key.detect_key_skill['read_sp_skill_p2']
                    refresh_key(key.detect_key_skill)
                    key.detect_key_skill['read_sp_skill_p2'] = temp_value
                if jump_btn_p2.is_clicked(event.pos) and can_click:
                    temp_value = not key.detect_key_skill['read_jump_p2']
                    refresh_key(key.detect_key_skill)
                    key.detect_key_skill['read_jump_p2'] = temp_value
                if left_move_btn_p2.is_clicked(event.pos) and can_click:
                    temp_value = not key.detect_key_skill['read_left_move_p2']
                    refresh_key(key.detect_key_skill)
                    key.detect_key_skill['read_left_move_p2'] = temp_value
                if right_move_btn_p2.is_clicked(event.pos)and can_click:
                    temp_value = not key.detect_key_skill['read_right_move_p2']
                    refresh_key(key.detect_key_skill)
                    key.detect_key_skill['read_right_move_p2'] = temp_value
    

        # print(type(keys))
            
            if any(detect):
                key_store = [x[1].upper() for x in new_key]
                for key_index in (key.status):
                    if keys[key_index] == True and can_click:
                        # print([x[1].upper() for x in new_key])
                        key_name = pygame.key.name(key_index).upper()
                        # if key_name == "UP":
                        #         key_name = "^"
                        # elif key_name == "DOWN":
                        #         key_name = r"\/"
                        # elif key_name  == "LEFT":
                        #         key_name = "<"
                        # elif key_name == "RIGHT":
                        #         key_name = ">"
                         
                        if key_name not in key_store:
                            
                        
                            # print(f"selected {pygame.key.name(key_index)}")
                            
                            
                            # print("has changes")
                            if True in detect:
                                detect_index = detect.index(True)
                                new_key[detect_index] = (key_index, key_name)
                                for i in key_list:
                                    # print(i)
                                    i.is_switched(False, False)
                                # Reset detect flags
                                for idx in range(len(detect)):
                                    detect[idx] = False
                                keybind_select_reset()
                                has_changes = True
                                update_key_display(key_list, new_key)
                        
                        else:
                            for index, item in enumerate(key.detect_key_skill):
                                if key.detect_key_skill[item] == True:
                                    if new_key[index][1] == key_name:
                                        keybind_select_reset()
                                        has_changes = True
                           
                                    else:
                                        draw_black_screen(0.5)
                                        # keyswap_modal.set_position((int(width * 0.5),int(height * 0.55)), False, True)
                                        keyswap_modal.open_modal()
                                        # print("watatas")
                                        display_confirmation = not True
                                        can_click = False
                                        opacity = 0.8
                                        
                       
                                    
                           
                        # break  # Remove to detect multiple
                    
                
                # for i in keys:
                #     if i in key.status:
                        
                    # for x,i in enumerate(keys):
                    #     if i == True:
                    #         print(x)
                        
        
        #------------------------
        #only load once because its so lag at game start
        if not load_green_bg:
            Animate_BG.green_bg.load_frames_type2()
            load_green_bg = True
        Animate_BG.green_bg.display(screen, speed=50)



        show_controls() #Show the controls in screen  




        keybinds.draw(screen, mouse_pos)

        reset_keybinds.draw(screen, mouse_pos)


        #functoinability
        skill_1_btn_p1.update(mouse_pos, key.detect_key_skill['read_skill_1_p1'])
        skill_2_btn_p1.update(mouse_pos, key.detect_key_skill['read_skill_2_p1'])
        skill_3_btn_p1.update(mouse_pos, key.detect_key_skill['read_skill_3_p1'])
        skill_4_btn_p1.update(mouse_pos, key.detect_key_skill['read_skill_4_p1'])


        basic_atk_btn_p1.update(mouse_pos, key.detect_key_skill['read_basic_atk_p1'])
        sp_skill_btn_p1.update(mouse_pos, key.detect_key_skill['read_sp_skill_p1'])

        jump_btn_p1.update(mouse_pos, key.detect_key_skill['read_jump_p1'])
        left_move_btn_p1.update(mouse_pos, key.detect_key_skill['read_left_move_p1'])
        right_move_btn_p1.update(mouse_pos, key.detect_key_skill['read_right_move_p1'])



        #Player 2 shesh


        skill_1_btn_p2.update(mouse_pos, key.detect_key_skill['read_skill_1_p2'])
        skill_2_btn_p2.update(mouse_pos, key.detect_key_skill['read_skill_2_p2'])
        skill_3_btn_p2.update(mouse_pos, key.detect_key_skill['read_skill_3_p2'])
        skill_4_btn_p2.update(mouse_pos, key.detect_key_skill['read_skill_4_p2'])


        basic_atk_btn_p2.update(mouse_pos, key.detect_key_skill['read_basic_atk_p2'])
        sp_skill_btn_p2.update(mouse_pos, key.detect_key_skill['read_sp_skill_p2'])

        jump_btn_p2.update(mouse_pos, key.detect_key_skill['read_jump_p2'])
        left_move_btn_p2.update(mouse_pos, key.detect_key_skill['read_left_move_p2'])
        right_move_btn_p2.update(mouse_pos, key.detect_key_skill['read_right_move_p2'])
        temp_button.update(mouse_pos, False)


        keyswap_cancel.update(mouse_pos, False)
        keyswap_replace.update(mouse_pos, False)




        

        #draw
        skill_1_btn_p1.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        skill_2_btn_p1.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        skill_3_btn_p1.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        skill_4_btn_p1.draw(screen, global_vars.TEXT_ANTI_ALIASING)

        basic_atk_btn_p1.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        sp_skill_btn_p1.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        jump_btn_p1.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        left_move_btn_p1.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        right_move_btn_p1.draw(screen, global_vars.TEXT_ANTI_ALIASING)



        skill_1_btn_p2.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        skill_2_btn_p2.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        skill_3_btn_p2.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        skill_4_btn_p2.draw(screen, global_vars.TEXT_ANTI_ALIASING)

        basic_atk_btn_p2.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        sp_skill_btn_p2.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        jump_btn_p2.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        left_move_btn_p2.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        right_move_btn_p2.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        # draw_black_screen(1)



        
        # skill_1_btn_p1.text = new_key[0][1]
        # skill_2_btn_p1.text = new_key[1][1]
        # skill_3_btn_p1.text = new_key[2][1]
        # skill_4_btn_p1.text = new_key[3][1]

        # basic_atk_btn_p1.text = new_key[4][1]
        # sp_skill_btn_p1.text = new_key[5][1]
        # jump_btn_p1.text = new_key[6][1]
        # left_move_btn_p1.text = new_key[7][1]
        # right_move_btn_p1.text = new_key[8][1]


        # skill_1_btn_p2.text = new_key[9][1]
        # skill_2_btn_p2.text = new_key[10][1]
        # skill_3_btn_p2.text = new_key[11][1]
        # skill_4_btn_p2.text = new_key[12][1]

        # basic_atk_btn_p2.text = new_key[13][1]
        # sp_skill_btn_p2.text = new_key[14][1]
        # jump_btn_p2.text = new_key[15][1]
        # left_move_btn_p2.text = new_key[16][1]
        # right_move_btn_p2.text = new_key[17][1]
        

        

        draw_black_screen(opacity)
        keyswap_modal.update(mouse_pos, mouse_press, None, max_selected=1)

        if display_confirmation:
            # print("display choice")
            display_keyswap_confirmation(True)
            
            
            # show_confirmation_modals()
            
            # print("Ni saka dapat ni")
        swapconfirm_yes.draw(screen, mouse_pos)
        swapconfirm_no.draw(screen, mouse_pos)



        if has_changes:
            
            save_before_exiting_modal()
            


#-------------------------------------END-----------------------------------------     



        
        # main.screen.blit(command_img, (0, 0))
        # main.screen.blit(control_img, (main.width/2, 0))
        menu_button.draw(screen, mouse_pos)

        pygame.display.update()
        main.clock.tick(main.FPS)


#-------------------------------------START-----------------------------------------


def update_key_display(key_list, new_key):
    
    for index,key in enumerate(key_list):
        key.text = display_inputs(new_key[index][1])




def keybind_select_reset(list_key:list=None):

    for detect_key in (key.detect_key_skill):
        # print(f"falsing {detect_key}")
        key.detect_key_skill[detect_key] = False
        



def refresh_key(list_key):
    for i in list_key:
        list_key[i] = False





def display_keyswap_confirmation(condition):
    if condition:
        swapconfirm_yes.hover_pos = ((width/2 + width*0.08),(height*0.6))
        swapconfirm_yes.rect = swapconfirm_yes.image.get_rect(center=((width/2 + width*0.08),(height*0.6)))

        swapconfirm_no.hover_pos = ((width/2 - width*0.08),(height*0.6))
        swapconfirm_no.rect = swapconfirm_no.image.get_rect(center=((width/2 - width*0.08),(height*0.6)))
    else:
        swapconfirm_yes.hover_pos = ((width/2 + width*0.08),(height*1.2))
        swapconfirm_yes.rect = swapconfirm_yes.image.get_rect(center=((width/2 + width*0.08),(height*1.2)))

        swapconfirm_no.hover_pos = ((width/2 - width*0.08),(height*1.2))
        swapconfirm_no.rect = swapconfirm_no.image.get_rect(center=((width/2 - width*0.08),(height*1.2)))




#---------------------------------------END-----------------------------------------













        


def info():
    hero_detail = main.pygame.transform.scale(
        pygame.image.load(resource_path('assets/hero info detail.png')).convert(), (main.width, main.height))
    hero_info = main.pygame.transform.scale(
        pygame.image.load(resource_path('assets/hero info dmg.png')).convert(), (main.width, main.height))

    next = ImageButton(
    image_path=text_box_img,
    pos=(main.width-80, 20),
    scale=0.75,
    text='Next',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=int(height * 0.02),  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)
    previous = ImageButton(
    image_path=text_box_img,
    pos=(main.width-80, 60),
    scale=0.75,
    text='previous',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=int(height * 0.02),  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)
    
    inffo = ImageButton(
    image_path=text_box_img,
    pos=(main.width-150, main.height/1.5),
    scale=0.75,
    text='burn damage = 5 for fire knight',
    font_path=r'assets\font\slkscr.ttf',  # or any other font path
    font_size=int(height * 0.015),  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)
    
    switch = False
    
    while True:
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        key_press = pygame.key.get_pressed()

        main.screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  
            if keys[pygame.K_ESCAPE]:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.is_clicked(event.pos):
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next.is_clicked(event.pos) and not switch:
                    switch = True
                    
                if previous.is_clicked(event.pos) and switch:
                    switch = False
                    
                
        if switch:
            main.screen.blit(hero_detail, (0, 0))
        else:
            main.screen.blit(hero_info, (0, 0))

        menu_button.draw(screen, mouse_pos)
        next.draw(screen, mouse_pos)
        previous.draw(screen, mouse_pos)
        inffo.draw(screen, mouse_pos) if switch else None

        pygame.display.update()
        main.clock.tick(main.FPS)


def main_menu():
    

    # background = main.pygame.transform.scale(
        # pygame.image.load(r'assets\backgrounds\8.png').convert(), (main.width, main.height))

    font = global_vars.get_font(100)
    default_size = ((main.width * main.DEFAULT_HEIGHT) / (main.height * main.DEFAULT_WIDTH))

    while True:
        # dev option
        if IMMEDIATE_RUN: # just a debug, does not matter anyway
            main.player_selection()
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        key_press = pygame.key.get_pressed()

        main.screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()   

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(event.pos):
                    return
            if keys[pygame.K_RETURN]:
                return
            if keys[pygame.K_KP_ENTER]:
                return

        # main.screen.blit(background, (0, 0))
        Animate_BG.dragon_bg.display(screen, speed=50)
        # Animate_BG.trees_bg.display(screen, speed=50)
        create_title('Fighting Kimhie', font, default_size, main.height * 0.2, color='Grey3')
        play_button.draw(main.screen, mouse_pos)

        pygame.display.update()
        main.clock.tick(main.FPS)

def reset_all():
    global fade_alpha, fading, fade_start_time, battle_result_recorded, winner
    global_vars.PAUSED = False
    global_vars.PAUSED_TOTAL_DURATION = 0
    global_vars.PAUSED_START = None
    battle_result_recorded = False  # Reset win tracking for new game
    winner = None  # Reset winner for new game
    # reset hero states
    heroes_to_reset = [x for x in main.hero1_group] + [x for x in main.hero2_group]
    if hasattr(main, 'hero3') and main.hero3 is not None:
        heroes_to_reset.append(main.hero3)
    for hero in heroes_to_reset:
        # clear public-style source sets (older code may use these)
        hero.freeze_sources = set()
        hero.root_sources = set()
        # clear internal status source lists used by `Player` methods
        try:
            hero._freeze_sources = []
        except Exception:
            pass
        try:
            hero._root_sources = []
        except Exception:
            pass
        try:
            hero._slow_sources = []
        except Exception:
            pass
        try:
            hero._silence_sources = []
        except Exception:
            pass

        # clear status flags; we will also call remove_movement_status to trigger any cleanup logic
        hero.frozen = False
        hero.rooted = False
        hero.stunned = False
        hero.slowed = False
        hero.silenced = False

        # Ensure symmetric removal (this clears derived state like speed_multiplier, atk_hasted, etc.)
        try:
            hero.remove_movement_status(1, source=None)
        except Exception:
            pass
        try:
            hero.remove_movement_status(2, source=None)
        except Exception:
            pass
        try:
            hero.remove_movement_status(3, source=None)
        except Exception:
            pass
        try:
            hero.remove_movement_status(4, source=None)
        except Exception:
            pass
        if hasattr(hero, 'atk_hasted'):
            # print('ahah')
            default_atk_speed_with_bonus = hero.get_atk_speed()
            hero.atk_hasted = False # removes the buff for forest ranger if possible
            hero.basic_attack_animation_speed = default_atk_speed_with_bonus
        if hasattr(hero, 'invisible'):
            hero.invisible = False
            hero.casting_invisible = False
            hero.invisible_duration = 0
        if hasattr(hero, 'flying'):
            hero.flying = False
            hero.flying_duration = 0
        hero.y_velocity = 0
        hero.x_velocity = 0
        hero.running = False
        hero.attacking1 = hero.attacking2 = hero.attacking3 = hero.sp_attacking = False
        hero.basic_attacking = hero.sp_attacking = False
        hero.special_active = False
        hero.animation_done = False

        for attack in hero.attacks:
            attack.reduce_cd(True)
        for attack in hero.attacks_special:
            attack.reduce_cd(True)
        
        hero.health = hero.max_health
        hero.mana = hero.max_mana
        hero.special = 0
        hero.temp_hp = hero.max_temp_hp
        if hasattr(hero, 'white_health_p1'):
            hero.white_health_p1 = hero.max_health
        if hasattr(hero, 'white_health_p2'):
            hero.white_health_p2 = hero.max_health

        if hasattr(hero, 'white_mana_p1'):
            hero.white_mana_p1 = hero.max_mana
        if hasattr(hero, 'white_mana_p2'):
            hero.white_mana_p2 = hero.max_mana

        hero.damage_numbers.clear()

        hero.x_pos = global_vars.X_POS_SPACING + random.randint(-20, 20) if hero.player_type == 1 else global_vars.DEFAULT_X_POS
        hero.y_pos = global_vars.DEFAULT_Y_POS
        
        hero.immortality_activated = False
        # Reset item cooldowns
        for item in hero.items:
            item.last_used = -item.cooldown if item.cooldown > 0 else 0
        
        # Reset bot-specific attributes to ensure proper restart
        if hasattr(hero, 'target'):
            hero.target = None  # Force re-target selection on next update
        if hasattr(hero, 'botkey_skill1'):
            # Reset all bot input keys
            hero.botkey_skill1 = hero.botkey_skill2 = hero.botkey_skill3 = hero.botkey_skill4 = False
            hero.botkey_right = hero.botkey_left = hero.botkey_jump = False
            hero.botkey_attack = False
            hero.botkey_special = False
            hero.forcemove_left = hero.forcemove_right = False
        if hasattr(hero, 'state'):
            hero.state = ''  # Reset bot state machine
        if hasattr(hero, 'attack_state'):
            hero.attack_state = ''
        
    attack_display.empty()

# NOTE: The mute button does not use this function
from button import RectButton
def settings(in_game=False):
    global paused
    
    font = global_vars.get_font(100)
    default_size = ((main.width * main.DEFAULT_HEIGHT) / (main.height * main.DEFAULT_WIDTH)) / 1.5
    
    setting_font = global_vars.get_font(int(height * 0.025))
    
    volume_clicked = False
    mute_hovered = False

    # ================================================================
    # ORGANIZED LAYOUT (matches the image perfectly)
    # ================================================================
    # 1. LEFT: MUTE + Volume slider (exactly where it appears in the image)
    volume_bar_x = width * 0.08          # left side
    volume_bar_y = height * 0.35

    volume_limit = {'min':100, 'max':300}
    current_volume = (global_vars.MAIN_VOLUME*100) + volume_limit['min']
    volume_button_rect = pygame.Rect(current_volume, volume_bar_y - 2, 13, 25)
    
    # Mute button (small square + label above, just like image)
    mute_rect = pygame.Rect(volume_bar_x - 65, volume_bar_y - 10, 40, 40)
    mute_clicked = global_vars.MUTE

    # Volume bar decor (black background bar)
    volume_bar_decor_rect = pygame.Rect(volume_bar_x - 5, volume_bar_y - 5,
                                        (volume_limit['max'] - volume_limit['min'] + 20), 30)

    # 2. CENTER UPPER: Hero bars (placed on the "bridge" area like in the image)
    hero_y = height * 0.48
    show_health_bar = RectButton(width * 0.30, hero_y,
                                 r'assets\font\slkscr.ttf', int(height * 0.025), (0, 255, 0), "Hero Health Bar")
    show_mana_bar = RectButton(width * 0.50, hero_y,
                               r'assets\font\slkscr.ttf', int(height * 0.025), (0, 255, 0), "Hero Mana Bar")
    show_special_bar = RectButton(width * 0.70, hero_y,
                                  r'assets\font\slkscr.ttf', int(height * 0.025), (0, 255, 0), "Hero Special Bar")

    # 3. BOTTOM ROW: All 5 toggle options (evenly spaced, exactly as in the image)
    bottom_y = height - height * 0.20
    anti_alias_button = RectButton(width * 0.10, bottom_y, r'assets\font\slkscr.ttf', int(height * 0.025), (0, 255, 0), "Text Anti-Aliasing")
    smooth_bg_button = RectButton(width * 0.28, bottom_y, r'assets\font\slkscr.ttf', int(height * 0.025), (0, 255, 0), "Smooth Background")
    show_distance_button = RectButton(width * 0.46, bottom_y, r'assets\font\slkscr.ttf', int(height * 0.025), (0, 255, 0), "Show Distance")
    show_hitbox_button = RectButton(width * 0.64, bottom_y, r'assets\font\slkscr.ttf', int(height * 0.025), (0, 255, 0), "Show Hitbox")
    # show_grid_button = RectButton(width * 0.82, bottom_y, r'assets\font\slkscr.ttf', int(height * 0.025), (0, 255, 0), "Show Grid (don't)")

    while True:
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        key_press = pygame.key.get_pressed()

        main.screen.fill((0, 0, 0))
        mute_hovered = mute_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()   

            if keys[pygame.K_ESCAPE]:
                # if not in_game:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.is_clicked(event.pos):
                    # if not in_game:
                    return
                
                # Mute toggle
                if mute_rect.collidepoint(event.pos):
                    mute_clicked = not mute_clicked
                    global_vars.MUTE = mute_clicked
                    pygame.mixer.music.set_volume(0 if global_vars.MUTE else global_vars.MAIN_VOLUME)
                
                # Volume drag start
                if volume_button_rect.collidepoint(event.pos):
                    volume_clicked = True

                # All toggle buttons
                if anti_alias_button.is_clicked(event.pos):
                    global_vars.TEXT_ANTI_ALIASING = anti_alias_button.toggle(global_vars.TEXT_ANTI_ALIASING)
                
                if smooth_bg_button.is_clicked(event.pos):
                    global_vars.SMOOTH_BG = smooth_bg_button.toggle(global_vars.SMOOTH_BG)
                
                if show_distance_button.is_clicked(event.pos):
                    global_vars.DRAW_DISTANCE = show_distance_button.toggle(global_vars.DRAW_DISTANCE)

                if show_hitbox_button.is_clicked(event.pos):
                    global_vars.SHOW_HITBOX = show_hitbox_button.toggle(global_vars.SHOW_HITBOX)

                # if show_grid_button.is_clicked(event.pos):
                #     global_vars.SHOW_GRID = show_grid_button.toggle(global_vars.SHOW_GRID)

                if show_health_bar.is_clicked(event.pos):
                    global_vars.SHOW_MINI_HEALTH_BAR = show_health_bar.toggle(global_vars.SHOW_MINI_HEALTH_BAR)

                if show_mana_bar.is_clicked(event.pos):
                    global_vars.SHOW_MINI_MANA_BAR = show_mana_bar.toggle(global_vars.SHOW_MINI_MANA_BAR)

                if show_special_bar.is_clicked(event.pos):
                    global_vars.SHOW_MINI_SPECIAL_BAR = show_special_bar.toggle(global_vars.SHOW_MINI_SPECIAL_BAR)

            elif event.type == pygame.MOUSEBUTTONUP:
                volume_clicked = False

        # ====================== VOLUME BAR LOGIC ======================
        volume_bar_rect = pygame.Rect(volume_bar_x, volume_bar_y, volume_button_rect.x - volume_bar_x, 20)

        if volume_clicked and not mute_clicked:
            volume_button_rect.x = mouse_pos[0]

        # Clamp volume slider
        if volume_button_rect.x >= volume_bar_x + (volume_limit['max'] - volume_limit['min']):
            volume_button_rect.x = volume_bar_x + (volume_limit['max'] - volume_limit['min'])
        elif volume_button_rect.x <= volume_bar_x:
            volume_button_rect.x = volume_bar_x

        # Calculate and apply volume
        global_vars.MAIN_VOLUME = ((volume_button_rect.x - volume_bar_x) / (volume_limit['max'] - volume_limit['min']))
        pygame.mixer.music.set_volume(0 if global_vars.MUTE else global_vars.MAIN_VOLUME)

        # ====================== BACKGROUND ======================
        Animate_BG.waterfall_rainy_bg.display(screen, speed=50) if not global_vars.SMOOTH_BG else Animate_BG.smooth_waterfall_rainy_bg.display(screen, speed=50)
        create_title('Settings', font, default_size, main.height * 0.2, color='Grey3')

        # ====================== MUTE BUTTON (small square) ======================
        mute_color = (0, 75, 0) if mute_hovered else (30, 30, 30)
        if mute_clicked:
            mute_color = (0, 150, 0)
        if mute_clicked and mute_hovered:
            mute_color = (0, 200, 0)
        pygame.draw.rect(screen, mute_color, mute_rect)

        # Mute label above the square (exactly like the image)
        mute_text = setting_font.render('MUTE', global_vars.TEXT_ANTI_ALIASING, white)
        mute_text_rect = mute_text.get_rect(center=(mute_rect.centerx, mute_rect.centery - mute_rect.height - 5))
        screen.blit(mute_text, mute_text_rect)

        # ====================== VOLUME BAR + PERCENTAGE ======================
        pygame.draw.rect(screen, black, volume_bar_decor_rect)
        pygame.draw.rect(screen, white if not mute_clicked else black, volume_bar_rect)
        pygame.draw.rect(screen, 'Red' if not mute_clicked else black, volume_button_rect)

        # Volume percentage
        vol_num_rect = pygame.Rect(volume_bar_x + (volume_limit['max'] - volume_limit['min']) + 30, volume_bar_y - 5, 60, 30)
        pygame.draw.rect(screen, black, vol_num_rect)
        vol_num = int(global_vars.MAIN_VOLUME * 100) if not mute_clicked else 0
        vol_num_font = global_vars.get_font(int(height * 0.025))
        vol_num_text = vol_num_font.render(f'{vol_num}%', global_vars.TEXT_ANTI_ALIASING, white)
        vol_num_text_rect = vol_num_text.get_rect(center=vol_num_rect.center)
        screen.blit(vol_num_text, vol_num_text_rect)

        # ====================== BUTTON UPDATES & DRAWING ======================
        # Hero bars (center upper)
        show_health_bar.update(mouse_pos, global_vars.SHOW_MINI_HEALTH_BAR)
        show_mana_bar.update(mouse_pos, global_vars.SHOW_MINI_MANA_BAR)
        show_special_bar.update(mouse_pos, global_vars.SHOW_MINI_SPECIAL_BAR)

        # Bottom row toggles
        anti_alias_button.update(mouse_pos, global_vars.TEXT_ANTI_ALIASING)
        smooth_bg_button.update(mouse_pos, global_vars.SMOOTH_BG)
        show_distance_button.update(mouse_pos, global_vars.DRAW_DISTANCE)
        show_hitbox_button.update(mouse_pos, global_vars.SHOW_HITBOX)
        # show_grid_button.update(mouse_pos, global_vars.SHOW_GRID)

        # Draw all buttons
        show_health_bar.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        show_mana_bar.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        show_special_bar.draw(screen, global_vars.TEXT_ANTI_ALIASING)

        anti_alias_button.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        smooth_bg_button.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        show_distance_button.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        show_hitbox_button.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        # show_grid_button.draw(screen, global_vars.TEXT_ANTI_ALIASING)

        menu_button.draw(screen, mouse_pos)

        pygame.display.update()
        main.clock.tick(main.FPS)



def show_dc_text(status=None, duration=5000):
    '''Self-contained "opponent left" notice. Shows for `duration` ms (or until
    the player presses ESC / clicks the menu button), then returns to the menu.
    Only meaningful when status == 'disconnected'.'''
    global load_sword_login_bg

    font = global_vars.get_font(60)
    status_start_time = pygame.time.get_ticks()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == main.pygame.QUIT:
                main.pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.is_clicked(event.pos):
                    return

        if not load_sword_login_bg:
            Animate_BG.sword_login.load_frames_type2()
            load_sword_login_bg = True
        Animate_BG.sword_login.display(screen, speed=10)

        create_title('lobby', font)
        if status == 'disconnected':
            create_timed_title('opponent left', status_start_time, duration, font, y_offset=150, color=red, scale=0.5)
            if pygame.time.get_ticks() - status_start_time >= duration:
                return

        menu_button.draw(screen, mouse_pos)

        main.pygame.display.update()
        main.clock.tick(main.FPS)


# Image Paths













if __name__ == '__main__':
    from heroes import lan_connect      
    main_menu()
    menu()




import math

class AnimationUtils:
    @staticmethod
    def shake(element, strength, duration, clock):
        """
        Shake an element (e.g., button or image) with configurable strength and duration.

        Args:
            element: The element to shake (must have a `rect` attribute).
            strength: The maximum offset for the shake.
            duration: The duration of the shake in milliseconds.
            clock: The pygame clock to manage time.
        """
        start_time = pygame.time.get_ticks()
        original_pos = element.rect.topleft

        while pygame.time.get_ticks() - start_time < duration:
            offset_x = random.randint(-strength, strength)
            offset_y = random.randint(-strength, strength)
            element.rect.topleft = (original_pos[0] + offset_x, original_pos[1] + offset_y)
            yield
            element.rect.topleft = original_pos

    @staticmethod
    def sine_wave_animation(start, end, speed, time):
        """
        Create a sine wave animation for smooth oscillation.

        Args:
            start: The starting value.
            end: The ending value.
            speed: The speed of the oscillation.
            time: The current time (e.g., pygame.time.get_ticks()).

        Returns:
            The current value based on the sine wave.
        """
        amplitude = (end - start) / 2
        midpoint = (end + start) / 2
        return midpoint + amplitude * math.sin(speed * time)

# Example usage of animations in the menu
def animate_button_hover(button, mouse_pos):
    """
    Animate button hover effect (e.g., scaling).

    Args:
        button: The button to animate.
        mouse_pos: The current mouse position.
    """
    if button.is_hovered(mouse_pos):
        button.scale = AnimationUtils.sine_wave_animation(0.8, 1.0, 0.005, pygame.time.get_ticks())
    else:
        button.scale = 0.8

# Add support for textured backgrounds
def set_background_texture(screen, texture_path):
    """
    Set a textured background for the game screen.

    Args:
        screen: The pygame screen object.
        texture_path: The file path to the texture image.
    """
    texture = pygame.image.load(texture_path)
    texture = pygame.transform.scale(texture, screen.get_size())
    screen.blit(texture, (0, 0))

# Example usage in the game loop
# Replace the plain color background with a texture
background_texture_path = resource_path('assets/black sand.jpg')  # Replace with your texture file
# set_background_texture(screen, background_texture_path)

# Add animations for elements entering the screen
def animate_element_entry(element, start_pos, end_pos, speed):
    """
    Animate an element entering the screen from a start position to an end position.

    Args:
        element: The element to animate (must have a `rect` attribute).
        start_pos: The starting position (x, y).
        end_pos: The ending position (x, y).
        speed: The speed of the animation.
    """
    element.rect.topleft = start_pos
    while element.rect.topleft != end_pos:
        current_x, current_y = element.rect.topleft
        target_x, target_y = end_pos
        new_x = current_x + (target_x - current_x) * speed
        new_y = current_y + (target_y - current_y) * speed
        element.rect.topleft = (int(new_x), int(new_y))
        yield

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

# Example usage:
# To use the new font, call the `load_font` function with the desired path and size.
# Example:
# new_font = load_font('path/to/your/font.ttf', 30)
# if new_font:
#     text_surface = new_font.render('Your Text Here', True, (255, 255, 255))
#     screen.blit(text_surface, (x, y