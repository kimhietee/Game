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
import random
import pygame
'''Forest Ranger Config'''
FR_JUMP_COUNT = 6
FR_RUN_COUNT = 8
FR_IDLE_COUNT = 8
FR_ATK1_COUNT = 7
FR_ATK3_COUNT = 9
FR_SP_COUNT = 16
FR_DEATH_COUNT = 4

FR_BASIC = 6
FR_ATK1 = 4
FR_ATK2 = 40
FR_ATK3 = 10
FR_SP = 3

FR_SPECIAL_ATK3 = 10
# ---------------------
# WANDERER_MAGICIAN_ATK1_MANA_COST = 70
# WANDERER_MAGICIAN_ATK2_MANA_COST = 125
# WANDERER_MAGICIAN_ATK3_MANA_COST = 125
# WANDERER_MAGICIAN_SP_MANA_COST = 170

FR_BASIC_SIZE = 1.5
FR_ATK1_SIZE = 2
FR_ATK2_SIZE = 1
FR_ATK3_SIZE = 1.5
FR_SP_SIZE = 1.3

FR_SPECIAL_ATK3_SIZE = 2
FR_SPECIAL_BASICATK1_SIZE = 2

# WANDERER_MAGICIAN_ATK1_COOLDOWN = 8000
# WANDERER_MAGICIAN_ATK2_COOLDOWN = 15000 + 9000
# WANDERER_MAGICIAN_ATK3_COOLDOWN = 26000
# WANDERER_MAGICIAN_SP_COOLDOWN = 60000

# WANDERER_MAGICIAN_ATK1_DAMAGE = 0 # dmg at the input, sry
# WANDERER_MAGICIAN_ATK2_DAMAGE = (18/40, 0)
# WANDERER_MAGICIAN_ATK3_DAMAGE = (30/10, 5) #26
# WANDERER_MAGICIAN_SP_DAMAGE = (55, 0)

# Important details to note as of version idk, date: 10/26/25
# - damage compare to other heroes with total basic attack damage (no items)
# - including the arrow stuck which is 1 damage
# - right = forest ranger

# --- RANKED HIGH DAMAGE --- 
# water princess = 30 <-> 18 about 5s
# wind hashahsin = 28 <-> 17 about 5s (wind hashashin about 26 dmg, identical to fire knight -> 26 dmg when compared)
# fire wizard = 26 <-> 18 about 6s
# fire knight = 26 <-> 18 about 6s
# wanderer magician = 19 <-> 18 about 5s 
# onre = 23 <-> 18 about 5s



class Forest_Ranger(Player): #NEXT WORK ON THE SPRITES THEN COPY EVERYTHING SINCE IM DONE 4/6/25 10:30pm
    def __init__(self, player_type, enemy):
        super().__init__(player_type, enemy)
        # print('from forest ranger. player:', player_type)
        # print(enemy) 
        self.player_type = player_type # 1 for player 1, 2 for player 2
        self.name = "Forest Ranger"
        # from heroes import items #make a button hard mode
        # self.items = items+items # from heroes.py

        self.hitbox_rect = pygame.Rect(0, 0, 45, 100)

        # stat
        self.strength = 32
        self.intelligence = 52
        self.agility = 30 # = 35

        self.base_health_regen = 0.8 # 1.12
        self.base_mana_regen = 5.4 # 5.92
        self.base_attack_damage = 0.5 # 3.5

        self.base_attack_speed = 100
        self.base_attack_time = 1700

        self.health_regen = self.calculate_regen(self.base_health_regen, self.hp_regen_per_str, self.strength) #0.8 + 32 * 0.01 = 1.12
        self.mana_regen = self.calculate_regen(self.base_mana_regen, self.mana_regen_per_int, self.intelligence) #5.4 + 52 * 0.01 = 5.92
        self.basic_attack_damage = self.calculate_regen(self.base_attack_damage, self.agi_mult, self.agility, basic_attack=True) # 0.5 + 30 * 0.1 = 3.5

        # Recalculate attack speed variables for fire wizard's base stats
        self.attack_speed = self.calculate_effective_as()
        self.basic_attack_cooldown = self.calculate_basic_attack_interval()
        self.basic_attack_animation_speed = global_vars.DEFAULT_ANIMATION_SPEED / (self.attack_speed / self.base_attack_speed)
        
        self.max_health = self.strength * self.str_mult
        self.max_mana = self.intelligence * self.int_mult
        # self.special_default_max_mana = self.max_mana # max mana and this variable mustt  be the same
        self.health = self.max_health
        self.mana = self.max_mana
        
        self.x = 50
        self.y = 50
        self.width = 200
        self.height = 20

        # real mana cost is commented
        self.atk1_mana_cost = 120 #100
        self.atk2_mana_cost = 100 #50 (40 when special)
        self.atk3_mana_cost = 170 #100
        self.sp_mana_cost = 220 #120
        self.atk3_mana_cost_for_special = 200 #100
        self.sp_mana_cost_for_special = 250 #120

        self.atk1_cooldown = 10000 + 5000 # 12 seconds
        self.atk2_cooldown = 7000
        self.atk3_cooldown = 12000
        self.sp_cooldown = 30000
        self.sp_cooldown_for_special = 90000
        self.atk3_cooldown_for_special = 25000

        self.atk1_damage = (0, 0) # buff
        self.atk2_damage = (10/8, 2) # roots arrow +50 mana
        self.atk3_damage = (15/8, 5) # green roots +70 mana
        self.sp_damage = (30/5, 0) # beam +150 mana

        #special
        self.sp_atk2_damage_2nd = (5/8, 0) # poison arrow +30 mana
        self.atk2_damage_2nd = (10/45, 0) # poison 2nd +30 mana
        self.sp_atk3_damage = (25/18, 0) # arrow rain roots +100 mana
        self.sp_damage_2nd = (70/30, 0) # laser beam +170 mana

        # self.damage_to_heal_percentage =

        self.arrow_stuck_duration = 5000
        self.arrow_stuck_damage = (self.basic_attack_damage * 0.3) - 0.05 # total dmg=1
        dmg_mult = 0
        self.atk1_damage = self.atk1_damage[0] + (self.atk1_damage[0] * dmg_mult), self.atk1_damage[1] + (self.atk1_damage[1] * dmg_mult)
        self.atk2_damage = self.atk2_damage[0] + (self.atk2_damage[0] * dmg_mult), self.atk2_damage[1] + (self.atk2_damage[1] * dmg_mult)
        self.atk3_damage = self.atk3_damage[0] + (self.atk3_damage[0] * dmg_mult), self.atk3_damage[1] + (self.atk3_damage[1] * dmg_mult)
        self.sp_damage = self.sp_damage[0] + (self.sp_damage[0] * dmg_mult), self.sp_damage[1] + (self.sp_damage[1] * dmg_mult)

        # (mana cost * multiplier) / skill total damage
        # ex. 100 / 0.5 = 50 / 10 = 5
        # (Skill mana cost / Desired mana refund) * attack total damage (modify the frames of attack)
        # mana refund for arrow is default at 2
        sk1 = 0
        sk2 = 50
        sk3 = 70
        sk4 = 100

        sk2_sp = 30 #x2
        sk3_sp = 100
        sk4_sp = 130
        # desired mana refund / skill damage (REAL)
        self.atk2_mana_refund = (sk2) / (self.atk2_damage[0] * 8 + self.atk2_damage[1])
        self.atk3_mana_refund = (sk3) / (self.atk3_damage[0] * 8 + self.atk3_damage[1])
        self.sp_mana_refund = (sk4) / (self.sp_damage[0] * 5 + self.sp_damage[1])

        self.sp_atk2_mana_refund_2nd = (sk2_sp) / (self.sp_atk2_damage_2nd[0] * 8 + self.sp_atk2_damage_2nd[1]) # poison arrow
        self.atk2_mana_refund_2nd = (sk2_sp) / (self.atk2_damage_2nd[0] * 45 + self.atk2_damage_2nd[1]) # poison 2nd
        self.sp_atk3_mana_refund = (sk3_sp) / (self.sp_atk3_damage[0] * 18 + self.sp_atk3_damage[1]) # arrow rain roots
        self.sp_mana_refund_2nd = (sk4_sp) / (self.sp_damage_2nd[0] * 30 + self.sp_damage_2nd[1]) # laser beam





        # Player Animation Source
        atk3_sp_ani = [r'assets\characters\Forest Ranger\PNG\3_atk\3_atk_', 12, 0]

        jump_ani = [r'assets\characters\Forest Ranger\PNG\jump_full\jump_', 22, 0]
        run_ani = [r'assets\characters\Forest Ranger\PNG\run\run_', 10, 0]
        idle_ani= [r'assets\characters\Forest Ranger\PNG\idle\idle_', 12, 0]
        atk1_ani= [r'assets\characters\Forest Ranger\PNG\roll\roll_', 8, 0]
        atk2_ani= [r'assets\characters\Forest Ranger\PNG\2_atk\2_atk_', 15, 0]
        atk3_ani= [r'assets\characters\Forest Ranger\PNG\air_atk\air_atk_', 10, 0]
        sp_ani= [r'assets\characters\Forest Ranger\PNG\sp_atk\sp_atk_', 17, 0]
        death_ani= [r'assets\characters\Forest Ranger\PNG\death\death_', 19, 0]

        self.atk1_sound = pygame.mixer.Sound(r'assets\sound effects\wanderer_magician\shine-8-268901 1.mp3')
        self.atk2_sound = pygame.mixer.Sound(r'assets\sound effects\wanderer_magician\wind-chimes-2-199848 2.mp3')
        self.atk3_sound = pygame.mixer.Sound(r'assets\sound effects\wanderer_magician\elemental-magic-spell-impact-outgoing-228342 3.mp3')
        self.sp_sound = pygame.mixer.Sound(r'assets\sound effects\wanderer_magician\Rasengan Sound Effect 4.mp3')
        self.atk1_sound.set_volume(0.4 * global_vars.MAIN_VOLUME)
        self.atk2_sound.set_volume(0.5 * global_vars.MAIN_VOLUME)
        self.atk3_sound.set_volume(0.4 * global_vars.MAIN_VOLUME)
        self.sp_sound.set_volume(0.3 * global_vars.MAIN_VOLUME)
        
        # # Player Skill Animations Source
        # basic = [r'assets\attacks\Basic Attack\wanderer magician\Charge_1_', WANDERER_MAGICIAN_BASIC, 1]
        # atk1 = [r'assets\attacks\wanderer magician\atk1\image_', WANDERER_MAGICIAN_ATK1, 1]
        atk2 = [r'assets\attacks\forest ranger\atk2\arrow_hit_entangle_', 8, 0]
        sp_atk2 = [r'assets\attacks\forest ranger\atk2_sp\arrow_hit_poison_', 8, 0]
        atk3 = [r'assets\attacks\forest ranger\atk3\diagonal_arrow_hit_thorns_', 8, 0]
        sp_atk3 = [r'assets\attacks\forest ranger\atk3_sp\arrow_shower_effect_', 18, 0]
        sp = [r'assets\attacks\forest ranger\atk4\beam_extension_effect_', 5, 0]

        # Player Skill Icons Source
        skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\forest_ranger\kkkk.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_2 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\forest_ranger\icon1.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\forest_ranger\icon2.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\forest_ranger\depositphotos_362566930-stock-illustration-vector-green-sun-rays.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_icon = pygame.transform.scale(pygame.image.load(r'assets\skill icons\forest_ranger\special_icon.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        # special_skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\ChatGPT Image Apr 18, 2025, 07_46_01 AM.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_2 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\forest_ranger\poison.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\forest_ranger\icon3.jpeg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\forest_ranger\hq720.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        
        # Player Attack Animations Load
        arrow_size = 2
        self.atk2 = self.load_img_frames(atk2[0], atk2[1], atk2[2], size=arrow_size)
        self.atk2_flipped = self.load_img_frames_flipped(atk2[0], atk2[1], atk2[2], size=arrow_size)
        self.atk3 = self.load_img_frames(atk3[0], atk3[1], atk3[2], size=arrow_size)
        self.atk3_flipped = self.load_img_frames_flipped(atk3[0], atk3[1], atk3[2], size=arrow_size)
        self.sp = self.load_img_frames(sp[0], sp[1], atk3[2], size=5)
        # self.sp_flipped = self.load_img_frames_flipped(sp[0], sp[1], atk3[2], size=5)

        self.sp_atk2 = self.load_img_frames(sp_atk2[0], sp_atk2[1], sp_atk2[2], size=arrow_size)
        self.sp_atk2_flipped = self.load_img_frames_flipped(sp_atk2[0], sp_atk2[1], sp_atk2[2], size=arrow_size)

        self.sp_atk3 = self.load_img_frames(sp_atk3[0], sp_atk3[1], sp_atk3[2], size=arrow_size)
        
        # Attack Skill Frames
        self.base_arrow = [
            pygame.transform.rotozoom(
            pygame.image.load(r"assets\attacks\forest ranger\arrow.png").convert_alpha(),
            angle=0, scale=2.0)
            ]
    
        self.base_arrow_flipped = [
            pygame.transform.flip(
            pygame.transform.rotozoom(
            pygame.image.load(r"assets\attacks\forest ranger\arrow.png").convert_alpha(),
            angle=0, scale=2.0), True, False)
            ]
        self.blank_frame = [
            pygame.transform.rotozoom(
            pygame.image.load(r"assets\attacks\forest ranger\atk4\blank frame\beam_extension_effect_10.png").convert_alpha(),
            angle=0, scale=2.0)
            ]
        
        # Buff
        self.atk1 = load_attack(
        filepath=r"assets\attacks\forest ranger\atk1\1.PNG",
        frame_width=10, 
        frame_height=10, 
        rows=9, 
        columns=5, 
        scale=1, 
        rotation=0,
    )
        

        self.atk2_sp_poison = load_attack(
        filepath=r"assets\attacks\forest ranger\atk2_sp_poison_circle\077.PNG",
        frame_width=10, 
        frame_height=10, 
        rows=10, 
        columns=5, 
        scale=1, 
        rotation=0,
    )
        
        self.sp_special = load_attack(
        filepath=r"assets\attacks\forest ranger\atk4_sp\XY02.PNG",
        frame_width=10, 
        frame_height=10, 
        rows=6, 
        columns=5, 
        scale=8, 
        rotation=-90,
    )
        
        self.sp_special_flipped = load_attack(
        filepath=r"assets\attacks\forest ranger\atk4_sp\XY02.PNG",
        frame_width=10, 
        frame_height=10, 
        rows=6, 
        columns=5, 
        scale=8, 
        rotation=90,
    )

        # Player Animations Load
        self.player_atk3_sp = self.load_img_frames(atk3_sp_ani[0], atk3_sp_ani[1], atk3_sp_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_atk3_sp_flipped = self.load_img_frames_flipped(atk3_sp_ani[0], atk3_sp_ani[1], atk3_sp_ani[2], DEFAULT_CHAR_SIZE_2)

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

        # Player Image and Rect
        self.image = self.player_idle[self.player_idle_index]
        self.rect = self.image.get_rect(midbottom = (self.x_pos, self.y_pos)) #(for p1)
        
        # # Player Icon Rects
        if self.player_type == 1:
            self.skill_1_rect = skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))

            self.special_rect = special_icon.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 4 + 50, SKILL_Y_OFFSET))

            self.special_skill_1_rect = skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.special_skill_2_rect = special_skill_2.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.special_skill_3_rect = special_skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.special_skill_4_rect = special_skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))

        elif self.player_type == 2:
            self.special_rect = special_icon.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 4 - 50, SKILL_Y_OFFSET))

            self.special_skill_1_rect = skill_1.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 3, SKILL_Y_OFFSET))
            self.special_skill_2_rect = special_skill_2.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 2, SKILL_Y_OFFSET))
            self.special_skill_3_rect = special_skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X, SKILL_Y_OFFSET))
            self.special_skill_4_rect = special_skill_4.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X, SKILL_Y_OFFSET))

            self.skill_1_rect = skill_1.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 3, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X, SKILL_Y_OFFSET))

        # Mana Values
        self.mana_cost_list = [
            self.atk1_mana_cost,
            self.atk2_mana_cost,
            self.atk3_mana_cost,
            self.sp_mana_cost
            ]

        # Modify
        self.lowest_mana_cost = self.mana_cost_list[1]

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
                skill_img=self.basic_icon3,
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
                skill_img=skill_1,
                cooldown=self.atk1_cooldown,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.mana_cost_list[1],
                skill_rect=self.special_skill_2_rect,
                skill_img=special_skill_2,
                cooldown=self.atk2_cooldown,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.atk3_mana_cost_for_special,
                skill_rect=self.special_skill_3_rect,
                skill_img=special_skill_3,
                cooldown=self.atk3_cooldown_for_special,
                mana=self.mana
            ),
            Attacks(
                mana_cost=self.sp_mana_cost_for_special,
                skill_rect=self.special_skill_4_rect,
                skill_img=special_skill_4,
                cooldown=self.sp_cooldown_for_special,
                mana=self.mana
            )
        ]

        self.attacks_special.append(
            Attacks(
                mana_cost=0,
                skill_rect=self.basic_icon_rect,
                skill_img=self.basic_icon3,
                cooldown=self.basic_attack_cooldown,
                mana=self.mana
            )
        )
   
        # Regen Rate
        self.hp_regen_rate = DEFAULT_HEALTH_REGENERATION
        self.mana_regen_rate = DEFAULT_MANA_REGENERATION

        # After Bar Reduces
        self.white_health_p1 = self.health
        self.white_mana_p1 = self.mana
        self.white_health_p2 = self.health
        self.white_mana_p2 = self.mana   


        # Trait: + 20% attack speed
        self.basic_attack_animation_speed = self.basic_attack_animation_speed-(self.basic_attack_animation_speed*0.2)
        # Trait: + 15% lifesteal
        self.lifesteal = 0.1
        # Trait : + (some values)% mana refund if hits enemy

        self.atk_hasted = False
        self.was_hasted = False
        self.atk_haste_duration = 0
        self.haste_value = DEFAULT_ANIMATION_SPEED #(120) #default, change in skill 1 config
        self.default_atk_speed = self.basic_attack_animation_speed

        self.jump_attack_pending = False
        self.jump_attack_time = 0
        self.get_jump_pos = 0
        self.jump_done = False
        self.jump_time = 0

        self.distance_covered = 0
        self.max_distance = 200
        self.dash_speed = 5

        # initialize current attack speed snapshot from base value
        self.get_current_atk_speed = self.basic_attack_animation_speed
        

    # Will modify the attack speed of forest ranger when basic attacking

    def atk2_animation(self, animation_speed=0):
        if self.facing_right:
            self.player_atk2_index, anim_active = self.animate(self.player_atk2, self.player_atk2_index, loop=False, basic_atk=False)
        else:
            self.player_atk2_index_flipped, anim_active = self.animate(self.player_atk2_flipped, self.player_atk2_index_flipped, loop=False, basic_atk=False)

        self.last_atk_time -= animation_speed

        if not anim_active:
            self.attacking2 = False
            self.basic_attacking = False  # Only matters if this was a basic attack
            self.player_atk2_index = 0
            self.player_atk2_index_flipped = 0    

    def atk3_animation(self, animation_speed=0):
        if not self.special_active:
            if self.facing_right:
                self.player_atk3_index, self.attacking3 = self.animate(self.player_atk3, self.player_atk3_index, loop=False)
            else:
                self.player_atk3_index_flipped, self.attacking3 = self.animate(self.player_atk3_flipped, self.player_atk3_index_flipped, loop=False)
        else:
            if self.facing_right:
                self.player_atk3_index, self.attacking3 = self.animate(self.player_atk3_sp, self.player_atk3_index, loop=False)
            else:
                self.player_atk3_index_flipped, self.attacking3 = self.animate(self.player_atk3_sp_flipped, self.player_atk3_index_flipped, loop=False)

        self.last_atk_time -= animation_speed

    def basic_animation(self, animation_speed=0): # will make the atk_haste False
        if self.facing_right:
            self.player_basic_index, self.basic_attacking, _ = self.animate(self.player_basic, self.player_basic_index, loop=False, basic_atk=True)
        else:
            self.player_basic_index_flipped, self.basic_attacking, _ = self.animate(self.player_basic_flipped, self.player_basic_index_flipped, loop=False, basic_atk=True)

        self.last_atk_time -= animation_speed

    def haste_atk(self, current_atk_speed, bonus_value=500):
        # Deprecated: haste now handled through attack_speed bonuses
        return current_atk_speed
    
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
                speed_modifier = 0.15,
                special_active_speed = 0.25,
                jump_force = self.jump_force,
                jump_force_modifier = 0.05
                )
            
        # ---------- Casting ----------
        if self.is_frozen():
            return
        
        if self.is_silenced() and not basic_hotkey:
            return
        
        if not self.special_active:
            if not self.jumping and not self.is_dead():
                if hotkey1 and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks[0].mana_cost and self.attacks[0].is_ready():
                        
                        attack = Attack_Display(
                            x=self.rect.centerx,
                            y=self.rect.centery + 0,
                            frames=self.atk1,
                            frame_duration=111.11, # 5 seconds (4999.95) (45 frames * duration(5000) = 111.11)
                            repeat_animation=1,
                            speed=7 if self.facing_right else -7,
                            dmg=0,
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=self.enemy,
                            follow=(False,True),
                            follow_offset=(0,60),
                            disable_collide=True,
                            follow_self=True,
                            sound=(True, self.atk1_sound , None, None),
                            delay=(True, 500),
                            ) # Replace with the target
                        attack_display.add(attack)

                        #speed buff
                        # increase speed for self
                        attack2 = Attack_Display(
                            x=self.rect.centerx,
                            y=self.rect.centery + 0,
                            frames=self.blank_frame,
                            frame_duration=5000, # 5 seconds
                            repeat_animation=1,
                            speed=0,
                            dmg=0,
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=[self],
                            follow=(True,False),
                            disable_collide=True,
                            follow_self=True,
                            follow_offset=(0, 40),
                            sound=(True, self.atk1_sound , None, None),
                            delay=(True, 500),
                            stop_movement=(True, 3, 3, 1.2),
                            ) # Replace with the target
                        attack_display.add(attack2)
                        self.mana -=  self.attacks[0].mana_cost
                        self.attacks[0].last_used_time = current_time
                        self.running = False
                        self.attacking1 = True
                        self.player_atk1_index = 0
                        self.player_atk1_index_flipped = 0

                        if not self.atk_hasted:
                            self.atk_hasted = True
                            self.haste_value = 300  # Attack speed bonus
                            self.atk_haste_duration = (pygame.time.get_ticks() + 611.11) + 5000
                            self.default_atk_speed = self.basic_attack_animation_speed  # Store the current attack speed as default
                        
 
                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 1 used')


                elif hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks[1].mana_cost and self.attacks[1].is_ready():
 

                        self.single_target()

                        attack = Attack_Display(
                            x=self.rect.centerx,
                            y=self.rect.centery + 60,
                            frames=self.base_arrow if self.facing_right else self.base_arrow_flipped,
                            frame_duration=5,
                            repeat_animation=1000,
                            speed=30 if self.facing_right else -30,
                            dmg=self.basic_attack_damage,
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=self.enemy,
                            moving=True,
                            sound=(True, self.atk1_sound, None, None),
                            kill_collide=True,                              # self.basic_attack_animation_speed * (Base Delay/Default Basic Attack Speed)
                            delay=(True, self.basic_attack_animation_speed * (1100 / DEFAULT_ANIMATION_SPEED)), #120*9.16667 = 1100 -> attack delay

                            hitbox_scale_x=0.1,
                            hitbox_scale_y=0.1,

                            add_mana=True,
                            mana_mult=2,

                            spawn_attack= {
                            'use_attack_onhit_pos': True,

                            'attack_kwargs': {
                                'frames': self.atk2 if self.facing_right else self.atk2_flipped,
                                'frame_duration': 187.5, # Root for 1.5s
                                'repeat_animation': 1,
                                'speed': 0,
                                'dmg': self.atk2_damage[0],
                                'final_dmg': self.atk2_damage[1],
                                'who_attacks': self,
                                'who_attacked': self.target,
                                'moving': False,
                                'sound': (True, self.atk2_sound, None, None),
                                'delay': (False, 0),
                                'stop_movement': (True, 2, 1),
                                'follow': (True, False),
                                'follow_offset': (-30 if self.facing_right else 30, random.randint(30, 45)),
                                'add_mana': True,
                                'mana_mult': self.atk2_mana_refund,
                                'hitbox_scale_x': 0.3,
                                'hitbox_scale_y': 0.3,

                                # leave arrow bullets
                                'spawn_attack':  {

                                    'attack_kwargs': {
                                        'x': self.target.x_pos,
                                        'y': self.target.y_pos + (random.randint(-40, 3)),
                                        'frames': self.base_arrow if self.facing_right else self.base_arrow_flipped,
                                        'frame_duration': self.arrow_stuck_duration, # slow for 1s (second / frames)
                                        'repeat_animation': 1,
                                        'speed': 0,
                                        'dmg': 0,
                                        'final_dmg': self.arrow_stuck_damage,
                                        'who_attacks': self,
                                        'who_attacked': self.target,
                                        'moving': False,
                                        'sound': (False, self.atk2_sound, None, None),
                                        'delay': (False, 0),
                                        'stop_movement': (False, 3, 2, 0.2),
                                        'follow': (False, True),
                                        'follow_offset': (random.randint(-30, 30), (random.randint(30, 45))),
                                        'add_mana': True,
                                        # 'mana_mult': self.sp_atk2_mana_refund_2nd,
                                        'hitbox_scale_x': 0.1,
                                        'hitbox_scale_y': 0.1,
                                    }
                                }
                            }
                        }
                            ,is_basic_attack=True
                            )
                        attack_display.add(attack)
                        self.mana -=  self.attacks[1].mana_cost
                        self.attacks[1].last_used_time = current_time
                        self.running = False
                        self.attacking2 = True
                        self.player_atk2_index = 0
                        self.player_atk2_index_flipped = 0

                        self.basic_attacking = True

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 2 used')

                elif hotkey3 and not self.attacking3 and not self.attacking1 and not self.attacking2 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >= self.attacks[2].mana_cost and self.attacks[2].is_ready():
                        self.jumping = True
                        self.jump_done = False
                        self.y_velocity = DEFAULT_JUMP_FORCE  # adjust jump strength as needed
                        self.jump_attack_pending = True
                        self.jump_attack_time = pygame.time.get_ticks() + 400  #  delay time before performing the attack
                        self.jump_time = pygame.time.get_ticks() + 1700 # time before falling down and stopping the  jump (attack done)
                        
                        
                        # attack = Attack_Display(
                        #     x=self.rect.centerx, # in front of him
                        #     y=self.rect.centery + 20,
                        #     frames=self.atk3,
                        #     frame_duration=100,
                        #     repeat_animation=1,
                        #     speed=5 if self.facing_right else -5,
                        #     dmg=self.atk3_damage[0],
                        #     final_dmg=self.atk3_damage[1],
                        #     who_attacks=self,
                        #     who_attacked=self.enemy,
                        #     sound=(True, self.atk3_sound , None, None),
                        #     delay=(True, 800),
                        #     moving=True
                        #     ) # Replace with the target
                        # attack_display.add(attack)
                        # print(WANDERER_MAGICIAN_ATK3_DAMAGE[0], WANDERER_MAGICIAN_ATK3_DAMAGE[1])
                        # self.mana -=  self.attacks[2].mana_cost
                        # self.attacks[2].last_used_time = current_time
                        # self.running = False
                        # self.attacking3 = True
                        # self.player_atk3_index = 0
                        # self.player_atk3_index_flipped = 0

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 3 used')
                elif hotkey4 and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >=  self.attacks[3].mana_cost and self.attacks[3].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx + 650 if self.facing_right else self.rect.centerx - 650, # in front of him
                            y=DEFAULT_Y_POS-50,
                            frames=self.sp,
                            frame_duration=100,
                            repeat_animation=1,
                            dmg=self.sp_damage[0],
                            final_dmg=self.sp_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            sound=(True, self.sp_sound , None, None),
                            delay=(True, 1200),

                            hitbox_scale_x=1,
                            hitbox_scale_y=0.10,

                            add_mana=True,
                            mana_mult=self.sp_mana_refund,
                            
                            # heals self if it hits enemy  (only heal for 50% of damage)
                            spawn_attack= {
                                'attack_kwargs': {
                                    'x': self.rect.centerx,
                                    'y': self.rect.centery,
                                    'frames': self.blank_frame,
                                    'frame_duration': 50, # slow for 1s (second / frames)
                                    'repeat_animation': 1,
                                    'speed': 0,
                                    'dmg': (self.sp_damage[0]*5)*0.5,
                                    'final_dmg': 0,
                                    'heal': True,
                                    'who_attacks': self,
                                    'who_attacked': self.enemy,
                                    'moving': False,
                                    'sound': (False, self.atk2_sound, None, None),
                                    'follow': (False, True),
                                    'follow_self': True
                                    }
                                }
                            ) 
                        attack_display.add(attack)
                        self.mana -=  self.attacks[3].mana_cost
                        # self.display_damage(50, interval=30, color=cyan2, size=50)
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

                elif not self.is_dead() and not self.jumping and basic_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >= 0 and self.can_basic_attack():
 

                        self.single_target()

                        attack = Attack_Display(
                            x=self.rect.centerx,
                            y=self.rect.centery + 60,
                            frames=self.base_arrow if self.facing_right else self.base_arrow_flipped,
                            frame_duration=5,
                            repeat_animation=1000,
                            speed=30 if self.facing_right else -30,
                            dmg=self.basic_attack_damage,
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=self.enemy,
                            moving=True,
                            sound=(True, self.atk1_sound, None, None),
                            kill_collide=True,                              # self.basic_attack_animation_speed * (Base Delay/Default Basic Attack Speed)
                            delay=(True, self.basic_attack_animation_speed * (1100 / DEFAULT_ANIMATION_SPEED)), # (1100/120=9.16667): 120*9.16667 = 1100 -> attack delay

                            hitbox_scale_x=0.1,
                            hitbox_scale_y=0.1,

                            add_mana=True,
                            mana_mult=2,
                            
                            # leave arrow bullets
                            spawn_attack= {

                                'attack_kwargs': {
                                    'x': self.target.x_pos,
                                    'y': self.target.y_pos + (random.randint(-40, 3)),
                                    'frames': self.base_arrow if self.facing_right else self.base_arrow_flipped,
                                    'frame_duration': self.arrow_stuck_duration, # slow for 1s (second / frames)
                                    'repeat_animation': 1,
                                    'speed': 0,
                                    'dmg': 0,
                                    'final_dmg': self.arrow_stuck_damage,
                                    'who_attacks': self,
                                    'who_attacked': self.target,
                                    'moving': False,
                                    'sound': (False, self.atk2_sound, None, None),
                                    'delay': (False, 0),
                                    'stop_movement': (False, 3, 2, 0.2),
                                    'follow': (False, True),
                                    'follow_offset': (random.randint(-30, 30), (random.randint(30, 45))),
                                    'add_mana': True,
                                    # 'mana_mult': self.sp_atk2_mana_refund_2nd,
                                    'hitbox_scale_x': 0.1,
                                    'hitbox_scale_y': 0.1,
                                    }
                                }
                            ,is_basic_attack=True
                            )
                        # self.atk_haste_duration = pygame.time.get_ticks()
                        # print(self.basic_attack_animation_speed) #120
                        # print(self.atk_haste_duration)
                        attack_display.add(attack)
                        self.mana -= 0
                        # self.display_damage(50, interval=30, color=cyan2, size=50)
                        self.attacks[4].last_used_time = current_time
                        self.running = False
                        self.attacking2 = True
                        self.player_atk2_index = 0
                        self.player_atk2_index_flipped = 0

                        self.basic_attacking = True
                        self.last_basic_attack_time = current_time

                        # print("Attack executed")
                    else:
                        pass

                elif special_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.special >= MAX_SPECIAL: # and self.attacks[5].special_is_ready(self.special)
                        self.special_active = True
                        self.basic_sound.play()
                    else:
                        pass






        else:
            if not self.jumping and not self.is_dead():
                if hotkey1 and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[0].mana_cost and self.attacks_special[0].is_ready():
                        attack = Attack_Display(
                            x=self.rect.centerx,
                            y=self.rect.centery + 0,
                            frames=self.atk1,
                            frame_duration=111.11, # 5 seconds (4999.95) (45 frames * duration(5000) = 111.11)
                            repeat_animation=1,
                            speed=7 if self.facing_right else -7,
                            dmg=0,
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=self.enemy,
                            follow=(False,True),
                            follow_offset=(0,60),
                            disable_collide=True,
                            follow_self=True,
                            sound=(True, self.atk1_sound , None, None),
                            delay=(True, 500)
                            ) # Replace with the target
                        attack_display.add(attack)

                        #speed buff
                        # increase speed for self
                        attack2 = Attack_Display(
                            x=self.rect.centerx,
                            y=self.rect.centery + 0,
                            frames=self.blank_frame,
                            frame_duration=5000, # 5 seconds
                            repeat_animation=1,
                            speed=0,
                            dmg=0,
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=self,
                            follow=(True,False),
                            disable_collide=True,
                            follow_self=True,
                            follow_offset=(0, 40),
                            sound=(True, self.atk1_sound , None, None),
                            delay=(True, 500),
                            stop_movement=(True, 3, 3, 1.4),
                            ) # Replace with the target
                        attack_display.add(attack2)
                        self.mana -=  self.attacks_special[0].mana_cost
                        self.attacks_special[0].last_used_time = current_time
                        self.running = False
                        self.attacking1 = True
                        self.player_atk1_index = 0
                        self.player_atk1_index_flipped = 0

                        if not self.atk_hasted:
                            self.atk_hasted = True
                            self.haste_value = 350  # Attack speed bonus
                            self.atk_haste_duration = (pygame.time.get_ticks() + 611.11) + 5000
                            self.default_atk_speed = self.basic_attack_animation_speed  # Store the current attack speed as default

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 1 used')


                elif hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[1].mana_cost and self.attacks_special[1].is_ready():
 

                        self.single_target()

                        attack = Attack_Display(
                            x=self.rect.centerx,
                            y=self.rect.centery + 60,
                            frames=self.base_arrow if self.facing_right else self.base_arrow_flipped,
                            frame_duration=5,
                            repeat_animation=1000,
                            speed=30 if self.facing_right else -30,
                            dmg=self.basic_attack_damage,
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=self.enemy,
                            moving=True,
                            sound=(True, self.atk1_sound, None, None),
                            kill_collide=True,                              # self.basic_attack_animation_speed * (Base Delay/Default Basic Attack Speed)
                            delay=(True, self.basic_attack_animation_speed * (1100 / DEFAULT_ANIMATION_SPEED)), #120*9.16667 = 1100 -> attack delay

                            hitbox_scale_x=0.1,
                            hitbox_scale_y=0.1,

                            add_mana=True,
                            mana_mult=2,

                            spawn_attack= {
                            'use_attack_onhit_pos': True,

                            'attack_kwargs': {
                                'frames': self.sp_atk2 if self.facing_right else self.sp_atk2_flipped,
                                'frame_duration': 125, # slow for 1s (second / frames)
                                'repeat_animation': 1,
                                'speed': 0,
                                'dmg': self.sp_atk2_damage_2nd[0],
                                'final_dmg': self.sp_atk2_damage_2nd[1],
                                'who_attacks': self,
                                # Do NOT preassign who_attacked here; let the spawned attack resolve the actual collided enemy.
                                'moving': False,
                                'sound': (True, self.atk2_sound, None, None),
                                'delay': (False, 0),
                                'stop_movement': (True, 3, 2, 0.2),
                                'follow': (True, False),
                                # Use a conservative follow vertical offset; avoid sampling target hitbox at cast time
                                'follow_offset': (-30 if self.facing_right else 30, (random.randint(30, 45))),
                                'add_mana': True,
                                'mana_mult': self.sp_atk2_mana_refund_2nd,
                                'hitbox_scale_x': 0.3,
                                'hitbox_scale_y': 0.3,
                                'spawn_attack': {
                                                'use_attack_onhit_pos': True,

                                                'attack_kwargs': {
                                                    'frames': self.atk2_sp_poison,
                                                    'frame_duration': 40, # slow 2s (second / frames)
                                                    'repeat_animation': 1,
                                                    'speed': 0,
                                                    'dmg': self.atk2_damage_2nd[0],
                                                    'final_dmg': self.atk2_damage_2nd[1],
                                                    'who_attacks': self,
                                                    # Defer who_attacked resolution to collision time
                                                    'sound': (True, self.atk2_sound, None, None),
                                                    'delay': (True, 1050),
                                                    'stop_movement': (True, 3, 2, 0.5),
                                                    'follow': (False, True),
                                                    # Avoid using target hitbox at cast; keep vertical small
                                                    'follow_offset': (0, (random.randint(30, 45))),
                                                    'add_mana': True,
                                                    'mana_mult': self.atk2_mana_refund_2nd,
                                                    'hitbox_scale_x': 0.3,
                                                    'hitbox_scale_y': 0.3,
                                                    
                                                    # leave arrow bullets
                                                    'spawn_attack': {

                                                        'attack_kwargs': {
                                                            # Do not hardcode x/y to the preselected target; spawn at collision point instead
                                                            'frames': self.base_arrow if self.facing_right else self.base_arrow_flipped,
                                                            'frame_duration': self.arrow_stuck_duration, # slow for 1s (second / frames)
                                                            'repeat_animation': 1,
                                                            'speed': 0,
                                                            'dmg': 0,
                                                            'final_dmg': self.arrow_stuck_damage,
                                                            'who_attacks': self,
                                                            # who_attacked deliberately omitted so Attack_Display will assign collided enemy
                                                            'moving': False,
                                                            'sound': (False, self.atk2_sound, None, None),
                                                            'delay': (False, 0),
                                                            'stop_movement': (False, 3, 2, 0.2),
                                                            'follow': (False, True),
                                                            'follow_offset': (random.randint(-30, 30), random.randint(-40, 80)),
                                                            'add_mana': True,
                                                            # 'mana_mult': self.sp_atk2_mana_refund_2nd,
                                                            'hitbox_scale_x': 0.1,
                                                            'hitbox_scale_y': 0.1,
                                                            }
                                                        }
                                                }
                                                
                                            }
                            }
                            
                        }
                            )
                        attack_display.add(attack)
                        self.mana -=  self.attacks_special[1].mana_cost
                        self.attacks_special[1].last_used_time = current_time
                        self.running = False
                        self.attacking2 = True
                        self.player_atk2_index = 0
                        self.player_atk2_index_flipped = 0

                        self.basic_attacking = True

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 2 used')

                elif hotkey3 and not self.attacking3 and not self.attacking1 and not self.attacking2 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[2].mana_cost and self.attacks_special[2].is_ready():
                        self.single_target()
                        target, target_detected = self.face_selective_target()
                        if not target_detected:
                            target = self.rect.centerx + (200 if self.facing_right else -200)  # Default to casting in front

                        attack = Attack_Display(
                            x=target,
                            y=DEFAULT_Y_POS - 100,
                            frames=self.sp_atk3,
                            frame_duration=111.111,
                            repeat_animation=1,
                            dmg=self.sp_atk3_damage[0],
                            final_dmg=self.sp_atk3_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            sound=(True, self.atk3_sound, None, None),
                            delay=(True, 1750),
                            follow=(False, target_detected),
                            follow_offset=(0, -50),
                            stop_movement=(True, 2, 2),
                            hitbox_scale_x=0.35,
                            hitbox_scale_y=1,
                            add_mana=True,
                            mana_mult=self.sp_atk3_mana_refund,
                                                        
                            # leave arrow bullets
                            spawn_attack= {

                                'attack_kwargs': {
                                    'x': self.target.x_pos,
                                    'y': self.target.y_pos + (random.randint(-40, 3)),
                                    'frames': self.base_arrow if self.facing_right else self.base_arrow_flipped,
                                    'frame_duration': self.arrow_stuck_duration, # slow for 1s (second / frames)
                                    'repeat_animation': 1,
                                    'speed': 0,
                                    'dmg': 0,
                                    'final_dmg': self.arrow_stuck_damage,
                                    'who_attacks': self,
                                    'who_attacked': self.enemy,
                                    'moving': False,
                                    'sound': (False, self.atk2_sound, None, None),
                                    'delay': (False, 0),
                                    'stop_movement': (False, 3, 2, 0.2),
                                    'follow': (False, True),
                                    'follow_offset': (random.randint(-30, 30), (random.randint(30, 45))),
                                    'add_mana': True,
                                    # 'mana_mult': self.sp_atk2_mana_refund_2nd,
                                    'hitbox_scale_x': 0.1,
                                    'hitbox_scale_y': 0.1,
                                    }
                                }

                        )
                        attack_display.add(attack)
                        self.mana -= self.attacks_special[2].mana_cost
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
                        attack = Attack_Display(
                            x=self.rect.centerx + 540 if self.facing_right else self.rect.centerx-540, # in front of him
                            y=DEFAULT_Y_POS-50,
                            frames=self.sp_special if self.facing_right else self.sp_special_flipped,
                            frame_duration=66.6666667, #2s(66.6666667), 1s(33.3333333)
                            repeat_animation=1,
                            dmg=self.sp_damage_2nd[0],
                            final_dmg=self.sp_damage_2nd[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            sound=(True, self.sp_sound , None, None),
                            delay=(True, 1200),

                            hitbox_scale_x=0.8,
                            hitbox_scale_y=1,

                            add_mana=True,
                            mana_mult=self.sp_mana_refund_2nd,

                            # heals self if it hits enemy once (once only 50% dmg) only heals 50% now! update!
                            spawn_attack= {
                                'attack_kwargs': {
                                    'x': self.rect.centerx,
                                    'y': self.rect.centery,
                                    'frames': self.blank_frame,
                                    'frame_duration': 50, # slow for 1s (second / frames)
                                    'repeat_animation': 1,
                                    'speed': 0,
                                    'dmg': (self.sp_damage_2nd[0]*30)*0.5,
                                    'final_dmg': 0,
                                    'heal': True,
                                    'who_attacks': self,
                                    'who_attacked': self.enemy,
                                    'moving': False,
                                    'sound': (False, self.atk2_sound, None, None),
                                    'follow': (False, True),
                                    'follow_self': True
                                    }
                                }
                            )
                        attack_display.add(attack)
                        self.mana -=  self.attacks_special[3].mana_cost
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

                elif not self.is_dead() and not self.jumping and basic_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >= 0 and self.can_basic_attack():
 

                        self.single_target()

                        attack = Attack_Display(
                            x=self.rect.centerx,
                            y=self.rect.centery + 60,
                            frames=self.base_arrow if self.facing_right else self.base_arrow_flipped,
                            frame_duration=2,
                            repeat_animation=2500,
                            speed=40 if self.facing_right else -40,
                            dmg=self.basic_attack_damage*1.2, # +20% damage in special mode
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=self.enemy,
                            moving=True,
                            sound=(True, self.atk1_sound, None, None),
                            kill_collide=True,                              # self.basic_attack_animation_speed * (Base Delay/Default Basic Attack Speed)
                            delay=(True, self.basic_attack_animation_speed * (1100 / DEFAULT_ANIMATION_SPEED)), # (1100/120=9.16667): 120*9.16667 = 1100 -> attack delay
                            hitbox_scale_x=0.1,
                            hitbox_scale_y=0.1,

                            add_mana=True,
                            mana_mult=2,

                            # leave arrow bullets
                            spawn_attack= {

                                'attack_kwargs': {
                                    'x': self.target.x_pos,
                                    'y': self.target.y_pos + (random.randint(-40, 3)),
                                    'frames': self.base_arrow if self.facing_right else self.base_arrow_flipped,
                                    'frame_duration': self.arrow_stuck_duration, # slow for 1s (second / frames)
                                    'repeat_animation': 1,
                                    'speed': 0,
                                    'dmg': 0,
                                    'final_dmg': self.arrow_stuck_damage,
                                    'who_attacks': self,
                                    'who_attacked': self.target,
                                    'moving': False,
                                    'sound': (False, self.atk2_sound, None, None),
                                    'delay': (False, 0),
                                    'stop_movement': (False, 3, 2, 0.2),
                                    'follow': (False, True),
                                    'follow_offset': (random.randint(-30, 30), (random.randint(30, 45))),
                                    'add_mana': True,
                                    # 'mana_mult': self.sp_atk2_mana_refund_2nd,
                                    'hitbox_scale_x': 0.1,
                                    'hitbox_scale_y': 0.1,
                                    }
                                }
                            ,
                            is_basic_attack=True
                            )
                        # self.atk_haste_duration = pygame.time.get_ticks()
                        # print(self.basic_attack_animation_speed) #120
                        # print(self.atk_haste_duration)
                        attack_display.add(attack)
                        self.mana -= 0
                        # self.display_damage(50, interval=30, color=cyan2, size=50)
                        self.attacks_special[4].last_used_time = current_time
                        self.running = False
                        self.attacking2 = True
                        self.player_atk2_index = 0
                        self.player_atk2_index_flipped = 0

                        self.basic_attacking = True
                        self.last_basic_attack_time = current_time

                        # print("Attack executed")
                    else:
                        pass

        # print(self.running)
        # print(self.player_type)
        # print(len(self.player_run), len(self.player_run_flipped))
        # print("Run Animation Index:", self.player_run_index)

     
    def trigger_dash(self): # this thing so buggy, fix this soon
        if self.distance_covered >= self.max_distance:
            self.distance_covered = 0
        else:
            if self.facing_right:
                self.x_pos += self.dash_speed
                self.distance_covered += self.dash_speed
            elif not self.facing_right:
                self.x_pos -= self.dash_speed
                self.distance_covered += self.dash_speed
            

    def update(self):
        
        # print(self.stunned)
        current_time_ticks = pygame.time.get_ticks() - global_vars.PAUSED_TOTAL_DURATION

        # print(self.distance_covered)
        if not self.is_dead():
            self.player_death_index = 0
            self.player_death_index_flipped = 0
        if self.is_dead():
            self.play_death_animation()
        elif self.attacking1:
            self.activate_dash = True
            if self.distance_covered >= self.max_distance:
                self.attacking1 = False
                self.distance_covered = 0
                self.activate_dash = False
                
                
            else: 
                if self.activate_dash:
                    self.trigger_dash()
            self.atk1_animation()
        elif self.jumping:
            self.jump_animation()
        elif self.running and not self.jumping:
            self.run_animation(self.running_animation_speed)
        elif self.attacking2:
            self.atk2_animation()
        elif self.attacking3:
            self.atk3_animation()
        elif self.sp_attacking:
            self.sp_animation() #fix the sp animation become attack 3 when special.
        elif self.basic_attacking:
            pass

        else:
            self.simple_idle_animation(RUNNING_ANIMATION_SPEED)

        # Apply gravity
        self.y_velocity += DEFAULT_GRAVITY
        self.y_pos += self.y_velocity

        

        # print(self.basic_attack_animation_speed)
        # print(f'cd:{self.basic_attack_cooldown}')
        # Update the player's position
        self.rect.midbottom = (self.x_pos, self.y_pos)

        # # Base and Bonus Attack Speed Variables
        # print(f"base_attack_speed: {self.base_attack_speed}")  # 300 (fire wizard specific)
        # print(f"base_attack_time: {self.base_attack_time}")    # 1700 (milliseconds)
        # print(f"bonus_attack_speed_flat: {self.bonus_attack_speed_flat}")  # 0
        # print(f"bonus_attack_speed_per: {self.bonus_attack_speed_per}")    # 0.0

        # # Calculated Attack Speed Values
        # print(f"attack_speed (effective): {self.attack_speed}")  # Calculated via calculate_effective_as()
        # print(f"basic_attack_cooldown: {self.basic_attack_cooldown}")  # Calculated via calculate_basic_attack_interval()
        # print(f"basic_attack_animation_speed: {self.basic_attack_animation_speed}")  # Calculated based on attack speed

        # # Timing and State Variables
        # print(f"last_basic_attack_time: {self.last_basic_attack_time}")  # Timestamp of last basic attack

        # # Related Constants (from global_vars)
        # print(f"AGILITY_AS_BONUS: {global_vars.AGILITY_AS_BONUS}")  # 1 (+1 AS per agility point)
        # print(f"BASIC_ATK_COOLDOWN: {global_vars.BASIC_ATK_COOLDOWN}")  # 500 (fallback cooldown in ms)
        # print(f"DEFAULT_ANIMATION_SPEED: {global_vars.DEFAULT_ANIMATION_SPEED}")  # 120 (frames per second)
        # print(f"MAX_ATTACK_SPEED: {global_vars.MAX_ATTACK_SPEED}")  # 700 (fastest cap)
        # print(f"MIN_ATTACK_SPEED: {global_vars.MIN_ATTACK_SPEED}")  # 20 (slowest cap)

        # # Method Results
        # print(f"calculate_effective_as(): {self.calculate_effective_as()}")  # Current effective attack speed
        # print(f"calculate_basic_attack_interval(): {self.calculate_basic_attack_interval()}")  # Current interval in ms
        # print(f"can_basic_attack(): {self.can_basic_attack()}")  # Boolean: ready to attack?
         
        
        # Update the health and mana bars
        if self.health != 0:
            if not DISABLE_MANA_REGEN:
                self.mana += (self.mana_regen + (self.mana_regen * (0.20 if not self.special_active else 0.30)))
            if not DISABLE_HEAL_REGEN:
                self.health += self.health_regen
        else:
            self.health = 0

        if not global_vars.DISABLE_SPECIAL_REDUCE:
            if self.special_active:
                self.special -= SPECIAL_DURATION
                if self.special <= 0:
                    self.special_active = False

        # print(self.basic_attack_animation_speed)
        if self.atk_hasted and not self.was_hasted:
            self.bonus_attack_speed_flat += self.haste_value
            self.speed = self.default_speed * 1.5  # increase move speed
            self.attack_speed = self.calculate_effective_as()
            self.basic_attack_cooldown = self.calculate_basic_attack_interval()
            self.basic_attack_animation_speed = global_vars.DEFAULT_ANIMATION_SPEED / (self.attack_speed / self.base_attack_speed)
            self.attacks[4].cooldown = self.basic_attack_cooldown
            self.attacks_special[4].cooldown = self.basic_attack_cooldown
            self.was_hasted = True
        elif not self.atk_hasted and self.was_hasted:
            self.bonus_attack_speed_flat -= self.haste_value
            self.speed = self.default_speed  # reset move speed
            self.attack_speed = self.calculate_effective_as()
            self.basic_attack_cooldown = self.calculate_basic_attack_interval()
            self.basic_attack_animation_speed = global_vars.DEFAULT_ANIMATION_SPEED / (self.attack_speed / self.base_attack_speed)
            self.attacks[4].cooldown = self.basic_attack_cooldown
            self.attacks_special[4].cooldown = self.basic_attack_cooldown
            self.was_hasted = False
        if self.atk_hasted and current_time_ticks >= self.atk_haste_duration:
            self.atk_hasted = False

        # atk3
        if not self.jump_attack_pending and not self.jump_done: # freeze y_pos when attacking starts
            # prevent going to y 0
            if not self.get_jump_pos <= 0:
                self.y_pos = self.get_jump_pos
        if not self.jump_done and pygame.time.get_ticks() >= self.jump_time: #
            self.jump_done = True
            self.jumping = True
            self.y_velocity = 0
        if self.jump_attack_pending and pygame.time.get_ticks() >= self.jump_attack_time:
            self.get_jump_pos = self.y_pos # get current y_pos to freeze when attacking
            self.jump_attack_pending = False # attacking starts
            self.jumping = False # override jumping animation with attack animation
            # enemy_posx = (hero1.x_pos if self.player_type == 2 else hero2.x_pos)
            # enemy_posy = (hero1.rect.centery if self.player_type == 2 else hero2.rect.centery)
            for i in [100,250,400]:
                self.single_target()
                attack = Attack_Display(
                    x=self.rect.centerx + i if self.facing_right else self.rect.centerx - i,
                    y=DEFAULT_Y_POS-20,
                    frames=self.atk3 if self.facing_right else self.atk3_flipped,
                    frame_duration=250,
                    repeat_animation=1,
                    speed=5 if self.facing_right else -5,
                    dmg=self.atk3_damage[0],
                    final_dmg=self.atk3_damage[1],
                    who_attacks=self,
                    who_attacked=self.enemy,
                    sound=(True, self.atk3_sound , None, None),
                    delay=(True, 600+i), #starting 700

                    hitbox_scale_x=0.15,
                    hitbox_scale_y=0.5,
                    hitbox_offset_x=20,

                    stop_movement=(True, 2, 1),

                    add_mana=True,
                    mana_mult=self.atk3_mana_refund
                    ,
                    # leave arrow bullets
                            spawn_attack= {
                                'attack_kwargs': {
                                    'x': self.target.x_pos,
                                    'y': self.target.y_pos + (random.randint(-40, 3)),
                                    'frames': self.base_arrow if self.facing_right else self.base_arrow_flipped,
                                    'frame_duration': self.arrow_stuck_duration, # slow for 1s (second / frames)
                                    'repeat_animation': 1,
                                    'speed': 0,
                                    'dmg': 0,
                                    'final_dmg': self.arrow_stuck_damage,
                                    'who_attacks': self,
                                    'who_attacked': self.target,
                                    'moving': False,
                                    'sound': (False, self.atk2_sound, None, None),
                                    'delay': (False, 0),
                                    'stop_movement': (False, 3, 2, 0.2),
                                    'follow': (False, True),
                                    'follow_offset': (random.randint(-30, 30), (random.randint(30, 45))),
                                    'add_mana': True,
                                    # 'mana_mult': self.sp_atk2_mana_refund_2nd,
                                    'hitbox_scale_x': 0.1,
                                    'hitbox_scale_y': 0.1,
                                    }
                                }
                    ) # Replace with the targe t
                attack_display.add(attack)
            self.mana -=  self.attacks[2].mana_cost
            self.attacks[2].last_used_time = pygame.time.get_ticks()
            self.running = False
            self.attacking3 = True
            self.player_atk3_index = 0
            self.player_atk3_index_flipped = 0
            # self.y_velocity -= DEFAULT_GRAVITY  # optional: cancel gravity impulse if you want freeze in air

        
        super().update()
                    #self.apply_item_bonuses()
        # print(self.basic_attack_damage)
                # self.max_mana = min(200, self.max_mana + 10)

        # self.special += 0.1
        # print(self.special)

        # pygame.draw.rect(screen, (255, 0, 0), self.rect)