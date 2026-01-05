import pygame

from global_vars import (
    width, height, icon, FPS, clock, screen, hero1, hero2, BASIC_SLASH_ANIMATION, BASIC_SLASH_SIZE, ICON_WIDTH, ICON_HEIGHT, BASIC_ATK_POSX, BASIC_ATK_POSY, BASIC_ATK_POSX_END, BASIC_SLASH_SIZE_BIG,
    white, red, black, green, cyan2, gold, MAX_SPECIAL, BASIC_ATK_COOLDOWN, MAIN_VOLUME,
    DEFAULT_HEALTH_REGENERATION, DEFAULT_MANA_REGENERATION,
    LITERAL_HEALTH_DEAD, DEFAULT_ANIMATION_SPEED, DEFAULT_ANIMATION_SPEED_FOR_JUMPING, RUNNING_ANIMATION_SPEED,
    JUMP_DELAY, RUNNING_SPEED, TEXT_ANTI_ALIASING,
    X_POS_SPACING, DEFAULT_X_POS, DEFAULT_Y_POS,
    DEFAULT_GRAVITY, DEFAULT_JUMP_FORCE, JUMP_LOGIC_EXECUTE_ANIMATION,
    WHITE_BAR_SPEED_HP, WHITE_BAR_SPEED_MANA, TEXT_DISTANCE_BETWEEN_STATUS_AND_TEXT,
    ZERO_WIDTH, TOTAL_WIDTH,
    attack_display
)
from sprite_loader import SpriteSheet, SpriteSheet_Flipped
# from attack import Attacks, Attack_Display
import random
import global_vars
import key

#AS OF 4/23/25 (12:15 AM)
'''SPECIAL LASTS 16-17 SECONDS
 if you don't do anything :))'''
'''
fire wizard
ult 64 w/ + damage
3rd 24
2nd 57-62 full duration
1st skill up 16

special
1st 22 center
2nd 52 full duration
3rd 28.5
ult 68


wanderer magician
1st idk it depends 7.5 - 30
heal 28
3rd 26
ult 52  

special
1st idk man it depends but increase dmg
heal 35
3rd 32
ult 65


fire knight dmg
1st 9
2nd 20
3rd 35
4th 55

special
1st 7.5
2nd 36
3rd 28-38 final (38 total)
4th 60-70 (70 total)


wind hashashin
1st 8
2nd 20
3rd 27
4th 60

special
1st 10
2nd 27  
3rd 29-32
4th 70
'''

def display_inputs(key):
        preset = ["^", "\/", "<", ">"]
        for index, i in enumerate(["UP", "DOWN", "LEFT", "RIGHT"]):
            if i == key:
                return preset[index]
        return key



        


class Player(pygame.sprite.Sprite):
    def __init__(self, player_type, enemy):
        super().__init__()
        # print('from player itself. player:', player_type)
        # print(enemy)
        self.enemy = enemy if type(enemy) is list else [enemy]
        self.player_type = player_type # 1 for player 1, 2 for player 2
        self.name = "Unknown"
        self.items = [] # contains 3 or less than 3 item classes. ex. 
                            # self.items = [Item("War Helmet", r"assets\item icons\in use\Icons_40.png", ["str", "str flat", "hp regen"], [0.05, 1, 0.04])]
        self.damage_reduce = 0
        self.special_increase = 0
        self.lifesteal = 0
        self.mana_refund = 0
        self.crit_chance = 0
        self.crit_damage = 0
        self.stunned = False
        self.frozen = False
        self.freeze_source = None
        self.rooted = False
        self.root_source = None
        self.speed_multiplier = 1.0
        self.slowed = False
        self.slow_source = None
        self.slow_speed = 0
        self.silenced = False
        self.mana_burn_per = [0, 0] # [0] = mana burned, [1] = mana to damage
        self.mana_burn_flat = [0, 0] # [0] = mana burned, [1] = mana to damage
        
        self.max_temp_hp = 0
        self.temp_hp = self.max_temp_hp

        self.immortality_activated = False
        self.immortality_duration = 0



        self.str_mult = 5
        self.int_mult = 5
        
        self.hp_regen_per_str = 0.01
        self.mana_regen_per_int = 0.01
        self.agi_mult = 0.1
        # fire knight bas = 20

        # attack speed stuff
        # base atk speed for every hero, modify each if you want to set base 
        self.base_attack_speed = 100 
        self.base_attack_time = 1700

        

        # stat
        self.strength = 40
        self.intelligence = 40
        self.agility = 40


        self.mana_regen = self.regen_per_second(DEFAULT_MANA_REGENERATION)
        self.health_regen = self.regen_per_second(DEFAULT_HEALTH_REGENERATION)

        # Attack Speed Calculation
        self.bonus_attack_speed_flat = 0
        self.bonus_attack_speed_per = 0.0
        #self.flat_as_reduction = 0
        #self.percent_as_reduction = 0.0
        self.last_basic_attack_time = -BASIC_ATK_COOLDOWN  # Ready initially (use your existing BASIC_ATK_COOLDOWN as fallback)

        # will be phased out soon
        self.basic_attack_cooldown = BASIC_ATK_COOLDOWN

        self.base_animation_speed = 120

        self.basic_attack_animation_speed = self.base_animation_speed # also set this one 
        
        self.default_animation_speed = self.base_animation_speed

        self.attack_speed = self.calculate_effective_as()

        attr_size = (24,24)
        # Strength icon
        self.strength_attribute_icon = pygame.transform.scale(
            pygame.image.load(r'assets\icons\Strength_attribute_symbol.webp').convert_alpha(),
            (attr_size[0], attr_size[1])
        )
        # Agility icon
        self.agility_attribute_icon = pygame.transform.scale(
            pygame.image.load(r'assets\icons\Agility_attribute_symbol.webp').convert_alpha(),
            (attr_size[0], attr_size[1])
        )
        # Intelligence icon
        self.intelligence_attribute_icon = pygame.transform.scale(
            pygame.image.load(r'assets\icons\Intelligence_attribute_symbol.webp').convert_alpha(),
            (attr_size[0], attr_size[1])
        )

        # Strength icon
        self.attack_speed_icon = pygame.transform.scale(
            pygame.image.load(r'assets\icons\atk spd icon.png').convert_alpha(),
            (attr_size[0], attr_size[1])
        )
        # Agility icon
        self.attack_time_icon = pygame.transform.scale(
            pygame.image.load(r'assets\icons\atk time icon.png').convert_alpha(),
            (attr_size[0], attr_size[1])
        )
        # Intelligence icon
        self.attack_damage_icon = pygame.transform.scale(
            pygame.image.load(r'assets\icons\atk dmg icon.png').convert_alpha(),
            (attr_size[0], attr_size[1])
        )

        
        # Base Stats
        self.max_health = 0
        self.max_mana = 0
        self.health = self.max_health
        self.mana = self.max_mana
        self.basic_attack_damage = 0

        self.max_special = MAX_SPECIAL
        self.special = 0
        self.special_active = False

        # Player Position
        self.x = 0
        self.y = 0
        self.width = 0

        #dmg
        self.atk1_cooldown = 0
        self.atk2_cooldown = 0
        self.atk3_cooldown = 0
        self.sp_cooldown = 0

        #self.damage_list = []
        #FORMULA = DESIRED DMG / TOTAL FRAME EX. dmg=25/34 == 0.6944
        self.atk1_damage = (0, 0)
        self.atk2_damage = (0, 0) # 60 total if ur in the center + the multiplier = 64
        self.atk3_damage = (0, 0)# 25+something 
        self.sp_damage = (0, 0) # (47.6, 14) = 61.6


        self.dmg_mult = 0

        self.atk1_damage = self.atk1_damage[0] + (self.atk1_damage[0] * self.dmg_mult), self.atk1_damage[1] + (self.atk1_damage[1] * self.dmg_mult)
        self.atk2_damage = self.atk2_damage[0] + (self.atk2_damage[0] * self.dmg_mult), self.atk2_damage[1] + (self.atk2_damage[1] * self.dmg_mult)
        self.atk3_damage = self.atk3_damage[0] + (self.atk3_damage[0] * self.dmg_mult), self.atk3_damage[1] + (self.atk3_damage[1] * self.dmg_mult)
        self.sp_damage = self.sp_damage[0] + (self.sp_damage[0] * self.dmg_mult), self.sp_damage[1] + (self.sp_damage[1] * self.dmg_mult)

        # Player Animation Source
        jump_ani = None
        run_ani = None
        idle_ani= None
        atk1_ani= None
        sp_ani= None
        death_ani= None

        # Player Skill Sounds Effects Source
        # self.atk1_sound = pygame.mixer.Sound(None)
        # self.atk2_sound = pygame.mixer.Sound(None)
        # self.atk3_sound = pygame.mixer.Sound(None)
        # self.sp_sound = pygame.mixer.Sound(None)
        # self.atk1_sound.set_volume(0.5)
        # self.atk2_sound.set_volume(0.1)
        # self.atk3_sound.set_volume(0.5)
        # self.sp_sound.set_volume(0.5)

        # Player Skill Animations Source
        atk1 = None
        atk2 = None
        atk3 = None
        sp = None

        # Player Skill Icons Source
        skill_1 = None
        skill_2 = None
        skill_3 = None
        skill_4 = None

        # Player Icon Rects
        self.skill_1_rect = skill_1
        self.skill_2_rect = skill_2
        self.skill_3_rect = skill_3
        self.skill_4_rect = skill_4

        # Player Attack Animations Load
        self.atk1 = atk1
        self.atk2 = atk2
        self.atk3 = atk3
        self.sp = sp

        # Player Animations Load
        self.player_basic = None
        self.player_basic_flipped = None

        self.player_jump = None
        self.player_jump_flipped = None
        self.player_idle = None
        self.player_idle_flipped = None
        self.player_run = None
        self.player_run_flipped = None
        self.player_atk1 = None
        self.player_atk1_flipped = None
        self.player_atk2 = None
        self.player_atk2_flipped = None
        self.player_atk3 = None
        self.player_atk3_flipped = None
        self.player_sp = None
        self.player_sp_flipped = None
        self.player_death = None
        self.player_death_flipped = None

        # Player Image and Rect
        self.image = None
        self.rect = None # (midbottom = (self.x_pos, self.y_pos)) if p2
        self.hitbox_rect = pygame.Rect(0, 0, 50, 50)
        
        # Player Animation States
        self.player_basic_index = 0
        self.player_basic_index_flipped = 0
        
        self.player_jump_index = 0
        self.player_jump_index_flipped = 0
        self.player_idle_index = 0
        self.player_idle_index_flipped = 0
        self.player_run_index = 0
        self.player_run_index_flipped = 0
        self.player_atk1_index = 0
        self.player_atk1_index_flipped = 0
        self.player_atk2_index = 0
        self.player_atk2_index_flipped = 0
        self.player_atk3_index = 0
        self.player_atk3_index_flipped = 0
        self.player_sp_index = 0
        self.player_sp_index_flipped = 0
        self.player_death_index = 0
        self.player_death_index_flipped = 0

        # Player Attacking States
        self.attacking1 = False
        self.attacking2 = False
        self.attacking3 = False
        self.sp_attacking = False
        self.basic_attacking = False

        self.basic_attacking = False

        # ...
        self.last_atk_time = 0

        # Player Position
        self.x_pos = X_POS_SPACING if self.player_type == 1 else DEFAULT_X_POS
        self.y_pos = DEFAULT_Y_POS

        # Gravity
        self.y_velocity = 0
        self.jumping = False

        # Mana Values
        self.mana_cost_list = []

        # Modify
        self.lowest_mana_cost = 0

        # Skills
        self.attacks = []

        # # Regen Rate
        # self.hp_regen_rate = DEFAULT_HEALTH_REGENERATION # Health regeneration rate per frame
        # self.mana_regen_rate = DEFAULT_MANA_REGENERATION  # Mana regeneration rate per frame

        # After Bar Reduces
        self.white_health_p1 = self.health
        self.white_mana_p1 = self.mana   

        self.white_health_p2 = self.health
        self.white_mana_p2 = self.mana   

        # Main Inheritance
        self.running = False
        self.jumping = False
        self.facing_right = True 
        self.speed = RUNNING_SPEED
        self.default_speed = self.speed
        self.running_animation_speed = RUNNING_ANIMATION_SPEED
        
        
        
        # self.basic_attack_animation_speed =self.basic_attack_animation_speed * 0.5 # 60

        self.mana_costs = []

        self.y_velocity = 0
        self.jumping = False

        self.target = None


        #Attack-------------------------------------------------------------

        basic_slash = [r'assets\attacks\Basic Attack\1', BASIC_SLASH_ANIMATION, 1]
        self.basic_slash = self.load_img_frames_tile_method(basic_slash[0], basic_slash[1], basic_slash[2], BASIC_SLASH_SIZE)
        self.basic_slash_flipped = self.load_img_frames_flipped_tile_method(basic_slash[0], basic_slash[1], basic_slash[2], BASIC_SLASH_SIZE)

        self.basic_slash_big = self.load_img_frames_tile_method(basic_slash[0], basic_slash[1], basic_slash[2], BASIC_SLASH_SIZE_BIG)
        self.basic_slash_flipped_big = self.load_img_frames_flipped_tile_method(basic_slash[0], basic_slash[1], basic_slash[2], BASIC_SLASH_SIZE_BIG)


        basic_slash2 = [r'assets\attacks\Basic Attack\2', BASIC_SLASH_ANIMATION, 1]
        self.basic_slash2 = self.load_img_frames_tile_method(basic_slash2[0], basic_slash2[1], basic_slash2[2], BASIC_SLASH_SIZE_BIG)
        self.basic_slash2_flipped = self.load_img_frames_flipped_tile_method(basic_slash2[0], basic_slash2[1], basic_slash2[2], BASIC_SLASH_SIZE_BIG)

        basic_slash3 = [r'assets\attacks\Basic Attack\3 small', 2, 1]
        self.basic_slash3 = self.load_img_frames_tile_method(basic_slash3[0], basic_slash3[1], basic_slash3[2], BASIC_SLASH_SIZE_BIG)
        self.basic_slash3_flipped = self.load_img_frames_flipped_tile_method(basic_slash3[0], basic_slash3[1], basic_slash3[2], BASIC_SLASH_SIZE_BIG)
        
        # melee
        self.basic_icon = pygame.transform.scale(pygame.image.load(r'assets\icons\Blade_Dance_icon.webp').convert_alpha(), (ICON_WIDTH / 1.5, ICON_HEIGHT / 1.5))

        # ranged
        self.basic_icon2 = pygame.transform.scale(pygame.image.load(r'assets\icons\aghanims-scepter-from-dota-2-made-in-blender-v0-ew9qzvl10s2d1.webp').convert_alpha(), (ICON_WIDTH / 1.5, ICON_HEIGHT / 1.5))  
        self.basic_icon3 = pygame.transform.scale(pygame.image.load(r'assets\icons\arrow image ICON.jpg').convert_alpha(), (ICON_WIDTH / 1.5, ICON_HEIGHT / 1.5))  
        
        self.basic_sound = pygame.mixer.Sound(r'assets\sound effects\jump.swing-whoosh-110410.mp3')
        self.basic_sound.set_volume(0.5 * MAIN_VOLUME)
        
        # modify in hero
        if self.player_type == 1:
            self.basic_icon_rect = self.basic_icon.get_rect(center=(BASIC_ATK_POSX, BASIC_ATK_POSY))
        if self.player_type == 2:
            self.basic_icon_rect = self.basic_icon.get_rect(center=(BASIC_ATK_POSX_END, BASIC_ATK_POSY))

        
        self.special_sound = pygame.mixer.Sound(r'assets\sound effects\heart-beat-137135.mp3')
        self.special_sound.set_volume(1 * MAIN_VOLUME)

        #Attack-------------------------------------------------------------
        self.last_health = self.health
        self.last_mana = self.mana
        self.last_temp_hp = self.temp_hp
        # self.just_spawned = True
        self.damage_numbers = []

        self.damage_font = global_vars.get_font(30)  # preload font


        # for reset_all() function
        self.health_bar_p1_after =0
        self.health_bar_p2_after =0
        self.mana_bar_p1_after =0
        self.mana_bar_p2_after =0
        

        # Player Status positioning
        self.player_1_x = 101    
        self.player_1_y = 150
        self.player_2_x = 96
        self.player_2_y = 150

        # Player Movement Limitations and Settings
        self.limit_movement_left = ZERO_WIDTH
        '''Prevent player moving left.'''
        self.limit_movement_right = TOTAL_WIDTH
        '''Prevent player moving right.'''
        self.jump_force = DEFAULT_JUMP_FORCE
        '''Jump strength/force of player.'''
        # self.detect_ground = DEFAULT_Y_POS
        # '''Limit where player detects the ground at y level.'''

    def display_damage(self, damage, interval=30, color=(255, 0, 0), size=None, health_modify=False, mana_modify=False):
        if not hasattr(self, 'rect'):
            return  # Safety check
        # Don't show healing text if player is already at max health or at the start of the game
        if not hasattr(self, "spawn_time") or pygame.time.get_ticks() - self.spawn_time < 50:
            return
        
        if health_modify:
            if self.health >= self.max_health:
                return
        if mana_modify:
            if self.mana >= self.max_mana:
                return
        # Don't show healing text if player is already at max health
        # Color (0,255,0) is used for heal display elsewhere
        
        if color == cyan2 and self.mana >= self.max_mana:
            return
        if color == gold and self.special >= self.max_special:
            return
        # if self.health > self.max_health: # don't show hp dmg when  game starts
        #     return

        # Random offset so numbers don’t overlap each other
        offset_x = random.randint(-20, 20)
        
        # Offset Y based on damage (higher damage = higher text)
        if damage > 20:
            offset_y = random.randint(90,100)
        elif damage > 10:
            offset_y = random.randint(70, 80)
        elif damage > 5:
            offset_y = random.randint(50, 60)
        else:
            offset_y = random.randint(10, 20)

        x = self.hitbox_rect.centerx + offset_x
        y = self.hitbox_rect.top - offset_y

        # Font size 
        if size is None:
            if damage > 20:
                size = size or (30 + int(damage))  # Big damage just adds to base size
            elif damage > 5:
                size = size or int(20 + damage * 2)  # Medium scaling
            else:
                size = size or int(20 + damage * 3)  # Small damage gets boosted 

        font = global_vars.get_font(size)

        # Format floating numbers cleanly
        if isinstance(damage, float):
            display_text = f"{damage:.1f}".rstrip('0').rstrip('.')  # E.g., 0.33 or 1.2
        elif abs(damage) < 0.001:
            display_text = "0"
        else:
            display_text = str(damage)

        self.damage_numbers.append({
            'text': display_text,
            'x': x,
            'y': y,
            'alpha': 255,
            'interval': interval,
            'color': color,
            'font': font
        })

       

    def update_damage_numbers(self, screen):
         # if getattr(self, "just_spawned", False):
        #         self.last_health = self.health
        #         self.just_spawned = False
        #         return
        if not hasattr(self, "spawn_time"):
            self.spawn_time = pygame.time.get_ticks()

        for dmg in self.damage_numbers[:]:
            # # Skip rendering and remove healing text if health is already at max
            dmg['y'] -= 1  # Move the text upward
            fade_amount = int(255 / dmg['interval'])
            dmg['alpha'] = max(0, dmg['alpha'] - fade_amount)

            if dmg['alpha'] <= 0:
                self.damage_numbers.remove(dmg)
                continue

            surf = dmg['font'].render(str(dmg['text']), TEXT_ANTI_ALIASING, dmg['color'])
            surf.set_alpha(dmg['alpha'])
            screen.blit(surf, (dmg['x'] - surf.get_width() // 2, dmg['y']))


    def detect_and_display_damage(self, interval=30):
        # This function only for health, check other call for display_damage()
        # print(self.health, self.last_health, 'ahah')
        # print(self.health >= self.max_health)
        # if self.temp_hp > 0:
        #     delta = self.temp_hp - self.last_health
        # else:
        delta = self.health - self.last_health

        # print(delta)
        if delta < 0:
            self.display_damage(-delta, interval=interval, health_modify=True)  # Normal damage (red)
        elif delta > self.health_regen*10:  # Only show healing if it's significant (not just natural regen)
            self.display_damage(delta, interval=interval, color=(0, 255, 0), health_modify=True)  # Green heal
        # self.last_health = self.temp_hp if self.temp_hp > 0 else self.health
        self.last_health = self.health

    def detect_and_display_mana(self, interval=30):
        # This function only for health, check other call for display_damage()
        # print(self.health, self.last_health, 'ahah')
        # print(self.health >= self.max_health)
        delta = self.mana - self.last_mana
        # print(delta)
        if delta < 0:
            pass # Do nothing if mana consumed (annoying display)
        elif delta > self.mana_regen*10:  # Only show healing if it's significant (not just natural regen)
            self.display_damage(delta, interval=interval, color=cyan2, mana_modify=True)  # Green heal
        self.last_mana = self.mana

    # def detect_and_display_temp_hp(self, interval=30):
    #     # This function only for health, check other call for display_damage()
    #     # print(self.health, self.last_health, 'ahah')
    #     # print(self.health >= self.max_health)
    #     delta = self.mana - self.last_mana
    #     # print(delta)
    #     if delta < 0:
    #         pass # Do nothing if mana consumed (annoying display)
    #     elif delta > DEFAULT_MANA_REGENERATION*10:  # Only show healing if it's significant (not just natural regen)
    #         self.display_damage(delta, interval=interval, color=cyan2, mana_modify=True)  # Green heal
    #     self.last_mana = self.mana


            
    def update_hitbox(self):
        # Center the hitbox inside the player's main rect
        self.hitbox_rect.center = (self.rect.midbottom[0], self.rect.midbottom[1] - 30)

    def draw_hitbox(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox_rect, 2)  # Red outline for debugging

    def display_items(self):
        pass

    def apply_stat_regen_rates(self, rate, stat):
        '''Called by apply_item_bonuses() after the stats(str,int, agi) is done calculated.'''
        return rate * stat
    
    def calculate_regen(self, base_regen=None, rate=0, stat=0, basic_attack=False):
        '''CALCULATES BOTH REGEN AND ATTACK DAMAGE! (sorry)

        - If base regen is None, applies the base_regen for the hero. (startup calculation)
        - Leave blank if only apply the rate and stat.(for adding item bonuses)

        For calculating the attack damage, make the basic_attack True so it doesn't divide into fps (will use actual value)
        
        base_attack_damage + agility * agi_mult : is the attack damage '''
        if base_regen is not None:
            if basic_attack: # don't divide into fps (actual value)
                return base_regen + self.apply_stat_regen_rates(rate, stat)
            else: # for hp and mana
                return self.regen_per_second(base_regen + self.apply_stat_regen_rates(rate, stat))
        else:# only for adding bonuses (doesn't use base_regen) 
            if basic_attack:  # don't divide into fps (actual value)
                self.apply_stat_regen_rates(rate, stat)
            else: # for hp and mana
                return self.regen_per_second(self.apply_stat_regen_rates(rate, stat))

    def apply_item_bonuses(self):
        '''misc - apply item bonuses (avoid noisy prints for performance)
        self.items is a list of item classes'''
        # First, collect all bonuses by type for efficient application
        bonuses = {typ: 0.0 for typ in set(t for item in self.items for t in item.bonus_type)}  # Unique types
        for item in self.items:
            for typ, val in item.info.items():
                bonuses[typ] += val

        # Apply flats first
        for typ, val in bonuses.items():
            # print(typ, "hp_regen_flat")
            # print(bonuses)
            if "_flat" in typ:
                # print(typ)
                base_stat = typ.replace("_flat", "")
                if base_stat == "all_stats":
                    self.strength += val
                    self.max_health = self.str_mult * self.strength
                    self.health_regen += self.calculate_regen(rate=self.hp_regen_per_str, stat=val)
                    self.intelligence += val
                    self.max_mana = self.int_mult * self.intelligence
                    self.mana_regen += self.calculate_regen(rate=self.mana_regen_per_int, stat=val)
                    self.agility += val # update atk with bonus agi
                    self.basic_attack_damage += self.calculate_regen(rate=self.agi_mult, stat=self.agility * val)


                elif base_stat == "str":
                    self.strength += val
                    self.max_health = self.str_mult * self.strength
                    self.health_regen += self.calculate_regen(rate=self.hp_regen_per_str, stat=val)

                elif base_stat == "int":
                    self.intelligence += val
                    self.max_mana = self.int_mult * self.intelligence
                    self.mana_regen += self.calculate_regen(rate=self.mana_regen_per_int, stat=val)


                elif base_stat == "agi":
                    self.agility += val # update atk with bonus agi
                    self.basic_attack_damage += self.calculate_regen(rate=self.agi_mult, stat=self.agility * val)



                elif base_stat == "hp":
                    self.max_health += val
                elif base_stat == "mana":
                    self.max_mana += val
                elif base_stat == "atk":
                    self.basic_attack_damage += val
                
                elif base_stat == "hp_regen":
                    self.health_regen += self.regen_per_second(val)
                    pass
                    # print(val, self.regen_per_second(val) * 60, self.health_regen * 60, 'total:', (self.health_regen + self.regen_per_second(val)) * 60)
                    # self.health_regen = self.health_regen + val / 60
                    # print('added hp regen to:', self.__class__.__name__)
                elif base_stat == "mana_regen":
                    self.mana_regen += self.regen_per_second(val)
                elif base_stat == "atk_speed":
                    self.bonus_attack_speed_flat += val
                    self.attack_speed = self.calculate_effective_as()
                    self.basic_attack_cooldown = self.calculate_basic_attack_interval()
                    # self.basic_attack_animation_speed = DEFAULT_ANIMATION_SPEED - ((DEFAULT_ANIMATION_SPEED * (self.base_attack_time / self.basic_attack_cooldown) - DEFAULT_ANIMATION_SPEED))
                    self.basic_attack_animation_speed = self.base_animation_speed / (self.attack_speed / self.base_attack_speed)

                    self.attacks[4].cooldown = self.basic_attack_cooldown
                    self.attacks_special[4].cooldown = self.basic_attack_cooldown

                elif typ == "mana_burn_flat":
                    self.mana_burn_flat[0] = val
                elif typ == "mana_burn_flat_dmg_per":
                    self.mana_burn_flat[1] = val

                    # Flat attack speed: Reduce anim speed (faster anim = faster atk)
                    # Scale: 100 flat = -10 anim speed (arbitrary, from your old 0.1 * val)
                    # self.basic_attack_animation_speed -= val * 0.1 #removed 0.1 (therefore val is 15)
                    
                    # Cooldown: 100 flat = -500ms (assuming ms; 100 flat = full base reduction if base=500)
                    # self.basic_attack_cooldown -= val * 5
                    # self.basic_attack_cooldown += ((self.basic_attack_cooldown-240) - (self.basic_attack_cooldown-240) - val)  # Adjust scalar if base
                    

                    # fire wizard stats:
                    # base attack time: 1.2s
                    # attack speed: 120

                    # atks per second = (100 + total atk speed) / base attack time
                    # seconds per atk = base attack time / (1 + total atk speed / 100)

                    #ex. + 100 atk speed, how much is the total?
                    # ___________ attack speed, ________ attk stime





                    # BASIC_ATTACK_COOLDOWN DEFAUT : 500 
                    
                    # 120 - (150 * 0.1) = 105
                    # total = 1,050 = 1.05 seconds
                    # 120 - 20
                    
                    #rules:
                    # attack speed must not go >  +140
                    # or below 20 

                    #ex. 600 atk speed = 0.24 second attack cooldown
                    
                    #cooldown threshold max(240, min(600, atkspeed?))
                    #260 maximum minus, 100 maximum addition

                    #500 - (240)  += (260 - val) 

                    #                                      base attack speed           base attack rate (each hero)
                    #hero 1 basic attack = 2seconds             100 + 20 = 120          0.95 second (950)
                    #hero 2 bascic attack = 1.5 seconds         90 + 15                 0.75 second (750)
                    #hero 3 basic attack = 3.2 seconds          120 + 15                0.5 second (500)



                    # item_1 = +50 attack speed
                    # hero_1 items = item_1. Total attack speed = base + bonus = 100+50 = 150, attack rate = 1.0 second - 

                    #(percentage % and flat bonuses)
                    #100% attack speed 100 -> 200       
                    
                    # add +20 attack speed

            # Abilities
            if typ == "extra_temp_hp":
                # print('addeddd')
                self.temp_hp += val
                self.max_temp_hp = self.temp_hp
            if typ == "immortality":
                pass
                # self.has_immortality = val
                # self.immortality_duration += val * 1000
                # print('temp hp:', self.temp_hp)
        # Apply percentages (multiplicative)

            if "_per" in typ:
                base_stat = typ.replace("_per", "")
                if base_stat == "all_stats":
                    self.strength *= (1 + val)
                    self.max_health = self.str_mult * self.strength
                    self.health_regen += self.calculate_regen(rate=self.hp_regen_per_str, stat=self.strength * val)
                    self.intelligence *= (1 + val)
                    self.max_mana = self.int_mult * self.intelligence
                    self.mana_regen += self.calculate_regen(rate=self.mana_regen_per_int, stat=self.intelligence * val)
                    self.agility *= (1 + val)
                    self.basic_attack_damage = self.agi_mult * self.agility


                elif base_stat == "str":
                    self.strength *= (1 + val)
                    self.max_health = self.str_mult * self.strength
                    self.health_regen += self.calculate_regen(rate=self.hp_regen_per_str, stat=self.strength * val)

                elif base_stat == "int":
                    self.intelligence *= (1 + val)
                    self.max_mana = self.int_mult * self.intelligence
                    self.mana_regen += self.calculate_regen(rate=self.mana_regen_per_int, stat=self.intelligence * val)

                elif base_stat == "agi":
                    self.agility *= (1 + val)
                    self.basic_attack_damage = self.agi_mult * self.agility
                    
                elif base_stat == "hp":
                    self.max_health *= (1 + val)
                elif base_stat == "mana":
                    self.max_mana *= (1 + val)
                elif base_stat == "atk":
                    self.basic_attack_damage *= (1 + val)
                elif base_stat == "move_speed":
                    self.speed *= (1 + val)
                    self.running_animation_speed += 10 * val  # Legacy scaling; consider *= (1 + val) for consistency
                    self.default_speed = self.speed
                elif base_stat == "atk_speed":
                    self.bonus_attack_speed_per += val
                    self.attack_speed = self.calculate_effective_as()
                    self.basic_attack_cooldown = self.calculate_basic_attack_interval()
                    # self.basic_attack_animation_speed = DEFAULT_ANIMATION_SPEED - ((DEFAULT_ANIMATION_SPEED * (self.base_attack_time / self.basic_attack_cooldown) - DEFAULT_ANIMATION_SPEED))
                    self.basic_attack_animation_speed = self.base_animation_speed / (self.attack_speed / self.base_attack_speed)

                    self.attacks[4].cooldown = self.basic_attack_cooldown
                    self.attacks_special[4].cooldown = self.basic_attack_cooldown


                elif typ == "mana_burn_per":
                    self.mana_burn_per[0] = val
                elif typ == "mana_burn_per_dmg":
                    self.mana_burn_per[1] = val


                    # Percentage: Reduce anim speed and cd by %
                    # self.basic_attack_animation_speed *= (1 - val)  # Lower = faster
                    # self.basic_attack_cooldown *= (1 - val)
                elif typ == "mana_reduce_per":
                    num_skills = len(self.attacks) - 1  # 4 skills, skip basic (assumes basic is last)
                    for i in range(num_skills):
                        self.attacks[i].mana_cost = int(self.attacks[i].mana_cost * (1 - val))
                        self.attacks_special[i].mana_cost = int(self.attacks_special[i].mana_cost * (1 - val))
                elif typ == "cd_reduce_per":
                    num_skills = len(self.attacks) - 1  # Now 4: Skills only, exclude basic attack
                    for i in range(num_skills):
                        self.attacks[i].cooldown = int(self.attacks[i].cooldown * (1 - val))
                        self.attacks_special[i].cooldown = int(self.attacks_special[i].cooldown * (1 - val))
                # CENTRALIZED BONUSES BEFORE APPLYING
                elif typ == "lifesteal_per":
                    self.lifesteal += val # must be higher than 1
                elif typ == "health_cost_per":
                    self.lifesteal += val  # Penalty as negative lifesteal # value must be less than 1
                elif typ == "dmg_reduce_per":
                    self.damage_reduce += val
                elif typ == "sp_increase_per":
                    self.special_increase += val
                elif typ == "mana_refund_per":
                    self.mana_refund += val
                elif typ == "crit_chance_per":
                    self.crit_chance += val
                elif typ == "crit_dmg_per":
                    self.crit_damage += val
                elif typ == "dmg_return_per": # negative value for enemy
                    for enemy in self.enemy:
                        enemy.lifesteal -= val
                elif typ == "mana_regen_per":
                    self.mana_regen *= (1 + val)
                elif typ == "hp_regen_per":
                    self.health_regen *= (1 + val)
                
                # For spell damage vvv -----------------------------------------------------
                elif typ == "spell_dmg_per":
                    # Apply bonus spell damage to each skill
                    self.atk1_damage = (self.atk1_damage[0] * (1 + val), self.atk1_damage[1] * (1 + val))
                    self.atk2_damage = (self.atk2_damage[0] * (1 + val), self.atk2_damage[1] * (1 + val))
                    self.atk3_damage = (self.atk3_damage[0] * (1 + val), self.atk3_damage[1] * (1 + val))
                    self.sp_damage = (self.sp_damage[0] * (1 + val), self.sp_damage[1] * (1 + val))

                    if hasattr(self, 'atk2_damage_2nd'): # For wind hashahin, or any heroes that needs attribute
                        self.atk2_damage_2nd = (self.atk2_damage_2nd[0] * (1 + val), self.atk2_damage_2nd[1] * (1 + val)) #reused by water princess
                    if hasattr(self, 'sp_damage_2nd'):
                        self.sp_damage_2nd = (self.sp_damage_2nd[0] * (1 + val), self.sp_damage_2nd[1] * (1 + val))
                    if hasattr(self, 'real_sp_damage'):
                        self.real_sp_damage *= (1 + val)

                    #some of these from water princess, will reuse some variable
                    if hasattr(self, 'atk3_damage_2nd'):
                        self.atk3_damage_2nd *= (1 + val)
                    if hasattr(self, 'atk1_damage_2nd'):
                        self.atk1_damage_2nd *= (1 + val)
                    if hasattr(self, 'sp_damage_3rd'): # For water princess
                        self.sp_damage_3rd = (self.sp_damage_3rd[0] * (1 + val), self.sp_damage_3rd[1] * (1 + val))
                    # can handle single, or tuple
                    if hasattr(self, 'sp_atk1_damage'):
                        if isinstance(self.sp_atk1_damage, tuple):
                            self.sp_atk1_damage = (self.sp_atk1_damage[0] * (1 + val), self.sp_atk1_damage[1] * (1 + val))
                        else:
                            self.sp_atk1_damage *= (1 + val)
                    if hasattr(self, 'sp_atk2_damage'):
                        if isinstance(self.sp_atk2_damage, tuple):
                            self.sp_atk2_damage = (self.sp_atk2_damage[0] * (1 + val), self.sp_atk2_damage[1] * (1 + val))
                        else:
                            self.sp_atk2_damage *= (1 + val)
                    if hasattr(self, 'sp_atk2_damage_2nd'): # For water princess
                        self.sp_atk2_damage_2nd = (self.sp_atk2_damage_2nd[0] * (1 + val), self.sp_atk2_damage_2nd[1] * (1 + val))
                    if hasattr(self, 'sp_atk2_damage_3rd'): # For water princess
                        self.sp_atk2_damage_3rd = (self.sp_atk2_damage_3rd[0] * (1 + val), self.sp_atk2_damage_3rd[1] * (1 + val))
                    if hasattr(self, 'sp_atk3_damage'): # For water princess
                        self.sp_atk3_damage = (self.sp_atk3_damage[0] * (1 + val), self.sp_atk3_damage[1] * (1 + val))
                # For spell damage ^^^ -----------------------------------------------------

        # Caps and safety
        self.attack_speed = self.calculate_effective_as()
        self.basic_attack_cooldown = self.calculate_basic_attack_interval()

        self.basic_attack_animation_speed = max(0.01, self.basic_attack_animation_speed)
        self.basic_attack_cooldown = max(0.01, self.basic_attack_cooldown)
        self.attacks[4].cooldown = self.basic_attack_cooldown
        self.attacks_special[4].cooldown = self.basic_attack_cooldown

        # Clamp current values
        self.health = min(self.health, self.max_health)
        self.mana = min(self.mana, self.max_mana)
        self.basic_attack_animation_speed = max(10, min(50, self.basic_attack_animation_speed))
        # Reapply hero-specific (e.g., arrow_stuck)
        if hasattr(self, 'arrow_stuck_damage'):
            # reapply bonus
            self.arrow_stuck_damage = (self.basic_attack_damage * 0.3) - 0.05  # total dmg=1


        # get final attack speed with bonuses
        self.get_current_atk_speed = self.basic_attack_animation_speed
        
    def get_atk_speed(self): # pls dont change this variable
        return self.get_current_atk_speed # im tired debugging
     

        # print(self.basic_attack_damage)

        # self.max_health = self.strength * self.str_mult
        # self.health = self.max_health
        # self.max_mana = self.intelligence * self.int_mult
        # self.mana = self.max_mana
        # self.basic_attack_damage = self.agility * self.agi_mult

    # def apply_item_bonuses(self):
    #     for item in self.items:
    #         for bonus_type, bonus_value in zip(item.bonus_type, item.bonus_value):
    #             if bonus_type == "hp":  # Percentage-based health bonus
    #                 self.max_health += self.max_health * bonus_value
    #                 self.health = self.max_health  # Update current health to match max health
    #             elif bonus_type == "hp_flat":  # Flat health bonus
    #                 self.max_health += bonus_value
    #                 self.health = self.max_health
    #             elif bonus_type == "mana":  # Percentage-based mana bonus
    #                 self.max_mana += self.max_mana * bonus_value
    #                 self.mana = self.max_mana  # Update current mana to match max mana
    #             elif bonus_type == "mana_flat":  # Flat mana bonus
    #                 self.max_mana += bonus_value
    #                 self.mana = self.max_mana
    #             elif bonus_type == "atk":  # Percentage-based attack bonus
    #                 self.basic_attack_damage += self.basic_attack_damage * bonus_value
    #             elif bonus_type == "atk_flat":  # Flat attack bonus
    #                 self.basic_attack_damage += bonus_value

    # Documentation

        # # First, gather primary stat bonuses
        # str_bonus = 0
        # int_bonus = 0
        # agi_bonus = 0

        # # First pass: apply percentage and flat bonuses to primary stats
        # for item in self.items:
        #     for bonus_type, bonus_value in zip(item.bonus_type, item.bonus_value):
        #         if bonus_type == "str":
        #             str_bonus += self.strength * bonus_value
        #         elif bonus_type == "str_flat":
        #             str_bonus += bonus_value
        #         elif bonus_type == "int":
        #             int_bonus += self.intelligence * bonus_value
        #         elif bonus_type == "int_flat":
        #             int_bonus += bonus_value
        #         elif bonus_type == "agi":
        #             agi_bonus += self.agility * bonus_value
        #         elif bonus_type == "agi_flat":
        #             agi_bonus += bonus_value

        # # Apply stat bonuses
        # self.strength += str_bonus
        # self.intelligence += int_bonus
        # self.agility += agi_bonus

        # # Recalculate derived stats based on new primary stats
        # self.max_health = self.strength * self.str_mult
        # self.max_mana = self.intelligence * self.int_mult
        # self.basic_attack_damage = self.agility * self.agi_mult
        # self.health = self.max_health
        # self.mana = self.max_mana

        # # Second pass: apply derived stat bonuses
        # for item in self.items:
        #     for bonus_type, bonus_value in zip(item.bonus_type, item.bonus_value):
        #         if bonus_type == "hp":
        #             self.max_health += self.max_health * bonus_value
        #             self.health = self.max_health
        #         elif bonus_type == "hp_flat":
        #             self.max_health += bonus_value
        #             self.health = self.max_health
        #         elif bonus_type == "mana":
        #             self.max_mana += self.max_mana * bonus_value
        #             self.mana = self.max_mana
        #         elif bonus_type == "mana_flat":
        #             self.max_mana += bonus_value
        #             self.mana = self.max_mana
        #         elif bonus_type == "atk":
        #             self.basic_attack_damage += self.basic_attack_damage * bonus_value
        #         elif bonus_type == "atk_flat":
        #             self.basic_attack_damage += bonus_value

    '''
    Image Loading Function Reference
    Each function loads a sequence of .png images from a specified folder, applies optional scaling and rotation, and returns a list of Pygame surfaces (frames). Use the correct function depending on the numbering format and modifications like flipping or rotating.

    📁 1. Basic Numbering (1.png, 2.png, 3.png, etc.)
    load_img_frames(folder, count, starts_at_zero=False, size=1)
    Use for: Simple numbered files like Attack_1_1.png, Attack_1_2.png, ...

    Modifiers: 🔹Scale only

    load_img_frames_rotate(folder, count, starts_at_zero=False, size=1, rotate=0)
    Same as above but adds 🔄 rotation

    load_img_frames_flipped(folder, count, starts_at_zero=False, size=1)
    Same as load_img_frames, but applies a horizontal 🔁 flip

    load_img_frames_flipped_rotate(folder, count, starts_at_zero=False, size=1, rotate=0)
    Combination of flipping + rotation

    📌 Example usage:

    python
    Copy
    Edit
    folder = r"assets\characters\Fire wizard\slash pngs\Attack_1_"
    frames = load_img_frames(folder, 9)
    🔢 2. Padded Numbering (01.png, 02.png, 03.png, etc.)
    load_img_frames_numbering_method_simple(folder, count, starts_at_zero=False, size=1)
    Use for: Padded filenames like 00.png, 01.png, ...

    Path format: folder + '01.png'

    Windows/Mac compatible path format

    load_img_frames_numbering_method(folder, count, starts_at_zero=False, size=1)
    Same as above, but forces backslash \ in path (Windows-specific)

    Path format: folder\01.png

    📌 Example usage:

    python
    Copy
    Edit
    folder = r"assets\attacks\fire wizard\atk2\"
    frames = load_img_frames_numbering_method_simple(folder, 5)
    🧱 3. Tile Format (tile000.png, tile001.png, ...)
    load_img_frames_tile_method(folder, count, starts_at_zero=False, size=1)
    Use for: tile000.png, tile001.png, ...

    Applies scale and returns frames

    Stops if file is not found

    load_img_frames_flipped_tile_method(folder, count, starts_at_zero=False, size=1)
    Same as above, but applies a horizontal 🔁 flip

    📌 Example usage:

    python
    Copy
    Edit
    folder = r"assets\attacks\fire wizard\atk1\"
    frames = load_img_frames_tile_method(folder, 10)
    📝 Notes
    count is the number of frames you want to load.

    starts_at_zero=True will start from 0, otherwise starts from 1.

    size=1 means no scaling (1.5 means 150% size, 0.5 means half size).

    rotate=0 means no rotation (positive = clockwise, negative = counterclockwise).

    Use raw string (r"your\path") or double backslashes ("your\\path") to avoid issues on Windows.

    '''


    def load_img_frames_v2(self, folder:str, count:int | tuple, starts_at_zero=False, size=1, typ='frames', flipped=False, rotate=0):
        ''' Can be used as loading attack frames and loading a spritesheet, provided that count is tuple
        
        - folder: path of single frame, without the numbering.
        
                if spritesheet, provide the spritesheet path (typ != 'frames')
        - count: int if typ == 'frames' (frame count)

                tuple if typ == 'spritesheet' (column, rows)
        '''
        if typ == "frames":
            images = []
            for i in range(count):
                img_path = (fr'{folder}{i + 1 - starts_at_zero}.png')
                image = pygame.transform.flip(pygame.image.load(img_path).convert_alpha(), flipped, False)
                image = pygame.transform.rotozoom(image, 0, size)
                images.append(image)
            return images
            
        else: # spritesheeet
            from heroes import load_attack, load_attack_flipped 
            if not flipped: # normal
                return load_attack(
                    filepath=folder,
                    columns=count[0], 
                    rows=count[1], 
                    scale=size, 
                    rotation=rotate)
            else:
                return load_attack_flipped(
                    filepath=folder,
                    columns=count[0], 
                    rows=count[1], 
                    scale=size, 
                    rotation=rotate)
            
    def load_img_frames(self, folder, count, starts_at_zero=False, size=1):
        '''
        assets\characters\Fire wizard\slash pngs\Attack_1_1.png
        assets\characters\Fire wizard\slash pngs\Attack_1_2.png
        '''
        images = []
        for i in range(count):
            img_path = (fr'{folder}{i + 1 - starts_at_zero}.png')
            image = pygame.image.load(img_path).convert_alpha()
            image = pygame.transform.rotozoom(image, 0, size)
            images.append(image)
        return images
    
    def load_img_frames_rotate(self, folder, count, starts_at_zero=False, size=1, rotate=0):
        '''
        assets\characters\Fire wizard\slash pngs\Attack_1_1.png
        assets\characters\Fire wizard\slash pngs\Attack_1_2.png
        ''' # same, add rotate
        images = []
        for i in range(count):
            img_path = (fr'{folder}{i + 1 - starts_at_zero}.png')
            image = pygame.image.load(img_path).convert_alpha()
            image = pygame.transform.rotozoom(image, rotate, size)
            images.append(image)
        return images
    
    def load_img_frames_numbering_method_simple(self, folder, count, starts_at_zero=False, size=1, rotate=0, flip=False):
        '''
        assets\attacks\fire wizard\atk2\01.png
        assets\attacks\fire wizard\atk2\02.png
        '''
        images = []
        for i in range(count):
            frame_number = i + (0 if starts_at_zero else 1)
            # 01 02
            img_path = (fr'{folder}{str(frame_number).zfill(2)}.png')
            # print(img_path)
            image = pygame.transform.flip(pygame.image.load(img_path).convert_alpha(), flip, False)
            image = pygame.transform.rotozoom(image, rotate, size)
            images.append(image)
        return images
    
    def load_img_frames_numbering_method(self, folder, count, starts_at_zero=False, size=1):
        '''
        assets\attacks\fire wizard\atk2\01.png
        ''' #same but force backslash
        images = []
        for i in range(count):
            frame_number = i + (0 if starts_at_zero else 1)
            # \01 \02
            img_path = (fr'{folder}\{str(frame_number).zfill(2)}.png')
            image = pygame.image.load(img_path).convert_alpha()
            image = pygame.transform.rotozoom(image, 0, size)
            images.append(image)
        return images
    
    
    def load_img_frames_flipped(self, folder, count, starts_at_zero=False, size=1):
        '''
        assets\characters\Fire wizard\slash pngs\Attack_1_1.png
        assets\characters\Fire wizard\slash pngs\Attack_1_2.png
        ''' # same but rotate flip
        images = []
        for i in range(count):
            # 1 2 3
            img_path = (fr'{folder}{i + 1 - starts_at_zero}.png')
            image = pygame.transform.flip(pygame.image.load(img_path).convert_alpha(), True, False)
            image = pygame.transform.rotozoom(image, 0, size)
            images.append(image)
        return images
    
    def load_img_frames_flipped_rotate(self, folder, count, starts_at_zero=False, size=1, rotate=0):
        '''
        assets\characters\Fire wizard\slash pngs\Attack_1_1.png
        assets\characters\Fire wizard\slash pngs\Attack_1_2.png
        ''' # same but rotate flip
        images = []
        for i in range(count):
            # 1 2 3
            img_path = (fr'{folder}{i + 1 - starts_at_zero}.png')
            image = pygame.transform.flip(pygame.image.load(img_path).convert_alpha(), True, False)
            image = pygame.transform.rotozoom(image, rotate, size)
            images.append(image)
        return images

    def load_img_frames_tile_method(self, folder, count, starts_at_zero=False, size=1):
        '''
        assets\attacks\fire wizard\atk1\tile000.png
        assets\attacks\fire wizard\atk1\tile001.png
        '''
        images = []
        for i in range(count):
            # Generate zero-padded file name (e.g., 0010)
            frame_number = i + (0 if starts_at_zero else 1)
            img_path = fr"{folder}\tile{frame_number:03d}.png"  # Zero-pad to 4 digits
            try:
                image = pygame.image.load(img_path).convert_alpha()
                image = pygame.transform.rotozoom(image, 0, size)
                images.append(image)
            except FileNotFoundError:
                print(f"File not found: {img_path}")
                break
        return images
    
    def load_img_frames_flipped_tile_method(self, folder, count, starts_at_zero=False, size=1):
        '''
        assets\attacks\fire wizard\atk1\tile000.png
        assets\attacks\fire wizard\atk1\tile001.png
        ''' # same but flip
        images = []
        for i in range(count):
            # Generate zero-padded file name (e.g., 0010)
            frame_number = i + (0 if starts_at_zero else 1)
            img_path = fr"{folder}\tile{frame_number:03d}.png"  # Zero-pad to 4 digits
            try:
                image = pygame.transform.flip(pygame.image.load(img_path).convert_alpha(), True, False)
                image = pygame.transform.rotozoom(image, 0, size)
                images.append(image)
            except FileNotFoundError:
                print(f"File not found: {img_path}")
                break
        return images
    
    def load_attack_class(self, filepath, frame_width, frame_height, rows, columns, scale=1, rotation=0, frame_duration=30):
        spritesheet = pygame.image.load(filepath).convert_alpha()
        spritesheet_width = spritesheet.get_width()
        spritesheet_height = spritesheet.get_height()
        # Debugging: Print the spritesheet dimensions and frame dimensions
        # print(f"Spritesheet size: {spritesheet_width}x{spritesheet_height}")
        calculated_frame_width = spritesheet_width // columns
        calculated_frame_height = spritesheet_height // rows
        # print(f"Calculated frame size: {calculated_frame_width}x{calculated_frame_height}")
        # Check if the provided frame dimensions match the calculated ones
        if frame_width != calculated_frame_width or frame_height != calculated_frame_height:
            # print(
            #     f"Warning: Provided frame dimensions ({frame_width}x{frame_height}) "
            #     f"do not match calculated dimensions ({calculated_frame_width}x{calculated_frame_height})."
            # )
            frame_width = calculated_frame_width
            frame_height = calculated_frame_height

        spritesheet = SpriteSheet(filepath, frame_width, frame_height, rows, columns, scale, rotation)
        frames = spritesheet.get_frames()
        return frames
    
    # def animate(self, frames, index, loop=True, basic_atk=False):
    #     current_time = pygame.time.get_ticks()
    #     #print(f"{self.__class__.__name__} animation speed: {self.basic_attack_animation_speed}")
    #     frame_duration = self.default_animation_speed if not self.basic_attacking else self.basic_attack_animation_speed
    #     #print(f"Animation type: {'basic' if self.basic_attacking else 'default'}, Duration: {frame_duration}")
    #     if current_time - self.last_atk_time > frame_duration:
    #         self.last_atk_time = current_time
    #         self.image = frames[int(index)]
    #         index += 1
    #         #print(basic_atk)
    #         if index >= len(frames):
    #             if loop:
    #                 index = 0  # Restart the animation
    #             else:
    #                 index = len(frames) - 1  # Stay on the last frame
    #                 return index, False  # Animation finished
    #     return index, True  # Animation stzill active
    
    def animate(self, frames, index, loop=True, basic_atk=False):
        if not frames:
            return 0, False
        frame_duration = self.basic_attack_animation_speed if self.basic_attacking else self.default_animation_speed
        # clamp index
        if index < 0:
            index = 0
        if index >= len(frames):
            index = 0 if loop else len(frames) - 1

        current_time = pygame.time.get_ticks()
        if current_time - self.last_atk_time > frame_duration:
            self.last_atk_time = current_time
            self.image = frames[int(index)]
            index += 1
            if index >= len(frames):
                if loop:
                    index = 0
                else:
                    index = len(frames) - 1
                    return index, False  # finished (non-loop)
        return index, True
    
    def jump_animation(self):
        if self.facing_right:
            self.player_jump_index, _ = self.animate(self.player_jump, self.player_jump_index, loop=False)
        else:
            self.player_jump_index_flipped, _ = self.animate(self.player_jump_flipped, self.player_jump_index_flipped, loop=False)
        
        self.last_atk_time -= DEFAULT_ANIMATION_SPEED_FOR_JUMPING  # Animation Speed Reduced

    def simple_idle_animation(self, animation_speed=0):
        if self.facing_right:
            self.player_idle_index, _ = self.animate(self.player_idle, self.player_idle_index, loop=True)
        else:
            self.player_idle_index_flipped, _ = self.animate(self.player_idle_flipped, self.player_idle_index_flipped, loop=True)

        self.last_atk_time -= animation_speed
        
    def run_animation(self, animation_speed=0):
        if self.facing_right:
            self.player_run_index, _ = self.animate(self.player_run, self.player_run_index, loop=True)
        else:
            self.player_run_index_flipped, _ = self.animate(self.player_run_flipped, self.player_run_index_flipped, loop=True)

        self.last_atk_time -= animation_speed
        
    def atk1_animation(self, animation_speed=0):
        if self.facing_right:
            self.player_atk1_index, self.attacking1 = self.animate(self.player_atk1, self.player_atk1_index, loop=False)
        else:
            self.player_atk1_index_flipped, self.attacking1 = self.animate(self.player_atk1_flipped, self.player_atk1_index_flipped, loop=False)

        self.last_atk_time -= animation_speed
        
    def atk2_animation(self, animation_speed=0):
        if self.facing_right:
            self.player_atk2_index, self.attacking2 = self.animate(self.player_atk2, self.player_atk2_index, loop=False)
        else:
            self.player_atk2_index_flipped, self.attacking2 = self.animate(self.player_atk2_flipped, self.player_atk2_index_flipped, loop=False)

        self.last_atk_time -= animation_speed
        
    def atk3_animation(self, animation_speed=0):
        if self.facing_right:
            self.player_atk3_index, self.attacking3 = self.animate(self.player_atk3, self.player_atk3_index, loop=False)
        else:
            self.player_atk3_index_flipped, self.attacking3 = self.animate(self.player_atk3_flipped, self.player_atk3_index_flipped, loop=False)

        self.last_atk_time -= animation_speed
        
    def sp_animation(self, animation_speed=0):
        if self.facing_right:
            self.player_sp_index, self.sp_attacking = self.animate(self.player_sp, self.player_sp_index, loop=False)
        else:
            self.player_sp_index_flipped, self.sp_attacking = self.animate(self.player_sp_flipped, self.player_sp_index_flipped, loop=False)

        self.last_atk_time -= animation_speed

    def basic_animation(self, animation_speed=0):
        if self.facing_right:
            self.player_basic_index, self.basic_attacking = self.animate(self.player_basic, self.player_basic_index, loop=False, basic_atk=True)
        else:
            self.player_basic_index_flipped, self.basic_attacking = self.animate(self.player_basic_flipped, self.player_basic_index_flipped, loop=False, basic_atk=True)

        self.last_atk_time -= animation_speed

        
    def play_death_animation(self):
        if self.is_dead():
            if self.facing_right:
                # Play normal death animation for facing right
                if self.player_death_index < len(self.player_death):  # If animation is still ongoing
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_atk_time > 140:  # Adjust frame duration as needed
                        self.last_atk_time = current_time
                        self.image = self.player_death[self.player_death_index]
                        self.player_death_index += 1
                else:
                    # Display the last frame of the death animation
                    self.image = self.player_death[-1]
            else:
                # Play flipped death animation for facing left
                if self.player_death_index < len(self.player_death_flipped):  # If animation is still ongoing
                    current_time = pygame.time.get_ticks()
                    if current_time - self.last_atk_time > 140:  # Adjust frame duration as needed
                        self.last_atk_time = current_time
                        self.image = self.player_death_flipped[self.player_death_index]
                        self.player_death_index += 1
                else:
                    # Display the last frame of the flipped death animation
                    self.image = self.player_death_flipped[-1]
                    

    def draw_health_bar(self, screen):
        """Draws a small health bar 10px above the player's hitbox."""
        bar_width = 50
        bar_height = 6

        # Health ratio (0.0 to 1.0)
        hp_ratio = max(0, min(1, self.health / self.max_health))

        # Calculate extension for temp_hp
        extension_width = int((self.temp_hp / self.max_health) * bar_width)

        # Health bar position (centered)
        bar_x = self.hitbox_rect.centerx - bar_width // 2
        bar_y = self.hitbox_rect.top - 14 - bar_height

        # Background (black bar)
        pygame.draw.rect(screen, black, (bar_x, bar_y, bar_width, bar_height))

        # Foreground (green health)
        green_width = int(bar_width * hp_ratio)
        pygame.draw.rect(screen, green, (bar_x, bar_y, green_width, bar_height))

        # Temp HP (gold extension)
        if self.temp_hp > 0:
            temp_ratio = max(0, min(1, self.temp_hp))
            temp_width = int(temp_ratio * extension_width)
            pygame.draw.rect(screen, gold, (bar_x + green_width, bar_y, temp_width, bar_height))
    def draw_mana_bar(self, screen):
        """Draws a small health bar 10px above the player's hitbox."""
        bar_width = 50
        bar_height = 4

        # Health ratio (0.0 to 1.0)
        mana_ratio = max(0, min(1, self.mana / self.max_mana))

        # Health bar position (10px above hitbox)
        bar_x = self.hitbox_rect.centerx - bar_width // 2
        bar_y = self.hitbox_rect.top - 10 - bar_height

        # Background (black bar)
        pygame.draw.rect(screen, black, (bar_x, bar_y, bar_width, bar_height))

        # Foreground (green health)
        blue_width = int(bar_width * mana_ratio)
        pygame.draw.rect(screen, cyan2, (bar_x, bar_y, blue_width, bar_height))
    def draw_special_bar(self, screen):
        """Draws a small health bar 10px above the player's hitbox."""
        bar_width = 50
        bar_height = 2

        # Health ratio (0.0 to 1.0)
        special_ratio = max(0, min(1, self.special / self.max_special))

        # Health bar position (10px above hitbox)
        bar_x = self.hitbox_rect.centerx - bar_width // 2
        bar_y = self.hitbox_rect.top - 20 - bar_height

        # Background (black bar)
        pygame.draw.rect(screen, black, (bar_x, bar_y, bar_width, bar_height))

        # Foreground (green health)
        gold_width = int(bar_width * special_ratio)
        pygame.draw.rect(screen, ('purple' if self.special == self.max_special else 'blue' if self.special_active else gold),
                          (bar_x, bar_y, gold_width, bar_height))

    def draw_regen_rate(self, screen, hp_regen, mana_regen, p1_posx=0, p1_posy=0, p2_posx1=0, p2_posx2=0, p2_posy=0):
        """
        Must call player_status first to initialize the variables passed.
        
        Draws the current health and mana regeneration rates on the health and mana bars.
        The text is green, half the size of the default font, and positioned slightly adjusted
        based on the player type (right for Player 1, left for Player 2).
        """
        font = global_vars.get_font(15)  # Half the default size
        regen_hp_color = green 
        regen_mana_color = cyan2

        # Health regeneration text
        health_regen_text = font.render(f"+{hp_regen * FPS:.2f}/s", True, regen_hp_color)
        mana_regen_text = font.render(f"+{mana_regen * FPS:.2f}/s", True, regen_mana_color)

        if self.player_type == 1:
            # Player 1: Adjust text slightly to the right
            screen.blit(health_regen_text, (p1_posx - health_regen_text.get_width() - 25, p1_posy + 7))
            screen.blit(mana_regen_text, (p1_posx - health_regen_text.get_width() - 25, p1_posy+50 + 7))
        elif self.player_type == 2:
            # Player 2: Adjust text slightly to the left
            screen.blit(health_regen_text, (p2_posx1+p2_posx2 + 15, p2_posy + 7))
            screen.blit(mana_regen_text, (p2_posx1+p2_posx2 + 15, p2_posy+50 + 7))
    
    # def draw_icon_and_value(self, screen, )
    def draw_stats(self, screen, stats=None, posy=50, gap=25, icon_gap=6):
        """
        Draws stats with icons on the screen.
        
        If stats is None, uses default strength, intelligence, agility.
        Otherwise, uses the provided list of dicts, each with:
        - 'icon': pygame.Surface
        - 'value': int/float
        - 'color': tuple (RGB)
        
        Example custom stats:
        stats = [
            {'icon': some_icon, 'value': 100, 'color': (255, 0, 0)},
            # ...
        ]
        """
        font = global_vars.get_font(15)

        if stats is None:
            # Default stats
            stats = [
                {'icon': self.strength_attribute_icon, 'value': self.strength, 'color': red},
                {'icon': self.intelligence_attribute_icon, 'value': self.intelligence, 'color': cyan2},
                {'icon': self.agility_attribute_icon, 'value': self.agility, 'color': green}
            ]

        posx1 = 135
        posx2 = width - posx1

        start_x = posx1 if self.player_type == 1 else posx2
        direction = 1 if self.player_type == 1 else -1

        x = start_x

        for attr in stats:
            icon = attr['icon']
            value = attr['value']
            color = attr['color']

            text = font.render(str(value), True, color)

            icon_y = posy + (text.get_height() - icon.get_height()) // 2

            if direction == 1:
                screen.blit(icon, (x, icon_y))
                screen.blit(text, (x + icon.get_width() + icon_gap, posy))
                x += icon.get_width() + text.get_width() + gap
            else:
                screen.blit(icon, (x - icon.get_width(), icon_y))
                screen.blit(text, (x - icon.get_width() - icon_gap - text.get_width(), posy))
                x -= icon.get_width() + text.get_width() + gap

            # Player 2: Adjust text slightly to the left
            # screen.blit(strength_text, (p2_posx1+p2_posx2 + 15, p2_posy + 27))
            # screen.blit(mana_regen_text, (p2_posx1+p2_posx2 + 15, p2_posy+50 + 27))
    
    # def draw_profile(self, center_pos, small=False, hero_sp=False):
    #     """
    #     Draw the player's current image as profile icon with border.
        
    #     Args:
    #         center_pos (tuple): Center position for the icon.
    #         small (bool or str): If True, use small size (50x50). If 'smallest', use 25x25.
    #         hero_sp (bool): If True, use gold border for special active.
    #     """
    #     if self.image is None:
    #         return
        
    #     if small == 'smallest':
    #         profile = pygame.transform.scale(self.image, (25, 25))
    #         offset = (15, 15)
    #         border = (30, 30)
    #     elif small:
    #         profile = pygame.transform.scale(self.image, (50, 50))
    #         offset = (25, 25)
    #         border = (60, 60)
    #     else:
    #         profile = pygame.transform.scale(self.image, (75, 75))
    #         offset = (37, 37)
    #         border = (85, 85)
        
    #     if hero_sp:
    #         color = gold
    #     else:
    #         color = black
        
    #     rect = profile.get_rect(center=center_pos)
    #     decor = pygame.Rect(rect.centerx - offset[0], rect.centery - offset[1], border[0], border[1])
    #     # pygame.draw.rect(screen, color, decor)
    #     screen.blit(profile, rect)

    def player_status(self, health, mana, special):
        # print(self.temp_hp)
        orange = 'orange'
        self.attack_stats = [
                {'icon': self.attack_speed_icon, 'value': f'{self.attack_speed:.0f}', 'color': orange},
                {'icon': self.attack_time_icon, 'value': f'{f'{self.basic_attack_cooldown / 1000:.2f}'}s', 'color': orange},
                {'icon': self.attack_damage_icon, 'value': f'{self.basic_attack_damage:.1f}', 'color': orange}
            ]
        
        self.attribute_stats = [
                {'icon': self.strength_attribute_icon, 'value': f'{self.strength:.0f}', 'color': red},
                {'icon': self.intelligence_attribute_icon, 'value': f'{self.intelligence:.0f}', 'color': cyan2},
                {'icon': self.agility_attribute_icon, 'value': f'{self.agility:.0f}', 'color': green}
            ]
        

        font = global_vars.get_font(20)
        p1_x = self.player_1_x
        p1_y = self.player_1_y
        p2_x = self.player_2_x
        p2_y = self.player_2_y

        # Re-declaring the values
        self.health = health
        self.mana = mana
        self.special = special

        # Color Definitions
        dark_red = 'darkred'  # Dark Red
        crimson = 'crimson'  # Crimson Red
        dark_olive_green = 'chartreuse'  # Dark Olive Green
        dim_gray = 'gray20'  # Dim Gray for decor

        if self.player_type == 1:
            self.health_bar_p1 = pygame.Rect(p1_x, p1_y, self.health, 20)
            self.health_bar_p1_after = pygame.Rect(p1_x, p1_y, self.white_health_p1, 20)
            self.mana_bar_p1 = pygame.Rect(p1_x, p1_y+50, self.mana, 20)
            self.mana_bar_p1_after = pygame.Rect(p1_x, p1_y+50, self.white_mana_p1, 20)

            self.special_bar_p1 = pygame.Rect(p1_x, p1_y-25, self.special, 10)

            self.temp_hp_bar_p1 = pygame.Rect(self.health_bar_p1.x + self.health_bar_p1.width, self.health_bar_p1.y, self.temp_hp, 20)


            # Recalculate mana decor width based on max mana
            self.hpdecor_end_p1 = self.max_health + self.temp_hp + 10
            self.manadecor_end_p1 = self.max_mana + 10  # Fixing mana decor width based on max mana

            self.hp_decor_p1 = pygame.Rect(p1_x-6, p1_y-5, self.hpdecor_end_p1, 30)
            self.mana_decor_p1 = pygame.Rect(p1_x-6, p1_y-5 + 50, self.manadecor_end_p1, 30)  # Fixed width for mana decor

            self.special_decor_p1 = pygame.Rect(p1_x-6, p1_y-5 - 25, self.max_special + 10, 20)

            # White rects
            if self.health < self.white_health_p1:
                self.white_health_p1 -= WHITE_BAR_SPEED_HP
            if self.health > self.white_health_p1:
                self.white_health_p1 += WHITE_BAR_SPEED_HP
            if self.mana < self.white_mana_p1:
                self.white_mana_p1 -= WHITE_BAR_SPEED_MANA
            if self.mana > self.white_mana_p1:
                self.white_mana_p1 += WHITE_BAR_SPEED_MANA

            # Health limit
            if self.health > self.max_health:
                self.health = self.max_health
            # Mana limit
            if self.mana > self.max_mana:
                self.mana = self.max_mana

            if self.special > self.max_special:
                self.special = self.max_special
            
            if self.special < 0:
                self.special = 0

            # Health and Mana Text Color Change
            # Health color logic based on percentage
            if self.health < (self.max_health * 0.2):  # Below 20%
                health_color = crimson
                bar_color = crimson
                fill_color = white
            elif self.health < (self.max_health * 0.4):  # Below 40%
                health_color = (255,200,200)
                bar_color = dark_olive_green  # Slight mix of green and dark red
                fill_color = dark_red
            else:  # Above 40%
                health_color = white
                bar_color = green
                fill_color = red

            mana_color = red if self.mana < self.lowest_mana_cost else white

            if self.special == self.max_special:
                special_color = 'purple'
            elif self.special_active:
                special_color = 'blue'
            else:
                special_color = 'yellow'

            # Health and Mana Text
            self.health_display_text_p1 = font.render(f'[{int(self.health + self.temp_hp)}]', TEXT_ANTI_ALIASING, health_color)
            self.mana_display_text_p1 = font.render(f'[{int(self.mana)}]', TEXT_ANTI_ALIASING, mana_color)

            self.special_display_text_p1 = font.render(f'[{int(self.special)}]', TEXT_ANTI_ALIASING, special_color)

            # Blit Texts
            screen.blit(self.health_display_text_p1, (
                self.hp_decor_p1.right + TEXT_DISTANCE_BETWEEN_STATUS_AND_TEXT,
                self.hp_decor_p1.top + (self.hp_decor_p1.height // 2 - self.health_display_text_p1.get_height() // 2)
                ))

            screen.blit(self.mana_display_text_p1, (
                self.mana_decor_p1.right + TEXT_DISTANCE_BETWEEN_STATUS_AND_TEXT,
                self.mana_decor_p1.top + (self.mana_decor_p1.height // 2 - self.mana_display_text_p1.get_height() // 2)
                ))
            
            screen.blit(self.special_display_text_p1, (
                self.special_decor_p1.right + TEXT_DISTANCE_BETWEEN_STATUS_AND_TEXT,
                self.special_decor_p1.top + (self.special_decor_p1.height // 2 - self.health_display_text_p1.get_height() // 2)
                ))

            # Draw Rects
            pygame.draw.rect(screen, dim_gray, self.hp_decor_p1)  # Slightly brighter decor color
            pygame.draw.rect(screen, fill_color, self.health_bar_p1_after)  # Design when hp is low
            pygame.draw.rect(screen, bar_color, self.health_bar_p1)  # Design when hp is low   

            pygame.draw.rect(screen, dim_gray, self.mana_decor_p1)  # Decor
            pygame.draw.rect(screen, white, self.mana_bar_p1_after)  # Design when mana is low
            pygame.draw.rect(screen, cyan2, self.mana_bar_p1)  # Design when mana is low

            pygame.draw.rect(screen, dim_gray, self.special_decor_p1)
            pygame.draw.rect(screen, special_color, self.special_bar_p1)

            pygame.draw.rect(screen, gold, self.temp_hp_bar_p1)


            # show health regen (call player_status() firsts)
            self.draw_regen_rate(screen, self.health_regen, self.mana_regen, p1_posx=self.player_1_x, p1_posy=self.player_1_y)
            # self.draw_stats(screen, 20, 70)




        elif self.player_type == 2:
            # Start positions aligned to the right
            self.hpdecor_end_p2 = self.max_health + self.temp_hp + 10
            self.manadecor_end_p2 = self.max_mana + 10  # Fixing mana decor width based on max mana

            self.specialdecor_end_p2 = self.max_special + 10






            self.healthdecor_p2_starting = width - self.hpdecor_end_p2 - p2_x
            self.manadecor_p2_starting = width - self.manadecor_end_p2 - p2_x

            self.specialdecor_p2_starting = width - self.specialdecor_end_p2 - p2_x

            # Decorations
            self.hp_decor_p2 = pygame.Rect(self.healthdecor_p2_starting, p2_y-5, self.hpdecor_end_p2, 30)
            self.mana_decor_p2 = pygame.Rect(self.manadecor_p2_starting, p2_y+50-5, self.manadecor_end_p2, 30)  # Fixed width for mana decor

            self.special_decor_p2 = pygame.Rect(self.specialdecor_p2_starting, p2_y-5 - 25, self.specialdecor_end_p2, 20)

            # Adjust bar starting x-position to align inside the decor with a 5px padding
            bar_x_start = self.hp_decor_p2.left + 5
            mana_bar_max_width = self.mana_decor_p2.width - 10

            special_bar_max_width = self.special_decor_p2.width - 10


            # Calculate dynamic bar widths based on percentage of current value
            self.special_bar_p2_width = int((self.special / self.max_special) * special_bar_max_width)
            
            self.mana_bar_p2_width = int((self.mana / self.max_mana) * mana_bar_max_width)
            self.white_mana_p2_width = int((self.white_mana_p2 / self.max_mana) * mana_bar_max_width)

            # Health and Mana Rects (bars should start from right side and shrink towards left)
            self.health_bar_p2 = pygame.Rect(self.hp_decor_p2.right - self.health - 5, p2_y, self.health, 20)
            self.health_bar_p2_after = pygame.Rect(self.hp_decor_p2.right - self.white_health_p2 - 5, p2_y, self.white_health_p2, 20)

            self.temp_hp_bar_p2 = pygame.Rect(self.health_bar_p2.x - self.temp_hp, self.health_bar_p2.y, self.temp_hp + 1, 20)
            
            self.mana_bar_p2 = pygame.Rect(self.mana_decor_p2.right - self.mana_bar_p2_width - 5, p2_y+50, self.mana_bar_p2_width, 20)
            self.mana_bar_p2_after = pygame.Rect(self.mana_decor_p2.right - self.white_mana_p2_width - 5, p2_y+50, self.white_mana_p2_width, 20)


            self.special_bar_p2 = pygame.Rect(self.special_decor_p2.right - self.special_bar_p2_width - 5, p2_y-25, self.special_bar_p2_width, 10)

            

            # White rects update logic
            if self.health > self.white_health_p2:
                self.white_health_p2 += WHITE_BAR_SPEED_HP
            if self.health < self.white_health_p2:
                self.white_health_p2 -= WHITE_BAR_SPEED_HP
            if self.mana > self.white_mana_p2:
                self.white_mana_p2 += WHITE_BAR_SPEED_MANA
            if self.mana < self.white_mana_p2:
                self.white_mana_p2 -= WHITE_BAR_SPEED_MANA

            # # Limits
            # self.health = min(self.health, self.max_health)
            # self.mana = min(self.mana, self.max_mana)

            # self.special = min(self.special, self.max_special)

            # Health limit
            if self.health > self.max_health:
                self.health = self.max_health
            # Mana limit
            if self.mana > self.max_mana:
                self.mana = self.max_mana

            if self.special > self.max_special:
                self.special = self.max_special
            
            if self.special < 0:
                self.special = 0

            # Texts
            if self.health < (self.max_health * 0.2):  # Below 20%
                health_color_p2 = crimson
                bar_color_p2 = crimson
                fill_color_p2 = white
            elif self.health < (self.max_health * 0.4):  # Below 40%
                health_color_p2 = (255,200,200)
                bar_color_p2 = dark_olive_green  # Slight mix of green and dark red
                fill_color_p2 = dark_red
            else:  # Above 40%
                health_color_p2 = white
                bar_color_p2 = green
                fill_color_p2 = red

            mana_color_p2 = red if self.mana < self.lowest_mana_cost else white

            if self.special == self.max_special:
                special_color_p2 = 'purple'
            elif self.special_active:
                special_color_p2 = 'blue'
            else:
                special_color_p2 = 'yellow'

            self.health_display_text_p2 = font.render(f'[{int(self.health + self.temp_hp)}]', TEXT_ANTI_ALIASING, health_color_p2)
            self.mana_display_text_p2 = font.render(f'[{int(self.mana)}]', TEXT_ANTI_ALIASING, mana_color_p2)

            self.special_display_text_p2 = font.render(f'[{int(self.special)}]', TEXT_ANTI_ALIASING, special_color_p2)

            

            # Blit Texts
            screen.blit(self.health_display_text_p2, (
                self.hp_decor_p2.left - self.health_display_text_p2.get_width() - TEXT_DISTANCE_BETWEEN_STATUS_AND_TEXT,
                self.hp_decor_p2.top + (self.hp_decor_p2.height // 2 - self.health_display_text_p2.get_height() // 2)
            ))
            screen.blit(self.mana_display_text_p2, (
                self.mana_decor_p2.left - self.mana_display_text_p2.get_width() - TEXT_DISTANCE_BETWEEN_STATUS_AND_TEXT,
                self.mana_decor_p2.top + (self.mana_decor_p2.height // 2 - self.mana_display_text_p2.get_height() // 2)
            ))

            screen.blit(self.special_display_text_p2, (
                self.special_decor_p2.left - self.special_display_text_p2.get_width() - TEXT_DISTANCE_BETWEEN_STATUS_AND_TEXT,
                self.special_decor_p2.top + (self.special_decor_p2.height // 2 - self.health_display_text_p2.get_height() // 2)
            ))

            
 

            # Draw Rects
            pygame.draw.rect(screen, dim_gray, self.hp_decor_p2)
            pygame.draw.rect(screen, fill_color_p2, self.health_bar_p2_after)
            pygame.draw.rect(screen, bar_color_p2, self.health_bar_p2)

            pygame.draw.rect(screen, dim_gray, self.mana_decor_p2)
            pygame.draw.rect(screen, white, self.mana_bar_p2_after)
            pygame.draw.rect(screen, cyan2, self.mana_bar_p2)

            pygame.draw.rect(screen, dim_gray, self.special_decor_p2)
            pygame.draw.rect(screen, special_color_p2, self.special_bar_p2)

            pygame.draw.rect(screen, gold, self.temp_hp_bar_p2)


            # show health regen (call player_status() firsts)
            self.draw_regen_rate(screen, self.health_regen, self.mana_regen, p2_posx1=self.healthdecor_p2_starting, p2_posx2=self.hpdecor_end_p2, p2_posy=self.player_2_y)
            

        

        # Variables are outside the class
        # Health and Mana Icon Draw
        # screen.blit(hp_icon, hp_icon_p1_rect)
        # screen.blit(hp_icon, hp_icon_p2_rect)
        # screen.blit(mana_icon, mana_icon_p1_rect)
        # screen.blit(mana_icon, mana_icon_p2_rect)

        self.draw_stats(screen,
                        self.attribute_stats,
                        posy=50,
                        gap=25,
                        icon_gap=6
                        )
        
        self.draw_stats(screen,
                        self.attack_stats,
                        posy=20,
                        gap=25,
                        icon_gap=6
                        )
        
        
        if self.health <= 0:
            self.health = 0
            self.winner = 2 if self.player_type == 1 else 1

            return self.winner
    
    # Don't forget to have input method on the players since their attacks are specific :))
    def input(self, hotkey1, hotkey2, hotkey3, hotkey4, right_hotkey, left_hotkey, jump_hotkey, basic_hotkey, special_hotkey):
        pass
                    # print(f"Attack did not execute: {self.mana}:")   
                # print('Skill 4 used')
                

            # if skill_1_rect.collidepoint(self.mouse_pos) and self.mouse_press[0]:
            #     self.attacking1 = True
            # if skill_2_rect.collidepoint(self.mouse_pos) and self.mouse_press[0]:
            #     self.attacking2 = True
            # if skill_3_rect.collidepoint(self.mouse_pos) and self.mouse_press[0]:
            #     self.attacking3 = True
            # if skill_4_rect.collidepoint(self.mouse_pos) and self.mouse_press[0]:
            #     self.sp_attacking = True


    def is_skill_clicked(self, mouse_pos, mana):
        """
        Checks if a skill rect is clicked and if the player has enough mana.

        Args:
            mouse_pos (tuple): The current mouse position.
            mana (int): The player's current mana.

        Returns:
            int: The index of the clicked skill, or -1 if no skill is clicked or not enough mana.
        """
        for i, rect in enumerate(self.rects):
            if (rect.collidepoint(mouse_pos)):
                if mana >= self.mana_costs[i]:
                    return i
                else:
                    print("Not enough mana!")
                    return -1
        return -1

    def can_die(self, damage):
        '''returns true if the damage taken can kill the player.'''
        return damage >= self.health
    
    def take_damage(self, damage, add_mana_to_self=False, enemy:object=None, add_mana_to_enemy=False, mana_multiplier=1):
        # immune to damage
        if self.immortality_activated:
            self.display_damage(damage, interval=30, color=gold, size=30)  # Optional feedback
            return
        
        current_time = pygame.time.get_ticks() / 1000 - global_vars.PAUSED_TOTAL_DURATION / 1000
        
        if self.can_die(damage) and not self.immortality_activated:
            for item in self.items:
                if 'immortality' in item.bonus_type and current_time - item.last_used >= item.cooldown: # check if dmg can kill hero
                    self.immortality_activated = True
                    self.immortality_duration = (current_time * 1000) + 7000
                    item.last_used = current_time
                
                    if item.attack_frames:
                        from heroes import Attack_Display
                        attack_display.add(Attack_Display(
                            x=self.rect.centerx, y=self.rect.top,
                            frames=item.attack_frames,
                            frame_duration=item.attack_frame_duration,
                            repeat_animation=item.attack_repeat,
                            dmg=0, final_dmg=0,
                            who_attacks=self, who_attacked=self.enemy,
                            speed=0, moving=False, heal=False,
                            continuous_dmg=False, per_end_dmg=(False, False),
                            disable_collide=True, stun=(False, 0),
                            sound=(False, None, None, None), kill_collide=False,
                            follow=(False, True), follow_self=True, follow_offset=(0,50)
                        ))
                    self.health = 1
                    return
            

        if self.is_dead():
            return
        if self.damage_reduce > 0:
            damage -= (damage * self.damage_reduce)
        
        # Absorb damage with temp_hp first
        if self.temp_hp > 0:
            temp_absorb = min(damage, self.temp_hp)
            self.temp_hp -= temp_absorb
            self.display_damage(damage)
            damage -= temp_absorb

        # adds mana to the attacker
        if add_mana_to_self and enemy is not None:
            self.add_mana(damage, enemy, mana_mult=mana_multiplier)
        
        # adds mana to the attacked player (which is self)
        if add_mana_to_enemy:
            self.add_mana(damage, mana_mult=mana_multiplier)
        
        # if enemy is not None:
        #     if enemy.mana_burn > 0:
        #         self.take_mana(damage * enemy.mana_burn, mana_burn=True)
                

        self.health = max(0, self.health - damage)  # Ensure health doesn't go below 0
        # print(f"THIS PLAYER took {damage} damage. Current health: {self.health}")

        
        if self.health <= 0:
            self.die()  # Trigger the death process
            self.play_death_animation()  # Play death animation

    def take_mana(self, mana, mana_burn=False):
        if self.is_dead():
            return
        self.mana = max(0, self.mana - mana)  # Ensure health doesn't go below 0
        # print(f"THIS PLAYER took {damage} damage. Current health: {self.health}")

    def take_mana_burn(self, enemy, amount, burn_per:int=0):
        'burns mana based on amount or damage dealt. deals damage based on mana burnt.'
        if self.is_dead():
            return
        # Already calculated at Attack_Display class
        self.mana = max(0, self.mana - amount)
        mana_to_damage = amount * burn_per
        enemy.take_damage(mana_to_damage, enemy=None)


            

    

    def is_dead(self):
        return hasattr(self, "health") and self.health <= LITERAL_HEALTH_DEAD
    
    def take_heal(self,heal): # add health
        if self.is_dead():
            return
        self.health = max(0, self.health + heal)
        self.display_damage(heal, color=green, health_modify=True)

    def take_temp_hp(self, temp_heal): # add health
        if self.is_dead():
            return
        self.temp_hp = max(0, self.temp_hp + temp_heal)
        self.display_damage(temp_heal, color=gold, size=25)

    def add_mana(self, mana, enemy:object=None, mana_mult=1): # add mana
        if enemy is not None: #called by take damage, adds mana to attacker if enemy is not None
            enemy.mana = max(0, enemy.mana + (mana*mana_mult))
            enemy.display_damage(mana*mana_mult, color=cyan2, mana_modify=True)
        else: #add mana to the attacked player, called by take_special?
            self.mana = max(0, self.mana + (mana*mana_mult)) # add mana to hero
            enemy.display_damage(mana*mana_mult, color=cyan2, mana_modify=True)

    def take_special(self, amount):
        if self.is_dead():
            return
        if self.special_increase > 0:
            amount += (amount * self.special_increase)
        self.special = max(0, self.special + amount)

        # adds mana to attacker using mana refund item bonus (multiplier < 1 or more)
        if self.mana_refund > 0:
            self.add_mana(amount, self, mana_mult=self.mana_refund)
            # print('mana added')

    def draw_distance(self, enemy): # self.enemy_distance = int(abs(self.player.x_pos - self.x_pos))
        # Accept either a single enemy object or a list of enemies
        font = global_vars.get_font(20)
        target = None
        # If a list was passed, pick the nearest valid enemy
        if isinstance(enemy, (list, tuple)):
            candidates = [e for e in enemy if e is not None and hasattr(e, 'x_pos')]
            if not candidates:
                return
            target = min(candidates, key=lambda e: abs(self.x_pos - getattr(e, 'x_pos', self.x_pos)))
        else:
            target = enemy

        if target is None or not hasattr(target, 'x_pos'):
            return

        try:
            enemy_distance = int(abs(self.x_pos - target.x_pos))
        except Exception:
            return

        enemy_distance_surf = font.render(str(enemy_distance), TEXT_ANTI_ALIASING, 'Red')
        screen.blit(enemy_distance_surf, (self.x_pos, self.y_pos - 120))
        left = self.x_pos if target.x_pos > self.x_pos else target.x_pos
        line_rect = pygame.rect.Rect((left), self.y_pos - 60, enemy_distance, 2)
        pygame.draw.rect(screen, 'Red', line_rect)
    
    def stun(self, stunned, x_pos, y_pos, adjust_y_pos, jump_force=DEFAULT_JUMP_FORCE, gravity=DEFAULT_GRAVITY):
        # I give up stunned stops attacking from magician, i will just not make it not attack while jumping
        if stunned:
            self.jumping = True
            self.y_pos = y_pos - adjust_y_pos
            self.x_pos = x_pos
            
        
    def movement_status(self, type, source=None, slow_rate=0.5):
        '''
        Apply frozen or rooted status
        type: freeze/root, 1=freeze, 2=root, 3=slow:tuple(slow, slow rate)
        mode: (or type)
            1 - while collides player, effect active, else none (collision only)
            2 - when collides player, effect active, until attack ends (if hit once)
            3 - effect active, until attack ends (full duration)
        '''
        if self.is_dead():
            return

        # Ensure storage structures exist
        if not hasattr(self, "_freeze_sources"):
            self._freeze_sources = []
        if not hasattr(self, "_root_sources"):
            self._root_sources = []
        if not hasattr(self, "_slow_sources"):
            self._slow_sources = []
        if not hasattr(self, "_silence_sources"):
            self._silence_sources = []
        if not hasattr(self, "_silence_sources"):
            self._silence_sources = []

        if type == 1:  # Freeze
            # add source if not already present
            if source not in self._freeze_sources:
                self._freeze_sources.append(source)
            # set flag if not already
            if not getattr(self, "frozen", False):
                self.running = False
                self.frozen = True
            # stop movement immediate
            # try:
            #     self.velocity.x = 0
            #     self.velocity.y = 0
            # except Exception:
            #     pass

        elif type == 2:  # Root
            if source not in self._root_sources:
                self._root_sources.append(source)
            if not getattr(self, "rooted", False):
                self.running = False
                self.rooted = True
            # try:
            #     self.velocity.x = 0
            #     self.velocity.y = 0
            # except Exception:
            #     pass

        if type == 3:  # Slow
            # add source if not already present
            if source not in self._slow_sources:
                self._slow_sources.append(source)
            # set flag if not already
            if not getattr(self, "slowed", False):
                self.speed_multiplier = slow_rate
                self.slow_speed = self.speed * self.speed_multiplier
                if not self.slowed:
                    self.slowed = True

        if type == 4:  # Silence
            if source not in self._silence_sources:
                self._silence_sources.append(source)
            if not getattr(self, "silenced", False):
                self.silenced = True

        # print(f"APPLY status {'freeze' if type == 1 else 'root' if type == 2 else 'slow'} from {source} in {self._freeze_sources if type == 1 else self._root_sources if type == 2 else self._slow_sources}")
    def remove_movement_status(self, type, source=None, slow_rate=1.0):
        """
        Remove frozen or rooted status only if *all* sources are cleared.
        """
        """
        Remove the named status only for the given source.
        If source is None, force-remove all sources and the status.
        """
        # Ensure storage structures exist
        if not hasattr(self, "_freeze_sources"):
            self._freeze_sources = []
        if not hasattr(self, "_root_sources"):
            self._root_sources = []
        if not hasattr(self, "_slow_sources"):
            self._slow_sources = []

        if type == 1:  # Freeze
            if source is None:
                # force remove all freezes
                self._freeze_sources.clear()
            else:
                # remove specific source if present
                try:
                    self._freeze_sources.remove(source)
                except ValueError:
                    pass
            # clear flag only if no other sources remain
            if len(self._freeze_sources) == 0:
                self.frozen = False
                # additional cleanup
                self.running = getattr(self, "running", False)
                # optional: reset velocities if relevant (or let physics resume)
                # self.velocity = pygame.math.Vector2(whatever)  # if you want

        elif type == 2:  # Root
            if source is None:
                self._root_sources.clear()
            else:
                try:
                    self._root_sources.remove(source)
                except ValueError:
                    pass

            if len(self._root_sources) == 0:
                self.rooted = False
                self.running = getattr(self, "running", False)

        elif type == 3:
            if source is None:
                self._slow_sources.clear()
            else:
                try:
                    self._slow_sources.remove(source)
                except ValueError:
                    pass
            if len(self._slow_sources) == 0:
                # Reset slow-related state when no slow sources remain
                self.slowed = False
                self.speed_multiplier = 1.0
                try:
                    # restore slow_speed to the base speed value
                    self.slow_speed = self.speed * self.speed_multiplier
                except Exception:
                    self.slow_speed = getattr(self, 'default_speed', getattr(self, 'speed', 0))
            
        elif type == 4:  # Silence
            if source is None:
                self._silence_sources.clear()
            else:
                try:
                    self._silence_sources.remove(source)
                except ValueError:
                    pass
            if len(self._silence_sources) == 0:
                self.silenced = False

        # print(f"REMOVE status {'freeze' if type == 1 else 'root' if type == 2 else 'slow'} from {source} in {self._freeze_sources if type == 1 else self._root_sources if type == 2 else self._slow_sources}")
                
    def draw_movement_status(self, screen, display=False):
        if display:
            if self.frozen or self.rooted:
                # Calculate overlay dimensions: 1/4 height from ground up
                overlay_height = self.hitbox_rect.height // (4 if self.rooted else 1)
                overlay_rect = pygame.Rect(
                    self.hitbox_rect.x,
                    self.hitbox_rect.bottom - overlay_height,  # from ground up
                    self.hitbox_rect.width,
                    overlay_height
                )

                # Choose color based on status
                if self.frozen:
                    color = (0, 100, 255, 50) # translucent blue
                elif self.rooted:
                    color = (139, 69, 19, 50) # brown, translucent
                elif self.silenced:
                    color = (100, 100, 100, 50)  # gray
                else:
                    color = (255, 255, 255, 0) # ???


                # Create surface for transparency
                overlay = pygame.Surface((overlay_rect.width, overlay_rect.height), pygame.SRCALPHA)
                overlay.fill(color)
                screen.blit(overlay, overlay_rect.topleft)

        # Optional: Draw hitbox outline (for debugging)
        # pygame.draw.rect(screen, (0, 255, 0), self.hitbox_rect, 2)

    def handle_speed(self):
        if self.slowed:
            self.speed = self.slow_speed
        else:
            self.speed = self.default_speed
            
    def die(self):
        if not self.is_dead():  # Check if the player is already dead
            self.health = 0  # Ensure the health is set to 0 when dying
            self.winner = 2 if self.player_type == 1 else 1  # Set the winner

    def move_to_screen(self): # drag the player when out of bounds
        # print('asd')
        if self.x_pos > width:
            self.x_pos -= 3
        if self.x_pos < 0:
            self.x_pos += 3













    def calculate_effective_as(self):
        """Effective Attack Speed.
        
        calculates:
        (base attack speed + attack speed from agility + flat attack speed from items) * attack speed multiplier

        required:
        - current agility
        - base attack speed
        - attack speed from items
        - attack speed multiplier

        """
        as_from_agility = self.agility * global_vars.AGILITY_AS_BONUS
        base_with_agility = self.base_attack_speed + as_from_agility
        effective_as = base_with_agility + self.bonus_attack_speed_flat# - self.flat_as_reduction
        total_percent = 1 + self.bonus_attack_speed_per# - self.percent_as_reduction
        effective_as *= max(0.0, total_percent)
        return max(global_vars.MIN_ATTACK_SPEED, min(global_vars.MAX_ATTACK_SPEED, effective_as))

    def calculate_basic_attack_interval(self):
        """Interval in ms: BAT / (AS / 100).
        
        base attack time / (total attack speed / 100)"""
        effective_as = self.calculate_effective_as()
        return self.base_attack_time / (effective_as / 100)

    def can_basic_attack(self):
        """Check if interval has passed."""
        current_time = pygame.time.get_ticks()
        return current_time - self.last_basic_attack_time >= self.calculate_basic_attack_interval()










            
    # ------------------------ HELPERS ------------------------
    def is_busy_attacking(self):
        """Returns True if the player is currently performing any attack."""
        return self.attacking1 or self.attacking2 or self.attacking3 or self.sp_attacking or self.basic_attacking

    def is_not_attacking(self):
        """Returns True if the player is not performing any skill or attack."""
        return not self.is_busy_attacking()

    def is_slowed(self):
        '''return true if slowed'''
        return self.slowed
    
    def is_frozen(self):
        '''return true if frozen'''
        return self.frozen
    
    def is_silenced(self):
        '''return true if silenced'''
        return self.silenced

    
    def can_move(self):
        """Return True if the player can move (not frozen or rooted or dead)."""
        return not (self.is_dead() or self.frozen or self.rooted)

    def can_cast(self):
        """Return True if the player can use skills (not frozen or dead)."""
        return not (self.is_dead() or self.frozen or self.silenced)
    
    def draw_hp(self):
        pass

    def is_using_skill_1(self):
        """Returns True if the player is currently performing skill 1."""
        return self.attacking1

    def is_using_skill_2(self):
        """Returns True if the player is currently performing skill 2."""
        return self.attacking2

    def is_using_skill_3(self):
        """Returns True if the player is currently performing skill 3."""
        return self.attacking3
    
    def is_using_skill_4(self):
            """Returns True if the player is performing the special attack."""
            return self.sp_attacking
    
    def is_using_basic_attack(self):
        """Returns True if the player is performing a basic attack."""
        return self.basic_attacking

    def can_cast_skill(self):
        """
        Returns True if the player is able to cast a skill.
        Handles silenced/frozen states automatically.
        """
        if self.frozen or self.silenced:
            return False
        return True

    def can_cast_specific_skill(self, skill_index):
        """Returns True if the specific skill is ready and player can cast it."""
        return self.can_cast_skill() and self.attacks[skill_index].is_ready() and self.mana >= self.attacks[skill_index].mana_cost

    def is_special_active(self):
        """Returns True if the player is in special mode."""
        return self.special_active

    def is_jumping_or_dead(self):
        """Returns True if player is jumping or dead."""
        return self.jumping or self.is_dead()

    def is_moving(self) -> bool:
        """Returns True if player is currently moving horizontally."""
        return self.running

    def is_facing_right(self):
        """Returns True if player is currently facing right."""
        return self.facing_right
    
    def regen_per_second(self, amount, fps=FPS) -> float:
        return amount / fps


    # ------------------------ Attack_Display class HELPERS ------------------------
    def attack_frame_count(self, default:pygame.Surface| list, flipped:pygame.Surface | list=None):
        """Returns the default frames when player is facing right, otherwise returns the flipped frames, as long as the flipped is provided.
        \nWhen only default is provided, always returns the default value. \n\nAccepts a list of attack frames.
        - default = surface list
        - flipped (optiona = flipped surface list"""
        return default if self.facing_right else flipped if flipped is not None else None
        
    def attack_position(self, target:object, axis:str='x', offset:int=0, require_facing:bool=False, positioning:str='centerx') -> int:
        """Returns x/y coordinate based on the target and offset starting from player.
        \nSet the offset either positive/negative values.
        - self.rect = starting position from player
        - self.target = starting position from detected enemy player
        - target (int value returned by particular method (self.target_enemy())) = starting position at specific position (probably the target)"""
        if axis == 'x':
            if positioning == 'centerx':
                position = target.centerx
        elif axis == 'y':
            #default to centery, for now.
            positioning = 'centery'
            if positioning == 'centery':
                position = target.centery
        # -----------------------------------------
        # Just checking the additional value if center x/y is not provided.
        if positioning not in ['centerx', 'centery']:
            if positioning == 'bottom':
                position = target.bottom
            elif positioning == 'left':
                position = target.left
            elif positioning == 'right':
                position = target.right
            elif positioning == 'top':
                position = target.top
        # -----------------------------------------
        if require_facing:
            final_position = position + offset if self.facing_right else position - offset
        else:
            final_position = position + offset
        return final_position
    
    def is_skill_ready(self, attack_mode, skill):
        '''if self.mana >= self.attacks[0].mana_cost and self.attacks[0].is_ready():'''
        attack_mana_cost = {}
        for num, val in enumerate(attack_mode):
            attack_mana_cost[num] = val.mana_cost
        # print(attack_mana_cost)
        return self.mana >= attack_mana_cost[skill] and attack_mode[skill].is_ready()

        
    def skill_duration(
        self,
        set_mode: tuple[str, int | float],
        frame_count: int = None,
        repeat_animation: int = 1,
        frame_divisor: int = 1,
        set_max_frame_duration: int = 100,
        print_values: bool = False
    ) -> tuple[float, int]:
        """
        Calculate animation frame duration and repeat count.

        set_mode:
            ('seconds', total_ms)
                - total_ms: total animation duration in milliseconds
                - requires frame_count

            ('frames', frame_duration)
                - frame_duration: duration of each frame in milliseconds

        frame_count:
            - Number of animation frames (used only in 'seconds' mode)

        repeat_animation:
            - How many times the animation repeats

        frame_divisor:
            - Divides frame duration and multiplies repeat count
            - Example: 2 = faster frames, more repeats

        set_max_frame_duration:
            - Maximum allowed duration per frame (ms)
            - Auto-increases repeat_animation if exceeded

        Returns:
            (frame_duration, repeat_animation)
        """


        if frame_divisor <= 0:
            raise ValueError("frame_divisor must be greater than 0")

        if set_mode[0] == 'seconds':
            if frame_count is None or frame_count <= 0:
                raise ValueError("frame_count must be greater than 0 when using 'seconds' mode")

            total_ms = set_mode[1]

            frame_duration = total_ms / frame_count

            # Manual divisor
            frame_duration /= frame_divisor
            repeat_animation *= frame_divisor

            # Auto-adjust if too slow
            safety = 0
            while frame_duration > set_max_frame_duration and safety < 10:
                repeat_animation += 1
                frame_duration = total_ms / (frame_count * repeat_animation)
                safety += 1

        elif set_mode[0] == 'frames':
            frame_duration = set_mode[1]

        else:
            raise ValueError("set_mode[0] must be 'seconds' or 'frames'")

        frame_duration = round(frame_duration, 2)

        if print_values:
            print(
                f"frame_duration={frame_duration}, "
                f"frame_count={frame_count}, "
                f"repeat_animation={repeat_animation}"
            )

        return frame_duration, repeat_animation




    # ------------------------ Targeting HELPERS ------------------------
    def single_target(self): # for single target spells, updates self.target when called.
        """Chooses a single enemy target (nearest enemy)"""
        if len(self.enemy) == 1:
            self.target = self.enemy[0]
        elif len(self.enemy) > 1:
            # Find closest enemy
            closest_enemy = None
            closest_distance = float('inf')
            for enemy in self.enemy:
                distance = abs(self.rect.centerx - enemy.rect.centerx)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_enemy = enemy
            self.target = closest_enemy if closest_enemy else random.choice(self.enemy)
        else:
            # No enemies available, use random as fallback
            self.target = random.choice(self.enemy)
    def face_selective_target(self):
        '''Pls call self.single_target() to update the self.target.
        
        Returns the targett and the detected target, store it to variable.'''
        # one liner is getting hard, took codes from bot_ai
        self.enemy_on_right = self.x_pos < (self.target.x_pos)
        self.enemy_on_left = self.x_pos > (self.target.x_pos)
        enemy_pos = (self.target.x_pos)
        target_detected = False
        if self.enemy_on_right and self.facing_right:
            target = enemy_pos
            target_detected = True
        elif self.enemy_on_right and not self.facing_right:
            target = self.rect.centerx + 300 if self.facing_right else self.rect.centerx - 300
        elif self.enemy_on_left and not self.facing_right:
            target = enemy_pos
            target_detected = True
        else:
            target = self.rect.centerx + 300 if self.facing_right else self.rect.centerx - 300
        return target, target_detected

    def target_enemy(self, position_fallback:int=150):
        """Returns a tuple (target, target_detected) store to variable depends on u.
        \n[0] - Returns the closest enemy position detected when facing the enemy in x-axis -> int.
        \n[1] - Returns if enemy is detected -> bool
        \nIf facing away from enemy/enemy not detected, targets the ground at provided position in x-axis."""
        self.single_target()
        target, target_detected = self.face_selective_target()
        if not target_detected:
            target = self.rect.centerx + (position_fallback if self.facing_right else -position_fallback)  # Default to casting in front
        return target, target_detected
    
    # ------------------------ Core Player Input Methods ------------------------
    
    def inputs(self,):
        """Base user input collection from saved hotkeys on controls.
        \nHandles input for all heroes"""
        # print("Entered Player.py")
        keybinds=key.read_settings()
        self.keys = pygame.key.get_pressed()
        self.input(
            (self.keys[keybinds['skill_1_p1'][0]]) if self.player_type == 1 else (self.keys[keybinds['skill_1_p2'][0]]), 
            (self.keys[keybinds['skill_2_p1'][0]]) if self.player_type == 1 else (self.keys[keybinds['skill_2_p2'][0]]), 
            (self.keys[keybinds['skill_3_p1'][0]]) if self.player_type == 1 else (self.keys[keybinds['skill_3_p2'][0]]), 
            (self.keys[keybinds['skill_4_p1'][0]]) if self.player_type == 1 else (self.keys[keybinds['skill_4_p2'][0]]),

            (self.keys[keybinds['right_move_p1'][0]]) if self.player_type == 1 else (self.keys[keybinds['right_move_p2'][0]]),
            (self.keys[keybinds['left_move_p1'][0]]) if self.player_type == 1 else (self.keys[keybinds['left_move_p2'][0]]),
            (self.keys[keybinds['jump_p1'][0]]) if self.player_type == 1 else (self.keys[keybinds['jump_p2'][0]]),

            (self.keys[keybinds['basic_atk_p1'][0]]) if self.player_type == 1 else (self.keys[keybinds['basic_atk_p2'][0]]),

            (self.keys[keybinds['sp_skill_p1'][0]]) if self.player_type == 1 else (self.keys[keybinds['sp_skill_p2'][0]])
            )
#sp=-0.1, default=-0.2 jump=-0.05
    def player_movement(self, right_hotkey, left_hotkey, jump_hotkey, current_time, jump_force, speed_modifier=0, special_active_speed=0.1, jump_force_modifier=0):
        '''Handles the player movement using user input (jump, move left/right).
        \nModify jump_force to increase/decrease the jump force of the player when jumping.
        \n- right,left,jump_hotkey = user input (no change)
        \n- current_time = get current time (no change)
        \n- jump_force: self.jump_force = DEFAULT_Y_POS
        \n- speed_modifier: base speed = 0
        \n- special_active_speed: increase speed when special mode = 0.1 (10%)'''
        
        if self.is_not_attacking():
            if right_hotkey:  # Move right
                self.running = True
                self.facing_right = True
                self.x_pos += (self.speed + ((self.speed * special_active_speed) if self.special_active else (self.speed * speed_modifier)))
                if self.x_pos > self.limit_movement_right - (self.hitbox_rect.width/2):  # Prevent moving beyond the screen
                    self.x_pos = self.limit_movement_right - (self.hitbox_rect.width/2)
            elif left_hotkey:  # Move left
                self.running = True
                self.facing_right = False
                self.x_pos -= (self.speed + ((self.speed * special_active_speed) if self.special_active else (self.speed * speed_modifier)))
                if self.x_pos < (self.limit_movement_left + (self.hitbox_rect.width/2)):  # Prevent moving beyond the screen
                    self.x_pos = (self.limit_movement_left + (self.hitbox_rect.width/2))
            else:
                self.running = False

            if jump_hotkey and self.y_pos == DEFAULT_Y_POS and current_time - self.last_atk_time > JUMP_DELAY:
                self.jumping = True
                self.y_velocity = jump_force * (1 + jump_force_modifier)
                self.last_atk_time = current_time  # Update the last jump time
    
    def item_activation(self, rect):
        'rect: simply passing self.rect that is updated. nevermind.'
        current_time_ticks = pygame.time.get_ticks() - global_vars.PAUSED_TOTAL_DURATION
        # Check for heal_when_low items
        current_time = pygame.time.get_ticks() / 1000 - global_vars.PAUSED_TOTAL_DURATION / 1000 # CHECKS SECONDS (NOT GAME TICKS)
        for item in self.items:
            
            if 'heal_when_low' in item.bonus_type:
                heal_mult = item.info['heal_when_low']
                if self.health <= self.max_health * 0.1 and current_time - item.last_used >= item.cooldown:
                    heal_amount = self.strength * heal_mult
                    self.take_heal(heal_amount)
                    item.last_used = current_time

                    if item.attack_frames:
                        from heroes import Attack_Display
                        attack_display.add(Attack_Display(
                            x=self.rect.centerx, y=self.rect.centery,
                            frames=item.attack_frames,
                            frame_duration=item.attack_frame_duration,
                            repeat_animation=item.attack_repeat,
                            dmg=0, final_dmg=0,
                            who_attacks=self, who_attacked=self.enemy,
                            speed=0, moving=False, heal=False,
                            continuous_dmg=False, per_end_dmg=(False, False),
                            disable_collide=True, stun=(False, 0),
                            sound=(False, None, None, None), kill_collide=False,
                            follow=(False, True), follow_self=True, follow_offset=(0,50)
                        ))

            if 'temp_hp_increase' in item.bonus_type:
                if current_time - item.last_used >= item.cooldown:
                    temp_hp_amount = item.info['temp_hp_increase']
                    self.take_temp_hp(temp_hp_amount)
                    item.last_used = current_time
                    
                    if item.attack_frames:
                        from heroes import Attack_Display
                        attack_display.add(Attack_Display(
                            x=self.rect.centerx, y=self.rect.centery,
                            frames=item.attack_frames,
                            frame_duration=item.attack_frame_duration,
                            repeat_animation=item.attack_repeat,
                            dmg=0, final_dmg=0,
                            who_attacks=self, who_attacked=self.enemy,
                            speed=0, moving=False, heal=False,
                            continuous_dmg=False, per_end_dmg=(False, False),
                            disable_collide=True, stun=(False, 0),
                            sound=(False, None, None, None), kill_collide=False,
                            follow=(False, True), follow_self=True, follow_offset=(0,30)
                        ))

            if 'temp_hp_increase' in item.bonus_type:
                if current_time - item.last_used >= item.cooldown:
                    temp_hp_amount = item.info['temp_hp_increase']
                    self.take_temp_hp(temp_hp_amount)
                    item.last_used = current_time
                    
                    if item.attack_frames:
                        from heroes import Attack_Display
                        attack_display.add(Attack_Display(
                            x=self.rect.centerx, y=self.rect.centery,
                            frames=item.attack_frames,
                            frame_duration=item.attack_frame_duration,
                            repeat_animation=item.attack_repeat,
                            dmg=0, final_dmg=0,
                            who_attacks=self, who_attacked=self.enemy,
                            speed=0, moving=False, heal=False,
                            continuous_dmg=False, per_end_dmg=(False, False),
                            disable_collide=True, stun=(False, 0),
                            sound=(False, None, None, None), kill_collide=False,
                            follow=(False, True), follow_self=True, follow_offset=(0,30)
                        ))

            if 'spawn_flame' in item.bonus_type:
                if current_time - item.last_used >= item.cooldown:
                    item.last_used = current_time
                    
                    if item.attack_frames:
                        from heroes import Attack_Display
                        for x in [-150, -50, 50, 150]:
                            attack_display.add(Attack_Display(
                                x=self.rect.centerx + x, y=DEFAULT_Y_POS - 28,
                                frames=item.attack_frames,
                                frame_duration=item.attack_frame_duration,
                                repeat_animation=item.attack_repeat,
                                dmg=10/FPS, final_dmg=0,
                                who_attacks=self, who_attacked=self.enemy,
                                speed=0, moving=False, heal=False,
                                continuous_dmg=False, per_end_dmg=(False, False),
                                disable_collide=False, stun=(False, 0),
                                sound=(False, None, None, None), kill_collide=False,
                                follow=(False, False), follow_self=False, follow_offset=(0,0),
                                hitbox_scale_x=0.3, hitbox_scale_y=0.6
                            ))

        if self.immortality_activated and current_time_ticks >= self.immortality_duration:
            self.immortality_activated = False

        # print(current_time_ticks, self.immortality_duration, self.immortality_activated)

    # Phased out code (since I don't use super.init)
    def update(self):
        """Base player update: handles universal effects."""
        self.draw_movement_status(screen)
        if not self.is_dead():
            self.draw_health_bar(screen) if global_vars.SHOW_MINI_HEALTH_BAR else None
            self.draw_mana_bar(screen) if global_vars.SHOW_MINI_MANA_BAR else None
            self.draw_special_bar(screen) if global_vars.SHOW_MINI_SPECIAL_BAR else None

            # -----------------------------------------------------------------------------------------------------
            self.item_activation(self.rect)
            # -----------------------------------------------------------------------------------------------------

            # Draws hero skills in game
            if global_vars.SINGLE_MODE_ACTIVE and self.player_type == 2 and not global_vars.show_bot_skills:
                pass
            else:
                if not self.special_active:
                    for attack in self.attacks:
                        attack.draw_skill_icon(screen, self.mana, self.special, self.player_type, player=self)
                else:
                    for attack in self.attacks_special:
                        attack.draw_skill_icon(screen, self.mana, self.special, self.player_type, player=self)

                if not self.special_active:
                    for mana in self.attacks:
                        mana.draw_mana_cost(screen, self.mana)
                else:
                    for mana in self.attacks_special:
                        mana.draw_mana_cost(screen, self.mana)

            
            self.handle_speed() # thit shii finally worked! (coder: kimhietee)

            if getattr(self, "hitbox_removed", False):
                # Restore previous hitbox size
                self.hitbox_rect.size = self.prev_hitbox_size
                self.hitbox_removed = False

        elif self.is_dead():
            if not getattr(self, "hitbox_removed", False):
                # Capture previous hitbox size
                self.prev_hitbox_size = self.hitbox_rect.size
                self.hitbox_rect.size = (0, 0)
                self.hitbox_removed = True


            # if being alived, 
            if not self.is_dead() and getattr(self, "hitbox_removed", True):
                self.hitbox_rect.size = self.prev_hitbox_size
                self.hitbox_removed = False


        # This part updated the code anyways if player is dead or not
        # -----------------------------------------------------------
        # Updates display damage/mana
        self.detect_and_display_damage()
        self.detect_and_display_mana()
        self.update_damage_numbers(screen)
        # print(self.basic_attack_animation_speed)

        if global_vars.SINGLE_MODE_ACTIVE and self.player_type == 2 and not global_vars.show_bot_stats:
            pass
        else:
            # Update the player status (health and mana bars)
            self.player_status(self.health, self.mana, self.special)

        self.update_hitbox()

        # update neccesities
        if global_vars.DRAW_DISTANCE:
            self.draw_distance(self.enemy)
        if global_vars.SHOW_HITBOX:
            
            self.draw_hitbox(screen)

        
        # -----------------------------
        # Stop at the ground level
        if self.y_pos > DEFAULT_Y_POS:
            self.y_pos = DEFAULT_Y_POS
            self.y_velocity = 0
            self.jumping = False 
        if self.y_pos > DEFAULT_Y_POS - JUMP_LOGIC_EXECUTE_ANIMATION:
            self.player_jump_index = 0
            self.player_jump_index_flipped = 0  
        self.inputs()
        self.move_to_screen()  



        self.calculate_effective_as()
        self.calculate_basic_attack_interval()







        # print(self.health_regen*60)
        # print(self.mana_regen*60)
        # print(self.basic_attack_damage)
        # print('aaaaaaaaaaaaaaaaaaaaaaaaa')
        # -----------------------------
            # print(self.slowed, 'default:', self.default_speed)
            # print('current:', self.speed)

            # if hasattr(self, 'atk_hasted'):
            #     pass
            # print(self.enemy)
                # print(self.get_current_atk_speed)
                # print('jump pos:', self.get_jump_pos)
                # print(self.y_pos)
                # print('jump time:', pygame.time.get_ticks() - self.jump_attack_time)
                # print('jump done:', self.jump_done)
                
                #test delay
                # if self.attacking3:
                #     print('attack start')
                # print(pygame.time.get_ticks())
                # print(self.sp_mana_refund)
            # print(self.items)
            
            # if self.player_type == 1:
            #     print(self.enemy)
            # print(self.frozen, self.can_cast(), self.can_move())
                # print(self.silenced)

        # if dead, remove the hitbox (NOTE: when revived after death, hitbox still removed)
        
        # delete/remove/kill hero if died for too long
            # self.dead_timer = self.dead_timer or pygame.time.get_ticks()
            # if pygame.time.get_ticks() - self.dead_timer >= 2000000: # reset the game after 5s to remove bugs (intented for creeps only)
            #     self.kill()
            # else:
            #     self.dead_timer = None
                
        # if self.is_dead:
        #     return
        # Handle global effects like stun or freeze
        # if self.stunned or getattr(self, "frozen", False):
        #     return

        # pygame.draw.rect(screen, (255, 0, 0), self.rect)


