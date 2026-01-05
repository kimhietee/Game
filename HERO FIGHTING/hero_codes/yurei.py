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
class Yurei(Player):
    def __init__(self, player_type, enemy):
        super().__init__(player_type, enemy)
        self.player_type = player_type # 1 for player 1, 2 for player 2
        self.name = "Yurei"

        self.hitbox_rect = pygame.Rect(0, 0, 45, 100)

        # stat
        self.strength = 36
        self.intelligence = 40
        self.agility = 37
        
        self.base_health_regen = 0.75 # 1.11
        self.base_mana_regen = 5.5 # 5.9
        self.base_attack_damage = 0.5 # 3.8

        self.base_attack_speed = 100
        self.base_attack_time = 1500

        self.base_animation_speed = 120

        self.health_regen = self.calculate_regen(self.base_health_regen, self.hp_regen_per_str, self.strength) #0.75 + 36 * 0.01 = 1.11
        self.mana_regen = self.calculate_regen(self.base_mana_regen, self.mana_regen_per_int, self.intelligence) #5.5 + 40 * 0.01 = 5.9
        self.basic_attack_damage = self.calculate_regen(self.base_attack_damage, self.agi_mult, self.agility, basic_attack=True) # 0.0 + 23 * 0.1 = 2.0

        # Recalculate attack speed variables for fire wizard's base stats
        self.attack_speed = self.calculate_effective_as()
        self.basic_attack_cooldown = self.calculate_basic_attack_interval()
        self.basic_attack_animation_speed = self.base_animation_speed / (self.attack_speed / self.base_attack_speed)

        
        self.max_health = self.strength * self.str_mult
        self.max_mana = self.intelligence * self.int_mult
        # self.special_default_max_mana = self.max_mana # max mana and this variable mustt  be the same
        self.special_bonus_mana = 240
        self.health = self.max_health
        self.mana = self.max_mana

        self.x = 50
        self.y = 50
        self.width = 200
        self.height = 20

        self.atk1_mana_cost = 50
        self.atk2_mana_cost = 70    
        self.atk3_mana_cost = 110
        self.sp_mana_cost = 80

        self.sp_atk1_mana_cost = 80

        # Trait: cd reduce
        cooldown_reduction = 1 - 0.15
        self.atk1_cooldown = int((9000 + 2000)*cooldown_reduction) # root duration
        self.atk2_cooldown = int((12000 + 2000)*cooldown_reduction)# + 2000 # frozen duration
        self.atk3_cooldown = int((20000 + 3000)*cooldown_reduction) # frozen duration
        self.sp_cooldown = int((20000 + 5000)*cooldown_reduction) #invi duration

        # cooldown already reduced, so when equipping items with
        # cd reduce, it will not stack

        self.sp_atk1_cooldown = 15000 + 2000

        self.atk1_damage = (12/20, 0)
        self.atk2_damage = (10/15,5)
        self.atk3_damage = (20/30, 0)
        # self.sp_damage = (55, 0)
        # self.sp_damage_2nd = (4.5/16, 0)

        self.sp_atk2_damage_2nd = (20/20, 0) # FOR ATTACK1 SPECIAL MODE ONLY!!

        dmg_mult = 0
        self.atk1_damage = self.atk1_damage[0] + (self.atk1_damage[0] * dmg_mult), self.atk1_damage[1] + (self.atk1_damage[1] * dmg_mult)
        self.atk2_damage = self.atk2_damage[0] + (self.atk2_damage[0] * dmg_mult), self.atk2_damage[1] + (self.atk2_damage[1] * dmg_mult)
        self.atk3_damage = self.atk3_damage[0] + (self.atk3_damage[0] * dmg_mult), self.atk3_damage[1] + (self.atk3_damage[1] * dmg_mult)
        self.sp_damage = self.sp_damage[0] + (self.sp_damage[0] * dmg_mult), self.sp_damage[1] + (self.sp_damage[1] * dmg_mult)

        # Player Animation Source
        # jump_ani = [r'assets\characters\Wanderer Magican\jump pngs\Jump_', WANDERER_MAGICIAN_JUMP_COUNT, 1]
        # run_ani = [r'assets\characters\Wanderer Magican\run pngs\Run_', WANDERER_MAGICIAN_RUN_COUNT, 1]
        # idle_ani= [r'assets\characters\Wanderer Magican\idle pngs\image_0-', WANDERER_MAGICIAN_IDLE_COUNT, 1]
        # atk1_ani= [r'assets\characters\Wanderer Magican\attack 1 pngs\image_0-', WANDERER_MAGICIAN_ATK1_COUNT, 1]
        # atk3_ani= [r'assets\characters\Wanderer Magican\attack 2 pngs\image_0-', WANDERER_MAGICIAN_ATK1_COUNT, 1]
        # sp_ani= [r'assets\characters\Wanderer Magican\charge pngs', WANDERER_MAGICIAN_SP_COUNT, 1]
        # death_ani= [r'assets\characters\Wanderer Magican\dead', WANDERER_MAGICIAN_DEATH_COUNT, 1]

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
        # atk2 = [r'assets\attacks\wanderer magician\atk2', WANDERER_MAGICIAN_ATK2, 1]
        # atk3 = [r'assets\attacks\wanderer magician\atk3\Explosion_blue_circle', WANDERER_MAGICIAN_ATK3, 0]
        # sp = [r'assets\attacks\wanderer magician\sp atk\vv', WANDERER_MAGICIAN_SP, 0]

        # special_atk3 = [r'assets\attacks\wanderer magician\special1\Explosion_blue_oval', WANDERER_MAGICIAN_SPECIAL_ATK3, 0]

        # Player Skill Icons Source
        skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\onre\magic-summon-circle-purple-magic-footage-162703660_iconl.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_2 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\onre\person-fade-away-green-fog-260nw-2585215663.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\onre\a.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\onre\dark-silhouette-woman-windblown-hair-her-form-dissolving-chaotic-cloud-black-dust-dissolves-violently-particles-393542673.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_icon = pygame.transform.scale(pygame.image.load(r'assets\skill icons\onre\aa.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        special_skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\onre\magic-summon-circle-purple-magic-footage-162703660_iconl.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_2 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\onre\person-fade-away-green-fog-260nw-2585215663.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\onre\a.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\onre\dark-silhouette-woman-windblown-hair-her-form-dissolving-chaotic-cloud-black-dust-dissolves-violently-particles-393542673.jpg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

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
        # self.basic = self.load_img_frames(basic[0], basic[1], basic[2], WANDERER_MAGICIAN_BASIC_SIZE)
        # self.basic_flipped = self.load_img_frames_flipped(basic[0], basic[1], basic[2], WANDERER_MAGICIAN_BASIC_SIZE)

        # self.atk1 = self.load_img_frames_rotate(atk1[0], atk1[1], atk1[2], WANDERER_MAGICIAN_ATK1_SIZE, 90)
        # self.atk1_flipped = self.load_img_frames_flipped_rotate(atk1[0], atk1[1], atk1[2], WANDERER_MAGICIAN_ATK1_SIZE, -90)
        # self.atk2 = self.load_img_frames_tile_method(atk2[0], atk2[1], atk2[2], WANDERER_MAGICIAN_ATK2_SIZE)
        # self.atk3 = self.load_img_frames(atk3[0], atk3[1], atk3[2], WANDERER_MAGICIAN_ATK3_SIZE)
        # self.sp = self.load_img_frames(sp[0], sp[1], sp[2], WANDERER_MAGICIAN_SP_SIZE)
        # self.sp_flipped = self.load_img_frames_flipped(sp[0], sp[1], sp[2], WANDERER_MAGICIAN_SP_SIZE)

        # self.special_atk3 = self.load_img_frames(special_atk3[0], special_atk3[1], special_atk3[2], WANDERER_MAGICIAN_SPECIAL_ATK3_SIZE)
        self.atk1 = load_attack(
        filepath=r"assets\attacks\Onre\atk1\322.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=4, 
        columns=5, 
        scale=1.4, 
        rotation=0,
    )
        self.atk1_sp = load_attack(
        filepath=r"assets\attacks\Onre\atk1\322.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=4, 
        columns=5, 
        scale=2.4, 
        rotation=0,
    )
        
        self.atk2 = load_attack(
        filepath=r"assets\attacks\Onre\atk2\326.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=3, 
        columns=5, 
        scale=1.2, 
        rotation=0
    )
        
        self.atk3 = load_attack(
        filepath=r"assets\attacks\Onre\atk3\093.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=6, 
        columns=5, 
        scale=0.5, 
        rotation=0
    )
        
        self.special_basic = load_attack(
        filepath=r"assets\attacks\Basic Attack\wanderer magician\basic atk special\4.png",
        frame_width=10, 
        frame_height=10, 
        rows=1, 
        columns=4, 
        scale=2, 
        rotation=0,
        frame_duration=100
    )
        self.special_basic_flipped = load_attack_flipped(
        filepath=r"assets\attacks\Basic Attack\wanderer magician\basic atk special\4.png",
        frame_width=10, 
        frame_height=10, 
        rows=1, 
        columns=4, 
        scale=2, 
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
        blank_frame = pygame.image.load(r'assets\characters\empty_frame.png')

        # self.player_jump = self.load_img_frames(jump_ani[0], jump_ani[1], jump_ani[2], DEFAULT_CHAR_SIZE)
        # self.player_jump_flipped = self.load_img_frames_flipped(jump_ani[0], jump_ani[1], jump_ani[2], DEFAULT_CHAR_SIZE)
        self.player_jump = load_attack(
        filepath=r"assets\characters\Onre\Flight.png",
        frame_width=100, 
        frame_height=100, 
        rows=1, 
        columns=6, 
        scale=DEFAULT_CHAR_SIZE, 
        rotation=0,
    )
        self.player_jump_flipped = load_attack_flipped(
        filepath=r"assets\characters\Onre\Flight.png",
        frame_width=100, 
        frame_height=100, 
        rows=1, 
        columns=6, 
        scale=DEFAULT_CHAR_SIZE, 
        rotation=0,
    )
        # self.player_idle = self.load_img_frames(idle_ani[0], idle_ani[1], idle_ani[2], DEFAULT_CHAR_SIZE)
        # self.player_idle_flipped = self.load_img_frames_flipped(idle_ani[0], idle_ani[1], idle_ani[2], DEFAULT_CHAR_SIZE)
        self.player_idle = load_attack(
        filepath=r"assets\characters\Onre\Idle.png",
        frame_width=128, 
        frame_height=128, 
        rows=1, 
        columns=6, 
        scale=DEFAULT_CHAR_SIZE, 
        rotation=0,
    )
        self.player_idle_flipped = load_attack_flipped(
        filepath=r"assets\characters\Onre\Idle.png",
        frame_width=100, 
        frame_height=100, 
        rows=1, 
        columns=6, 
        scale=DEFAULT_CHAR_SIZE, 
        rotation=0,
    )
        self.player_run = load_attack(
        filepath=r"assets\characters\Onre\Run.png",
        frame_width=100, 
        frame_height=100, 
        rows=1, 
        columns=7, 
        scale=DEFAULT_CHAR_SIZE, 
        rotation=0,
    )
        self.player_run_flipped = load_attack_flipped(
        filepath=r"assets\characters\Onre\Run.png",
        frame_width=100, 
        frame_height=100, 
        rows=1, 
        columns=7, 
        scale=DEFAULT_CHAR_SIZE, 
        rotation=0,
    )
        # self.player_run = self.load_img_frames(run_ani[0], run_ani[1], run_ani[2], DEFAULT_CHAR_SIZE)
        # self.player_run_flipped = self.load_img_frames_flipped(run_ani[0], run_ani[1], run_ani[2], DEFAULT_CHAR_SIZE)
        self.player_atk1 = load_attack(
        filepath=r"assets\characters\Onre\Attack_2.png",
        frame_width=100, 
        frame_height=100, 
        rows=1, 
        columns=4,
        scale=DEFAULT_CHAR_SIZE, 
        rotation=0,
    )
        self.player_atk1_flipped = load_attack_flipped(
        filepath=r"assets\characters\Onre\Attack_2.png",
        frame_width=100, 
        frame_height=100, 
        rows=1, 
        columns=4, 
        scale=DEFAULT_CHAR_SIZE,
        rotation=0,
    )
        # self.player_atk1 = self.load_img_frames(atk1_ani[0], atk1_ani[1], atk1_ani[2], DEFAULT_CHAR_SIZE)
        # self.player_atk1_flipped = self.load_img_frames_flipped(atk1_ani[0], atk1_ani[1], atk1_ani[2], DEFAULT_CHAR_SIZE)
        
    #     self.player_atk2 = load_attack(
    #     filepath=r"assets\characters\Onre\Dead.png",
    #     frame_width=100, 
    #     frame_height=100, 
    #     rows=1, 
    #     columns=6, 
    #     scale=DEFAULT_CHAR_SIZE, 
    #     rotation=0,
    # )
    #     self.player_atk2_flipped = load_attack_flipped(
    #     filepath=r"",
    #     frame_width=100, 
    #     frame_height=100, 
    #     rows=1, 
    #     columns=6, 
    #     scale=DEFAULT_CHAR_SIZE, 
    #     rotation=0,
    # )
        # self.player_atk2 = self.player_idle[:9]
        # self.player_atk2_flipped = self.player_idle_flipped[:2]
        self.player_atk3 = load_attack( #circling water
        filepath=r"assets\characters\Onre\Scream.png",
        frame_width=100, 
        frame_height=100, 
        rows=1, 
        columns=7, 
        scale=DEFAULT_CHAR_SIZE, 
        rotation=0,
    )
        self.player_atk3_flipped = load_attack_flipped( #circling water
        filepath=r"assets\characters\Onre\Scream.png",
        frame_width=100, 
        frame_height=100, 
        rows=1, 
        columns=7, 
        scale=DEFAULT_CHAR_SIZE, 
        rotation=0,
    )
        # self.player_atk3 = self.load_img_frames(atk3_ani[0], atk3_ani[1], atk3_ani[2], DEFAULT_CHAR_SIZE)
        # self.player_atk3_flipped = self.load_img_frames_flipped(atk3_ani[0], atk3_ani[1], atk3_ani[2], DEFAULT_CHAR_SIZE)
        self.player_sp = load_attack( #circling water
        filepath=r"assets\characters\Onre\Dead.png",
        frame_width=100, 
        frame_height=100, 
        rows=1, 
        columns=6, 
        scale=DEFAULT_CHAR_SIZE, 
        rotation=0,
    )
        self.player_sp_flipped = load_attack_flipped( #circling water
        filepath=r"assets\characters\Onre\Dead.png",
        frame_width=100, 
        frame_height=100, 
        rows=1, 
        columns=6, 
        scale=DEFAULT_CHAR_SIZE, 
        rotation=0,
    )
        self.player_sp.append(blank_frame)
        self.player_sp_flipped.append(blank_frame)
        # self.player_sp = self.load_img_frames_tile_method(sp_ani[0], sp_ani[1], sp_ani[2], DEFAULT_CHAR_SIZE)
        # self.player_sp_flipped = self.load_img_frames_flipped_tile_method(sp_ani[0], sp_ani[1], sp_ani[2], DEFAULT_CHAR_SIZE)
        self.player_death = load_attack( #circling water
        filepath=r"assets\characters\Onre\Dead.png",
        frame_width=100, 
        frame_height=100, 
        rows=1, 
        columns=6, 
        scale=DEFAULT_CHAR_SIZE, 
        rotation=0,
    )
        self.player_death_flipped = load_attack_flipped( #circling water
        filepath=r"assets\characters\Onre\Dead.png",
        frame_width=100, 
        frame_height=100, 
        rows=1, 
        columns=6, 
        scale=DEFAULT_CHAR_SIZE, 
        rotation=0,
    )
        self.player_death.append(blank_frame)
        self.player_death_flipped.append(blank_frame)
        # self.player_death = self.load_img_frames_tile_method(death_ani[0], death_ani[1], death_ani[2], DEFAULT_CHAR_SIZE)
        # self.player_death_flipped = self.load_img_frames_flipped_tile_method(death_ani[0], death_ani[1], death_ani[2], DEFAULT_CHAR_SIZE)

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
                mana_cost=self.sp_atk1_mana_cost,
                skill_rect=self.special_skill_1_rect,
                skill_img=special_skill_1,
                cooldown=self.sp_atk1_cooldown,
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

        self.invisible = False
        self.invisible_duration = 0
        self.casting_invisible = False

    def atk1_animation(self, animation_speed=0):
        if self.facing_right:
            self.player_atk1_index, anim_active = self.animate(self.player_atk1, self.player_atk1_index, loop=False)
        else:
            self.player_atk1_index_flipped, anim_active = self.animate(self.player_atk1_flipped, self.player_atk1_index_flipped, loop=False)

        self.last_atk_time -= animation_speed

        if not anim_active:
            self.attacking1 = False
            self.basic_attacking = False  # Only matters if this was a basic attack
            self.player_atk1_index = 0
            self.player_atk1_index_flipped = 0     

    # okay I'm not gonna combine invisible and normal animation :((
    def animate_invi(self, frames, index, loop=True, invisible=False):
        current_time = pygame.time.get_ticks()
        frame_duration = self.default_animation_speed if not self.basic_attacking else self.basic_attack_animation_speed
        if current_time - self.last_atk_time > frame_duration:
            self.last_atk_time = current_time
            if invisible:
                if index < len(frames): # only increase index if not in last frame
                    self.image = frames[int(index)]
                    index += 1
            else:
                self.image = frames[int(index)]
                index += 1
            if index >= len(frames):
                self.casting_invisible = False if invisible else None # now invisible!
                if loop:
                    index = 0  # Restart the animation
                else:
                    if invisible:
                        self.image = frames[-1] # stay in last frame
                        if pygame.time.get_ticks() >= self.invisible_duration:
                            self.invisible = False
                            index = len(frames) - 1  # Stay on the last frame
                            print('end of invi')
                            return index, index, False  # set index for normal and flipped frames
                    else:
                        index = len(frames) - 1  # Stay on the last frame
                        return index, False  # Animation finished
                        
        if invisible: return index, index, True # animation still active
        else: return index, True  # Animation finished  # Animation stzill active
            

    def sp_animation(self, animation_speed=0):
        if self.facing_right:
            self.player_sp_index, self.player_sp_index_flipped, self.sp_attacking = self.animate_invi(self.player_sp, self.player_sp_index, loop=False, invisible=True)
        else:
            self.player_sp_index_flipped, self.player_sp_index, self.sp_attacking = self.animate_invi(self.player_sp_flipped, self.player_sp_index_flipped, loop=False, invisible=True)

        self.last_atk_time -= animation_speed


    def take_damage(self, damage, add_mana_to_self=False, enemy:object=None, add_mana_to_enemy=False, mana_multiplier=1):
        if self.invisible:
            return
        else:
            super().take_damage(damage, add_mana_to_self, enemy, add_mana_to_enemy, mana_multiplier)
        
    def is_busy_attacking(self):
        """Override to allow movement when invisible, even if sp_attacking.
        
        Cannot move while casting invisible, if done, can move """
        return (self.attacking1 or self.attacking2 or self.attacking3 or self.basic_attacking) or (self.sp_attacking and self.casting_invisible)
    
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
                speed_modifier = 0.05,
                special_active_speed = 0.25,
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
                if hotkey1 and not self.attacking1 and not self.attacking2 and not self.attacking3  and not self.basic_attacking:
                    if self.mana >=  self.attacks[0].mana_cost and self.attacks[0].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx,
                            y=self.rect.centery + 30,
                            frames=self.atk1,
                            frame_duration=100, # 2 seconds 20 frames
                            repeat_animation=1,
                            speed=0,
                            dmg=self.atk1_damage[0],
                            final_dmg=self.atk1_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            sound=(True, self.atk1_sound , None, None),
                            stop_movement=(True, 2, 2),
                            delay=(True, 100), # self.basic_attack_animation_speed * (Base Delay/Default Basic Attack Speed)
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


                elif hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3  and not self.basic_attacking:
                    if self.mana >=  self.attacks[1].mana_cost and self.attacks[1].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx, # in front of him
                            y=self.rect.centery,
                            frames=self.player_run if self.facing_right else self.player_run_flipped,
                            frame_duration=DEFAULT_ANIMATION_SPEED,
                            repeat_animation=10,
                            speed=self.speed if self.facing_right else -self.speed,
                            moving=True,
                            dmg=0, 
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=self.enemy,
                            sound=(True, self.atk2_sound , None, None),
                            kill_collide=True,
                            hitbox_scale_x=0.3,
                            hitbox_offset_y=150,


                            spawn_attack= {
                                'use_attack_onhit_pos': True,

                                    'attack_kwargs': {
                                    'frames': self.atk2,
                                    'frame_duration': 66.667, # freeze for 1s (second / frames) 15 frames
                                    'repeat_animation': 1,
                                    'speed': 0,
                                    'dmg': self.atk2_damage[0],
                                    'final_dmg': self.atk2_damage[1],
                                    'who_attacks': self,
                                    # defer who_attacked to collision time
                                    'moving': False,
                                    'sound': (True, self.atk2_sound, None, None),
                                    'delay': (False, 0),
                                    'stop_movement': (True, 1, 2),
                                }
                            }
                            )
                        attack_display.add(attack)
                        self.mana -=  self.attacks[1].mana_cost
                        self.attacks[1].last_used_time = current_time
                        self.running = False
                        # self.attacking2 = True
                        # self.player_atk2_index = 0
                        # self.player_atk2_index_flipped = 0

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 2 used')

                elif hotkey3 and not self.attacking3 and not self.attacking1 and not self.attacking2  and not self.basic_attacking:
                    if self.mana >= self.attacks[2].mana_cost and self.attacks[2].is_ready():
                        # self.jumping = True
                        # self.y_velocity = DEFAULT_JUMP_FORCE  # adjust jump strength as needed
                        # self.jump_attack_pending = True
                        # self.jump_attack_time = pygame.time.get_ticks() + 200  # 500ms later
                        # Create an attack
                        # print("Z key pressed")
                        # if self.jump_attack_pending and pygame.time.get_ticks() >= self.jump_attack_time:
                        #     self.jump_attack_pending = False
                        # print(self.enemy)
                        self.single_target()

                        attack = Attack_Display(
                            x=self.target.rect.centerx,
                            y=self.target.rect.centery + 40,
                            frames=self.atk3,
                            frame_duration=100, # 30 frames, 3 seconds
                            repeat_animation=1,
                            dmg=self.atk3_damage[0],
                            final_dmg=self.atk3_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            sound=(True, self.atk3_sound , None, None),
                            stop_movement=(True, 1, 2)
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

                        self.mana -=  self.attacks[3].mana_cost
                        self.attacks[3].last_used_time = current_time
                        self.running = False
                        self.sp_attacking = True
                        self.player_sp_index = 0
                        self.player_sp_index_flipped = 0

                        self.invisible = True
                        self.invisible_duration = (pygame.time.get_ticks()+820) + 5000
                        self.casting_invisible = True

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 4 used')

                elif basic_hotkey and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >= 0 and self.can_basic_attack():
                        attack = Attack_Display(
                            x=self.rect.centerx + 30 if self.facing_right else self.rect.centerx - 30,
                            y=self.rect.centery + 20,
                            frames=self.basic_slash3 if self.facing_right else self.basic_slash3_flipped,
                            frame_duration=BASIC_FRAME_DURATION+150,
                            repeat_animation=1,
                            speed=0,
                            dmg=self.basic_attack_damage,
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=self.enemy,

                            sound=(True, self.basic_sound, None, None),
                            delay=(True, self.basic_attack_animation_speed * (200 / self.base_animation_speed)), # self.basic_attack_animation_speed * (Base Delay/Default Basic Attack Speed)
                            moving=True,
                            is_basic_attack=True
                            )
                        attack_display.add(attack)
                        self.mana -= 0
                        self.attacks[4].last_used_time = current_time
                        self.running = False
                        self.attacking1 = True
                        self.player_atk1_index = 0
                        self.player_atk1_index_flipped = 0
                        self.last_basic_attack_time = current_time
                        # print("Attack executed")
                    else:
                        pass

                elif special_hotkey  and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.special >= MAX_SPECIAL: # and self.attacks[5].special_is_ready(self.special)
                        self.special_active = True
                        self.basic_sound.play()
                    else:
                        pass






        else:
            if not self.jumping and not self.is_dead():
                if hotkey1 and not self.attacking1 and not self.attacking2 and not self.attacking3  and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[0].mana_cost and self.attacks_special[0].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        # for i in [0, 200, 400, 600, 800]:
                        attack = Attack_Display(
                            x=self.rect.centerx,
                            y=self.rect.centery - 30,
                            frames=self.atk1_sp,
                            frame_duration=125, # 2 seconds 20 frames
                            repeat_animation=1,
                            speed=0,
                            dmg=self.sp_atk2_damage_2nd[0],
                            final_dmg=self.sp_atk2_damage_2nd[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            sound=(True, self.atk1_sound , None, None),
                            stop_movement=(True, 2, 2),
                            delay=(True, 100),
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


                elif hotkey2 and not self.attacking2 and not self.attacking1 and not self.attacking3  and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[1].mana_cost and self.attacks_special[1].is_ready():
                        for i in [True, False]:
                            attack = Attack_Display(
                                x=self.rect.centerx, # in front of him
                                y=self.rect.centery,
                                frames=self.player_run if i else self.player_run_flipped,
                                frame_duration=DEFAULT_ANIMATION_SPEED,
                                repeat_animation=10,
                                speed=self.speed if i else -self.speed,
                                moving=True,
                                dmg=0, 
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=self.enemy,
                                sound=(True, self.atk2_sound , None, None),
                                kill_collide=True,
                                hitbox_scale_x=0.3,
                                hitbox_offset_y=150,


                                spawn_attack= {
                                    'use_attack_onhit_pos': True,

                                        'attack_kwargs': {
                                        'frames': self.atk2,
                                        'frame_duration': 133.33, # freeze for 2s (second / frames) 15 frames
                                        'repeat_animation': 1,
                                        'speed': 0,
                                        'dmg': self.atk2_damage[0],
                                        'final_dmg': self.atk2_damage[1],
                                        'who_attacks': self,
                                        # defer who_attacked to collision time
                                        'moving': False,
                                        'sound': (True, self.atk2_sound, None, None),
                                        'delay': (False, 0),
                                        'stop_movement': (True, 1, 2),
                                    }
                                }
                                )
                            attack_display.add(attack)
                        self.mana -=  self.attacks_special[1].mana_cost
                        self.attacks_special[1].last_used_time = current_time
                        self.running = False
                        # self.attacking2 = True
                        # self.player_atk2_index = 0
                        # self.player_atk2_index_flipped = 0

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 2 used')

                elif hotkey3 and not self.attacking3 and not self.attacking1 and not self.attacking2  and not self.basic_attacking:
                    if self.mana >=  self.attacks_special[2].mana_cost and self.attacks_special[2].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        
                        self.single_target()
                        attack = Attack_Display(
                            x=self.target.rect.centerx,
                            y=self.target.rect.centery + 40,
                            frames=self.atk3,
                            frame_duration=133.33, # 30 frames, 4 seconds
                            repeat_animation=1,
                            dmg=self.atk3_damage[0]*1.5,
                            final_dmg=self.atk3_damage[1]*1.5,
                            who_attacks=self,
                            who_attacked=self.enemy,
                            sound=(True, self.atk3_sound , None, None),
                            stop_movement=(True, 1, 2)
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
                        attack = Attack_Display(
                            x=self.rect.centerx, # in front of him
                            y=self.rect.centery,
                            frames=self.player_run if self.facing_right else self.player_run_flipped,
                            frame_duration=DEFAULT_ANIMATION_SPEED,
                            repeat_animation=10,
                            speed=self.speed if self.facing_right else -self.speed,
                            moving=True,
                            dmg=0, 
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=self.enemy,
                            sound=(True, self.atk2_sound , None, None),
                            kill_collide=True,
                            hitbox_scale_x=0.3,
                            hitbox_offset_y=150,


                            spawn_attack= {
                                'use_attack_onhit_pos': True,

                                'attack_kwargs': {
                                    'frames': self.atk2,
                                    'frame_duration': 133.33, # freeze for 2s (second / frames) 15 frames
                                    'repeat_animation': 1,
                                    'speed': 0,
                                    'dmg': self.atk2_damage[0]*1.25,
                                    'final_dmg': self.atk2_damage[1],
                                    'who_attacks': self,
                                    # defer who_attacked to collision time
                                    'moving': False,
                                    'sound': (True, self.atk2_sound, None, None),
                                    'delay': (False, 0),
                                    'stop_movement': (True, 1, 2),
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

                        self.invisible = True
                        self.invisible_duration = (pygame.time.get_ticks()+820) + 5000
                        self.casting_invisible = True

                        # print("Attack executed")
                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")   
                    # print('Skill 4 used')

                elif basic_hotkey and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >= 0 and self.can_basic_attack():
                        attack = Attack_Display(
                            x=self.rect.centerx + 30 if self.facing_right else self.rect.centerx - 30,
                            y=self.rect.centery + 20,
                            frames=self.basic_slash3 if self.facing_right else self.basic_slash3_flipped,
                            frame_duration=BASIC_FRAME_DURATION+150,
                            repeat_animation=1,
                            speed=0,
                            dmg=self.basic_attack_damage * DEFAULT_BASIC_ATK_DMG_BONUS,
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=self.enemy,

                            sound=(True, self.basic_sound, None, None),
                            delay=(True, self.basic_attack_animation_speed * (200 / self.base_animation_speed)), # self.basic_attack_animation_speed * (Base Delay/Default Basic Attack Speed)
                            moving=True,
                            is_basic_attack=True
                            )
                        attack_display.add(attack)
                        self.mana -= 0
                        self.attacks_special[4].last_used_time = current_time
                        self.running = False
                        self.attacking1 = True
                        self.player_atk1_index = 0
                        self.player_atk1_index_flipped = 0
                        self.last_basic_attack_time = current_time
                        # print("Attack executed")
                    else:
                        pass

     
    def draw_health_bar(self, screen):
        if not self.invisible:
            super().draw_health_bar(screen)
        else:
            return
    def draw_mana_bar(self, screen):
        if not self.invisible:
            super().draw_mana_bar(screen)
        else:
            return
    def draw_special_bar(self, screen):
        if not self.invisible:
            super().draw_special_bar(screen)
        else:
            return
    def update(self):
        
        
        if not self.is_dead():
            self.player_death_index = 0
            self.player_death_index_flipped = 0
        if self.is_dead():
            self.play_death_animation()
        elif self.attacking1:
            if not self.invisible: self.atk1_animation()
            else: self.attacking1 = False
        # elif self.attacking2:
        #     self.atk2_animation()
        elif self.attacking3:
            if not self.invisible: self.atk3_animation()
            else: self.attacking3 = False
        elif self.jumping:
            if not self.invisible: self.jump_animation()
            else: self.jumping = False
        elif self.running and not self.jumping:
            if not self.invisible: self.run_animation()
            else: self.running = False

        if self.sp_attacking:
            self.sp_animation()
        
        else:
            if not self.is_dead():
                self.simple_idle_animation(RUNNING_ANIMATION_SPEED)

        
        
        

        # print(self.attacking1, self.attacking2, self.attacking3, self.sp_attacking, self.basic_attacking)

        # Apply gravity
        self.y_velocity += DEFAULT_GRAVITY/2
        self.y_pos += self.y_velocity/2
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
                if self.special <= 0:
                    self.special_active = False


        # if self.invisible:
        #     print(f'invisible for: {int((self.invisible_duration-pygame.time.get_ticks())/1000)}s')
        # if self.casting_invisible == True: # 820 CAST TIME!
        #     print('cast time')
        #     print((self.invisible_duration-pygame.time.get_ticks()))
        # # print(self.is_dead())

        
        # print(self.sp_attacking)
        # print(self.invisible)


                
                    #self.apply_item_bonuses()
        # print(self.basic_attack_damage)
                # self.max_mana = min(200, self.max_mana + 10)

        # self.special += 0.1
        # print(self.special)

        # pygame.draw.rect(screen, (255, 0, 0), self.rect)
        
        super().update() 
        # if not self.is_dead() and not self.invisible:
        #     self.draw_health_bar(screen) if global_vars.SHOW_MINI_HEALTH_BAR else None
        #     self.draw_mana_bar(screen) if global_vars.SHOW_MINI_MANA_BAR else None
        #     self.draw_special_bar(screen) if global_vars.SHOW_MINI_SPECIAL_BAR else None