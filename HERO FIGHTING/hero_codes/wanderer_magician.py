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
WANDERER_MAGICIAN_JUMP_COUNT = 6
WANDERER_MAGICIAN_RUN_COUNT = 8
WANDERER_MAGICIAN_IDLE_COUNT = 8
WANDERER_MAGICIAN_ATK1_COUNT = 7
WANDERER_MAGICIAN_ATK3_COUNT = 9
WANDERER_MAGICIAN_SP_COUNT = 16
WANDERER_MAGICIAN_DEATH_COUNT = 4

WANDERER_MAGICIAN_BASIC = 6
WANDERER_MAGICIAN_ATK1 = 4
WANDERER_MAGICIAN_ATK2 = 40
WANDERER_MAGICIAN_ATK3 = 10
WANDERER_MAGICIAN_SP = 3

WANDERER_MAGICIAN_SPECIAL_ATK3 = 10
# ---------------------
# WANDERER_MAGICIAN_ATK1_MANA_COST = 70
# WANDERER_MAGICIAN_ATK2_MANA_COST = 125
# WANDERER_MAGICIAN_ATK3_MANA_COST = 125
# WANDERER_MAGICIAN_SP_MANA_COST = 170

WANDERER_MAGICIAN_BASIC_SIZE = 1.5
WANDERER_MAGICIAN_ATK1_SIZE = 2
WANDERER_MAGICIAN_ATK2_SIZE = 1
WANDERER_MAGICIAN_ATK3_SIZE = 1.5
WANDERER_MAGICIAN_SP_SIZE = 1.3

WANDERER_MAGICIAN_SPECIAL_ATK3_SIZE = 2
WANDERER_MAGICIAN_SPECIAL_BASICATK1_SIZE = 2

# WANDERER_MAGICIAN_ATK1_COOLDOWN = 8000
# WANDERER_MAGICIAN_ATK2_COOLDOWN = 15000 + 9000
# WANDERER_MAGICIAN_ATK3_COOLDOWN = 26000
# WANDERER_MAGICIAN_SP_COOLDOWN = 60000

# WANDERER_MAGICIAN_ATK1_DAMAGE = 0 # dmg at the input, sry
# WANDERER_MAGICIAN_ATK2_DAMAGE = (18/40, 0)
# WANDERER_MAGICIAN_ATK3_DAMAGE = (30/10, 5) #26
# WANDERER_MAGICIAN_SP_DAMAGE = (55, 0)


class Wanderer_Magician(Player): #NEXT WORK ON THE SPRITES THEN COPY EVERYTHING SINCE IM DONE 4/6/25 10:30pm
    def __init__(self, player_type, enemy):
        super().__init__(player_type, enemy)
        self.player_type = player_type # 1 for player 1, 2 for player 2
        self.name = "Wanderer Magician"

        self.hitbox_rect = pygame.Rect(0, 0, 50, 100)

        # stat
        self.strength = 40
        self.intelligence = 36
        self.agility = 35

        self.base_health_regen = 0.6 # 1.0
        self.base_mana_regen = 6.75 # 
        self.base_attack_damage = 0.2 # 3.7

        self.base_attack_speed = 100
        self.base_attack_time = 1600

        self.base_animation_speed = 120
        self.min_animation_speed = 60
        self.attack_speed_modifier = 0.5

        self.health_regen = self.calculate_regen(self.base_health_regen, self.hp_regen_per_str, self.strength) #0.6 + 40 * 0.01 = 1.0
        self.mana_regen = self.calculate_regen(self.base_mana_regen, self.mana_regen_per_int, self.intelligence) #6.75 + 36 * 0.01 = 7.01
        self.basic_attack_damage = self.calculate_regen(self.base_attack_damage, self.agi_mult, self.agility, basic_attack=True) # 0.0 + 35 * 0.1 = 3.5

        # Recalculate attack speed variables for fire wizard's base stats
        self.attack_speed = self.calculate_effective_as()
        self.basic_attack_cooldown = self.calculate_basic_attack_interval()
        self.basic_attack_animation_speed = self.calculate_attack_animation_speed()
        
        self.base_max_mana = self.intelligence * self.int_mult
        
        self.max_health = self.strength * self.str_mult
        self.max_mana = self.base_max_mana
        # self.special_default_max_mana = self.max_mana # max mana and this variable mustt  be the same
        self.special_bonus_mana = 240
        self.health = self.max_health
        self.mana = self.max_mana

        self.x = 50
        self.y = 50
        self.width = 200
        self.height = 20

        self.atk1_mana_cost = 65
        self.atk2_mana_cost = 150
        self.atk3_mana_cost = 125
        self.sp_mana_cost = 175

        self.atk1_cooldown = 8000
        self.atk2_cooldown = 13000 + 9000 #heal duration
        self.atk3_cooldown = 17000  
        self.sp_cooldown = 60000

        self.atk1_damage = (0, 0)
        self.atk2_damage = (20/40, 0) # 30 heal, slow -> 37 heal if special, quick
        self.atk3_damage = (26/10, 8) #26
        self.sp_damage = (55, 0) # 68.75 is the special dmg 
        self.sp_damage_2nd = (5/16, 0.5) # * 15 = 67.5 (when calculating [0] value, * 15, if [1], * 30)

        dmg_mult = 0
        self.atk1_damage = self.atk1_damage[0] + (self.atk1_damage[0] * dmg_mult), self.atk1_damage[1] + (self.atk1_damage[1] * dmg_mult)
        self.atk2_damage = self.atk2_damage[0] + (self.atk2_damage[0] * dmg_mult), self.atk2_damage[1] + (self.atk2_damage[1] * dmg_mult)
        self.atk3_damage = self.atk3_damage[0] + (self.atk3_damage[0] * dmg_mult), self.atk3_damage[1] + (self.atk3_damage[1] * dmg_mult)
        self.sp_damage = self.sp_damage[0] + (self.sp_damage[0] * dmg_mult), self.sp_damage[1] + (self.sp_damage[1] * dmg_mult)

        # Player Animation Source
        jump_ani = [r'assets\characters\Wanderer Magican\jump pngs\Jump_', WANDERER_MAGICIAN_JUMP_COUNT, 1]
        run_ani = [r'assets\characters\Wanderer Magican\run pngs\Run_', WANDERER_MAGICIAN_RUN_COUNT, 1]
        idle_ani= [r'assets\characters\Wanderer Magican\idle pngs\image_0-', WANDERER_MAGICIAN_IDLE_COUNT, 1]
        atk1_ani= [r'assets\characters\Wanderer Magican\attack 1 pngs\image_0-', WANDERER_MAGICIAN_ATK1_COUNT, 1]
        atk3_ani= [r'assets\characters\Wanderer Magican\attack 2 pngs\image_0-', WANDERER_MAGICIAN_ATK1_COUNT, 1]
        sp_ani= [r'assets\characters\Wanderer Magican\charge pngs', WANDERER_MAGICIAN_SP_COUNT, 1]
        death_ani= [r'assets\characters\Wanderer Magican\dead', WANDERER_MAGICIAN_DEATH_COUNT, 1]

        self.atk1_sound = pygame.mixer.Sound(r'assets\sound effects\wanderer_magician\shine-8-268901 1.mp3')
        self.atk2_sound = pygame.mixer.Sound(r'assets\sound effects\wanderer_magician\wind-chimes-2-199848 2.mp3')
        self.atk3_sound = pygame.mixer.Sound(r'assets\sound effects\wanderer_magician\elemental-magic-spell-impact-outgoing-228342 3.mp3')
        self.sp_sound = pygame.mixer.Sound(r'assets\sound effects\wanderer_magician\Rasengan Sound Effect 4.mp3')
        self.atk1_sound.set_volume(0.4 * global_vars.MAIN_VOLUME)
        self.atk2_sound.set_volume(0.5 * global_vars.MAIN_VOLUME)
        self.atk3_sound.set_volume(0.4 * global_vars.MAIN_VOLUME)
        self.sp_sound.set_volume(0.3 * global_vars.MAIN_VOLUME)

        # # Player Skill Animations Source
        basic = [r'assets\attacks\Basic Attack\wanderer magician\Charge_1_', WANDERER_MAGICIAN_BASIC, 1]
        atk1 = [r'assets\attacks\wanderer magician\atk1\image_', WANDERER_MAGICIAN_ATK1, 1]
        atk2 = [r'assets\attacks\wanderer magician\atk2', WANDERER_MAGICIAN_ATK2, 1]
        atk3 = [r'assets\attacks\wanderer magician\atk3\Explosion_blue_circle', WANDERER_MAGICIAN_ATK3, 0]
        sp = [r'assets\attacks\wanderer magician\sp atk\vv', WANDERER_MAGICIAN_SP, 0]

        special_atk3 = [r'assets\attacks\wanderer magician\special1\Explosion_blue_oval', WANDERER_MAGICIAN_SPECIAL_ATK3, 0]

        # Player Skill Icons Source
        skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\Icon_06.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_2 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\Icon_08.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\Icon9.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\Massive_Rasen.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_icon = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\special.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        special_skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\ChatGPT Image Apr 18, 2025, 07_46_01 AM.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_2 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\HealingWindIcon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\Icon4.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\wanderer_magician\Icon_02.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        # # Player Icon Rects
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
        self.basic = self.load_img_frames(basic[0], basic[1], basic[2], WANDERER_MAGICIAN_BASIC_SIZE)
        self.basic_flipped = self.load_img_frames_flipped(basic[0], basic[1], basic[2], WANDERER_MAGICIAN_BASIC_SIZE)

        self.atk1 = self.load_img_frames_rotate(atk1[0], atk1[1], atk1[2], WANDERER_MAGICIAN_ATK1_SIZE, 90)
        self.atk1_flipped = self.load_img_frames_flipped_rotate(atk1[0], atk1[1], atk1[2], WANDERER_MAGICIAN_ATK1_SIZE, -90)
        self.atk2 = self.load_img_frames_tile_method(atk2[0], atk2[1], atk2[2], WANDERER_MAGICIAN_ATK2_SIZE)
        self.atk3 = self.load_img_frames(atk3[0], atk3[1], atk3[2], WANDERER_MAGICIAN_ATK3_SIZE)
        self.sp = self.load_img_frames(sp[0], sp[1], sp[2], WANDERER_MAGICIAN_SP_SIZE)
        self.sp_flipped = self.load_img_frames_flipped(sp[0], sp[1], sp[2], WANDERER_MAGICIAN_SP_SIZE)

        self.special_atk3 = self.load_img_frames(special_atk3[0], special_atk3[1], special_atk3[2], WANDERER_MAGICIAN_SPECIAL_ATK3_SIZE)

        self.special_basic = load_attack(
        filepath=r"assets\attacks\Basic Attack\wanderer magician\basic atk special\4.png",
        frame_width=10, 
        frame_height=10, 
        rows=1, 
        columns=4, 
        scale=WANDERER_MAGICIAN_SPECIAL_BASICATK1_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.special_basic_flipped = load_attack_flipped(
        filepath=r"assets\attacks\Basic Attack\wanderer magician\basic atk special\4.png",
        frame_width=10, 
        frame_height=10, 
        rows=1, 
        columns=4, 
        scale=WANDERER_MAGICIAN_SPECIAL_BASICATK1_SIZE, 
        rotation=0,
        frame_duration=100
    )
        
        self.sp_special = load_attack(
        filepath=r"assets\attacks\wanderer magician\sp atk special\2.png",
        frame_width=100, 
        frame_height=100, 
        rows=1, 
        columns=8, 
        scale=3, 
        rotation=0,
        frame_duration=100
    )

        # Player Animations Load
        self.player_jump = self.load_img_frames(jump_ani[0], jump_ani[1], jump_ani[2], DEFAULT_CHAR_SIZE)
        self.player_jump_flipped = self.load_img_frames_flipped(jump_ani[0], jump_ani[1], jump_ani[2], DEFAULT_CHAR_SIZE)
        self.player_idle = self.load_img_frames(idle_ani[0], idle_ani[1], idle_ani[2], DEFAULT_CHAR_SIZE)
        self.player_idle_flipped = self.load_img_frames_flipped(idle_ani[0], idle_ani[1], idle_ani[2], DEFAULT_CHAR_SIZE)
        self.player_run = self.load_img_frames(run_ani[0], run_ani[1], run_ani[2], DEFAULT_CHAR_SIZE)
        self.player_run_flipped = self.load_img_frames_flipped(run_ani[0], run_ani[1], run_ani[2], DEFAULT_CHAR_SIZE)
        self.player_atk1 = self.load_img_frames(atk1_ani[0], atk1_ani[1], atk1_ani[2], DEFAULT_CHAR_SIZE)
        self.player_atk1_flipped = self.load_img_frames_flipped(atk1_ani[0], atk1_ani[1], atk1_ani[2], DEFAULT_CHAR_SIZE)
        self.player_atk2 = self.player_idle[:9]
        self.player_atk2_flipped = self.player_idle_flipped[:2]
        self.player_atk3 = self.load_img_frames(atk3_ani[0], atk3_ani[1], atk3_ani[2], DEFAULT_CHAR_SIZE)
        self.player_atk3_flipped = self.load_img_frames_flipped(atk3_ani[0], atk3_ani[1], atk3_ani[2], DEFAULT_CHAR_SIZE)
        self.player_sp = self.load_img_frames_tile_method(sp_ani[0], sp_ani[1], sp_ani[2], DEFAULT_CHAR_SIZE)
        self.player_sp_flipped = self.load_img_frames_flipped_tile_method(sp_ani[0], sp_ani[1], sp_ani[2], DEFAULT_CHAR_SIZE)
        self.player_death = self.load_img_frames_tile_method(death_ani[0], death_ani[1], death_ani[2], DEFAULT_CHAR_SIZE)
        self.player_death_flipped = self.load_img_frames_flipped_tile_method(death_ani[0], death_ani[1], death_ani[2], DEFAULT_CHAR_SIZE)

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
                skill_img=self.basic_icon2,
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
                mana_cost=self.mana_cost_list[1],
                skill_rect=self.special_skill_2_rect,
                skill_img=special_skill_2,
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
                skill_img=self.basic_icon2,
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

        self.jump_attack_pending = False
        self.jump_attack_time = 0

    def atk1_animation(self, animation_speed=0):
        if self.facing_right:
            self.player_atk1_index, anim_active = self.animate(self.player_atk1, self.player_atk1_index, loop=False, basic_atk=True)
        else:
            self.player_atk1_index_flipped, anim_active = self.animate(self.player_atk1_flipped, self.player_atk1_index_flipped, loop=False, basic_atk=True)

        self.last_atk_time -= animation_speed

        if not anim_active:
            self.attacking1 = False
            self.basic_attacking = False  # Only matters if this was a basic attack
            self.player_atk1_index = 0
            self.player_atk1_index_flipped = 0        

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
                speed_modifier = 0,
                special_active_speed = 0.1,
                jump_force = self.jump_force,
                jump_force_modifier = 0
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
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx,
                            y=self.rect.centery + 30,
                            frames=self.atk1 if self.facing_right else self.atk1_flipped,
                            frame_duration=100,
                            repeat_animation=5,
                            speed=7 if self.facing_right else -7,
                            dmg=random.choice([2.5, 2.5, 2.5, 5, 5, 5, 5, 5, 7.5, 10]) * 3, #30% chance for non crit, 50% chance for crit 2x, 10% chance for super crit 3x and 10% change for super mega crit 4x
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=self.enemy,
                            moving=True,

                            kill_collide=True,
                            sound=(True, self.atk1_sound , None, None),
                            delay=(True, self.basic_attack_animation_speed * (500 / DEFAULT_ANIMATION_SPEED)), # self.basic_attack_animation_speed * (Base Delay/Default Basic Attack Speed)
                            ) # Replace with the target
                        attack_display.add(attack)
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


                elif hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks[1].mana_cost and self.attacks[1].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx, # in front of him
                            y=self.rect.centery + 20,
                            frames=self.atk2,
                            frame_duration=100,
                            repeat_animation=2,
                            speed=5 if self.facing_right else -5,
                            dmg=self.atk2_damage[0], 
                            final_dmg=self.atk2_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,

                            heal=True,
                            sound=(True, self.atk2_sound , None, None)) # Replace with the target
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

                elif hotkey3 and not self.attacking3 and not self.attacking1 and not self.attacking2 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >= self.attacks[2].mana_cost and self.attacks[2].is_ready():
                        # self.jumping = True
                        # self.y_velocity = DEFAULT_JUMP_FORCE  # adjust jump strength as needed
                        # self.jump_attack_pending = True
                        # self.jump_attack_time = pygame.time.get_ticks() + 200  # 500ms later
                        # Create an attack
                        # print("Z key pressed")
                        # if self.jump_attack_pending and pygame.time.get_ticks() >= self.jump_attack_time:
                        #     self.jump_attack_pending = False
                        self.single_target()
                        attack = Attack_Display(
                            x=self.target.x_pos,
                            y=self.target.y_pos - 30,
                            frames=self.atk3,
                            frame_duration=100,
                            repeat_animation=1,
                            speed=5 if self.facing_right else -5,
                            dmg=self.atk3_damage[0],
                            final_dmg=self.atk3_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            sound=(True, self.atk3_sound , None, None),
                            delay=(True, 800)
                            ) # Replace with the target
                        attack_display.add(attack)
                        self.mana -=  self.attacks[2].mana_cost
                        self.attacks[2].last_used_time = current_time
                        self.running = False
                        self.attacking3 = True
                        self.player_atk3_index = 0
                        self.player_atk3_index_flipped = 0
                            # self.y_velocity = 0  # optional: cancel gravity impulse if you want freeze in air

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
                            x=self.rect.centerx, # in front of him
                            y=self.rect.centery,
                            frames=self.sp if self.facing_right else self.sp_flipped,
                            frame_duration=40,
                            repeat_animation=30,
                            speed=5 if self.facing_right else -5,
                            dmg=self.sp_damage[0],
                            final_dmg=self.sp_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            moving=True,

                            kill_collide=True,
                            sound=(True, self.sp_sound , None, None),
                            delay=(True, 5000)
                            ) 
                        attack_display.add(attack)
                        self.mana -=  self.attacks[3].mana_cost
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
                        attack = Attack_Display(
                            x=self.rect.centerx,
                            y=self.rect.centery + random.randint(0, 40),
                            frames=self.basic if self.facing_right else self.basic_flipped,
                            frame_duration=100,
                            repeat_animation=5,
                            speed=7 if self.facing_right else -7,
                            dmg=self.basic_attack_damage,
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=self.enemy,
                            moving=True,

                            sound=(True, self.atk1_sound, None, None),
                            kill_collide=True,
                            delay=(True, self.basic_attack_animation_speed * (500 / self.base_animation_speed)), # self.basic_attack_animation_speed * (Base Delay/Default Basic Attack Speed) # 500/120
                            is_basic_attack=True
                        )
                    
                        attack_display.add(attack)
                        self.mana -= 0
                        self.attacks[4].last_used_time = current_time
                        self.running = False
                        self.attacking1 = True
                        self.player_atk1_index = 0
                        self.player_atk1_index_flipped = 0

                        self.basic_attacking = True
                        self.last_basic_attack_time = current_time
                        # print(self.basic_attack_animation_speed)

                        # Experiment Codes
                        # plan: when attack longer moving, greater damage
                    #     periodic_spawn={
                    #         'attack_kwargs': {
                    #             'x': width+100,
                    #             'y': self.rect.centery + random.randint(0, 40),
                    #             'frames': self.atk1 if self.facing_right else self.atk1_flipped,
                    #             'frame_duration': 100,
                    #             'repeat_animation': 5,
                    #             'speed': -7 if self.facing_right else 7,
                    #             'dmg': random.choice([2.5, 2.5, 2.5, 5, 5, 5, 5, 5, 7.5, 10 ]) * 3,
                    #             'final_dmg': 0,
                    #             'who_attacks': self,
                    #             'who_attacked': self.enemy,
                    #             'moving': True,
                    #             'sound': (False, self.atk1_sound, None, None),
                    #             'delay': (True, 300),
                    #             'kill_collide': True
                    #         },
                    #         'interval': 1000,
                    #         'repeat_count': 5,
                    #         'use_attack_pos': False,
                    #     }
                    # )
                        

                    #     periodic_spawn= {
                    #         'attack_kwargs': {
                    #             'frames': self.atk3,
                    #             'frame_duration': 100,
                    #             'repeat_animation': 3,
                    #             'speed': 0,
                    #             'dmg': self.atk3_damage[0],
                    #             'final_dmg': self.atk3_damage[1],
                    #             'who_attacks': self,
                    #             'who_attacked': self.enemy,
                    #             'moving': False,
                    #             'sound': (False, self.atk3_sound, None, None),
                    #             'delay': (False, 0)
                    #         },
                    #         'interval': 500,
                    #         'repeat_count': 20,
                    #         'use_attack_pos': True,
                    #     }
                    # )

                    

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
                        # Create an attack
                        # print("Z key pressed")
                        for i in [(0, 30), (40, 60), (40, 0)]:
                            attack = Attack_Display(
                                x=self.rect.centerx - i[0] if self.facing_right else self.rect.centerx + i[0],
                                y=self.rect.centery + i[1] if self.facing_right else self.rect.centery + i[1],
                                frames=self.atk1 if self.facing_right else self.atk1_flipped,
                                frame_duration=100,
                                repeat_animation=5,
                                speed=7 if self.facing_right else -7,
                                dmg=random.choice([2.5, 2.5, 2.5, 5, 5, 5, 5, 5, 7.5, 10 ]) * 1.2,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=self.enemy,
                                moving=True,

                                kill_collide=True,
                            sound=(True, self.atk1_sound , None, None),
                            delay=(True, self.basic_attack_animation_speed * (500 / DEFAULT_ANIMATION_SPEED)) # self.basic_attack_animation_speed * (Base Delay/Default Basic Attack Speed)) # Replace with the target
                            )
                            attack_display.add(attack)
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


                elif hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[1].mana_cost and self.attacks_special[1].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx, # in front of him
                            y=self.rect.centery + 20,
                            frames=self.atk2,
                            frame_duration=40,
                            repeat_animation=1,
                            speed=5 if self.facing_right else -5,
                            dmg=(self.atk2_damage[0]*2) + ((self.atk2_damage[0]*2) * (SPECIAL_MULTIPLIER * 0.25)),
                            final_dmg=self.atk2_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,

                            heal=True,
                            sound=(True, self.atk2_sound , None, None)) # Replace with the target
                        attack_display.add(attack)
                        self.mana -=  self.attacks_special[1].mana_cost
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
                    if self.mana >=  self.attacks_special[2].mana_cost and self.attacks_special[2].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        self.single_target()
                        attack = Attack_Display(
                            x=self.target.x_pos,
                            y=self.target.y_pos - 30,
                            frames=self.special_atk3,
                            frame_duration=100,
                            repeat_animation=1,
                            speed=5 if self.facing_right else -5,
                            dmg=self.atk3_damage[0] + (self.atk3_damage[0] * (SPECIAL_MULTIPLIER * 0.15)),
                            final_dmg=self.atk3_damage[1] + (self.atk3_damage[1] * (SPECIAL_MULTIPLIER * 0.15)),
                            who_attacks=self,
                            who_attacked=self.enemy,
                            sound=(True, self.atk3_sound , None, None),
                            delay=(True, 800)
                            ) # Replace with the target
                        attack_display.add(attack)
                        self.mana -=  self.attacks_special[2].mana_cost
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

                        self.single_target()
                        attack = Attack_Display(
                            x=self.target.x_pos,
                            y=self.target.y_pos + 40,
                            frames=self.sp_special,
                            frame_duration=160,
                            repeat_animation=30,
                            speed=5 if self.facing_right else -5,
                            dmg=self.sp_damage_2nd[0],
                            final_dmg=self.sp_damage_2nd[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            moving=False,
                            follow=(False, True),
                            follow_offset=(0, 50),

                            kill_collide=False,
                            sound=(True, self.sp_sound , self.atk3_sound, None),
                            delay=(True, 800)
                            )
                        attack_display.add(attack)
                        self.mana -=  self.attacks_special[3].mana_cost
                        self.attacks_special[3].last_used_time = current_time
                        self.running = False
                        self.attacking3 = True
                        self.player_atk3_index = 0
                        self.player_atk3_index_flipped = 0

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 4 used')

            if not self.is_dead() and not self.jumping and basic_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                if self.mana >= 0 and self.can_basic_attack():
                    for i in [(500, random.randint(0, 30)), (700, random.randint(0, 30)), (900, random.randint(0, 30))]:
                        attack = Attack_Display(
                            x=self.rect.centerx,
                            y=self.rect.centery + i[1],
                            frames=self.special_basic if self.facing_right else self.special_basic_flipped,
                            frame_duration=100,
                            repeat_animation=5,
                            speed=8 if self.facing_right else -8,
                            dmg=(self.basic_attack_damage / 3) * DEFAULT_BASIC_ATK_DMG_BONUS,
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=self.enemy,
                            moving=True,

                            sound=(True, self.basic_sound, self.atk1_sound, None),
                            kill_collide=True,
                            delay=(True, self.basic_attack_animation_speed * (i[0] / self.base_animation_speed)), # self.basic_attack_animation_speed * (Base Delay/Default Basic Attack Speed)

                            hitbox_scale_x=0.2,
                            hitbox_scale_y=0.2,
                        #     spawn_attack= {
                        #     'attack_kwargs': {
                        #         'frames': self.atk3,
                        #         'frame_duration': 100,
                        #         'repeat_animation': 1,
                        #         'speed': 0,
                        #         'dmg': self.atk3_damage[0],
                        #         'final_dmg': self.atk3_damage[1],
                        #         'who_attacks': self,
                        #         'who_attacked': self.enemy,
                        #         'moving': False,
                        #         'sound': (False, self.atk3_sound, None, None),
                        #         'delay': (False, 0)
                        #     },
                        #     'use_attack_onhit_pos': True
                            
                        # }
                        is_basic_attack=True
                        )
                            
                        attack_display.add(attack)


                    

                    self.mana -= 0
                    self.attacks_special[4].last_used_time = current_time
                    self.running = False
                    self.attacking1 = True
                    self.player_atk1_index = 0
                    self.player_atk1_index_flipped = 0
                    
                    self.basic_attacking = True
                    self.last_basic_attack_time = current_time

                    # print("Attack executed")
                else:
                    pass

        # print(self.running)
        # print(self.player_type)
        # print(len(self.player_run), len(self.player_run_flipped))
        # print("Run Animation Index:", self.player_run_index)

     
        
    def update(self):
        # if self.jump_attack_pending and pygame.time.get_ticks() >= self.jump_attack_time:
        #     self.jump_attack_pending = False
        #     attack = Attack_Display(
        #         x=hero1.x_pos if self.player_type == 2 else hero2.x_pos, #self.rect.centerx + 150 if self.facing_right else self.rect.centerx - 150, # in front of him
        #         y=hero1.y_pos - 30 if self.player_type == 2 else hero2.y_pos - 30,
        #         frames=self.atk3,
        #         frame_duration=100,
        #         repeat_animation=1,
        #         speed=5 if self.facing_right else -5,
        #         dmg=self.atk3_damage[0],
        #         final_dmg=self.atk3_damage[1],
        #         who_attacks=self,
        #         who_attacked=self.enemy,
        #         sound=(True, self.atk3_sound , None, None),
        #         delay=(True, 800)
        #         ) # Replace with the target
        #     attack_display.add(attack)
        #     # self.mana -=  self.attacks[2].mana_cost
        #     # self.attacks[2].last_used_time = current_time
        #     self.running = False
        #     self.attacking3 = True
        #     self.player_atk3_index = 0
        #     self.player_atk3_index_flipped = 0
        #     self.y_velocity -= DEFAULT_GRAVITY*7  # optional: cancel gravity impulse if you want freeze in air
        # print(self.stunned)
                

         
        
        if not self.is_dead():
            self.player_death_index = 0
            self.player_death_index_flipped = 0
        if self.is_dead():
            self.play_death_animation()
        elif self.attacking1:
            self.atk1_animation()
        elif self.attacking3:
            self.atk3_animation()
        elif self.jumping:
            self.jump_animation()
        elif self.running and not self.jumping:
            self.run_animation(self.running_animation_speed)
        elif self.attacking2:
            self.atk2_animation()
        
        elif self.sp_attacking:
            self.sp_animation(-11)

        else:
            self.simple_idle_animation(RUNNING_ANIMATION_SPEED)

        # Apply gravity
        self.y_velocity += DEFAULT_GRAVITY
        self.y_pos += self.y_velocity
        # if not self.jump_attack_pending:
        #     self.y_velocity += DEFAULT_GRAVITY
        #     self.y_pos += self.y_velocity
        
        

        # print(self.basic_attack_animation_speed)
        # print(f'cd:{self.basic_attack_cooldown}')
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
                self.max_mana = min(self.special_bonus_mana, self.max_mana + 10)
                if self.special <= 0:
                    self.special_active = False
                    self.max_mana = min(self.base_max_mana, self.max_mana + 10)
                    #self.apply_item_bonuses()
        # print(self.basic_attack_damage)
                # self.max_mana = min(200, self.max_mana + 10)

        # self.special += 0.1
        # print(self.special)

        # pygame.draw.rect(screen, (255, 0, 0), self.rect)
        
        super().update()

