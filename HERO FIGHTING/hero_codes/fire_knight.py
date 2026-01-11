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
FIRE_KNIGHT_JUMP_COUNT = 20
FIRE_KNIGHT_RUN_COUNT = 8 
FIRE_KNIGHT_IDLE_COUNT = 8
FIRE_KNIGHT_ATK1_COUNT = 11
FIRE_KNIGHT_ATK2_COUNT = 19
FIRE_KNIGHT_ATK3_COUNT = 28
FIRE_KNIGHT_SP_COUNT = 18
FIRE_KNIGHT_DEATH_COUNT = 13


FIRE_KNIGHT_ATK1_MANA_COST = 30
FIRE_KNIGHT_ATK2_MANA_COST = 80
FIRE_KNIGHT_ATK3_MANA_COST = 140
FIRE_KNIGHT_SP_MANA_COST = 180

FIRE_KNIGHT_ATK1_SIZE = 5
FIRE_KNIGHT_ATK2_SIZE = 1.5
FIRE_KNIGHT_ATK3_SIZE = 2
FIRE_KNIGHT_SP_SIZE = 2.5

#1=49, 2=20, 3=60, 4=65 atk frames

FIRE_KNIGHT_ATK1_COOLDOWN = 5000
FIRE_KNIGHT_ATK2_COOLDOWN = 16000
FIRE_KNIGHT_ATK3_COOLDOWN = 26000
FIRE_KNIGHT_SP_COOLDOWN = 60000

FIRE_KNIGHT_ATK1_DAMAGE = (10/49, 0)
FIRE_KNIGHT_ATK2_DAMAGE = (25/20, 5)
FIRE_KNIGHT_ATK3_DAMAGE = (40/60, 10) #35
FIRE_KNIGHT_SP_DAMAGE = (60/65, 15) # 55

FIRE_KNIGHT_BURN_DAMAGE = 10

class Display_Text: # display damage taken text previously (not working for now)
    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.num_txt = ''
        self.health = health
        self.health_detect = 0

        self.font = pygame.font.SysFont('Times New Roman', 25)
        self.text = self.font.render(self.num_txt, global_vars.TEXT_ANTI_ALIASING, 'Red')
        
        self.health_now = self.health
        if self.health_now >= self.health_detect:
            self.health_detect = self.health
        else:
            self.num_txt = str(self.health_detect - self.health_now)
            screen.blit(self.num_txt, (self.x, self.y - 100))
            self.health_detect = self.health
        
  

class Fire_Knight(Player):
    def __init__(self, player_type, enemy):
        super().__init__(player_type, enemy)
        # self.display_text = Display_Text(self.x_pos, self.y_pos, self.health)

        self.player_type = player_type
        self.name = "Fire Knight"

        self.hitbox_rect = pygame.Rect(0, 0, 50, 100)

        # stat
        self.strength = 42
        self.intelligence = 36
        self.agility = 33 # 32*2 = 64 agility(65 -> 64) # NOO REVERT BACK! 64 -> 65

        self.base_health_regen = 1.1 # 1.52
        self.base_mana_regen = 4.85 # 5.21
        self.base_attack_damage = 3.4 # 6.7

        self.base_attack_speed = 60
        self.base_attack_time = 1800

        self.base_animation_speed = 120
        self.min_animation_speed = 80
        self.attack_speed_modifier = 0.5

        self.health_regen = self.calculate_regen(self.base_health_regen, self.hp_regen_per_str, self.strength) #1.1 + 42 * 0.01 = 1.52
        self.mana_regen = self.calculate_regen(self.base_mana_regen, self.mana_regen_per_int, self.intelligence) #4.85 + 36 * 0.01 = 5.21
        self.basic_attack_damage = self.calculate_regen(self.base_attack_damage, self.agi_mult, self.agility, basic_attack=True) # 0.2 + 63 * 0.1 = 6.5

        # Recalculate attack speed variables for fire wizard's base stats
        self.attack_speed = self.calculate_effective_as()
        self.basic_attack_cooldown = self.calculate_basic_attack_interval()
        self.basic_attack_animation_speed = self.calculate_attack_animation_speed()


        # Base Stats
        self.max_health = (self.strength * self.str_mult) + 20
        self.max_mana = (self.intelligence * self.int_mult)
        self.health = self.max_health
        self.mana = self.max_mana

        # Player Position
        self.x = 50
        self.y = 50
        self.width = 200

        self.atk1_mana_cost = 30
        self.atk2_mana_cost = 80
        self.atk3_mana_cost = 150   
        self.sp_mana_cost = 180

        self.atk1_cooldown = 5000
        self.atk2_cooldown = 18000
        self.atk3_cooldown = 26000
        self.sp_cooldown = 60000

        self.atk1_damage = (10/49, 2)
        self.atk2_damage = (26/20, 2) #27 = 32, 3 = 29, 26 = 28
        self.atk3_damage = (35/60, 7)
        self.sp_damage = (50/65, 15) 
        self.special_sp_damage1 = (20/10, 0) # 25, total 70 damage #start
        self.special_sp_damage2 = (60/10, 0) # 45 #explosion (total=70 -> )
        

        dmg_mult = 0
        self.atk1_damage = self.atk1_damage[0] + (self.atk1_damage[0] * dmg_mult), self.atk1_damage[1] + (self.atk1_damage[1] * dmg_mult)
        self.atk2_damage = self.atk2_damage[0] + (self.atk2_damage[0] * dmg_mult), self.atk2_damage[1] + (self.atk2_damage[1] * dmg_mult)
        self.atk3_damage = self.atk3_damage[0] + (self.atk3_damage[0] * dmg_mult), self.atk3_damage[1] + (self.atk3_damage[1] * dmg_mult)
        self.sp_damage = self.sp_damage[0] + (self.sp_damage[0] * dmg_mult), self.sp_damage[1] + (self.sp_damage[1] * dmg_mult)
        self.special_sp_damage1 = self.special_sp_damage1[0] + (self.special_sp_damage1[0] * dmg_mult), self.special_sp_damage1[1] + (self.special_sp_damage1[1] * dmg_mult)
        self.special_sp_damage2 = self.special_sp_damage2[0] + (self.special_sp_damage2[0] * dmg_mult), self.special_sp_damage2[1] + (self.special_sp_damage2[1] * dmg_mult)
        
        
        # Player Animation Source
        jump_ani = [r'assets\characters\fire knight\03_jump\jump_', FIRE_KNIGHT_JUMP_COUNT, 0]
        run_ani = [r'assets\characters\fire knight\02_run\run_', FIRE_KNIGHT_RUN_COUNT, 0]
        idle_ani = [r'assets\characters\fire knight\01_idle\idle_', FIRE_KNIGHT_IDLE_COUNT, 0]
        atk1_ani = [r'assets\characters\fire knight\05_1_atk\1_atk_', FIRE_KNIGHT_ATK1_COUNT, 0]
        atk2_ani = [r'assets\characters\fire knight\06_2_atk\2_atk_', FIRE_KNIGHT_ATK2_COUNT, 0]
        atk3_ani = [r'assets\characters\fire knight\07_3_atk\3_atk_', FIRE_KNIGHT_ATK3_COUNT, 0]
        sp_ani = [r'assets\characters\fire knight\08_sp_atk\sp_atk_', FIRE_KNIGHT_SP_COUNT, 0]
        death_ani = [r'assets\characters\fire knight\11_death\death_', FIRE_KNIGHT_DEATH_COUNT, 0]

        # Player Skill Sounds Effects Source
        self.atk1_sound = pygame.mixer.Sound(r'assets\sound effects\fire_wizard\short-fire-whoosh_1-317280-[AudioTrimmer.com].mp3')
        self.atk2_sound = pygame.mixer.Sound(r'assets\sound effects\fire knight\2nd.mp3')
        self.atk3_sound = pygame.mixer.Sound(r'assets\sound effects\fire knight\3rrd.mp3')
        self.sp_sound = pygame.mixer.Sound(r'assets\sound effects\fire knight\ult.mp3')
        self.atk1_sound.set_volume(0.5 * global_vars.MAIN_VOLUME)
        self.atk2_sound.set_volume(0.5 * global_vars.MAIN_VOLUME)
        self.atk3_sound.set_volume(0.5 * global_vars.MAIN_VOLUME)
        self.sp_sound.set_volume(0.5 * global_vars.MAIN_VOLUME)

        self.burn_sound = pygame.mixer.Sound(r'assets\sound effects\fire_wizard\fire-sound-310285-[AudioTrimmer.com].mp3')
        self.burn_sound.set_volume(0.5 * global_vars.MAIN_VOLUME)

        # Player Skill Animations Source
        # atk1 = [r'', FIRE_KNIGHT_ATK1, 1]
        # atk2 = [r', FIRE_KNIGHT_ATK2, 1]
        # atk3 = [r'assets\attacks\fire knight\atk3\png_', FIRE_KNIGHT_ATK3, 1]
        # sp = [r'assets\attacks\fire knight\sp atk', FIRE_KNIGHT_SP, 1]

        # Player Skill Icons Source
        skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire knight\3.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_2 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire knight\4.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire knight\5.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire knight\6.png').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_icon = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire knight\special icon.jpeg').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

        special_skill_1 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire knight\FirebrandIcon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_2 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire knight\ForgeStrikeIcon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_3 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire knight\InfernalLegacyIcon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))
        special_skill_4 = pygame.transform.scale(pygame.image.load(r'assets\skill icons\fire knight\FireShieldIcon.webp').convert_alpha(), (ICON_WIDTH, ICON_HEIGHT))

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
        self.atk1 = load_attack(
        filepath=r"assets\attacks\fire knight\atk1\6_flamelash_spritesheet.png",
        frame_width=100, 
        frame_height=100, 
        rows=7, 
        columns=7, 
        scale=FIRE_KNIGHT_ATK1_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.atk1_flipped = load_attack_flipped(
        filepath=r"assets\attacks\fire knight\atk1\6_flamelash_spritesheet.png",
        frame_width=100, 
        frame_height=100, 
        rows=7, 
        columns=7, 
        scale=FIRE_KNIGHT_ATK1_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.atk2 = load_attack(
        filepath=r"assets\attacks\fire knight\atk2\414.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=4, 
        columns=5, 
        scale=FIRE_KNIGHT_ATK2_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.atk3 = load_attack(
        filepath=r"assets\attacks\fire knight\atk3\D65.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=12, 
        columns=5, 
        scale=FIRE_KNIGHT_ATK3_SIZE, 
        rotation=0,
        frame_duration=100
    )
        self.sp = load_attack(
        filepath=r"assets\attacks\fire knight\sp\D30.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=13, 
        columns=5, 
        scale=FIRE_KNIGHT_SP_SIZE, 
        rotation=0,
        frame_duration=100
    )
        



        # 10 FRAMES INITIAL EXPLOSION
        self.sp_special1 = load_attack(
        filepath=r"assets\attacks\fire knight\021.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=2, 
        columns=5, 
        scale=3, 
        rotation=0,
        frame_duration=100
    )
        # 10 FRAMES EXPLOSION
        self.sp_special2 = load_attack(
        filepath=r"assets\attacks\fire knight\038.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=2, 
        columns=5, 
        scale=3, 
        rotation=0,
        frame_duration=100
    )
        
        self.burn = load_attack(
        filepath=r"assets\attacks\fire knight\D65 cropped.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=8, 
        columns=5, 
        scale=1, 
        rotation=0,
        frame_duration=100 
    )
        self.atk3_special = load_attack(
        filepath=r"assets\attacks\fire knight\083.PNG",
        frame_width=100, 
        frame_height=100, 
        rows=4, 
        columns=5, 
        scale=FIRE_KNIGHT_ATK2_SIZE, 
        rotation=0,
        frame_duration=100
    )
      
    
        
    

        # Player Animations Load
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
        self.player_sp_flipped = self.load_img_frames_flipped(sp_ani[0], sp_ani[1], sp_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_death = self.load_img_frames(death_ani[0], death_ani[1], death_ani[2], DEFAULT_CHAR_SIZE_2)
        self.player_death_flipped = self.load_img_frames_flipped(death_ani[0], death_ani[1], death_ani[2], DEFAULT_CHAR_SIZE_2)

        # Player Image and Rect
        self.image = self.player_idle[self.player_idle_index]
        self.rect = self.image.get_rect(midbottom = (self.x_pos, self.y_pos)) #(for p1)
        
        # Mana Values
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
                mana_cost=int(self.mana_cost_list[0] - (self.mana_cost_list[0] * 0.3)),
                skill_rect=self.special_skill_1_rect,
                skill_img=special_skill_1,
                cooldown=int(self.atk1_cooldown/2),
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

        # self.health_detect = 0

        #health = 20, if health > prev health = prev health - health 
        self.health_regen = self.health_regen + (self.health_regen*0.15)


    
    
    
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
                speed_modifier = -0.2,
                special_active_speed = -0.1,
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
                    if self.mana >=  self.attacks[0].mana_cost and self.attacks[0].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx + 80 if self.facing_right else self.rect.centerx - 80,
                            y=self.rect.centery + 30,
                            frames=self.atk1 if self.facing_right else self.atk1_flipped,
                            frame_duration=20,
                            repeat_animation=1,
                            speed=3.5 if self.facing_right else -3.5,
                            dmg=self.atk1_damage[0],
                            final_dmg=self.atk1_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            sound=(True, self.atk1_sound , None, None),
                            delay=(True, self.basic_attack_animation_speed * (700 / DEFAULT_ANIMATION_SPEED)), # self.basic_attack_animation_speed * (Base Delay/Default Basic Attack Speed)
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
                    if self.mana >=  self.attacks[1].mana_cost and self.attacks[1].is_ready():
                        # Create an attack
                        # print("Z key pressed")
                        # for i in [40*2, 80*2, 120*2, 160*2, 200*2]:
                        attack = Attack_Display(
                            x=self.rect.centerx + 130 if self.facing_right else self.rect.centerx - 130, # in front of him
                            y=self.rect.centery + 30,
                            frames=self.atk2,
                            frame_duration=150,
                            repeat_animation=1,
                            speed=5 if self.facing_right else -5,
                            dmg=self.atk2_damage[0],
                            final_dmg=self.atk2_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            stun=(True, 50),
                            sound=(True, self.atk2_sound , None, None),
                            delay=(True, 700)
                        )
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
                    if self.mana >=  self.attacks[2].mana_cost and self.attacks[2].is_ready():
                        # Create an attack
                        print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx + 180 if self.facing_right else self.rect.centerx - 180, # in front of him
                            y=self.rect.centery + 30,
                            frames=self.atk3,
                            frame_duration=20,
                            repeat_animation=1,
                            speed=0.5 if self.facing_right else -0.5,
                            dmg=self.atk3_damage[0],
                            final_dmg=self.atk3_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            sound=(True, self.atk3_sound , None, None),
                            delay=(True, 700)
                            )
                        attack_display.add(attack)
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
                        attack = Attack_Display(
                            x=self.rect.centerx + 200 if self.facing_right else self.rect.centerx - 200, # in front of him
                            y=self.rect.centery - 50,
                            frames=self.sp,
                            frame_duration=20,
                            repeat_animation=1,
                            speed=5 if self.facing_right else -5,
                            dmg=self.sp_damage[0],
                            final_dmg=self.sp_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            sound=(True, self.sp_sound , None, None),
                            hitbox_scale_x=0.7
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
                        attack = Attack_Display(
                            x=self.rect.centerx + 70 if self.facing_right else self.rect.centerx - 70,
                            y=self.rect.centery + 90,
                            frames=self.basic_slash_big if self.facing_right else self.basic_slash_flipped_big,
                            frame_duration=BASIC_FRAME_DURATION + 50,
                            repeat_animation=1,
                            speed=0,
                            dmg=self.basic_attack_damage,
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=self.enemy,

                            sound=(True, self.basic_sound, None, None),
                            delay=(True, self.basic_attack_animation_speed * (700 / self.base_animation_speed)), # self.basic_attack_animation_speed * (Base Delay/Default Basic Attack Speed)
                            moving=True
                            ,is_basic_attack=True

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
                        attack = Attack_Display(
                            x=self.rect.centerx + 80 if self.facing_right else self.rect.centerx - 80,
                            y=self.rect.centery + 30,
                            frames=self.atk1 if self.facing_right else self.atk1_flipped,
                            frame_duration=5,
                            repeat_animation=1,
                            speed=3.5 if self.facing_right else -3.5,
                            dmg=self.atk1_damage[0]* 0.6,
                            final_dmg=self.atk1_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            sound=(True, self.atk1_sound , None, None),
                            delay=(True, self.basic_attack_animation_speed * (700 / DEFAULT_ANIMATION_SPEED)), # self.basic_attack_animation_speed * (Base Delay/Default Basic Attack Speed)
                            hitbox_scale_x=0.4
                            ,hitbox_scale_y=0.4
                            ) # Replace with the target
                        attack_display.add(attack)

                        # This fire don't work properly, need fixing soon
                        self.single_target()
                        burn_attack = Attack_Display(
                            x=self.rect.centerx + 80 if self.facing_right else self.rect.centerx - 80, # in front of him
                            y=self.rect.centery + 100,
                            frames=self.burn,
                            frame_duration=200,
                            repeat_animation=2,
                            speed=0.5 if self.facing_right else -0.5,
                            dmg=0,
                            final_dmg=FIRE_KNIGHT_BURN_DAMAGE * 0.2,
                            who_attacks=self,
                            who_attacked=self.target,
                            sound=(True, self.burn_sound, None, None),
                            delay=(True, self.basic_attack_animation_speed * (700 / DEFAULT_ANIMATION_SPEED)), # self.basic_attack_animation_speed * (Base Delay/Default Basic Attack Speed)
                            follow=(True, False),
                            follow_offset=(0, 80)
                            )
                        attack_display.add(burn_attack)

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
                        for i in [(130, 700), (250, 1700), (370, 2700)]:
                            attack = Attack_Display(
                                x=self.rect.centerx + i[0] if self.facing_right else self.rect.centerx - i[0], # in front of him
                                y=self.rect.centery + 30,
                                frames=self.atk2,
                                frame_duration=150,
                                repeat_animation=1,
                                speed=1 if self.facing_right else -1,
                                dmg=self.atk2_damage[0] * 0.4,
                                final_dmg=self.atk2_damage[1] * 0.4,
                                who_attacks=self,
                                who_attacked=self.enemy,
                                stun=(True, 50),
                                sound=(True, self.atk2_sound , None, None),
                                delay=(True, i[1]),

                                moving=True,
                                continuous_dmg=True
                                ) # Replace with the target
                            attack_display.add(attack)

                            self.single_target()
                            burn_attack = Attack_Display(
                            x=self.rect.centerx + i[0] if self.facing_right else self.rect.centerx - i[0], # in front of him
                            y=self.rect.centery + 100,
                            frames=self.burn,
                            frame_duration=200,
                            repeat_animation=2,
                            speed=0.5 if self.facing_right else -0.5,
                            dmg=0,
                            final_dmg=FIRE_KNIGHT_BURN_DAMAGE * 0.4,
                            who_attacks=self,
                            who_attacked=self.target,
                            sound=(True, self.burn_sound, None, None),
                            delay=(True, i[1]),
                            follow=(True, False),
                            follow_offset=(0, 80)
                            )
                            attack_display.add(burn_attack)
                        
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
                        print("Z key pressed")
                        attack = Attack_Display(
                            x=self.rect.centerx + 130 if self.facing_right else self.rect.centerx - 130, # in front of him
                            y=self.rect.centery + 30,
                            frames=self.atk3_special,
                            frame_duration=200,
                            repeat_animation=1,
                            speed=5 if self.facing_right else -5,
                            dmg=self.atk2_damage[0]*1.6,
                            final_dmg=self.atk2_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            stun=(True, 100),
                            sound=(True, self.atk2_sound , None, None),
                            delay=(True, 700)
                        )
                        
                        attack_display.add(attack)

                        self.single_target()
                        burn_attack = Attack_Display(
                            x=self.rect.centerx + 130 if self.facing_right else self.rect.centerx - 130, # in front of him
                            y=self.rect.centery + 100,
                            frames=self.burn,
                            frame_duration=200,
                            repeat_animation=2,
                            speed=0.5 if self.facing_right else -0.5,
                            dmg=0,
                            final_dmg=FIRE_KNIGHT_BURN_DAMAGE,
                            who_attacks=self,
                            who_attacked=self.target,
                            sound=(True, self.burn_sound, None, None),
                            delay=(True, 700),
                            follow=(True, False),
                            follow_offset=(0, 80)
                            )
                        attack_display.add(burn_attack)
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
                        
                        for i in [
                            (self.sp_special1, False, 100, 230, self.special_sp_damage1[0], self.special_sp_damage1[1]),
                            (self.sp_special2, True, 90, 200, self.special_sp_damage2[0], self.special_sp_damage2[1])]: # special 1 = gold explode
                            attack = Attack_Display(
                                x=self.rect.centerx + 250 if self.facing_right else self.rect.centerx - 250, # in front of him
                                y=self.rect.centery + i[2],
                                frames=i[0],
                                frame_duration=i[3],
                                repeat_animation=1,
                                speed=5 if self.facing_right else -5,
                                dmg=i[4],
                                final_dmg=i[5],
                                who_attacks=self,
                                who_attacked=self.enemy,
                                sound=(True, self.sp_sound , None, None),
                                delay=(i[1], 1200),
                                follow=(False, False)
                                ) # Replace with the target
                            attack_display.add(attack)

                            self.single_target()
                            burn_attack = Attack_Display(
                                x=self.rect.centerx + i[3] if self.facing_right else self.rect.centerx - i[3], # in front of him
                                y=self.rect.centery + i[2],
                                frames=self.burn,
                                frame_duration=200,
                                repeat_animation=2,
                                speed=0.5 if self.facing_right else -0.5,
                                dmg=0,
                                final_dmg=FIRE_KNIGHT_BURN_DAMAGE * 0.5,
                                who_attacks=self,
                                who_attacked=self.target,
                                sound=(True, self.burn_sound, None, None),
                                delay=(i[1], 1200),
                                follow=(True, False),
                                follow_offset=(0, 80)
                                )
                            attack_display.add(burn_attack)

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
                        attack = Attack_Display(
                            x=self.rect.centerx + 70 if self.facing_right else self.rect.centerx - 70,
                            y=self.rect.centery + 90,
                            frames=self.basic_slash_big if self.facing_right else self.basic_slash_flipped_big,
                            frame_duration=BASIC_FRAME_DURATION + 50,
                            repeat_animation=1,
                            speed=0 if self.facing_right else 0,
                            dmg=self.basic_attack_damage*DEFAULT_BASIC_ATK_DMG_BONUS,
                            final_dmg=0,
                            who_attacks=self,
                            who_attacked=self.enemy,
                            delay=(True, self.basic_attack_animation_speed * (700 / self.base_animation_speed)), # self.basic_attack_animation_speed * (Base Delay/Default Basic Attack Speed)
                            sound=(True, self.basic_sound, None, None),
                            moving=True
                            ,is_basic_attack=True

                            
                            )
                        attack_display.add(attack)

                        self.single_target()
                        burn_attack = Attack_Display(
                            x=self.rect.centerx + 70 if self.facing_right else self.rect.centerx - 70, # in front of him
                            y=self.rect.centery + 100,
                            frames=self.burn,
                            frame_duration=200,
                            repeat_animation=2,
                            speed=0.5 if self.facing_right else -0.5,
                            dmg=0,
                            final_dmg=FIRE_KNIGHT_BURN_DAMAGE * 0.1,
                            who_attacks=self,
                            who_attacked=self.target,
                            sound=(True, self.burn_sound, None, None),
                            delay=(True, self.basic_attack_animation_speed * (700 / DEFAULT_ANIMATION_SPEED)), # self.basic_attack_animation_speed * (Base Delay/Default Basic Attack Speed)
                            follow=(True, False),
                            follow_offset=(0, 80)
                            )
                        attack_display.add(burn_attack)
                        self.mana -= 0
                        self.attacks_special[4].last_used_time = current_time
                        self.running = False
                        self.attacking1 = True
                        self.player_atk1_index = 0
                        self.player_atk1_index_flipped = 0
                        self.basic_sound.play()

                        self.basic_attacking = True
                        self.last_basic_attack_time = current_time
                        # print("Attack executed")
                    else:
                        pass
                
     
            

    def update(self):
        # self.display_text = Display_Text(self.x_pos, self.y_pos, self.health)

        # self.health_regen += 0.0001

         

        if not self.is_dead():
            self.player_death_index = 0
            self.player_death_index_flipped = 0
        if self.is_dead():
            self.play_death_animation()
        elif self.jumping:
            self.jump_animation()
        elif self.running and not self.jumping:
            self.run_animation(self.running_animation_speed-2)
        elif self.attacking1:
            self.atk1_animation()
        elif self.attacking2:
            self.atk2_animation()
        elif self.attacking3:
            self.atk3_animation()
        elif self.sp_attacking:
            self.sp_animation()
        elif self.basic_attacking:
            pass
            # self.basic_animation(self.basic_attack_animation_speed)
        else:
            self.simple_idle_animation(RUNNING_ANIMATION_SPEED)

        
        

        # Apply gravity
        self.y_velocity += (DEFAULT_GRAVITY + (DEFAULT_GRAVITY * 0.03))
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

        
        super().update()