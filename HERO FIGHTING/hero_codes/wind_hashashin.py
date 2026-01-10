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
WIND_HASHASHIN_BASIC_COUNT = 4
WIND_HASHASHIN_JUMP_COUNT = 6
WIND_HASHASHIN_RUN_COUNT = 8 
WIND_HASHASHIN_IDLE_COUNT = 8
WIND_HASHASHIN_ATK1_COUNT = 7 # using the sp animation
WIND_HASHASHIN_ATK2_COUNT = 7
WIND_HASHASHIN_ATK3_COUNT = 26
WIND_HASHASHIN_SP_COUNT = 30
WIND_HASHASHIN_DEATH_COUNT = 19

# WIND_HASHASHIN_ATK1
# WIND_HASHASHIN_ATK2
# WIND_HASHASHIN_ATK3
# WIND_HASHASHIN_SP =

# WIND_HASHASHIN_ATK1_MANA_COST = int(base1 - (base1 * percen))
# WIND_HASHASHIN_ATK2_MANA_COST = int(base2 - (base2 * percen))
# WIND_HASHASHIN_ATK3_MANA_COST = int(base3 - (base3 * percen))
# WIND_HASHASHIN_SP_MANA_COST = int(base4 - (base4 * percen))

#atk rank doesn't matter here
WIND_HASHASHIN_ATK1_SIZE = 0.8 # smoke
WIND_HASHASHIN_ATK2_SIZE = 0.8 # tornado
WIND_HASHASHIN_ATK3_SIZE = 1 # circcle
WIND_HASHASHIN_SP_SIZE = 1  # x slash

WIND_HASHASHIN_ATK3_SPECIAL_SIZE = 2

#1=60, 2=45, 3=20, 4=15

# WIND_HASHASHIN_ATK1_COOLDOWN = 7000
# WIND_HASHASHIN_ATK2_COOLDOWN = 14000
# WIND_HASHASHIN_ATK3_COOLDOWN = 26000
# WIND_HASHASHIN_SP_COOLDOWN = 60000

# WIND_HASHASHIN_ATK1_DAMAGE = (10, 0) #smoke dmg
# WIND_HASHASHIN_ATK2_DAMAGE = (35/45, 0) #tornado
# WIND_HASHASHIN_ATK2_DAMAGE_2ND = (15/15, 5) # x slash
# WIND_HASHASHIN_ATK3_DAMAGE = 0.24 #not used
# WIND_HASHASHIN_SP_DAMAGE = (200/20, 25) # circle
# WIND_HASHASHIN_SP_DAMAGE_2ND = (15/15, 5) # x slash

# WIND_HASHASHIN_REAL_SP_DAMAGE = 16 #0.225

#skl  = atk1 fraame
#skl2 = atk2 frame, sp frame
#skl3 = atk3 frame, sp frame


class Wind_Hashashin(Player):
    def __init__(self, player_type, enemy):
        super().__init__(player_type, enemy)
        self.player_type = player_type
        self.name = "Wind Hashashin"

        self.hitbox_rect = pygame.Rect(0, 0, 50, 80)

        # stat
        self.strength = 38
        self.intelligence = 40
        self.agility = 24 #(13*4=52)



        self.base_health_regen = 0.85 # 1.23
        self.base_mana_regen = 5.1 # 5.1 + 0.4 = 5.5
        self.base_attack_damage = 0.0 # 4.8

        self.base_attack_speed = 110
        self.base_attack_time = 1700

        self.base_animation_speed = 120
        self.min_animation_speed = 50
        self.attack_speed_modifier = 0.6

        self.health_regen = self.calculate_regen(self.base_health_regen, self.hp_regen_per_str, self.strength) #0.8 + 38 * 0.01 = 1.2
        self.mana_regen = self.calculate_regen(self.base_mana_regen, self.mana_regen_per_int, self.intelligence) #5.1 + 40 * 0.01 = 5.5
        self.basic_attack_damage = self.calculate_regen(self.base_attack_damage, self.agi_mult, self.agility, basic_attack=True) # 0.0 + 13 * 0.1 = 1.3

        # Recalculate attack speed variables for fire wizard's base stats
        self.attack_speed = self.calculate_effective_as()
        self.basic_attack_cooldown = self.calculate_basic_attack_interval()
        self.basic_attack_animation_speed = self.calculate_attack_animation_speed()

        # Base Stats
        self.max_health = (self.strength * self.str_mult)
        self.max_mana = (self.intelligence * self.int_mult)
        self.health = self.max_health
        self.mana = self.max_mana


        # Player Position
        self.x = 50
        self.y = 50
        self.width = 200

        percen = 0.15
        base1 = 50
        base2 = 70 #80
        base3 = 130 #140
        base4 = 200

        self.atk1_mana_cost = int(base1 - (base1 * percen)) # 47 !
        self.atk2_mana_cost = int(base2 - (base2 * percen))
        self.atk3_mana_cost = int(base3 - (base3 * percen))
        self.sp_mana_cost = int(base4 - (base4 * percen))


        self.atk1_cooldown = 7000
        self.atk2_cooldown = 10000 #14000 -> 10000
        self.atk3_cooldown = 26000
        self.sp_cooldown = 60000

        self.atk1_damage = (10, 0) #smoke dmg
        self.atk2_damage = (35/45, 0) #tornado
        self.atk2_damage_2nd = (13/15, 5) # x slash
        self.atk3_damage = (0, 0) #not used
        self.sp_damage = (200/20, 25) # circle
        self.sp_damage_2nd = (13/15, 5) # x slash
        self.real_sp_damage = 16 # times 4

        #SKILL DAMAGE before
        #10
        #26
        #30
        #72

        #sp
        #3 each
        #30
        #37
        #86

        # Player Animation Source1.png
        basic_ani = [r'assets\characters\wind hasashin\PNG\3_atk\3_atk_', WIND_HASHASHIN_BASIC_COUNT, 0]

        jump_ani = [r'assets\characters\Wind hasashin\PNG\j_up\j_up_', WIND_HASHASHIN_JUMP_COUNT, 0]
        run_ani = [r'assets\characters\wind hasashin\PNG\run\run_', WIND_HASHASHIN_RUN_COUNT, 0]
        idle_ani = [r'assets\characters\wind hasashin\PNG\idle\idle_', WIND_HASHASHIN_IDLE_COUNT, 0]
        atk1_ani = [r'assets\characters\wind hasashin\PNG\sp_atk\sp_atk_', WIND_HASHASHIN_ATK1_COUNT, 0]
        atk2_ani = [r'assets\characters\wind hasashin\PNG\air_atk\air_atk_', WIND_HASHASHIN_ATK2_COUNT, 0]
        atk3_ani = [r'assets\characters\wind hasashin\PNG\3_atk\3_atk_', WIND_HASHASHIN_ATK3_COUNT, 0]
        sp_ani = [r'assets\characters\wind hasashin\PNG\sp_atk\sp_atk_', WIND_HASHASHIN_SP_COUNT, 0]
        death_ani = [r'assets\characters\wind hasashin\PNG\death\death_', WIND_HASHASHIN_DEATH_COUNT, 0]

        # Player Skill Sounds Effects Source
        self.atk1_sound = pygame.mixer.Sound(r'assets\sound effects\wind hashashin\1st.mp3')
        self.atk2_sound = pygame.mixer.Sound(r'assets\sound effects\wind hashashin\2nd.mp3')
        self.atk3_sound = pygame.mixer.Sound(r'assets\sound effects\wind hashashin\3rd.mp3')
        self.sp_sound = pygame.mixer.Sound(r'assets\sound effects\wind hashashin\4th 1, slash.mp3')
        self.atk1_sound.set_volume(0.5 * global_vars.MAIN_VOLUME)
        self.atk2_sound.set_volume(0.4 * global_vars.MAIN_VOLUME)
        self.atk3_sound.set_volume(0.4 * global_vars.MAIN_VOLUME)
        self.sp_sound.set_volume(0.3 * global_vars.MAIN_VOLUME)
        
        self.x_slash_sound = pygame.mixer.Sound(r'assets\sound effects\wind hashashin\x slash 2nd,3rd, 4th.mp3')
        self.sp_sound2 = pygame.mixer.Sound(r'assets\sound effects\wind hashashin\4th 2, flesh hit.mp3')
        self.x_slash_sound.set_volume(0.3 * global_vars.MAIN_VOLUME)
        self.sp_sound2.set_volume(0.4 * global_vars.MAIN_VOLUME)

        self.atk3_sound_special = pygame.mixer.Sound(r'assets\sound effects\fire knight\3rrd.mp3')
        self.atk3_sound_special.set_volume(0.5 * global_vars.MAIN_VOLUME)
        # (The rest of the code follows same structure and renaming logic...)
        # Player Skill Animations Source
        # atk1 = [r'', FIRE_KNIGHT_ATK1, 1]
        # atk2 = [r', FIRE_KNIGHT_ATK2, 1]
        # atk3 = [r'assets\attacks\fire knight\atk3\png_', FIRE_KNIGHT_ATK3, 1]
        # sp = [r'assets\attacks\fire knight\sp atk', FIRE_KNIGHT_SP, 1]

        # Player Skill Icons Source
        skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wind_hasashin\WindHashira.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_2 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wind_hasashin\3yzqiwcug5qc1.jpeg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wind_hasashin\What is Danmokou_.jpeg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wind_hasashin\download.jpeg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_icon = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wind_hasashin\aleksey-bayura-sketch-ninja1.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        special_skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wind_hasashin\7316955-HSC00001-7.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wind_hasashin\wmremove-transformed.jpeg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wind_hasashin\MarkForDeathIcon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        # Player Icon Rects
        if self.player_type == 1:
            self.skill_1_rect = skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))
            
            self.special_rect = special_icon.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 4 + 50, SKILL_Y_OFFSET))

            self.special_skill_1_rect = special_skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.special_skill_2_rect = skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.special_skill_3_rect = special_skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.special_skill_4_rect = special_skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))

        elif self.player_type == 2:
            self.special_rect = special_icon.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 4 - 50, SKILL_Y_OFFSET))

            self.special_skill_1_rect = special_skill_1.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 3, SKILL_Y_OFFSET))
            self.special_skill_2_rect = skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 2, SKILL_Y_OFFSET))
            self.special_skill_3_rect = special_skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X, SKILL_Y_OFFSET))
            self.special_skill_4_rect = special_skill_4.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X, SKILL_Y_OFFSET))
            
            self.skill_1_rect = skill_1.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 3, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X, SKILL_Y_OFFSET))

        # Player Attack Animations Load (atk doesn't matter, some attack will be used on other attack)
        self.atk1 = load_attack(
        filepath=r"assets\attacks\wind hasashin\1.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=12, 
        columns=5, 
        scale=WIND_HASHASHIN_ATK1_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.atk2 = load_attack(
        filepath=r"assets\attacks\wind hasashin\2.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=9, 
        columns=5, 
        scale=WIND_HASHASHIN_ATK2_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.atk2 = load_attack_flipped(
        filepath=r"assets\attacks\wind hasashin\2.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=9, 
        columns=5, 
        scale=WIND_HASHASHIN_ATK2_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.atk3 = load_attack(
        filepath=r"assets\attacks\wind hasashin\3.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=4, 
        columns=5, 
        scale=WIND_HASHASHIN_ATK3_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.sp = load_attack(
        filepath=r"assets\attacks\wind hasashin\4.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=3, 
        columns=5, 
        scale=WIND_HASHASHIN_SP_SIZE, 
        rotation=0,
        frame_duration=100
    )
        



        self.atk3_special = load_attack(
        filepath=r"assets\attacks\fire knight\083.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=4, 
        columns=5, 
        scale=WIND_HASHASHIN_ATK3_SPECIAL_SIZE, 
        rotation=0,
        frame_duration=100
    )
        

        # Player Animations Load
        self.player_basic = self.load_img_frames(basic_ani[0], basic_ani[1], basic_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_basic_flipped = self.load_img_frames_flipped(basic_ani[0], basic_ani[1], basic_ani[2], DEFAULT_CHAR_SIZE_2)
        
        self.player_jump = self.load_img_frames(jump_ani[0], jump_ani[1], jump_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_jump_flipped = self.load_img_frames_flipped(jump_ani[0], jump_ani[1], jump_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_idle = self.load_img_frames(idle_ani[0], idle_ani[1], idle_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_idle_flipped = self.load_img_frames_flipped(idle_ani[0], idle_ani[1], idle_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_run = self.load_img_frames(run_ani[0], run_ani[1], run_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_run_flipped = self.load_img_frames_flipped(run_ani[0], run_ani[1], run_ani[2], DEFAULT_CHAR_SIZE_2)    
        self.player_atk1 = self.load_img_frames(atk1_ani[0], atk1_ani[1], atk1_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_atk1_flipped = self.load_img_frames_flipped(atk1_ani[0], atk1_ani[1], atk1_ani[2], DEFAULT_CHAR_SIZE_2)  
        self.player_atk2 = self.load_img_frames(atk2_ani[0], atk2_ani[1], atk2_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_atk2_flipped = self.load_img_frames_flipped(atk2_ani[0], atk2_ani[1], atk2_ani[2], DEFAULT_CHAR_SIZE_2)  
        self.player_atk3 = self.load_img_frames(atk3_ani[0], atk3_ani[1], atk3_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_atk3_flipped = self.load_img_frames_flipped(atk3_ani[0], atk3_ani[1], atk3_ani[2], DEFAULT_CHAR_SIZE_2)  
        self.player_sp = self.load_img_frames(sp_ani[0], sp_ani[1], sp_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_sp_flipped = self.load_img_frames_flipped(sp_ani[0], sp_ani[1], sp_ani[2], DEFAULT_CHAR_SIZE_2) # ?
        self.player_death = self.load_img_frames(death_ani[0], death_ani[1], death_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_death_flipped = self.load_img_frames_flipped(death_ani[0], death_ani[1], death_ani[2], DEFAULT_CHAR_SIZE_2)

        #this is the ultimate skill using player sp animation as attack animation
        self.real_sp = self.player_sp

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

        self.attacks_special = [
            Attacks(
                mana_cost=self.mana_cost_list[0],
                skill_rect=self.special_skill_1_rect,
                skill_img=special_skill_1,
                cooldown=self.atk1_cooldown,
                mana=self.mana
            ),
            Attacks(
                mana_cost=int(self.mana_cost_list[1]*1.5),
                skill_rect=self.special_skill_2_rect,
                skill_img=skill_3,
                cooldown=int(self.atk2_cooldown*1.5),
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
        
        self.atk1_move_speed = 1
        self.atk2_move_speed = 1
        self.atk3_move_speed = 4

        # Skill 1  configuration
        self.default_dash_speed = 12
        self.default_max_distance = 500

        self.special_dash_speed = 15
        self.special_max_distance = 800

        self.activate_dash = False
        self.distance_covered = 0
        self.dash_speed = 5
        self.max_distance = 600 #(400 -> 600)

        
    
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
                speed_modifier = 0.2,
                special_active_speed = 0.25,
                jump_force = self.jump_force,
                jump_force_modifier = 0.1
                )
            
        # ---------- Casting ----------
        if self.is_frozen():
            return
        
        if self.is_silenced() and not basic_hotkey:
            return
        
        if not self.special_active:
            if not self.is_dead():
                if hotkey1 and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks[0].mana_cost and self.attacks[0].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx,
                            y=self.rect.centery + 60,
                            frames=self.atk1,
                            frame_duration=20,
                            repeat_animation=1,
                            speed=-1.5 if self.facing_right else 1.5,
                            dmg=self.atk1_damage[0],
                            final_dmg=self.atk1_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            moving=True,
                            sound=(True, self.atk1_sound , None, None),
                            stop_movement=(True, 3, 2, 0.8)
                            ) # Replace with the target
                        attack_display.add(attack)
                        #dash  
                        self.mana -=  self.attacks[0].mana_cost
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

            if not self.jumping and not self.is_dead(): # can be cast while jumping, I hope...
                if hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks[1].mana_cost and self.attacks[1].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        # for i in [40*2, 80*2, 120*2, 160*2, 200*2]:
                        for i in [
                            (self.atk2, True, 30, 30, self.atk2_damage[0], False, self.atk2_damage[1]), # 0 = frames, 1 = moving, 2 = pos, 3 = duration, 4 = dmg, 5 = stun
                            (self.sp, False, 70, 40, self.atk2_damage_2nd[0], False, self.atk2_damage_2nd[1])
                            ]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i[2] if self.facing_right else self.rect.centerx - i[2], # in front of him
                                y=self.rect.centery + 50,
                                frames=i[0],
                                frame_duration=i[3],
                                repeat_animation=1,
                                speed=10 if self.facing_right else -10,
                                dmg=i[4],
                                final_dmg=i[6],
                                who_attacks=self,
                                who_attacked=self.enemy,
                                moving=i[1],
                                continuous_dmg=i[1],
                                stun=(i[5], 40),
                                sound=(True, self.atk2_sound, self.x_slash_sound, None),
                                
                                stop_movement=(i[1], 3, 2, 0.5)
                                ) # Replace with the target
                            attack_display.add(attack)
                        self.mana -=  self.attacks[1].mana_cost
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

            if not self.jumping and not self.is_dead():
                if hotkey3 and not self.attacking3 and not self.attacking1 and not self.attacking2 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks[2].mana_cost and self.attacks[2].is_ready():
                        # Create an attack
                        current_time2 = pygame.time.get_ticks()
                        # print("Z key pressed")  # 0 = frames, 1 = moving, 2 = pos, 3 = duration, 4 = dmg
                        
                        for i in [
                            (self.atk3, True, 100, 70, self.sp_damage[0], self.sp_damage[1]), # 0 = frames, 1 = moving, 2 = pos, 3 = duration, 4 = dmg, 5 = stun
                            (self.sp, False, 100, 50, self.sp_damage_2nd[0], self.sp_damage_2nd[1])
                            ]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i[2] if self.facing_right else self.rect.centerx - i[2], # in front of him
                                y=self.rect.centery + 50,
                                frames=i[0],
                                frame_duration=i[3],
                                repeat_animation=1,
                                speed=0 if self.facing_right else 0,
                                dmg=i[4],
                                final_dmg=i[5],
                                who_attacks=self,
                                who_attacked=self.enemy,
                                moving=i[1],
                                stun=(True, 0),
                                sound=(True, self.atk3_sound , self.x_slash_sound, None)
                                )
                            attack_display.add(attack)
                                    
                                    
                        # if current_time2 - self.last_atk_time > 1500:
                        #     attack_display.add(attack)
                        #     self.last_atk_time = current_time2
                        self.mana -=  self.attacks[2].mana_cost
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
                        # Target selection: find closest enemy

                        self.single_target()
                        
                        attack = Attack_Display(
                                x=self.rect.centerx,
                                y=self.rect.centery + 60,
                                frames=self.atk1, #frames=self.real_sp,
                                frame_duration=0.1,
                                repeat_animation=4,
                                speed=0 if self.facing_right else 0,
                                dmg=self.real_sp_damage,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=self.target,
                                per_end_dmg=(False, True),
                                disable_collide=True,
                                sound=(True, self.sp_sound, self.x_slash_sound, self.sp_sound2),
                                repeat_sound=True,
                                damage_mode='single'
                                )
                                # Replace with the target
                        attack_display.add(attack)
                        self.mana -=  self.attacks[3].mana_cost
                        self.attacks[3].last_used_time = current_time
                        self.running = False
                        self.sp_attacking = True
                        self.player_sp_index = 0
                        self.player_sp_index_flipped = 0

                        
                        # self.sp_sound.play()
                        # self.x_slash_sound.play()
                        # self.sp_sound2.play()
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 4 used')

                elif basic_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >= 0 and self.can_basic_attack():
                        for i in [0, 300]:
                            attack = Attack_Display(
                                x=self.rect.centerx + 60 if self.facing_right else self.rect.centerx - 60,
                                y=self.rect.centery + 50,
                                frames=self.basic_slash2 if self.facing_right else self.basic_slash2_flipped,
                                frame_duration=BASIC_FRAME_DURATION / 2,
                                repeat_animation=1,
                                speed=4 if self.facing_right else -4,
                                dmg=self.basic_attack_damage,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=self.enemy,
                                sound=(True, self.basic_sound, None, None),
                                moving=True,
                                delay=(True, self.basic_attack_animation_speed * (i / self.base_animation_speed)), # self.basic_attack_animation_speed * (Base Delay/Default Basic Attack Speed),

                                hitbox_scale_y=0.3,
                                hitbox_scale_x=0.3,
                                # hitbox_offset_x=30 if self.facing_right else -30,
                                # hitbox_offset_y=60
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
            if not self.is_dead():
                if hotkey1 and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[0].mana_cost and self.attacks_special[0].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        for i in [0, 200, 400, 600, 800, 1000]: # 6
                            attack = Attack_Display(
                                x=self.rect.centerx,
                                y=self.rect.centery + 60,
                                frames=self.atk1,
                                frame_duration=10,
                                repeat_animation=1,
                                speed=-1 if self.facing_right else 1,
                                dmg=self.atk1_damage[0] * 0.3,
                                final_dmg=self.atk1_damage[1],
                                who_attacks=self,
                                who_attacked=self.enemy,
                                moving=True,
                                sound=(True, self.atk1_sound, None, None),
                                delay=(True, i),
                                use_live_position_on_delay=True,
                                stop_movement=(True, 3, 1, 0.7)
                                ) # Replace with the target
                            attack_display.add(attack)
                        #dash  
                        self.mana -=  self.attacks_special[0].mana_cost
                        self.attacks_special[0].last_used_time = current_time
                        self.running = False
                        self.attacking1 = True
                        self.player_atk1_index = 0
                        self.player_atk1_index_flipped = 0

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 1 used')

            if not self.jumping and not self.is_dead(): # can be cast while jumping, I hope...
                if hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[1].mana_cost and self.attacks_special[1].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        # for i in [40*2, 80*2, 120*2, 160*2, 200*2]:

                        for i in [
                            (self.atk3, True, 100, 70, self.sp_damage[0], self.sp_damage[1]/2), # 0 = frames, 1 = moving, 2 = pos, 3 = duration, 4 = dmg, 5 = stun
                            (self.sp, False, 100, 50, self.sp_damage_2nd[0], self.sp_damage_2nd[1])
                            ]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i[2] if self.facing_right else self.rect.centerx - i[2], # in front of him
                                y=self.rect.centery + 50,
                                frames=i[0],
                                frame_duration=i[3],
                                repeat_animation=1,
                                speed=0 if self.facing_right else 0,
                                dmg=i[4],
                                final_dmg=i[5],
                                who_attacks=self,
                                who_attacked=self.enemy,
                                moving=i[1],
                                stun=(True, 0),
                                sound=(True, self.atk3_sound , self.x_slash_sound, None)
                                )
                            attack_display.add(attack)
                        self.mana -=  self.attacks_special[1].mana_cost
                        self.attacks_special[1].last_used_time = current_time
                        self.running = False
                        self.attacking3 = True
                        self.player_atk3_index = 0
                        self.player_atk3_index_flipped = 0

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 2 used')

            if not self.jumping and not self.is_dead():
                if hotkey3 and not self.attacking3 and not self.attacking1 and not self.attacking2 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[2].mana_cost and self.attacks_special[2].is_ready():
                        # Create an attack
                        current_time2 = pygame.time.get_ticks()
                        # print("Z key pressed")  # 0 = frames, 1 = moving, 2 = pos, 3 = duration, 4 = dmg
                        
                        for i in [
                            (self.atk3_special, True, 130, 100, self.atk2_damage[0] * 2.4, True, self.atk2_damage[1], -20), # 0 = frames, 1 = moving, 2 = pos, 3 = duration, 4 = dmg, 5 = stun
                            (self.sp, False, 70, 40, self.atk2_damage_2nd[0] * 2, False, self.atk2_damage_2nd[1], 50)
                            ]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i[2] if self.facing_right else self.rect.centerx - i[2], # in front of him
                                y=self.rect.centery + i[7],
                                frames=i[0],
                                frame_duration=i[3],
                                repeat_animation=1,
                                speed=7 if self.facing_right else -7,
                                dmg=i[4],
                                final_dmg=i[6],
                                who_attacks=self,
                                who_attacked=self.enemy,
                                moving=i[1],
                                continuous_dmg=i[1],
                                stun=(i[5], 40),
                                sound=(True, self.atk3_sound_special , self.x_slash_sound, None)
                                ) # Replace with the target
                            attack_display.add(attack)

                        self.mana -=  self.attacks_special[2].mana_cost
                        self.attacks_special[2].last_used_time = current_time
                        self.running = False
                        self.attacking2 = True
                        self.player_atk2_index = 0
                        self.player_atk2_index_flipped = 0
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 3 used')
                elif hotkey4 and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[3].mana_cost and self.attacks_special[3].is_ready():
                        # Target selection: find closest enemy
                        self.single_target()
                        
                        attack = Attack_Display(
                                x=self.rect.centerx,
                                y=self.rect.centery + 60,
                                frames=self.atk1, #frames=self.real_sp,
                                frame_duration=5,
                                repeat_animation=4,
                                speed=0 if self.facing_right else 0,
                                dmg=self.real_sp_damage * 0.4,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=self.target,
                                per_end_dmg=(False, True),
                                disable_collide=True,
                                sound=(True, self.sp_sound, self.x_slash_sound, self.sp_sound2),
                                repeat_sound=True,
                                damage_mode='single'
                                )
                        attack_display.add(attack)

                        for i in [1500, 3000, 4500, 6000]:
                            attack1 = Attack_Display(
                                    x=self.target.x_pos,
                                    y=self.target.y_pos - 150,
                                    frames=self.real_sp, #frames=self.real_sp,
                                    frame_duration=120,
                                    repeat_animation=1,
                                    speed=0 if self.facing_right else 0,
                                    dmg=self.real_sp_damage * 0,
                                    final_dmg=0,
                                    who_attacks=self,
                                    who_attacked=self.target,
                                    per_end_dmg=(False, True),
                                    disable_collide=False,
                                    sound=(True, self.sp_sound, self.sp_sound2, self.x_slash_sound),
                                    repeat_sound=True,
                                    delay=(True, i),
                                    follow=(False, True)
                                    )
                                    # Replace with the target
                            attack_display.add(attack1)

                            attack2 = Attack_Display(
                                x=self.rect.centerx,
                                y=self.rect.centery + 60,
                                frames=self.atk1, #frames=self.real_sp,
                                frame_duration=5,
                                repeat_animation=4,
                                speed=0 if self.facing_right else 0,
                                dmg=self.real_sp_damage * 0.2,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=self.target,
                                per_end_dmg=(False, True),
                                disable_collide=True,
                                sound=(True, self.sp_sound, self.x_slash_sound, self.sp_sound2),
                                repeat_sound=True,
                                delay=(True, i)
                                )
                            attack_display.add(attack2)

                        




                        self.mana -=  self.attacks_special[3].mana_cost
                        self.attacks_special[3].last_used_time = current_time
                        self.running = False
                        self.sp_attacking = True
                        self.player_sp_index = 0
                        self.player_sp_index_flipped = 0
                        # self.sp_sound.play()
                        # self.x_slash_sound.play()
                        # self.sp_sound2.play()
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 4 used')

                elif basic_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >= 0 and self.can_basic_attack():
                        for i in [0, 300]:
                            attack = Attack_Display(
                                x=self.rect.centerx + 60 if self.facing_right else self.rect.centerx - 60,
                                y=self.rect.centery + 50,
                                frames=self.basic_slash2 if self.facing_right else self.basic_slash2_flipped,
                                frame_duration=BASIC_FRAME_DURATION / 2,
                                repeat_animation=2,
                                speed=6 if self.facing_right else -6,
                                dmg=self.basic_attack_damage*DEFAULT_BASIC_ATK_DMG_BONUS,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=self.enemy,
                                moving=True,
                                heal=False,
                                continuous_dmg=False,
                                per_end_dmg=(False, False),
                                disable_collide=False,
                                stun=(False, 0),
                                sound=(True, self.basic_sound, None, None),
                                kill_collide=False,
                                delay=(True, self.basic_attack_animation_speed * (i / self.base_animation_speed)), # self.basic_attack_animation_speed * (Base Delay/Default Basic Attack Speed),

                                hitbox_scale_y=0.4,
                                hitbox_scale_x=0.4,
                                hitbox_offset_x=170,
                                hitbox_offset_y=60
                                ,is_basic_attack=True
                                )
                            attack_display.add(attack)
                        self.mana -= 0
                        self.attacks_special[4].last_used_time = current_time
                        self.running = False
                        self.basic_attacking = True
                        self.player_basic_index = 0
                        self.player_basic_index_flipped = 0
                        self.basic_sound.play()
                        self.last_basic_attack_time = current_time
                        # print("Attack executed")
                    else:
                        pass
            
          
        
    # def activate_skill_1(self):
    #     if not self.special_active:
    #         self.atk1_move_speed += 0.3
    #         self.y_velocity = 0
    #         if self.facing_right:
    #             self.x_pos += self.atk1_move_speed
    #         else:
    #             self.x_pos -= self.atk1_move_speed
    #     else:
    #         self.atk1_move_speed += 0.3
    #         self.y_pos -= 0.2
    #         self.y_velocity = 0
    #         if self.facing_right:
    #             self.x_pos += self.atk1_move_speed
    #         else:
    #             self.x_pos -= self.atk1_move_speed
    #         self.jumping = True
    #         self.y_velocity = (DEFAULT_JUMP_FORCE * 0.5)

    def trigger_dash(self): # this thing so buggy, fix this soon
        if self.distance_covered < self.max_distance:
            if self.facing_right:
                self.x_pos += self.dash_speed
                self.distance_covered += self.dash_speed
            elif not self.facing_right:
                self.x_pos -= self.dash_speed
                self.distance_covered += self.dash_speed
        else:
            self.distance_covered = 0
        # print(self.distance_covered)
        
        
    
    
    def update(self):
        


         
        
        if not self.is_dead():
            self.player_death_index = 0
            self.player_death_index_flipped = 0
        if self.is_dead():
            self.play_death_animation()
        
        elif self.running and not self.jumping:
            self.run_animation(self.running_animation_speed+3)
            self.atk1_move_speed, self.atk2_move_speed = 1, 1

        elif self.attacking1: # fixing the damn bug for this hero
            self.activate_dash = True
            
            if not self.special_active:
                self.dash_speed = self.default_dash_speed
                self.max_distance = self.default_max_distance
            else:
                self.dash_speed = self.special_dash_speed
                self.max_distance = self.special_max_distance

            if self.distance_covered >= self.max_distance:
                self.activate_dash = False
                self.attacking1 = False
                self.distance_covered = 0
            else: 
                if self.activate_dash:
                    self.trigger_dash()
            self.atk1_animation()  

        elif self.jumping:
            self.jump_animation()
            self.atk1_move_speed, self.atk2_move_speed = 1, 1
            
        elif self.attacking2: # not special, used by skill2, when special, used by skill 3
            self.atk1_move_speed += 0.4 #just trying, plan is to make this special move that knokes back enemies 
            # if not self.special_active:
            #     if self.player_type == 1: # idea for slow, if enemy ffacing right, - x pos, else + x pos
            #         if self.facing_right:
            #             hero2.x_pos += self.atk2_move_speed
            #         else:
            #             hero2.x_pos -= self.atk2_move_speed
            #     if self.player_type == 2:
            #         if self.facing_right:
            #             hero1.x_pos += self.atk2_move_speed
            #         else:
            #             hero1.x_pos -= self.atk2_move_speed
            # elif self.special_active:
            #     if self.player_type == 1: # idea for slow, if enemy ffacing right, - x pos, else + x pos
            #         if self.facing_right:
            #             hero2.x_pos += self.atk3_move_speed
            #         else:
            #             hero2.x_pos -= self.atk3_move_speed
            #     if self.player_type == 2:
            #         if self.facing_right:
            #             hero1.x_pos += self.atk3_move_speed
            #         else:
            #             hero1.x_pos -= self.atk3_move_speed
            self.atk2_animation()
        elif self.attacking3:
            self.atk3_animation(2) #animation speed increase
            self.atk1_move_speed, self.atk2_move_speed = 1, 1
        elif self.sp_attacking:
            # Ensure the target is valid before accessing its attributes
            if self.target is not None and not self.target.is_dead():
                self.x_pos = self.target.x_pos
                self.y_pos = self.target.y_pos
            else:
                # Reset the target and stop the special attack if the target is invalid
                self.target = None
                self.sp_attacking = False
            self.sp_animation()
            self.atk1_move_speed, self.atk2_move_speed = 1, 1

        elif self.basic_attacking:
            self.basic_animation()
            
        else:
            self.simple_idle_animation(RUNNING_ANIMATION_SPEED+3)
            self.atk1_move_speed, self.atk2_move_speed = 1, 1

        # Apply gravity
        # if not self.attacking2:
        self.y_velocity += (DEFAULT_GRAVITY - (DEFAULT_GRAVITY * 0.02))
        self.y_pos += self.y_velocity
        # else:
        #     self.jumping = False

        

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

        # print(self.target) #good
        super().update()