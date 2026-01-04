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
import heroes
from player import Player
import global_vars
import pygame

from summon import create_summon_bot
from summons.skeleton import Skeleton

# Animation Counts
FIRE_WIZARD_BASIC_COUNT = 10
FIRE_WIZARD_JUMP_COUNT = 6
FIRE_WIZARD_RUN_COUNT = 8 
FIRE_WIZARD_IDLE_COUNT = 7
FIRE_WIZARD_ATK1_COUNT = 8
FIRE_WIZARD_SP_COUNT = 14
FIRE_WIZARD_DEATH_COUNT = 6

FIRE_WIZARD_ATK1 = 12 - 2 # reduce frame
FIRE_WIZARD_ATK2 = 53
FIRE_WIZARD_ATK3 = 34
FIRE_WIZARD_SP = 28
# ---------------------
# print((FIRE_WIZARD_ATK2 * 0.01) * 4 * 5)
FIRE_WIZARD_ATK1_MANA_COST = 50
FIRE_WIZARD_ATK2_MANA_COST = 80
FIRE_WIZARD_ATK3_MANA_COST = 100
FIRE_WIZARD_SP_MANA_COST = 200

FIRE_WIZARD_ATK1_SIZE = 3
FIRE_WIZARD_ATK2_SIZE = 0.3
FIRE_WIZARD_ATK3_SIZE = 0.3
FIRE_WIZARD_SP_SIZE = 1.3

class Fire_Wizard(Player):
    # Update log for heroes

        #wind hashashin
        # Skill 1: (10, 0) = 10 -> (8, 0) = 8
        # Skill 2: (35/45, 0):tornado = 5-6 + (15/15, 5):slash = 20 = 25-26 -> (35/45, 0):tornado = 5-6 + (12/15, 4):slash = 16 = 21-22
        # Skill 3: (200/20, 25):whirl = 10 + (15/15, 5):slash = 10 = 30 -> (35/45, 0):whirl = 5-6 + (12/15, 4):slash = 16 = 26
        # Skill 4: 18 * 4 = 72 -> 14.5 * 4 = 58

        # Skill 1: 3 * 6:per smoke = 0-18 -> 2.4 * 6:per smoke = 0-14.4
        # Skill 2: 30 -> 26
        # Skill 3: 37 = 37
        # Skill 4: 86 -> 69

        #fire knight nerf
        # Skill 1: (10/49, 2) = 12 -> (10/49, 1) = 11
        # Skill 2: (26/20, 2) = 30 -> (26/20, 2) = 28
        # Skill 3: (35/60, 10) = 45 -> (35/60, 7) = 42
        # Skill 4: 80 = 80

        #Skill 4: 
            # Swapped damage explosion
        # (10/10, 50):start + (25/10, 5):explosion = 90
        # -> (25/10, 5):start + (10/10, 45):explosion = 85



        # Wind hashashin buff
        # 8 -> 10 (dash speed and distance: 10 -> 12 (400 -> 500), sp: 12 -> 15 (600 -> 800))
        # x slashes (both slashes) (12/15, 4) -> (13/15, 5) total=(23-24 dmg)
        # 26 -> 28 (due to x slash)
        # 58 -> 64 (16)

        #fire knight nerf and wind hashashin buff
        #fire knight:
        # Trait: +20% Health Regen -> +15% Health Regen
        # Intelligence: 40 = 40, 180 -> 200 (removed -20 max mana)
        # Skill 1: 0
        # Skill 2: cd 16s - > 20s, mana cost 80 -> 100
        # Skill 3: cd 26s - > 30s, mana cost 140 -> 160
        # Skill 4: mana cost 180 -> 200, dmg = (65/65, 15) = 80 -> (60/65, 15) = 75 
        #            -> (25/10, 5):start = (10/10, 40):explosion = 80

        #wind hashashin:
        # Skill 1: (10/49, 2) = 12 -> (10/49, 1) = 11
        # Skill 2: (28/20, 2) = 30 -> (26/20, 2) = 28
        # Skill 3: (35/60, 10) = 45 -> (35/60, 7) = 42
        # Skill 4: 80 = 80

        #fire knight buff/nerf
        # Trait: +15% Health Regen -> +20% Health Regen
        # Skill 1: (10/49, 2) = 12 -> (10/49, 1) = 11
        # Skill 2: cd 20s - > 18s, mana cost 80 -> 100
        # Skill 3: cd 30s - > 26s, mana cost 160 -> 150
        # Skill 4: 0


        #wanderer magician nerf
        # special basic attack: (3.2/2.4)3 = 4 -> (3.2/2.5)3 = 3.84 per hit
        # special skill 3:  Damage Multiplier 25% -> 15%

        #fire knight nerf
        # Trait: +20% Health Regen -> +15% Health Regen
        # Skill 1: (10/49, 1) = 11 -> (10/49, 2) = 12
        # Skill 4: (60/65, 15) = 75 -> (50/65, 15) = 65
        # Special:
        # Skill 4: (attack no longer stick to enemy)
            # (25/10, 5):start = 30, (10/10, 40):explosion = 50 = 80 -> 
            # (20/10, 5):start = 25, (40/10, 5):explosion = 45 = 80

        # fire knight nerf
        # Intelligence: 40 = 200 mana ->  Intelligence: 36 = 180 mana
        # Skill 4: mana cost 200 -> 180
        #           damage = 75 -> 65

        # fire knight buff/update
        # Skill 2: mana cost 100 -> 80
        # SKill 4 hitbox modified
        # Skill 4 special: total damage = 70(20,40,5,5) = 100 (30,60,5,5)
        # 100 -> 80

        # fire wizard buff
        # Skill 4: damage (50/28, 10) = 60 -> (55/28, 10) -> 65
        
        # fire wizard update
        # Skill 2: reworked skill, low cooldown, low damage, special not changed

        # wanderer magician buff
        # Agility: 32 -> 35
        # Skill 1: mana cost 70 -> 65
        # Skill 2: cooldown 29s -> 24s, (26/10, 8) = 34 -> (29/10, 8) = 37
        # Skill 3: cooldown 26s -> 22s
        # Skill 4 special: (4.5/16, 0) = 67.5 -> (5/16, 1) = 90

        # forest ranger buff
        # I forgot...

        # fire wizard buff
        # trait: dmg_mult 10% -> 20%
        # Skill 2: mana cost 30 -> 15, cooldown 3s -> 1s

        # wanderer magician buff
        # Skill 2: cooldown 24s -> 22s, (15/40, 0)*2 = 30 heal -> (20/40, 0)*2 = 40 heal
        # Skill 3: cooldown 22s -> 17s

        # forest ranger nerf/buff
        # Agility: 38 -> 35
        # Strength: 33 -> 32
        # trait: lifesteal: 0.15 -> 0.1
        # arrow_stuck_damage: (self.basic_attack_damage * 0.3) - 0.05 = 1 ->  (self.basic_attack_damage * 0.5) - 0.25 = 1.5
        # dash speed: 4 -> 5

        # fire wizard update 12/9/25
        # trait: dmg_mult 20% -> 10% (20% is not actually implemented, too OP)
        # Skill 2: reverted back to original version with rework

        #update
        # water princess:
        # Skill 1: mana cost 100 -> 40, cooldown 15s -> 5, damage/heal 5/20 -> 5/10
        # reverted back to original
        # Skill 1: mana cost 100 -> 80, cooldown 15s -> 10s, damage/heal 5/20 -> 10/20
        

    def __init__(self, player_type, enemy):
        super().__init__(player_type, enemy)
        self.player_type = player_type # 1 for player 1, 2 for player 2
        self.name = "Fire Wizard"

        self.hitbox_rect = pygame.Rect(0, 0, 50, 100)

        # stat
        self.strength = 40
        self.intelligence = 40
        self.agility = 26 # real agility = 27
        
        # hp = 1.0, mana = 6.0, atk = 0.1
        self.base_health_regen = 0.8 # +0.4 = 1.2
        self.base_mana_regen = 5.3 # +0.4 = 5.7
        self.base_attack_damage = 0.1 # +2.6 = 2.7

        self.base_attack_speed = 100
        self.base_attack_time = 1700

        self.health_regen = self.calculate_regen(self.base_health_regen, self.hp_regen_per_str, self.strength) #0.8 + 40 * 0.01 = 1.2
        self.mana_regen = self.calculate_regen(self.base_mana_regen, self.mana_regen_per_int, self.intelligence) #5.3 + 40 * 0.01 = 5.7
        self.basic_attack_damage = self.calculate_regen(self.base_attack_damage, self.agi_mult, self.agility, basic_attack=True) # 0.1 + 26 * 0.1 = 2.7
        
        # Recalculate attack speed variables for fire wizard's base stats
        self.attack_speed = self.calculate_effective_as()
        self.basic_attack_cooldown = self.calculate_basic_attack_interval()
        self.basic_attack_animation_speed = global_vars.DEFAULT_ANIMATION_SPEED / (self.attack_speed / self.base_attack_speed)

        #2 attack per basic attack (5.6 DPS)
        # Base Stats
        self.max_health = self.strength * self.str_mult #40 * 5 = 200HP (max)
        self.max_mana = self.intelligence * self.int_mult #40 * 5 = 200Mana (max)
        self.health = self.max_health
        self.mana = self.max_mana
        # 1.4
        # 5.9
        # 4.05
        
        # BASIC_ATK_DAMAGE2

        
        # Player Position
        self.x = 50
        self.y = 50
        self.width = 200

        #mana cost
        self.atk1_mana_cost = 50
        self.atk2_mana_cost = 75
        self.atk3_mana_cost = 100
        self.sp_mana_cost = 200
        self.atk2_mana_cost_sp = 80
        
        #dmg
        self.atk1_cooldown = 7000 # 7000
        self.atk2_cooldown = 10000
        self.atk3_cooldown = 26000
        self.sp_cooldown = 60000
        self.atk2_cooldown_sp = 5000 + 13000
        #FORMULA = DESIRED DMG / TOTAL FRAME EX. dmg=25/34 == 0.6944
        self.damage_list = [
            (13, 0),
            (20/53, 0), #total damage=130
            (40/34, 0),
            (50/28, 10)
        ]
        self.atk1_damage = self.damage_list[0]
        self.atk2_damage = self.damage_list[1]
        self.atk3_damage = self.damage_list[2]
        self.sp_damage = self.damage_list[3] 
        dmg_mult = 0.1
        self.atk1_damage = self.atk1_damage[0] + (self.atk1_damage[0] * dmg_mult), self.atk1_damage[1] + (self.atk1_damage[1] * dmg_mult)
        self.atk2_damage = self.atk2_damage[0] + (self.atk2_damage[0] * dmg_mult), self.atk2_damage[1] + (self.atk2_damage[1] * dmg_mult)
        self.atk3_damage = self.atk3_damage[0] + (self.atk3_damage[0] * dmg_mult), self.atk3_damage[1] + (self.atk3_damage[1] * dmg_mult)
        self.sp_damage = self.sp_damage[0] + (self.sp_damage[0] * dmg_mult), self.sp_damage[1] + (self.sp_damage[1] * dmg_mult)

        # Player Animation Source
        basic_ani = [r'assets\characters\Fire wizard\slash pngs\Attack_1_', FIRE_WIZARD_BASIC_COUNT, 1]
        
        jump_ani = [r'assets\characters\Fire wizard\jump pngs\Jump_', FIRE_WIZARD_JUMP_COUNT, 1]
        run_ani = [r'assets\characters\Fire wizard\run pngs\Run_', FIRE_WIZARD_RUN_COUNT, 1]
        idle_ani= [r'assets\characters\Fire wizard\idle pngs\image_0-', FIRE_WIZARD_IDLE_COUNT, 1]
        atk1_ani= [r'assets\characters\Fire wizard\fireball pngs\image_0-', FIRE_WIZARD_ATK1_COUNT, 1]
        sp_ani= [r'assets\characters\Fire wizard\flame jet pngs\image_0-', FIRE_WIZARD_SP_COUNT, 1]
        death_ani= [r'assets\characters\Fire wizard\dead\tile00', FIRE_WIZARD_DEATH_COUNT, 1]

        # Player Skill Sounds Effects Source
        self.atk1_sound = pygame.mixer.Sound(r'assets\sound effects\fire_wizard\short-fire-whoosh_1-317280-[AudioTrimmer.com].mp3')
        self.atk2_sound = pygame.mixer.Sound(r'assets\sound effects\fire_wizard\fire-sound-efftect-21991.mp3')
        self.atk3_sound = pygame.mixer.Sound(r'assets\sound effects\fire_wizard\fire-sound-310285-[AudioTrimmer.com].mp3')
        self.sp_sound = pygame.mixer.Sound(r'assets\sound effects\fire_wizard\052168_huge-explosion-85199.mp3')
        self.atk1_sound.set_volume(0.5 * global_vars.MAIN_VOLUME)
        self.atk2_sound.set_volume(0.1 * global_vars.MAIN_VOLUME)
        self.atk3_sound.set_volume(0.5 * global_vars.MAIN_VOLUME)
        self.sp_sound.set_volume(0.5 * global_vars.MAIN_VOLUME)

        # Player Skill Animations Source
        atk1 = [r'assets\attacks\fire wizard\atk1', FIRE_WIZARD_ATK1, 1]
        atk2 = [r'assets\attacks\fire wizard\atk2', FIRE_WIZARD_ATK2, 1]
        atk3 = [r'assets\attacks\fire wizard\atk3\png_', FIRE_WIZARD_ATK3, 1]
        sp = [r'assets\attacks\fire wizard\sp atk', FIRE_WIZARD_SP, 1]

        self.bonus_type = "strength"
        self.bonus_value = self.strength

        # Player Skill Icons Source
        skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire_wizard\FireballIcon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_2 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire_wizard\GlyphOfFireIcon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire_wizard\RodOfPower29Icon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire_wizard\MeteorIcon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_icon = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire_wizard\kim special icon.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        special_skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire_wizard\FlameReaveIcon29.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire_wizard\SmiteIcon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire_wizard\VolcanicOrb29Icon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        # Player Icon Rects
        if self.player_type == 1:
            self.skill_1_rect = skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))

            self.special_rect = special_icon.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 4 + 50, SKILL_Y_OFFSET))

            self.special_skill_1_rect = special_skill_1.get_rect(center=(X_POS_SPACING + START_OFFSET_X, SKILL_Y_OFFSET))
            self.special_skill_2_rect = skill_2.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X, SKILL_Y_OFFSET))
            self.special_skill_3_rect = special_skill_3.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 2, SKILL_Y_OFFSET))
            self.special_skill_4_rect = special_skill_4.get_rect(center=(X_POS_SPACING + START_OFFSET_X + SPACING_X * 3, SKILL_Y_OFFSET))

        elif self.player_type == 2:
            self.special_rect = special_icon.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 4 - 50, SKILL_Y_OFFSET))

            self.special_skill_1_rect = special_skill_1.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 3, SKILL_Y_OFFSET))
            self.special_skill_2_rect = skill_2.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 2, SKILL_Y_OFFSET))
            self.special_skill_3_rect = special_skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X, SKILL_Y_OFFSET))
            self.special_skill_4_rect = special_skill_4.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X, SKILL_Y_OFFSET))

            self.skill_1_rect = skill_1.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 3, SKILL_Y_OFFSET))
            self.skill_2_rect = skill_2.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X * 2, SKILL_Y_OFFSET))
            self.skill_3_rect = skill_3.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X - SPACING_X, SKILL_Y_OFFSET))
            self.skill_4_rect = skill_4.get_rect(center=(DEFAULT_X_POS - START_OFFSET_X, SKILL_Y_OFFSET))

        # Player Attack Animations Load
        self.atk1 = self.load_img_frames_tile_method(atk1[0], atk1[1], atk1[2], FIRE_WIZARD_ATK1_SIZE)
        self.atk1_flipped = self.load_img_frames_flipped_tile_method(atk1[0], atk1[1], atk1[2], FIRE_WIZARD_ATK1_SIZE)
        self.atk2 = self.load_img_frames_numbering_method(atk2[0], atk2[1], atk2[2], FIRE_WIZARD_ATK2_SIZE)
        self.atk3 = self.load_img_frames_numbering_method_simple(atk3[0], atk3[1], atk3[2], FIRE_WIZARD_ATK3_SIZE)
        self.sp = self.load_img_frames_numbering_method(sp[0], sp[1], sp[2], FIRE_WIZARD_SP_SIZE)

        # Player Animations Load
        self.player_basic = self.load_img_frames(basic_ani[0], basic_ani[1], basic_ani[2], DEFAULT_CHAR_SIZE)
        self.player_basic_flipped = self.load_img_frames_flipped(basic_ani[0], basic_ani[1], basic_ani[2], DEFAULT_CHAR_SIZE)

        self.player_jump = self.load_img_frames(jump_ani[0], jump_ani[1], jump_ani[2], DEFAULT_CHAR_SIZE)
        self.player_jump_flipped = self.load_img_frames_flipped(jump_ani[0], jump_ani[1], jump_ani[2], DEFAULT_CHAR_SIZE)
        self.player_idle = self.load_img_frames(idle_ani[0], idle_ani[1], idle_ani[2], DEFAULT_CHAR_SIZE)
        self.player_idle_flipped = self.load_img_frames_flipped(idle_ani[0], idle_ani[1], idle_ani[2], DEFAULT_CHAR_SIZE)
        self.player_run = self.load_img_frames(run_ani[0], run_ani[1], run_ani[2], DEFAULT_CHAR_SIZE)
        self.player_run_flipped = self.load_img_frames_flipped(run_ani[0], run_ani[1], run_ani[2], DEFAULT_CHAR_SIZE)    
        self.player_atk1 = self.load_img_frames(atk1_ani[0], atk1_ani[1], atk1_ani[2], DEFAULT_CHAR_SIZE)
        self.player_atk1_flipped = self.load_img_frames_flipped(atk1_ani[0], atk1_ani[1], atk1_ani[2], DEFAULT_CHAR_SIZE)  
        self.player_atk2 = self.player_atk1
        self.player_atk2_flipped = self.player_atk1_flipped
        self.player_atk3 = self.player_atk1
        self.player_atk3_flipped = self.player_atk1_flipped
        self.player_sp = self.load_img_frames(sp_ani[0], sp_ani[1], sp_ani[2], DEFAULT_CHAR_SIZE)
        self.player_sp_flipped = self.load_img_frames_flipped(sp_ani[0], sp_ani[1], sp_ani[2], DEFAULT_CHAR_SIZE)
        self.player_death = self.load_img_frames(death_ani[0], death_ani[1], death_ani[2], DEFAULT_CHAR_SIZE)
        self.player_death_flipped = self.load_img_frames_flipped(death_ani[0], death_ani[1], death_ani[2], DEFAULT_CHAR_SIZE)

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
                mana_cost=self.atk2_mana_cost_sp,
                skill_rect=self.special_skill_2_rect,
                skill_img=skill_2,
                cooldown=self.atk2_cooldown_sp,
                mana=self.mana
            ),
            Attacks(
                mana_cost=int(self.mana_cost_list[2] - (self.mana_cost_list[2] * 0.2)),
                skill_rect=self.special_skill_3_rect,
                skill_img=special_skill_3,
                cooldown=self.atk3_cooldown,
                mana=self.mana
            ),
            Attacks(
                mana_cost=int(self.mana_cost_list[3] - (self.mana_cost_list[3] * 0.2)),
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
                    if self.mana >= self.attacks[0].mana_cost and self.attacks[0].is_ready():
                        
                        attack = Attack_Display(
                            x=self.rect.centerx - 20 if self.facing_right else self.rect.centerx + 20,
                            y=self.rect.centery + 30,
                            frames=self.atk1 if self.facing_right else self.atk1_flipped,
                            frame_duration=100,
                            repeat_animation=1,
                            speed=6 if self.facing_right else -6,
                            dmg=self.atk1_damage[0],
                            final_dmg=self.atk1_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            moving=True,
                            delay=(True, 800),
                            sound=(True, self.atk1_sound, None, None),

                            hitbox_scale_x=0.4
                            ,hitbox_scale_y=0.4
                            ) # Replace with the target
                        attack_display.add(attack)
                        self.mana -= self.attacks[0].mana_cost
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
                        # for i in [-200*3, -160*3, -120*3, -80*3, -40*3, 0, 40*3, 80*3, 120*3, 160*3, 200*3]:
                        #     attack = Attack_Display(
                        #         x=self.rect.centerx + 120 if self.facing_right else self.rect.centerx - 120, # in front of him
                        #         y=self.rect.centery + 30,
                        #         frames=self.atk2,
                        #         frame_duration=62.893, # 20seconds total #3.33 seconds each
                        #         repeat_animation=6,
                        #         speed=5 if self.facing_right else -5,
                        #         dmg=self.atk2_damage[0],
                        #         final_dmg=self.atk2_damage[1],
                        #         who_attacks=self,
                        #         who_attacked=self.enemy,
                        #         delay=(True, 800),
                        #         sound=(True, self.atk2_sound, None, None),
                        #         # stop_movement=(True,4,1)
                        #         ) # Replace with the target
                        #     attack_display.add(attack)

                        for i in [60*2, 120*2, 180*2]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i if self.facing_right else self.rect.centerx - i, # in front of him
                                y=self.rect.centery + 30,
                                frames=self.atk2,
                                frame_duration=62.893, # 20seconds total #3.33 seconds each
                                repeat_animation=6,
                                speed=5 if self.facing_right else -5,
                                dmg=self.atk2_damage[0],
                                final_dmg=self.atk2_damage[1],
                                who_attacks=self,
                                who_attacked=self.enemy,
                                delay=(True, 800),
                                sound=(True, self.atk2_sound, None, None)
                                ) # Replace with the target
                            attack_display.add(attack)

                        self.mana -= self.attacks[1].mana_cost
                        self.attacks[1].last_used_time = current_time
                        self.running = False
                        self.attacking2 = True
                        self.player_atk2_index = 0
                        self.player_atk2_index_flipped = 0
                        
                        

                        # summon = create_summon_bot(Skeleton, self.player_type, self.enemy)
                        # global_vars.summon_display.add(summon)

                        
                        # global_vars.assign_summon_enemy(self.player_type)
                        # for hero in (hero1_group if self.player_type == 2 else hero2_group):
                        #     hero.enemy = list(global_vars.summon_display)

                        # for h in hero1_group:
                        # h.enemy = list(hero2_group)

                    else:
                        pass
                        # print(f"Attack did not execute: {self.mana}:")               
                    # print('Skill 2 used')

                elif hotkey3 and not self.attacking3 and not self.attacking1 and not self.attacking2 and not self.sp_attacking and not self.basic_attacking:
                    if self.mana >= self.attacks[2].mana_cost and self.attacks[2].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx + 120 if self.facing_right else self.rect.centerx - 120, # in front of him
                            y=self.rect.centery + 30,
                            frames=self.atk3,
                            frame_duration=60,
                            repeat_animation=1,
                            speed=0.5 if self.facing_right else -0.5,
                            dmg=self.atk3_damage[0],
                            final_dmg=self.atk3_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            delay=(True, 800),
                            sound=(True, self.atk3_sound , None, None),
                                # stop_movement=(True,3,1, 0.2)
                            ) # Replace with the target
                        attack_display.add(attack)
                        self.mana -= self.attacks[2].mana_cost
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
                        attack = Attack_Display(
                            x=self.rect.centerx + 200 if self.facing_right else self.rect.centerx - 200, # in front of him
                            y=self.rect.centery - 100,
                            frames=self.sp,
                            frame_duration=80,
                            repeat_animation=1,
                            speed=5 if self.facing_right else -5,
                            dmg=self.sp_damage[0],
                            final_dmg=self.sp_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            sound=(True, self.sp_sound, None, None),
                                # stop_movement=(True, 3, 3, 0.5)
                            ) # Replace with the target
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

                elif basic_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >= 0 and self.can_basic_attack():
                        for i in [200, 900]:
                            attack = Attack_Display(
                                x=self.rect.centerx + 40 if self.facing_right else self.rect.centerx - 40,
                                y=self.rect.centery + 40,
                                frames=self.basic_slash if self.facing_right else self.basic_slash_flipped,
                                frame_duration=BASIC_FRAME_DURATION,
                                repeat_animation=1,
                                speed=0,
                                dmg=self.basic_attack_damage,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=self.enemy,

                                sound=(True, self.basic_sound, None, None),
                                delay=(True, self.basic_attack_animation_speed * (i / DEFAULT_ANIMATION_SPEED)), # self.basic_attack_animation_speed * (Base Delay/Default Basic Attack Speed)
                                moving=True,
                                is_basic_attack=True
                                )
                            attack_display.add(attack)
                        self.mana -= 0
                        self.attacks[4].cooldown = self.basic_attack_cooldown
                        self.attacks_special[4].cooldown = self.basic_attack_cooldown
                        self.attacks[4].last_used_time = current_time
                        self.running = False
                        self.basic_attacking = True
                        self.player_basic_index = 0
                        self.player_basic_index_flipped = 0
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
                    if self.mana >=  self.attacks_special[0].mana_cost and self.attacks_special[0].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        for i in [-50, 0, 50, 100]:
                            attack = Attack_Display(
                                x=self.rect.centerx - i if self.facing_right else self.rect.centerx + i,
                                y=self.rect.centery - i,
                                frames=self.atk1 if self.facing_right else self.atk1_flipped,
                                frame_duration=100,
                                repeat_animation=1,
                                speed=7 if self.facing_right else -7,
                                dmg=self.atk1_damage[0]/3,
                                final_dmg=self.atk1_damage[1],
                                who_attacks=self,
                                who_attacked=self.enemy,
                                moving=True,
                            sound=(True, self.atk1_sound , None, None),
                            delay=(True, 800)) # Replace with the target
                            attack_display.add(attack)
                            

                            attack2 = Attack_Display(
                                x=self.rect.centerx + i if self.facing_right else self.rect.centerx - i,
                                y=self.rect.centery - i,
                                frames=self.atk1_flipped if self.facing_right else self.atk1,
                                frame_duration=100,
                                repeat_animation=1,
                                speed=-7 if self.facing_right else 7,
                                dmg=self.atk1_damage[0]/6,
                                final_dmg=self.atk1_damage[1],
                                who_attacks=self,
                                who_attacked=self.enemy,
                                moving=True,
                            delay=(True, 800)) # Replace with the target
                            attack_display.add(attack2)
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
                        for i in [-200*3, -160*3, -120*3, -80*3, -40*3, 0, 40*3, 80*3, 120*3, 160*3, 200*3]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i if self.facing_right else self.rect.centerx - i, # in front of him
                                y=self.rect.centery + 30,
                                frames=self.atk2,
                                frame_duration=47.16, # 15 seconds = damage / 2
                                repeat_animation=6,
                                speed=5 if self.facing_right else -5,
                                dmg=self.atk2_damage[0]/2,
                                final_dmg=self.atk2_damage[1]/2,
                                who_attacks=self,
                                who_attacked=self.enemy,
                            delay=(True, 800)) # Replace with the target
                            attack_display.add(attack)
                        self.atk2_sound.play()
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
                        attack = Attack_Display(
                            x=self.rect.centerx + 120 if self.facing_right else self.rect.centerx - 120, # in front of him
                            y=self.rect.centery + 30,
                            frames=self.atk3,
                            frame_duration=60,
                            repeat_animation=2,
                            speed=1 if self.facing_right else -1,
                            dmg=self.atk3_damage[0] * 0.7,
                            final_dmg=self.atk3_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            moving=True,
                            continuous_dmg=True,
                            sound=(True, self.atk3_sound , None, None),
                            delay=(True, 800)) # Replace with the target
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
                        for i in [-1000, -500, 0, 500, 1000]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i if self.facing_right else self.rect.centerx - i, # in front of him
                                y=self.rect.centery - 100,
                                frames=self.sp,
                                frame_duration=80,
                                repeat_animation=1,
                                speed=5 if self.facing_right else -5,
                                dmg=self.sp_damage[0]/1.1,
                                final_dmg=self.sp_damage[1]/1.1,
                                who_attacks=self,
                                who_attacked=self.enemy,
                            sound=(True, self.sp_sound , None, None)) # Replace with the target
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

                elif basic_hotkey and not self.sp_attacking and not self.attacking1 and not self.attacking2 and not self.attacking3 and not self.basic_attacking:
                    if self.mana >= 0 and self.can_basic_attack():
                        
                        for i in [200, 900]:
                            attack = Attack_Display(
                                x=self.rect.centerx + 40 if self.facing_right else self.rect.centerx - 40,
                                y=self.rect.centery + 40,
                                frames=self.basic_slash if self.facing_right else self.basic_slash_flipped,
                                frame_duration=BASIC_FRAME_DURATION,
                                repeat_animation=1,
                                speed=0,
                                dmg=self.basic_attack_damage  * DEFAULT_BASIC_ATK_DMG_BONUS,
                                final_dmg=0,
                                who_attacks=self,
                                who_attacked=self.enemy,

                                sound=(True, self.basic_sound, None, None),
                                delay=(True, self.basic_attack_animation_speed * (i / DEFAULT_ANIMATION_SPEED)), # self.basic_attack_animation_speed * (Base Delay/Default Basic Attack Speed)
                                moving=True,
                                is_basic_attack=True
                                )
                            attack_display.add(attack)
                        self.mana -= 0
                        self.attacks_special[4].last_used_time = current_time
                        self.running = False
                        self.basic_attacking = True
                        self.player_basic_index = 0
                        self.player_basic_index_flipped = 0
                        self.last_basic_attack_time = current_time

                        # print("Attack executed")
                    else:
                        pass

                
     
            
        
    
    def update(self):
        
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
         
        
        if not self.is_dead():
            self.player_death_index = 0
            self.player_death_index_flipped = 0
        if self.is_dead():
            self.play_death_animation()
        elif self.jumping:
            self.jump_animation()
        elif self.running and not self.jumping:
            self.run_animation(self.running_animation_speed)
        elif self.attacking1:
            self.atk1_animation()
        elif self.attacking2:
            self.atk2_animation()
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

        
        super().update()