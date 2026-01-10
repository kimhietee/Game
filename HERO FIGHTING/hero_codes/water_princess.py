from global_vars import (IMMEDIATE_RUN,
    width, height, icon, FPS, clock, screen, hero1, hero2, fire_wizard_icon, wanderer_magician_icon, fire_knight_icon, wind_hashashin_icon, water_princess_icon, forest_ranger_icon, yurei_icon,
    white, red, black, green, cyan2, gold, play_button_img, text_box_img, loading_button_img, menu_button_img,
    waterfall_icon, lava_icon, dark_forest_icon, trees_icon, 
    DEFAULT_WIDTH, DEFAULT_HEIGHT, scale, center_pos, font_size, BASIC_ATK_COOLDOWN, BASIC_FRAME_DURATION, BASIC_ATK_DAMAGE, BASIC_ATK_DAMAGE2, BASIC_ATK_DAMAGE3, BASIC_ATK_DAMAGE4,
    DISABLE_HEAL_REGEN, DEFAULT_HEALTH_REGENERATION, DEFAULT_MANA_REGENERATION, BASIC_ATK_POSX, BASIC_ATK_POSX_END, BASIC_ATK_POSY, SPECIAL_MULTIPLIER, MAX_SPECIAL, SPECIAL_DURATION, DISABLE_SPECIAL_REDUCE,
    LOW_HP, LITERAL_HEALTH_DEAD, SINGLE_MODE_ACTIVE, SHOW_HITBOX, DRAW_DISTANCE,
    DEFAULT_CHAR_SIZE, DEFAULT_CHAR_SIZE_2, DEFAULT_ANIMATION_SPEED, DEFAULT_ANIMATION_SPEED_FOR_JUMPING,
    JUMP_DELAY, RUNNING_SPEED, RUNNING_ANIMATION_SPEED, DEFAULT_BASIC_ATK_DMG_BONUS,
    X_POS_SPACING, DEFAULT_X_POS, DEFAULT_Y_POS, SPACING_X, START_OFFSET_X, SKILL_Y_OFFSET,
    ICON_WIDTH, ICON_HEIGHT, MAX_ITEM,
    DEFAULT_GRAVITY, DEFAULT_JUMP_FORCE, JUMP_LOGIC_EXECUTE_ANIMATION,
    WHITE_BAR_SPEED_HP, WHITE_BAR_SPEED_MANA, TEXT_DISTANCE_BETWEEN_STATUS_AND_TEXT,
    PLAYER_1, PLAYER_2, PLAYER_1_SELECTED_HERO, PLAYER_2_SELECTED_HERO, PLAYER_1_ICON, PLAYER_2_ICON,
    DISABLE_MANA_REGEN,
    attack_display, MULT, dmg_mult,

    ZERO_WIDTH, TOTAL_WIDTH
)
from heroes import Attacks, Attack_Display
from sprite_loader import load_attack, load_attack_flipped
from player import Player
import global_vars
import pygame
# Animation Counts
# WATER_PRINCESS_BASIC_COUNT = 
WATER_PRINCESS_JUMP_COUNT = 6
WATER_PRINCESS_RUN_COUNT = 10
WATER_PRINCESS_IDLE_COUNT = 8
WATER_PRINCESS_ATK1_COUNT = 7
WATER_PRINCESS_ATK2_COUNT = 27
WATER_PRINCESS_ATK3_COUNT = 12
WATER_PRINCESS_SP_COUNT = 32
WATER_PRINCESS_DEATH_COUNT = 16

WATER_PRINCESS_SURF_COUNT = 8

# WATER_PRINCESS_ATK1 = 0
# WATER_PRINCESS_ATK2 = 0
# WATER_PRINCESS_ATK3 = 0
# WATER_PRINCESS_SP = 0
# ---------------------
# print((WATER_PRINCESS_ATK2 * 0.01) * 4 * 5)

WATER_PRINCESS_ATK1_SIZE = 2
WATER_PRINCESS_ATK2_SIZE = 2
WATER_PRINCESS_ATK3_SIZE = 1
WATER_PRINCESS_SP_SIZE = 4  


class Water_Princess(Player):
    def __init__(self, player_type, enemy):
        super().__init__(player_type, enemy)
        # self.display_text = Display_Text(self.x_pos, self.y_pos, self.health)

        self.player_type = player_type
        self.name = "Water Princess"

        self.hitbox_rect = pygame.Rect(0, 0, 50, 100)

        # stat
        self.strength = 38 
        self.intelligence = 48
        self.agility = 20 # real agility = 20

        #base attack instances
        self.atk_instance = [1.5, 1.0, 5.0] #multiplier for basic attacks # TOTAL ATTACK DMG = 15.0
        # 1st atk = 2.0*1.5 = 3
        # 2nd atk = 2.0 = 2
        # 3rd atk = 2.0 * 5 = 10
        

        #special attack instances
        sp_mult_atk = 1.2
        self.special_instance = [1.5 * sp_mult_atk, 1.0 * sp_mult_atk, 5.0 * sp_mult_atk] #multiplier for basic attacks
        # 1st atk = 2.0*1.8 = 3.6
        # 2nd atk = 2.0 *1.2= 2.4
        # 3rd atk = 2.0 * 6 = 12

        
        self.base_health_regen = 0.8 # 1.2
        self.base_mana_regen = 6.05 # 6.53
        self.base_attack_damage = 0.0 # 2.0

        self.base_attack_speed = 60
        self.base_attack_time = 3700

        self.base_animation_speed = 120
        self.min_animation_speed = 80
        self.attack_speed_modifier = 0.4

        self.health_regen = self.calculate_regen(self.base_health_regen, self.hp_regen_per_str, self.strength) #0.8 + 40 * 0.01 = 1.2
        self.mana_regen = self.calculate_regen(self.base_mana_regen, self.mana_regen_per_int, self.intelligence) #6.05 + 48 * 0.01 = 6.53
        self.basic_attack_damage = self.calculate_regen(self.base_attack_damage, self.agi_mult, self.agility, basic_attack=True) # 0.0 + 20 * 0.1 = 2.0

        # Recalculate attack speed variables for fire wizard's base stats
        self.attack_speed = self.calculate_effective_as()
        self.basic_attack_cooldown = self.calculate_basic_attack_interval()
        self.basic_attack_animation_speed = self.calculate_attack_animation_speed()

        # Base Stats
        self.max_health = (self.strength * self.str_mult)
        self.max_mana = (self.intelligence * self.int_mult)
        self.health = self.max_health
        self.mana = self.max_mana

        # self.basic_atk1_dmg = self.basic_attack_damage*5
        # self.basic_atk2_dmg = self.basic_attack_damage*1.5

        # Player Position
        self.x = 50
        self.y = 50
        self.width = 200

        # SPECIAL TRAIT
            # Mana cost delayed
            # Mana cast high, but mana cost delay reduced by 15%
            #example:
            # if mana cost is 160, reduce mama until end of attack frame, 
            # but that 160 is reduced by 15%
            # total mana depleted = (160*0.85 or 160-(160*0.15)) = 136 total mana cost

            # mana reduce 20% if special active



        self.atk1_mana_cost = 80
        self.atk2_mana_cost = 160
        self.atk3_mana_cost = 200
        self.sp_mana_cost = 240

        #go to attacks section to calculate mana

        self.atk1_cooldown = 10000
        self.atk2_cooldown = 26000
        self.atk3_cooldown = 40000
        self.sp_cooldown = 65000

        self.atk1_damage = (10/40, 0)
        self.atk1_damage_2nd = 20 #-----
        self.atk2_damage = (12.5/40, 0) # total dmg 40 #rain
        self.atk2_damage_2nd = (3/40, 5) #circling
        self.atk3_damage = (15/25, 0) 
        self.atk3_damage_2nd = 20 #-----

        self.sp_damage = (20/35, 0) 
        self.sp_damage_2nd = (10/42, 20) 
        self.sp_damage_3rd = (10/15, 0) #-----

        self.sp_atk1_damage = 0.2 # (5/25, 0) #-----
        self.sp_atk2_damage = 0.3#(totaldmg 9*2=18) # =0.4166 (12.5/30, 0) # rain #-----
        self.sp_atk2_damage_2nd = (5/30, 2) #(*5) #circling #------
        self.sp_atk2_damage_3rd = (2/15, 5) #(*10) #watershot #-----
        self.sp_atk3_damage = (15/20, 0) #10+(15*2)= #-----
        # sp_atk3 heal = 20/2:instant=10, 
        # dmg_mult = 0
        # self.atk1_damage = self.atk1_damage[0] + (self.atk1_damage[0] * dmg_mult), self.atk1_damage[1] + (self.atk1_damage[1] * dmg_mult)
        # self.atk2_damage = self.atk2_damage[0] + (self.atk2_damage[0] * dmg_mult), self.atk2_damage[1] + (self.atk2_damage[1] * dmg_mult)
        # self.atk3_damage = self.atk3_damage[0] + (self.atk3_damage[0] * dmg_mult), self.atk3_damage[1] + (self.atk3_damage[1] * dmg_mult)
        # self.sp_damage = self.sp_damage[0] + (self.sp_damage[0] * dmg_mult), self.sp_damage[1] + (self.sp_damage[1] * dmg_mult)
        
        self.player_surf_index = 0
        self.player_surf_index_flipped = 0

        self.player_atk1_2nd_index = 0
        self.player_atk1_2nd_index_flipped = 0
        
        # Player Animation Source
        basic_ani = [r'assets\characters\Water princess\png\08_2_atk\2_atk_', 21, 0]
        atk1_ani_2nd = [r'assets\characters\Water princess\png\12_defend\defend_', 12, 0]

        jump_ani = [r'assets\characters\Water princess\png\04_j_up\j_up_', WATER_PRINCESS_JUMP_COUNT, 0]
        run_ani = [r'assets\characters\Water princess\png\02_walk\walk_', WATER_PRINCESS_RUN_COUNT, 0]

        surf_ani = [r'assets\characters\Water princess\png\03_surf\surf_', WATER_PRINCESS_SURF_COUNT, 0]

        idle_ani = [r'assets\characters\Water princess\png\01_idle\idle_', WATER_PRINCESS_IDLE_COUNT, 0]
        atk1_ani = [r'assets\characters\Water princess\png\07_1_atk\1_atk_', WATER_PRINCESS_ATK1_COUNT, 0]
        atk2_ani = [r'assets\characters\Water princess\png\09_3_atk\3_atk_', WATER_PRINCESS_ATK2_COUNT, 0]
        atk3_ani = [r'assets\characters\Water princess\png\11_heal\heal_', WATER_PRINCESS_ATK3_COUNT, 0]
        sp_ani = [r'assets\characters\Water princess\png\10_sp_atk\sp_atk_', WATER_PRINCESS_SP_COUNT, 0]
        death_ani = [r'assets\characters\Water princess\png\14_death\death_', WATER_PRINCESS_DEATH_COUNT, 0]

        # Player Skill Sounds Effects Source
        self.atk1_sound = pygame.mixer.Sound(r'assets\sound effects\water princess\water-splash-short.mp3') # hit water
        self.atk2_sound = pygame.mixer.Sound(r'assets\sound effects\water princess\water-flowing-sound-.mp3') # flowing water
        self.atk3_sound = pygame.mixer.Sound(r'assets\sound effects\water princess\drop splash water.mp3') # bubbles
        self.sp_sound = pygame.mixer.Sound(r'assets\sound effects\water princess\ice-freezing-sequences-02-116786.mp3') #freeze

        self.sound_1 = pygame.mixer.Sound(r'assets\sound effects\water princess\water-splash-deep.mp3') # splash deep
        self.sound_2 = pygame.mixer.Sound(r'assets\sound effects\water princess\water-stream.mp3') # stream
        self.sound_3 = pygame.mixer.Sound(r'assets\sound effects\water princess\water-splash-02-352021.mp3') # splash flowing deep

        self.atk1_sound.set_volume(0.8 * global_vars.MAIN_VOLUME)
        self.atk2_sound.set_volume(0.7 * global_vars.MAIN_VOLUME)
        self.atk3_sound.set_volume(0.4 * global_vars.MAIN_VOLUME)
        self.sp_sound.set_volume(0.9 * global_vars.MAIN_VOLUME)
        
        self.sound_1.set_volume(0.7 * global_vars.MAIN_VOLUME)
        self.sound_2.set_volume(0.7 * global_vars.MAIN_VOLUME)
        self.sound_2.set_volume(0.6 * global_vars.MAIN_VOLUME)

        # Player Skill Animations Source
        # atk1 = [r'', WATER_PRINCESS_ATK1, 1]
        # atk2 = [r', WATER_PRINCESS_ATK2, 1]
        # atk3 = [r'HERO FIGHTING\assets\attacks\fire knight\atk3\png_', WATER_PRINCESS_ATK3, 1]
        # sp = [r'HERO FIGHTING\assets\attacks\fire knight\sp atk', WATER_PRINCESS_SP, 1]

        # Player Skill Icons Source
        skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\water_princess\472234276_8613137162147060_446401069957588690_n.jpeg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_2 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\water_princess\tumblr_8ca04de6143efee03f34ea8c32aca437_a117ed18_1280.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\water_princess\Screenshot 2025-01-26 221227.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\water_princess\Untitled (1 x 1 in).png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_icon = pygame.transform.scale(pygame.image.load(r'assets\skill icons\water_princess\placeholder.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        special_skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\water_princess\472234276_8613137162147060_446401069957588690_n.jpeg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_2 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\water_princess\tumblr_8ca04de6143efee03f34ea8c32aca437_a117ed18_1280.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\water_princess\Screenshot 2025-01-26 221227.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\water_princess\Untitled (1 x 1 in).png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        # Player Icon Rects
        if self.player_type == 1:
            self.skill_1_rect = skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))

            self.special_rect = special_icon.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 4 + 50, SKILL_Y_OFFSET))

            self.special_skill_1_rect = special_skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.special_skill_2_rect = special_skill_2.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.special_skill_3_rect = special_skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.special_skill_4_rect = special_skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))

        elif self.player_type == 2:
            self.special_rect = special_icon.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 4 - 50, SKILL_Y_OFFSET))

            self.special_skill_1_rect = special_skill_1.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 3, SKILL_Y_OFFSET))
            self.special_skill_2_rect = special_skill_2.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 2, SKILL_Y_OFFSET))
            self.special_skill_3_rect = special_skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X, SKILL_Y_OFFSET))
            self.special_skill_4_rect = special_skill_4.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X, SKILL_Y_OFFSET))

            self.skill_1_rect = skill_1.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 3, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X, SKILL_Y_OFFSET))

        # Player Attack Animations Load
        self.atk1 = load_attack( # rain
        filepath=r"assets\attacks\water princess\1.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=8, 
        columns=5, 
        scale=WATER_PRINCESS_ATK1_SIZE, 
        rotation=0,
    )
        self.atk2 = load_attack( #circling water
        filepath=r"assets\attacks\water princess\2.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=8, 
        columns=5, 
        scale=WATER_PRINCESS_ATK2_SIZE, 
        rotation=0,
    )
        self.atk2_rain = load_attack(
        filepath=r"assets\attacks\water princess\1.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=8, 
        columns=5, 
        scale=6, 
        rotation=-45,
    )
        self.atk2_rain_flipped = load_attack(
        filepath=r"assets\attacks\water princess\1.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=8, 
        columns=5, 
        scale=6, 
        rotation=45,
    )
        
        self.atk3 = load_attack( # healing frames
        filepath=r"assets\attacks\water princess\3.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=5, 
        columns=5, 
        scale=WATER_PRINCESS_ATK3_SIZE, 
        rotation=0,
    )
        
        self.sp = load_attack( # bubbles
        filepath=r"assets\attacks\water princess\4.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=7, 
        columns=5, 
        scale=WATER_PRINCESS_SP_SIZE, 
        rotation=0,
    )
        
        self.watershot = load_attack(
        filepath=r"assets\attacks\water princess\watershot.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=3 , 
        columns=5, 
        scale=1, 
        rotation=0,
    )
        self.watershot_flipped = load_attack_flipped(
        filepath=r"assets\attacks\water princess\watershot.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=3 , 
        columns=5, 
        scale=1, 
        rotation=0,
    )
        

        self.sp_atk1 = load_attack(
        filepath=r"assets\attacks\water princess\sp_atk1.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=5, 
        columns=5, 
        scale=1.5, 
        rotation=0,
    )
        self.sp_atk2 = load_attack(
        filepath=r"assets\attacks\water princess\sp_atk2.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=6, 
        columns=5, 
        scale=2, 
        rotation=0,
    )
        self.sp_atk3 = load_attack(
        filepath=r"assets\attacks\water princess\sp_atk3.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=4, 
        columns=5, 
        scale=1.2, 
        rotation=0,
    )
        self.sp_atk4 = load_attack(
        filepath=r"assets\attacks\water princess\sp_atk4.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=7, 
        columns=5, 
        scale=4, 
        rotation=0,
    )
    
        # assets\attacks\water princess\basic_atk1\water60000
        # assets\attacks\water princess\atk4\splash big\water400
        self.sp1 = self.load_img_frames_numbering_method_simple(r"assets\attacks\water princess\atk4\spiral\water900", 42, starts_at_zero=True,
        size=0.2)

        self.sp2 = self.load_img_frames_numbering_method_simple(r"assets\attacks\water princess\atk4\splash big\water400", 16, starts_at_zero=True,
        size=0.3)

        self.basic_atk1 = self.load_img_frames_numbering_method_simple(r"assets\attacks\water princess\basic_atk1\water600", 12, starts_at_zero=True,
        rotate=90, size=0.15)

        self.basic_atk1_flipped = self.load_img_frames_numbering_method_simple(r"assets\attacks\water princess\basic_atk1\water600", 12, starts_at_zero=True,
        rotate=-90, flip=True, size=0.15)

        self.basic_atk2 = self.load_img_frames_numbering_method_simple(r"assets\attacks\water princess\basic_atk2\water5_", 31, starts_at_zero=True,
        size=0.5, flip=True)

        self.basic_atk2_flipped = self.load_img_frames_numbering_method_simple(r"assets\attacks\water princess\basic_atk2\water5_", 31, starts_at_zero=True,
        size=0.6)
# (fr'{folder}{str(frame_number).zfill(2)}.png')

        
    

        # Player Animations Load
        self.player_basic = self.load_img_frames(basic_ani[0], basic_ani[1], basic_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_basic_flipped = self.load_img_frames_flipped(basic_ani[0], basic_ani[1], basic_ani[2], DEFAULT_CHAR_SIZE_2)

        self.player_jump = self.load_img_frames(jump_ani[0], jump_ani[1], jump_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_jump_flipped = self.load_img_frames_flipped(jump_ani[0], jump_ani[1], jump_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_idle = self.load_img_frames(idle_ani[0], idle_ani[1], idle_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_idle_flipped = self.load_img_frames_flipped(idle_ani[0], idle_ani[1], idle_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_run = self.load_img_frames(run_ani[0], run_ani[1], run_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_run_flipped = self.load_img_frames_flipped(run_ani[0], run_ani[1], run_ani[2], DEFAULT_CHAR_SIZE_2)  

        self.player_surf = self.load_img_frames(surf_ani[0], surf_ani[1], surf_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_surf_flipped = self.load_img_frames_flipped(surf_ani[0], surf_ani[1], surf_ani[2], DEFAULT_CHAR_SIZE_2)

        self.player_atk1_2nd = self.load_img_frames(atk1_ani_2nd[0], atk1_ani_2nd[1], atk1_ani_2nd[2], DEFAULT_CHAR_SIZE_2)
        self.player_atk1_2nd_flipped = self.load_img_frames_flipped(atk1_ani_2nd[0], atk1_ani_2nd[1], atk1_ani_2nd[2], DEFAULT_CHAR_SIZE_2)

        self.player_atk1 = self.load_img_frames(atk1_ani[0], atk1_ani[1], atk1_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_atk1_flipped = self.load_img_frames_flipped(atk1_ani[0], atk1_ani[1], atk1_ani[2], DEFAULT_CHAR_SIZE_2)  
        self.player_atk2 = self.load_img_frames(atk2_ani[0], atk2_ani[1], atk2_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_atk2_flipped = self.load_img_frames_flipped(atk2_ani[0], atk2_ani[1], atk2_ani[2], DEFAULT_CHAR_SIZE_2)  
        self.player_atk3 = self.load_img_frames(atk3_ani[0], atk3_ani[1], atk3_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_atk3_flipped = self.load_img_frames_flipped(atk3_ani[0], atk3_ani[1], atk3_ani[2], DEFAULT_CHAR_SIZE_2)  
        self.player_sp = self.load_img_frames(sp_ani[0], sp_ani[1], sp_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_sp_flipped = self.load_img_frames_flipped(sp_ani[0], sp_ani[1], sp_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_death = self.load_img_frames(death_ani[0], death_ani[1], death_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_death_flipped = self.load_img_frames_flipped(death_ani[0], death_ani[1], death_ani[2], DEFAULT_CHAR_SIZE_2)

        # Player Image and Rect
        self.image = self.player_idle[self.player_idle_index]
        self.rect = self.image.get_rect(midbottom = (self.x_pos, self.y_pos)) #(for p1)
        
        # Mana Values
        self.mana_cost_list = [
            self.atk1_mana_cost,
            self.atk2_mana_cost,
            self.atk3_mana_cost,
            self.sp_mana_cost
            ]

        # Modify
        self.lowest_mana_cost = self.mana_cost_list[0]

        

        # Skills
        self.attacks = [
            Attacks(
                mana_cost=self.mana_cost_list[0],
                skill_rect=self.skill_1_rect,
                skill_img=skill_1,
                cooldown=self.atk1_cooldown,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[1],
                skill_rect=self.skill_2_rect,
                skill_img=skill_2,
                cooldown=self.atk2_cooldown,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[2],
                skill_rect=self.skill_3_rect,
                skill_img=skill_3,
                cooldown=self.atk3_cooldown,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[3],
                skill_rect=self.skill_4_rect,
                skill_img=skill_4,
                cooldown=self.sp_cooldown,
                mana=self.mana
            )
        ]

        self.attacks.append(
            Attacks(
                mana_cost=0,
                skill_rect=self.basic_icon_rect,
                skill_img=self.basic_icon,
                cooldown=self.basic_attack_cooldown,
                mana=self.mana
            )
        )

        self.attacks.append(
            Attacks(
                mana_cost=0,
                skill_rect=self.special_rect,
                skill_img=special_icon,
                cooldown=0,
                mana=0,
                special_skill=True
            )
        )

        
        

        #special
        self.attacks_special = [
            Attacks(
                mana_cost=self.mana_cost_list[0],
                skill_rect=self.special_skill_1_rect,
                skill_img=special_skill_1,
                cooldown=self.atk1_cooldown,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[1],
                skill_rect=self.special_skill_2_rect,
                skill_img=skill_2,
                cooldown=self.atk2_cooldown,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[2],
                skill_rect=self.special_skill_3_rect,
                skill_img=special_skill_3,
                cooldown=self.atk3_cooldown,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[3],
                skill_rect=self.special_skill_4_rect,
                skill_img=special_skill_4,
                cooldown=self.sp_cooldown,
                mana=self.mana
            )
        ]

        self.attacks_special.append(
            Attacks(
                mana_cost=0,
                skill_rect=self.basic_icon_rect,
                skill_img=self.basic_icon,
                cooldown=self.basic_attack_cooldown,
                mana=self.mana
            )
        )

        # Regen Rate
        self.hp_regen_rate = DEFAULT_HEALTH_REGENERATION # Health regeneration rate per frame
        self.mana_regen_rate = DEFAULT_MANA_REGENERATION  # Mana regeneration rate per frame

        # After Bar Reduces
        self.white_health_p1 = self.health
        self.white_mana_p1 = self.mana   
        self.white_health_p2 = self.health
        self.white_mana_p2 = self.mana  


        
        # make sure the divisor aligned with how many frames the attack is, 
        # (you can refer to the dmg since they are the same)
        # print(self.attacks[0].mana_cost)
        '''the calculations are correct, must test with mana_reduce items'''
        '''calculated mana is not correct, need to update correct values to apply mana_reduce items'''
        '''refer to the new function below'''

        '''good, the values are now correct.'''

        self.mana_mult =0 
        self.atk1_mana_consume = 0
        self.atk2_mana_consume = 0
        self.atk3_mana_consume = 0
        self.atk4_mana_consume = 0
        self.atk1_special_mana_consume = 0
        self.atk2_special_mana_consume = 0
        self.atk3_special_mana_consume = 0
        self.atk4_special_mana_consume = 0

    def draw_movement_status(self, screen, display=True):
        super().draw_movement_status(screen, display)

    def update_mana_values(self):
        self.mana_mult = 0.2 if not self.special_active else 0.25
        self.atk1_mana_consume = (self.attacks[0].mana_cost/40) - ((self.attacks[0].mana_cost/40)*self.mana_mult)
        self.atk2_mana_consume = (self.attacks[1].mana_cost/40) - ((self.attacks[1].mana_cost/40)*self.mana_mult)
        self.atk3_mana_consume = (self.attacks[2].mana_cost/25) - ((self.attacks[2].mana_cost/25)*self.mana_mult)
        self.atk4_mana_consume = (self.attacks[3].mana_cost/35) - ((self.attacks[3].mana_cost/35)*self.mana_mult)

        self.atk1_special_mana_consume = (self.attacks_special[0].mana_cost/25) - ((self.attacks_special[0].mana_cost/25)*self.mana_mult)
        self.atk2_special_mana_consume = (self.attacks[1].mana_cost/40) - ((self.attacks[1].mana_cost/40)*self.mana_mult)
        self.atk3_special_mana_consume = (self.attacks[2].mana_cost/25) - ((self.attacks[2].mana_cost/25)*self.mana_mult)
        self.atk4_special_mana_consume = (self.attacks[3].mana_cost/35) - ((self.attacks[3].mana_cost/35)*self.mana_mult)
    
    def input(self, hotkey1, hotkey2, hotkey3, hotkey4, right_hotkey, left_hotkey, jump_hotkey, basic_hotkey, special_hotkey):
        """The most crucial part of collecting user input.
        - Processes player input each frame, handling movement and skill casting based on state."""
        # ---------- Core ----------        
        self.keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if self.is_dead():
            return
        
        # ---------- Moving ----------
        if self.can_move():
            self.player_movement(right_hotkey, left_hotkey, jump_hotkey, current_time,
                speed_modifier = -0.075,
                special_active_speed = 0.4,
                jump_force = self.jump_force,
                jump_force_modifier = -0.05
                )
            
        # ---------- Casting ----------
        if self.is_frozen():
            return
        
        if self.is_silenced() and not basic_hotkey:
            return
        
        if not self.special_active:
            if not self.jumping and not self.is_dead():
                if hotkey1 and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >= self.attacks[0].mana_cost and self.attacks[0].is_ready():
                        for i in [
                            (80, 40, 100, self.atk1_damage[0], self.atk1_damage[1], self.atk1_sound, False, 0.4, 0.4, True, True, True, True, (self.atk1, self.atk1)),
                            (70, 80, 100, self.atk1_damage_2nd, 0, self.atk2_sound, True, 0.7, 0.6, False, False, False, False, (self.basic_slash, self.basic_slash_flipped)) # this is so inefficient
                        ]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i[0] if self.facing_right else self.rect.centerx -i[0],
                                y=self.rect.centery + i[1],
                                frames=i[13][0] if self.facing_right else i[13][1],
                                frame_duration=i[2],
                                repeat_animation=1,
                                speed=0,
                                dmg=i[3],
                                final_dmg=i[4],
                                who_attacks=self,
                                who_attacked=self.enemy,
                                delay=(True, self.basic_attack_animation_speed * (300 / self.base_animation_speed)), # self.basic_attack_animation_speed * (Base Delay/Base Animation Speed)
                                sound=(True, i[5], None, None),

                                moving=i[6],
                                hitbox_scale_x=i[7],
                                hitbox_scale_y=i[8],

                                heal=i[9],
                                heal_enemy=i[10],

                                continuous_dmg=i[11],

                                consume_mana=[i[12], self.atk1_mana_consume]

                            )
                            attack_display.add(attack)

                        
                        
                        # self.mana -= self.attacks[0].mana_cost
                        self.attacks[0].last_used_time = current_time
                        self.running = False
                        self.attacking1 = True
                        self.player_atk1_index = 0
                        self.player_atk1_index_flipped = 0
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 1 used')


                elif hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >= self.attacks[1].mana_cost and self.attacks[1].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        for i in [(300,True), (1000,False)]: # WATER RAIN
                            attack = Attack_Display(
                                x=self.rect.centerx + 350 if self.facing_right else self.rect.centerx -350,
                                y=self.rect.centery,
                                frames=self.atk2_rain if self.facing_right else self.atk2_rain_flipped,
                                frame_duration=80,
                                repeat_animation=1,
                                speed=0,
                                dmg=self.atk2_damage[0],
                                final_dmg=self.atk2_damage[1],
                                who_attacks=self,
                                who_attacked=self.enemy,
                                moving=False,
                                delay=(True, i[0]),
                                sound=(i[1], self.atk2_sound, self.sound_2, None),
                                hitbox_scale_x=0.4
                                ,hitbox_scale_y=0.4,
                                consume_mana=[i[1], self.atk2_mana_consume]
                                ) # Replace with the target
                            attack_display.add(attack)

                        for i in [(300,170), (800, 340), (1300,0), (1800, 680), (2300, 510)]:
                            attack = Attack_Display( # CIRCLING WATERS
                                x=self.rect.centerx + i[1] if self.facing_right else self.rect.centerx -i[1],
                                y=self.rect.centery + 50,
                                frames=self.atk2,
                                frame_duration=80,
                                repeat_animation=1,
                                speed=0,
                                dmg=self.atk2_damage_2nd[0],
                                final_dmg=self.atk2_damage_2nd[1],
                                who_attacks=self,
                                who_attacked=self.enemy,
                                moving=False,
                                delay=(True, i[0]),
                                sound=(True, self.atk1_sound, None, None),
                                hitbox_scale_x=0.4
                                ,hitbox_scale_y=0.4
                                ) # Replace with the target
                            attack_display.add(attack)
                        # self.mana -= self.attacks[1].mana_cost
                        self.attacks[1].last_used_time = current_time
                        self.running = False
                        self.attacking2 = True
                        self.player_atk2_index = 0
                        self.player_atk2_index_flipped = 0
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 2 used')

                elif hotkey3 and not self.attacking3 and not self.attacking1 and not self.attacking2 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >= self.attacks[2].mana_cost and self.attacks[2].is_ready():
                        attack = Attack_Display(
                                x=self.rect.centerx,
                                y=self.rect.centery + 100,
                                frames=self.atk3,
                                frame_duration=100,
                                repeat_animation=1,
                                speed=0,
                                dmg=self.atk3_damage_2nd,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=self.enemy,
                                delay=(True, 400),
                                sound=(True, self.sound_3 , None, None),
                                follow_self=True,
                                follow=(False, True), # some bug happended while i code the attack
                                heal=True,
                                self_moving=True,
                                self_kill_collide=True,
                                follow_offset=(0, 70)
                                )
                        attack_display.add(attack)

                        attack2 = Attack_Display(
                                x=self.rect.centerx,
                                y=self.rect.centery + 100,
                                frames=self.atk3,
                                frame_duration=100,
                                repeat_animation=1,
                                speed=0,
                                dmg=self.atk3_damage[0],
                                final_dmg=self.atk3_damage[1],
                                who_attacks=self,
                                who_attacked=self.enemy,
                                delay=(True, 400),
                                sound=(True, self.atk2_sound , None, None),
                                follow_self=True,
                                follow=(False, True),
                                heal=True,
                                self_moving=False,
                                self_kill_collide=False,
                                follow_offset=(0, 70),
                                consume_mana=[True, self.atk3_mana_consume]
                                )
                        attack_display.add(attack2)
                        
                        # self.mana -= self.attacks[2].mana_cost
                        self.attacks[2].last_used_time = current_time
                        self.running = False
                        self.attacking3 = True
                        self.player_atk3_index = 0
                        self.player_atk3_index_flipped = 0

                        
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 3 used')
                elif hotkey4 and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >=  self.attacks[3].mana_cost and self.attacks[3].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        for i in [
                #    0-frame  1-dur   2-pos      3-stun     4-delay     5-hitbox scale  6-cnsm mana 7-dmg/fnldmg
                     (self.sp, 100, (130, -100), (False, 0), (True, 200), (0.55, 0.5), True, self.sp_damage),#bubble
                     (self.sp1, 40, (120, 60), (True, 60), (True, 50), (0.3, 0.5), False, self.sp_damage_2nd),#spiral
                     (self.sp2, 80, (120, 60), (True, 5), (True, 1500), (0.3, 0.5), False, self.sp_damage_3rd)#splash
                        ]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i[2][0] if self.facing_right else self.rect.centerx - i[2][0], # in front of him
                                y=self.rect.centery + i[2][1],
                                frames=i[0],
                                frame_duration=i[1],
                                repeat_animation=1,
                                speed=5 if self.facing_right else -5,
                                dmg=i[7][0],
                                final_dmg=i[7][1],
                                who_attacks=self,
                                who_attacked=self.enemy,
                                sound=(True if i[4][1]  <= 50 else False, self.sound_2, self.sound_1, self.sound_3),
                                stun=(i[3][0], i[3][1]),
                                delay=(i[4][0], i[4][1]),
                                hitbox_scale_x=i[5][0],
                                hitbox_scale_y=i[5][1], 
                                consume_mana=[i[6], self.atk4_mana_consume],
                                stop_movement=(True, 1, 2)
                                
                                ) # Replace with the target
                            attack_display.add(attack)


                        # self.mana -=  self.attacks[3].mana_cost
                        self.attacks[3].last_used_time = current_time
                        self.running = False
                        self.sp_attacking = True
                        self.player_sp_index = 0
                        self.player_sp_index_flipped = 0

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 4 used')

                elif basic_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >= 0 and self.can_basic_attack():
                        for i in [
                            (200, self.basic_atk2, self.basic_atk2_flipped, 30, (50, 60, 0.4, 0.2), self.basic_attack_damage*self.atk_instance[0]),
                            (1000, self.basic_slash, self.basic_slash_flipped, 100, (70, 80, 0.8, 0.6), self.basic_attack_damage*self.atk_instance[1]),
                            (2200, self.basic_atk1, self.basic_atk1_flipped, 80, (60, 75, 0.75, 0.2), self.basic_attack_damage*self.atk_instance[2])
                            
                            ]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i[4][0] if self.facing_right else self.rect.centerx - i[4][0],
                                y=self.rect.centery + i[4][1],
                                frames=i[1] if self.facing_right else i[2],
                                frame_duration=i[3],
                                repeat_animation=1,
                                speed=0,
                                dmg=i[5],
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=self.enemy,

                                sound=(True, self.basic_sound, None, None),
                                delay=(True, self.basic_attack_animation_speed * (i[0] / self.base_animation_speed)), # self.basic_attack_animation_speed * (Base Delay/Base Animation Speed)
                                moving=True,
                                hitbox_scale_x=i[4][2],
                                hitbox_scale_y=i[4][3]
                                ,
                                is_basic_attack=True
                                )
                            attack_display.add(attack)
                        self.mana -= 0
                        self.attacks[4].last_used_time = current_time
                        self.running = False
                        self.basic_attacking = True
                        self.player_basic_index = 0
                        self.player_basic_index_flipped = 0
                        self.basic_sound.play()
                        self.last_basic_attack_time = current_time
                        # print("Attack executed")
                    else:
                        pass

                elif special_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.special >= MAX_SPECIAL: # and self.attacks[5].special_is_ready(self.special)
                        self.special_active = True
                        self.special_sound.play()
                    else:
                        pass











                    
        else:
            if not self.jumping and not self.is_dead():
                if hotkey1 and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >= self.attacks_special[0].mana_cost and self.attacks_special[0].is_ready():
                        for i in [
                            (80, 40, 100, self.sp_atk1_damage, 0, self.atk1_sound, False, 0.2, 0.4, False, False, True, True, (self.sp_atk1, self.sp_atk1)),
                            (70, 80, 100, self.atk1_damage_2nd, 0, self.sp_sound, True, 0.7, 1.2, False, False, False, False, (self.basic_slash, self.basic_slash_flipped)) # this is so inefficient
                        ]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i[0] if self.facing_right else self.rect.centerx -i[0],
                                y=self.rect.centery + i[1],
                                frames=i[13][0] if self.facing_right else i[13][1],
                                frame_duration=i[2],
                                repeat_animation=1,
                                speed=0,
                                dmg=i[3],
                                final_dmg=i[4],
                                who_attacks=self,
                                who_attacked=self.enemy,
                                delay=(True, 300),
                                sound=(True, i[5], None, None),

                                moving=i[6],
                                hitbox_scale_x=i[7],
                                hitbox_scale_y=i[8],

                                heal=i[9],
                                heal_enemy=i[10],

                                continuous_dmg=i[11],
                                stun=(i[11], 40),

                                consume_mana=[i[12], self.atk1_special_mana_consume],

                                stop_movement=(True, 1, 2)

                            )
                            attack_display.add(attack)

                        # self.mana -= self.attacks[0].mana_cost
                        self.attacks_special[0].last_used_time = current_time
                        self.running = False
                        self.attacking1 = True
                        self.player_atk1_2nd_index = 0
                        self.player_atk1_2nd_index_flipped = 0
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 1 used')


                elif hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >= self.attacks_special[1].mana_cost and self.attacks_special[1].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        for i in [(300,True), (1000,False)]: # WATER RAIN
                            attack = Attack_Display(
                                x=self.rect.centerx + 350 if self.facing_right else self.rect.centerx -350,
                                y=self.rect.centery,
                                frames=self.atk2_rain if self.facing_right else self.atk2_rain_flipped,
                                frame_duration=80,
                                repeat_animation=1,
                                speed=0,
                                dmg=self.sp_atk2_damage,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=self.enemy,
                                moving=False,
                                delay=(True, i[0]),
                                sound=(True, self.atk2_sound, self.sound_2, self.atk3_sound),
                                hitbox_scale_x=0.4
                                ,hitbox_scale_y=0.4,
                                consume_mana=[i[1], self.atk2_special_mana_consume]
                                ) # Replace with the target
                            attack_display.add(attack)

                        for i in [(300,170), (800, 340), (1300,0), (1800, 680), (2300, 510)]:
                            attack = Attack_Display( # CIRCLING WATERS
                                x=self.rect.centerx + i[1] if self.facing_right else self.rect.centerx -i[1],
                                y=self.rect.centery + 50,
                                frames=self.sp_atk2,
                                frame_duration=80,
                                repeat_animation=1,
                                speed=0,
                                dmg=self.sp_atk2_damage_2nd[0],
                                final_dmg=self.sp_atk2_damage_2nd[1],
                                who_attacks=self,
                                who_attacked=self.enemy,
                                moving=False,
                                delay=(True, i[0]),
                                sound=(True, self.atk1_sound, None, None),
                                hitbox_scale_x=0.4
                                ,hitbox_scale_y=0.4,
                                stop_movement=(True, 1, 1)
                                ) # Replace with the target
                            attack_display.add(attack)

                        for i in [(300,510), (1300, 680), (1800,0), (2300, 340), (2800, 170)]:
                            attack = Attack_Display( # WATER SHOT
                                x=self.rect.centerx + i[1] if self.facing_right else self.rect.centerx -i[1],
                                y=self.rect.centery + 50,
                                frames=self.watershot if not self.facing_right else self.watershot_flipped,
                                frame_duration=50,
                                repeat_animation=1,
                                speed=0,
                                dmg=self.sp_atk2_damage_3rd[0],
                                final_dmg=self.sp_atk2_damage_3rd[1],
                                who_attacks=self,
                                who_attacked=self.enemy,
                                moving=False,
                                delay=(True, i[0]),
                                sound=(True, self.atk1_sound, None, None),
                                hitbox_scale_x=0.7
                                ,hitbox_scale_y=0.7,
                                stop_movement=(True, 1, 1)
                                ) # Replace with the target
                            attack_display.add(attack)

                        for i in [(600,680), (1600, 510), (1900,0), (2200, 170), (2500, 340)]:
                            attack = Attack_Display( # WATER SHOT
                                x=self.rect.centerx + i[1] if self.facing_right else self.rect.centerx -i[1],
                                y=self.rect.centery + 50,
                                frames=self.watershot if not self.facing_right else self.watershot_flipped,
                                frame_duration=50,
                                repeat_animation=1,
                                speed=0,
                                dmg=self.sp_atk2_damage_3rd[0],
                                final_dmg=self.sp_atk2_damage_3rd[1],
                                who_attacks=self,
                                who_attacked=self.enemy,
                                moving=False,
                                delay=(True, i[0]),
                                sound=(False, None, None, None),
                                hitbox_scale_x=0.7
                                ,hitbox_scale_y=0.7,
                                stop_movement=(True, 1, 1)
                                ) # Replace with the target
                            attack_display.add(attack)

                        
                        # self.mana -= self.attacks[1].mana_cost
                        self.attacks_special[1].last_used_time = current_time
                        self.running = False
                        self.attacking2 = True
                        self.player_atk2_index = 0
                        self.player_atk2_index_flipped = 0
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 2 used')

                elif hotkey3 and not self.attacking3 and not self.attacking1 and not self.attacking2 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >= self.attacks_special[2].mana_cost and self.attacks_special[2].is_ready():
                        attack = Attack_Display(
                                x=self.rect.centerx,
                                y=self.rect.centery + 100,
                                frames=self.atk3,
                                frame_duration=100,
                                repeat_animation=1,
                                speed=0,
                                dmg=self.atk3_damage_2nd/2,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=self.enemy,
                                delay=(True, 400),
                                sound=(True, self.atk2_sound , None, None),
                                follow_self=True,
                                follow=(False, True), # some bug happended while i code the attack
                                heal=True,
                                self_moving=True,
                                self_kill_collide=True,
                                follow_offset=(0, 70)
                                )
                        attack_display.add(attack)

                        attack2 = Attack_Display(
                                x=self.rect.centerx,
                                y=self.rect.centery + 100,
                                frames=self.atk3,
                                frame_duration=100,
                                repeat_animation=1,
                                speed=0,
                                dmg=0,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=self.enemy,
                                delay=(True, 400),
                                sound=(True, self.sound_3 , None, None),
                                follow_self=True,
                                follow=(False, True),
                                heal=True,
                                self_moving=False,
                                self_kill_collide=False,
                                follow_offset=(0, 70),
                                consume_mana=[True, self.atk3_special_mana_consume]
                                )
                        attack_display.add(attack2)

                        attack3 = Attack_Display(
                                x=self.rect.centerx,
                                y=self.rect.centery + 100,
                                frames=self.sp_atk3,
                                frame_duration=120,
                                repeat_animation=2,
                                speed=0,
                                dmg=self.sp_atk3_damage[0],
                                final_dmg=self.sp_atk3_damage[1],
                                who_attacks=self,
                                who_attacked=self.enemy,
                                delay=(True, 400),
                                sound=(True, self.sp_sound , None, None),
                                follow_self=True,
                                follow=(False, True),
                                heal=True,
                                self_moving=False,
                                self_kill_collide=False,
                                follow_offset=(0, 70),
                                consume_mana=[False, self.atk3_mana_consume]
                                )
                        attack_display.add(attack3)
                        
                        # self.mana -= self.attacks[2].mana_cost
                        self.attacks_special[2].last_used_time = current_time
                        self.running = False
                        self.attacking3 = True
                        self.player_atk3_index = 0
                        self.player_atk3_index_flipped = 0
                        
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 3 used')
                elif hotkey4 and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[3].mana_cost and self.attacks_special[3].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        for i in [
                #    0-frame  1-dur   2-pos      3-stun     4-delay     5-hitbox scale  6-cnsm mana 7-dmg/fnldmg 8-moving
                     (self.sp, 100, (130, -100), (False, 0), (True, 200), (0.55, 0.5), True, self.sp_damage, (False,0)),#bubble
                     (self.sp_atk4, 50, (130, -100), (False, 0), (True, 200), (0.55, 0.5), True, self.sp_damage, (False,0)),#bubble2ndfront
                     (self.sp_atk4,50,(550, -100),(False, 0),(True, 1600), (0.55, 0.5), False, self.sp_damage, (False,0)),#bubble2ndend
                     (self.sp1, 40, (120, 60), (True, 60), (True, 50), (0.3, 0.5), False, self.sp_damage_2nd, (True, 4.5)),#spiral
                     (self.sp2, 80, (550, 60), (True, 5), (True, 1500), (0.3, 0.5), False, self.sp_damage_3rd, (False,0))#splash
                        ]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i[2][0] if self.facing_right else self.rect.centerx - i[2][0], # in front of him
                                y=self.rect.centery + i[2][1],
                                frames=i[0],
                                frame_duration=i[1],
                                repeat_animation=1,
                                speed=i[8][1] if self.facing_right else -i[8][1],
                                dmg=i[7][0],
                                final_dmg=i[7][1],
                                who_attacks=self,
                                who_attacked=self.enemy,
                                sound=(True if i[4][1] <= 50 else False, self.atk3_sound, self.atk2_sound, self.sound_2),
                                stun=(i[3][0], i[3][1]),
                                delay=(i[4][0], i[4][1]),
                                hitbox_scale_x=i[5][0],
                                hitbox_scale_y=i[5][1],
                                consume_mana=[i[6], self.atk4_special_mana_consume/2],
                                moving=i[8][0],
                                stop_movement=(True, 1, 2)
                                ) # Replace with the target
                            attack_display.add(attack)

                        for i in [(100,130*1.23), (300, 191.1*1.23), (700,275*1.23), (1100, 369.5*1.23), (1500, 550*1.23)]:
                            attack = Attack_Display( # WATER SHOT
                                x=self.rect.centerx + i[1] if self.facing_right else self.rect.centerx -i[1],
                                y=self.rect.centery + 30,
                                frames=self.watershot if not self.facing_right else self.watershot_flipped,
                                frame_duration=40,
                                repeat_animation=1,
                                speed=0,
                                dmg=self.sp_atk2_damage_3rd[1],
                                final_dmg=self.sp_atk2_damage_3rd[1],
                                who_attacks=self,
                                who_attacked=self.enemy,
                                moving=True,
                                delay=(True, i[0]),
                                sound=(True if i[0] <= 100 else False, self.sound_2, self.sound_1, self.sound_3),
                                hitbox_scale_x=0.7
                                ,hitbox_scale_y=0.7
                                ) # Replace with the target
                            attack_display.add(attack)

                        # self.mana -=  self.attacks[3].mana_cost
                        self.attacks_special[3].last_used_time = current_time
                        self.running = False
                        self.sp_attacking = True
                        self.player_sp_index = 0
                        self.player_sp_index_flipped = 0

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 4 used')

                elif basic_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >= 0 and self.can_basic_attack():
                        for i in [
                            (200, self.basic_atk2, self.basic_atk2_flipped, 30, (50, 60, 0.4, 0.2), self.basic_attack_damage*self.special_instance[0],(False, 1, 1)),
                            (1000, self.basic_slash, self.basic_slash_flipped, 100, (70, 80, 0.8, 0.6), self.basic_attack_damage*self.special_instance[1],(False, 1, 1)),
                            (2200, self.basic_atk1, self.basic_atk1_flipped, 80, (60, 75, 0.75, 0.2), self.basic_attack_damage*self.special_instance[2],(True, 1, 1))
                            
                            ]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i[4][0] if self.facing_right else self.rect.centerx - i[4][0],
                                y=self.rect.centery + i[4][1],
                                frames=i[1] if self.facing_right else i[2],
                                frame_duration=i[3],
                                repeat_animation=1,
                                speed=0,
                                dmg=i[5],
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=self.enemy,

                                sound=(True, self.basic_sound, None, None),
                                delay=(True, self.basic_attack_animation_speed * (i[0] / self.base_animation_speed)), # self.basic_attack_animation_speed * (Base Delay/Base Animation Speed)
                                moving=True,
                                hitbox_scale_x=i[4][2],
                                hitbox_scale_y=i[4][3],
                                stop_movement=i[6]
                                ,
                                is_basic_attack=True
                                )
                            attack_display.add(attack)
                        self.mana -= 0
                        self.attacks[4].last_used_time = current_time
                        self.running = False
                        self.basic_attacking = True
                        self.player_basic_index = 0
                        self.player_basic_index_flipped = 0
                        self.basic_sound.play()
                        self.last_basic_attack_time = current_time

                        # print("Attack executed")
                    else:
                        pass

                
     
            
    def run_animation(self, animation_speed=0):
        if not self.special_active:
            if self.facing_right:
                self.player_run_index, _ = self.animate(self.player_run, self.player_run_index, loop=True)
            else:
                self.player_run_index_flipped, _ = self.animate(self.player_run_flipped, self.player_run_index_flipped, loop=True)
        else:
            if self.facing_right:
                self.player_surf_index, _ = self.animate(self.player_surf, self.player_surf_index, loop=True)
            else:
                self.player_surf_index_flipped, _ = self.animate(self.player_surf_flipped, self.player_surf_index_flipped, loop=True)

        self.last_atk_time -= animation_speed
    
    def simple_idle_animation(self, animation_speed=0):
        if not self.special_active:
            if self.facing_right:
                self.player_idle_index, _ = self.animate(self.player_idle, self.player_idle_index, loop=True)
            else:
                self.player_idle_index_flipped, _ = self.animate(self.player_idle_flipped, self.player_idle_index_flipped, loop=True)
        else:
            if self.facing_right:
                self.player_surf_index, _ = self.animate(self.player_surf, self.player_surf_index, loop=True)
            else:
                self.player_surf_index_flipped, _ = self.animate(self.player_surf_flipped, self.player_surf_index_flipped, loop=True)

        self.last_atk_time -= animation_speed

    def atk1_animation(self, animation_speed=0):
        if not self.special_active:
            if self.facing_right:
                self.player_atk1_index, self.attacking1 = self.animate(self.player_atk1, self.player_atk1_index, loop=False)
            else:
                self.player_atk1_index_flipped, self.attacking1 = self.animate(self.player_atk1_flipped, self.player_atk1_index_flipped, loop=False)

        else:
            if self.facing_right:
                self.player_atk1_2nd_index, self.attacking1 = self.animate(self.player_atk1_2nd, self.player_atk1_2nd_index, loop=False)
            else:
                self.player_atk1_2nd_index_flipped, self.attacking1 = self.animate(self.player_atk1_2nd_flipped, self.player_atk1_2nd_index_flipped, loop=False)
        self.last_atk_time -= animation_speed

    def update(self):

         
        
        if not self.is_dead():
            self.player_death_index = 0
            self.player_death_index_flipped = 0
        if self.is_dead():
            self.play_death_animation()
        elif self.jumping:
            self.jump_animation()
        elif self.running and not self.jumping:
            self.run_animation(animation_speed=self.running_animation_speed)
                

        elif self.attacking1:
            self.atk1_animation()
        elif self.attacking2:
            self.atk2_animation(-4)
        elif self.attacking3:
            self.atk3_animation()
        elif self.sp_attacking:
            self.sp_animation()
        elif self.basic_attacking:
            self.basic_animation()
        else:
            self.simple_idle_animation(RUNNING_ANIMATION_SPEED)

        # Apply gravity
        self.y_velocity += DEFAULT_GRAVITY
        self.y_pos += self.y_velocity

        

        # Update the player's position
        self.rect.midbottom = (self.x_pos, self.y_pos)

        
        
        # Update the health and mana bars
        if self.health != 0:
            if not DISABLE_MANA_REGEN:
                self.mana += self.mana_regen
            if not DISABLE_HEAL_REGEN:
                self.health += self.health_regen
        else:
            self.health = 0

        if not global_vars.DISABLE_SPECIAL_REDUCE:
            if self.special_active:
                self.special -= SPECIAL_DURATION
                if self.special <= 0:
                    self.special_active = False


        # if self.running:
        #     print('is running')
        self.update_mana_values()
        '''test code are below, for checking correct mana values'''
        # self.atk1_mana_consume = (self.attacks[0].mana_cost/40) - ((self.attacks[0].mana_cost/40)*self.mana_mult)
        # print(self.attacks[0].mana_cost)

        
        super().update()