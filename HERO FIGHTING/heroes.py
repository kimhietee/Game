'''
step 1: copy hero

step 2: set unique values like animation frames, sound, constants,
        input position, frame duration, repeats on attacks using Attack_Display
(this step takes a while and confusing since you need to path images correctly)
                                                                            
step 3: on player selection function,
        create new value on the p1/p2_select lists using PlayerSelector class.
        Last image pathing, for the profile image 

step 4: i will try that now.
        I just did.

step 5: test if works...

step.. done
'''


'''
Based on what I remembered:

step 1: add to player selector
        for drawing and selection of the hero icon
'''



'''
Guide on making an attack:

sample code from wind 
ashin atk 4

attack = Attack_Display(
    x=hero1.x_pos if self.player_type == 1 else hero2.x_pos, # in front of him
    y=hero1.y_pos - 100 if self.player_type == 1 else hero2.y_pos - 100,
    frames=self.sp, #frames=self.real_sp,
    frame_duration=40,
    repeat_animation=4,
    speed=0 if self.facing_right else 0,
    dmg=WIND_HASHASHIN_REAL_SP_DAMAGE,
    who_attacks=self,
    who_attacked=hero1 if self.player_type == 2 else hero2,
    moving=False,
    heal=False,
    continuous_dmg=False,
    per_end_dmg=(False, True))

from fire knight atk2

attack = Attack_Display(
    x=self.rect.centerx + 130 if self.facing_right else self.rect.centerx - 130, # in front of him
    y=self.rect.centery + 30,
    frames=self.atk2,
    frame_duration=150,
    repeat_animation=1,
    speed=5 if self.facing_right else -5,
    dmg=FIRE_KNIGHT_ATK2_DAMAGE,
    who_attacks=self,
    who_attacked=hero1 if self.player_type == 2 else hero2,
    moving=False,
    heal=False,
    continuous_dmg=False,
    per_end_dmg=(False, False),
    disable_collide=False,
    stun=True)

    
x                 x pos for the attack
y                 y pos for the attack
frames            attack animation path
frame_duration    how long each frame in ms(millisecond)
repeat_animation  animate again
speed             if moving, set speed, else, nothing
dmg               damage amount (make sure if only hit dmg(projectile), or every frame(none, or if moving and continuous dmg), or specific(per_end_dmg))
who_attacks       self
who_attacked      enemy
moving            projectile
heal              heal self
continuous_dmg    damages every frame if moving is true, if collide
per_end_dmg       damages every specific repeat animation, guide below:
disable_collide   don't apply damage when attack rect collides enemy
stun              toggle jump for the enemy, making it stun (stun logic for me :))
sound             play sound when attack is done
kill_collide      kill enemy when attack rect collides with enemy

guide:
 0 = when the attack collides with the enemy, apply dmg
 1 = damages enemy anyway (collide or not, don't matter)

 
 nahh ignore these notes, this was my fixing arc that I'm losing my mind working on it,
 ain't touching it until bug again.
 (
current notice: 4/10/25, 8:30pm
YES it finally worked, if you set per_end_dmg[1] to true, deals damage every attack animation ends,
damage depends on repeat animation on how many time. if per_end_dmg[0] is true, damages enemy whether the attack collided or not,
but this still apply the damage every animation ends, it just don't require any collision.


 note: if you collide with the original rect, occur bug where colliding damages you(a lot)
 wrong fix: turn moving to true and speed to 0 (if you dont want to move)
 fix: i removed the collide sprite, idk whats going on now. I fix a lot, etc...
 update: I deleted it (IM MAD!)
 )
'''


# AS OF 4/23/25 (12:11 AM)
'''
Some player info:
Fire Wizard:
- 
+ 5% damage
SPECIAL
+ 10% move speed
+ 8 projectiles (skill 1) 16.7% damage each attack - 83% damage (skill 1)
+ 5 explosions (skill 4) 33% damage each attack - 67% damage (skill 4)
+ 11 fires (skill 2) - 50% damage
+ 3 times repeats (skill 3) + moving - 20% damage

Wanderer Magician:
- 
+ 20% mana regeneration
+ atk2 heal
+ ranged basic attack
+ 300% damage atk1 (random damage) [2.5, 2.5, 2.5, 5, 5, 5, 5, 5, 7.5, 10]
SPECIAL
+ 3 projectiles (skill 1) + 20% damage each attack
+ faster healing (skill 2) 2/ + heal
+ 10% move speed
+ 10% mana regeneration
+ 40 max mana
+ 250% damage/heal
- short range atk3 but + damage (25%)

Fire Knight:
- 20% move speed
- 5% jump boost
- 40 max mana
- +3% gravity
+ 20 max health
+ 20% health regeneration
+ atk2 long stun
SPECIAL
+ 10% move speed
+ 0 cd skill_1
+ 2 slashes (skill 1) 30% damage each attack + 40% mana cost reduction
+ 3 attacks (skill 2) 60% damage each attack   - 60% end damage (skill 2) 
+ fire tornado attack with stun + small amount dmg
+ 50% damage (skill 4)
+ 20% final damage (skill 4)
+ all skill BURN damage [# damage] (only 20% for skill 1) 
    (only 40% for skill 2) (50% for skill 4) (10% for basic attack)

Wind Hashashin:
- 10 max health
- 50 max mana
+ 20% move speed
+ 10% jump boost
+ -2% gravity
+ 15% mana cost reduction
+ atk3 short stun
SPECIAL
+ skill 1 8 attacks (75% damage each) jumping high
+ atk2 short stun
+ atk3 fire tornado + knockback and damage
+ 10% damage, multiple attacks (1st atk 57%, 2nd & 3rd atks 30%)

'''


# from global_vars import (
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

# import pygame
# import pygame.sprite
# import random
# from attack import Attacks, Attack_Display
# from sprite_loader import (SpriteSheet, SpriteSheet_Flipped, load_attack, load_attack_flipped)
# from player import Player
# from heroes import Fire_Wizard, Wanderer_Magician, Fire_Knight, Wind_Hashashin
# from gameloop import create_title
# from gameloop import menu
# from gameloop import menu_button


import pygame
import random
import time
import math
import copy
import pygame.sprite
from global_vars import (IMMEDIATE_RUN,
    width, height, icon, FPS, clock, screen, hero1, hero2, fire_wizard_icon, wanderer_magician_icon, fire_knight_icon, wind_hashashin_icon, water_princess_icon, forest_ranger_icon, yurei_icon, chthulu_icon, phantom_assassin_icon,
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
    attack_display, MULT, dmg_mult, item_page,

    ZERO_WIDTH, TOTAL_WIDTH, item_equip_hashmap
)

from sprite_loader import SpriteSheet, SpriteSheet_Flipped, load_attack, load_attack_flipped
from player import Player
from player import display_inputs
from button import ImageButton
from bot_ai import create_bot
import Animate_BG
import global_vars

import key
from path_helper import resource_path
import global_vars

# from chance import Chance

pygame.init()

pygame.display.set_icon(icon)
pygame.display.set_caption("HERO FIGHTING")

# botchance = Chance(0.3) # ticks every 0.3 seconds

# while True:
#     botchance.update(50)
#=-------------------
# Font Sizes
FONT = global_vars.get_font(30)

# Icons
#positions, formula : spec_pos/size, eg 50/720 = 0.0695
cstm_pos = 0.039 #width 50
cstm_pos2 = 0.222 #160
cstm_pos3 = 0.291 #210
hp_icon = pygame.transform.rotozoom(pygame.image.load(resource_path('assets/icons/health icon.png')).convert_alpha(), 0, 0.05)
mana_icon = pygame.transform.rotozoom(pygame.image.load(resource_path('assets/icons/mana icon.png')).convert_alpha(), 0, 0.065)
hp_icon_p1_rect = hp_icon.get_rect(center=(int(width*cstm_pos)+1, int(height*cstm_pos2)+1-20))
mana_icon_p1_rect = mana_icon.get_rect(center=(int(width*cstm_pos)+1, int(height*cstm_pos3)+1-20))
hp_icon_p2_rect = hp_icon.get_rect(center=(width - int(width*cstm_pos)-1, int(height*cstm_pos2)+1-20))
mana_icon_p2_rect = mana_icon.get_rect(center=(width - int(width*cstm_pos)-1, int(height*cstm_pos3)+1-20))




def draw_hp_mana_icons():
    screen.blit(hp_icon, hp_icon_p1_rect)
    screen.blit(hp_icon, hp_icon_p2_rect)
    screen.blit(mana_icon, mana_icon_p1_rect)
    screen.blit(mana_icon, mana_icon_p2_rect)


        # print(self.health)
        # self.regenerate_mana()



        
                        
                    

            # print(f"{self.who_attacked} took {self.dmg} damage! Current HP: {self.who_attacked.health}")



# Empty frame attack (singular image)
empty_frame = None
# empty_frame = [
#     pygame.transform.rotozoom(
#     pygame.image.load(r"assets\attacks\empty_frame.png").convert_alpha(),
#     angle=0, scale=2.0)
#     ]


class Attacks:
    '''
    Core skill class used by heroes, which is used by the hero skill inputs.
    
    Displays the skill on the UI and updates the current state of the skill.
    
    
    Contains skill image, mana_cost, cooldown, and hero's current mana.
    
    '''


    def __init__(self, mana_cost:int, skill_rect:pygame.Rect, skill_img:pygame.Surface, cooldown:int, mana:int='self.mana', damage:list=[0,0], special_skill=False,
                 skill_name='', skill_stats='', skill_desc='', mana_refund=1, hero=None):
        self.mana_cost = mana_cost
        self.skill_rect = skill_rect
        self.skill_img = skill_img
        self.cooldown = cooldown
        self.mana = mana  # Not used
        self.damage = damage[0] + damage[1] # total raw damage
        self.mana_refund = mana_refund # include display dynamic mana refund if the hero has this.
        self.hero = hero  # Store hero reference for dynamic values
        # Internally store raw last-used timestamp and a snapshot of paused-total at that moment
        self.last_used_time = -cooldown  # raw pygame.time.get_ticks() value when used
        self._last_used_paused_total = 0   # global_vars.PAUSED_TOTAL_DURATION snapshot at use
        
        self.atk_mana_cost = 0
        self.special_skill = special_skill

        # Dynamically scaled font sizes
        self.cooldown_font_size = int(height * 0.0416 *1.3)  # ~30 at 720p
        self.mana_font_size = int(height * 0.0208 *1.3)      # ~15 at 720p

        self.special_font_size = int(height * 0.0208 *1.3)

        # Offset for positioning mana text (scaled vertically)
        self.mana_y_offset = int(self.skill_rect.height * 0.35)      # ~50 at 720p
        
        self.special_y_offset = int(self.skill_rect.height * 0.35)

        self.button_icon = pygame.image.load(resource_path('assets/icons/button.png')).convert_alpha()

        self.hovered = False

        self.skill_count:int = -1
        self.skill_name:str = skill_name
        self.skill_stats:dict = skill_stats
        self.skill_desc:str = skill_desc

        self.remaining_ms = 0 # used to check the current cooldown (LAN)


    def reduce_cd(self, val=False):
        if val:
            # Reset cooldown: set last_used_time such that the attack is ready now
            self._last_used_time = -self.cooldown
            self._last_used_paused_total = 0
        return val
         

    @property
    def last_used_time(self):
        # expose raw stored timestamp for backward compatibility
        return self._last_used_time

    @last_used_time.setter
    def last_used_time(self, value):
        # whenever code sets last_used_time, capture the current paused-total snapshot
        self._last_used_time = value
        self._last_used_paused_total = global_vars.PAUSED_TOTAL_DURATION

    def time_since_use(self):
        """Return milliseconds elapsed since last use, excluding paused durations."""
        paused_total = global_vars.PAUSED_TOTAL_DURATION
        # Include the ongoing pause duration so the clock is fully frozen while paused.
        # Without this, PAUSED_TOTAL_DURATION doesn't update until unpause, causing
        # the cooldown to keep ticking down during pause and then jump back on resume.
        if global_vars.active_net_client is None: # Only apply pause logic for local player, not bots or remote clients
            if global_vars.PAUSED and global_vars.PAUSED_START is not None:
                paused_total += pygame.time.get_ticks() - global_vars.PAUSED_START

        effective_now = pygame.time.get_ticks() - paused_total
        effective_last = self.last_used_time - self._last_used_paused_total
        # print(effective_now - effective_last)
        return effective_now - effective_last

    def is_ready(self):
        return self.time_since_use() >= self.cooldown


    def get_skill_cooldown(self):
        '''get literal skill cd
        
        returns value like this example debug:
        
        skill 1 [6466]
        skill 2 [0]
        skill 3 [12541]
        skill 4 [0]
        skill 5 [584.19]
        skill 6 [0]'''
        return max(0, self.cooldown - self.time_since_use())
    
    # Is being called to game loop
    def draw_skill_icon(self, screen, mana, special=0, player_type=0, max_special=MAX_SPECIAL, player=None):
        # print("Has entered Heroes")
        # Check if player is silenced or frozen
        # For basic attacks: only frozen blocks them, silenced allows them
        # For skills: both frozen and silenced block them
        is_silenced = player and getattr(player, 'silenced', False)
        is_frozen = player and getattr(player, 'frozen', False)
        is_disabled_basic = is_frozen  # Basic attacks only blocked by freeze
        is_disabled_skill = is_frozen or is_silenced  # Skills blocked by both freeze and silence
        
        # Check if this is a basic attack by comparing with basic_icon_rect
        self.is_basic_attack = False
        if player_type == 1:
            self.is_basic_attack = self.skill_rect == hero1.basic_icon_rect
        elif player_type == 2:
            self.is_basic_attack = self.skill_rect == hero2.basic_icon_rect
        
        # Determine the key to display based on the player type
        keybinds=key.read_settings()
        key_text = ""
        if player_type == 1:
            key_text = display_inputs(keybinds['skill_1_p1'][1]) if self.skill_rect == hero1.skill_1_rect else \
                    display_inputs(keybinds['skill_2_p1'][1]) if self.skill_rect == hero1.skill_2_rect else \
                    display_inputs(keybinds['skill_3_p1'][1]) if self.skill_rect == hero1.skill_3_rect else \
                    display_inputs(keybinds['skill_4_p1'][1]) if self.skill_rect == hero1.skill_4_rect else \
                    display_inputs(keybinds['basic_atk_p1'][1]) if self.skill_rect == hero1.basic_icon_rect else \
                    display_inputs(keybinds['sp_skill_p1'][1]) if self.skill_rect == hero1.special_rect else ""
        elif player_type == 2:
            key_text = display_inputs(keybinds['skill_1_p2'][1]) if self.skill_rect == hero2.skill_1_rect else \
                    display_inputs(keybinds['skill_2_p2'][1]) if self.skill_rect == hero2.skill_2_rect else \
                    display_inputs(keybinds['skill_3_p2'][1]) if self.skill_rect == hero2.skill_3_rect else \
                    display_inputs(keybinds['skill_4_p2'][1]) if self.skill_rect == hero2.skill_4_rect else \
                    display_inputs(keybinds['basic_atk_p2'][1]) if self.skill_rect == hero2.basic_icon_rect else \
                    display_inputs(keybinds['sp_skill_p2'][1]) if self.skill_rect == hero2.special_rect else ""

        # Existing logic for drawing the skill icon
        if not self.special_skill:
            # Determine if this skill icon is disabled (for basic attacks: only if frozen, for skills: if frozen or silenced)
            current_is_disabled = is_disabled_basic if self.is_basic_attack else is_disabled_skill
            
            if current_is_disabled:
                # If disabled, show darkened icon with red X (but only for skills, not basic attacks when just silenced)
                dark_overlay = pygame.Surface(self.skill_rect.size)
                dark_overlay.fill((0, 0, 0))
                dark_overlay.set_alpha(150)
                screen.blit(self.skill_img, self.skill_rect)
                screen.blit(dark_overlay, self.skill_rect)
                
                # Draw red X to indicate skill is disabled (only for skills, not for basic attacks when just silenced)
                if not (self.is_basic_attack and is_silenced and not is_frozen):  # Allow basic when just silenced
                    x_font = global_vars.get_font(self.cooldown_font_size)
                    x_text = x_font.render('X', global_vars.TEXT_ANTI_ALIASING, (255, 0, 0))
                    screen.blit(x_text, (
                        self.skill_rect.centerx - x_text.get_width() // 2,
                        self.skill_rect.centery - x_text.get_height() // 2
                    ))
            elif not self.is_ready():
                dark_overlay = pygame.Surface(self.skill_rect.size)
                dark_overlay.fill((0, 0, 0))
                dark_overlay.set_alpha(128)
                screen.blit(self.skill_img, self.skill_rect)
                screen.blit(dark_overlay, self.skill_rect)

                # Draw scaled cooldown text
                font = global_vars.get_font(self.cooldown_font_size * (1 if not self.is_basic_attack else 0.8))
                # Use time_since_use() so display matches actual cooldown logic and accounts for pauses
                self.remaining_ms = self.get_skill_cooldown()
                cooldown_time = f'{max(0, self.remaining_ms / 1000):.1f}' if self.is_basic_attack else  max(0, self.remaining_ms // 1000)
                cooldown_text = font.render(str(cooldown_time), global_vars.TEXT_ANTI_ALIASING, 'Red')
                screen.blit(cooldown_text, (
                    self.skill_rect.centerx - cooldown_text.get_width() // 2,
                    self.skill_rect.centery - cooldown_text.get_height() // 2
                ))

            elif mana < self.mana_cost:
                dark_overlay = pygame.Surface(self.skill_rect.size)
                dark_overlay.fill((0, 0, 0))
                dark_overlay.set_alpha(128)
                screen.blit(self.skill_img, self.skill_rect)
                screen.blit(dark_overlay, self.skill_rect)

                # Mana cost when not enough mana
                mana_font = global_vars.get_font(self.mana_font_size)
                self.atk_mana_cost = mana_font.render(f'[{self.mana_cost}]', global_vars.TEXT_ANTI_ALIASING, 'Red')
                screen.blit(self.atk_mana_cost, (
                    self.skill_rect.centerx - self.atk_mana_cost.get_width() // 2,
                    self.skill_rect.top - self.mana_y_offset
                ))
            else:
                screen.blit(self.skill_img, self.skill_rect)

        else:
            # Special skills are always blocked by silence (can't use sp skills when silenced)
            current_is_disabled = is_disabled_skill
            
            if current_is_disabled:
                # If silenced/frozen, show darkened icon with red X for special skill
                dark_overlay = pygame.Surface(self.skill_rect.size)
                dark_overlay.fill((0, 0, 0))
                dark_overlay.set_alpha(150)
                screen.blit(self.skill_img, self.skill_rect)
                screen.blit(dark_overlay, self.skill_rect)
                
                # Draw red X
                x_font = global_vars.get_font(self.special_font_size)
                x_text = x_font.render('X', global_vars.TEXT_ANTI_ALIASING, (255, 0, 0))
                screen.blit(x_text, (
                    self.skill_rect.centerx - x_text.get_width() // 2,
                    self.skill_rect.centery - x_text.get_height() // 2
                ))
            elif not special >= max_special:
                dark_overlay = pygame.Surface(self.skill_rect.size)
                dark_overlay.fill((0, 0, 0))
                dark_overlay.set_alpha(128)
                screen.blit(self.skill_img, self.skill_rect)
                screen.blit(dark_overlay, self.skill_rect)

                special_font = global_vars.get_font(self.special_font_size)
                self.atk_special_cost = special_font.render(f'[{max_special}]', global_vars.TEXT_ANTI_ALIASING, 'azure3')
                screen.blit(self.atk_special_cost, (
                    self.skill_rect.centerx - self.atk_special_cost.get_width() // 2,
                    self.skill_rect.top - self.special_y_offset
                ))
            else:
                special_font = global_vars.get_font(self.special_font_size)
                self.atk_special_cost = special_font.render(f'[{max_special}]', global_vars.TEXT_ANTI_ALIASING, 'yellow')
                screen.blit(self.atk_special_cost, (
                    self.skill_rect.centerx - self.atk_special_cost.get_width() // 2,
                    self.skill_rect.top - self.special_y_offset
                ))
                screen.blit(self.skill_img, self.skill_rect)

        # Draw the key text below the skill icon
        key_font = global_vars.get_font(self.mana_font_size)
        button_icon = pygame.transform.scale(self.button_icon, (90, 70))
        # button_icon_rect = button_icon.get_rect(topleft=(key_pos_x - 10, key_pos_y - 5))

        key_text_render = key_font.render(key_text, True, 'azure3')
        
        screen.blit(button_icon, (
            self.skill_rect.centerx - 45,
            self.skill_rect.bottom - 20  # Position below the skill icon
        ))
        # print(key_font.size(key_text)[0])
        screen.blit(key_text_render, (
            self.skill_rect.centerx - key_text_render.get_width() // 2,
            self.skill_rect.bottom + 5  # Position below the skill icon
        ))

    def draw_mana_cost(self, screen, mana):
        if not self.special_skill:
            mana_font = global_vars.get_font(self.mana_font_size)
            color = 'Cyan2' if mana >= self.mana_cost else 'Red'
            self.atk_mana_cost = mana_font.render(f'[{self.mana_cost}]', global_vars.TEXT_ANTI_ALIASING, color)

            screen.blit(self.atk_mana_cost, (
                self.skill_rect.centerx - self.atk_mana_cost.get_width() // 2,
                self.skill_rect.top - self.mana_y_offset
            ))

    def set_skill_count(self, n):
        self.skill_count = n

    def update_stat_info(self):
        '''updates the latest mana cost and cooldown.
        
        if damage is set to 0, auto calculate damage.'''
        if type(self.skill_stats) == dict:
            for name, value in self.skill_stats.items():
                if name == 'Damage':
                    if type(self.skill_stats['Damage']) == list:
                        self.skill_stats['Damage'][0] = round(self.damage, 2)
                elif name == 'Heal':
                    if type(self.skill_stats['Heal']) == list:
                        self.skill_stats['Heal'][0] = round(self.damage, 2)
                elif name == 'Mana as Damage':
                    if type(self.skill_stats['Mana as Damage']) == list:
                        if type(self.skill_stats['Mana as Damage'][0]) == str:
                            break
                        self.skill_stats['Mana as Damage'][0] = round(self.damage * self.mana_refund, 2)

                    # else: # for basic attack damage, don't use list (im confused)
                    #     if self.hero is not None:
                    #         self.skill_stats['Damage'] = [self.hero.basic_attack_damage+123, 'red']
        
            # by default
            self.skill_stats['Mana Cost'] = [self.mana_cost, 'cyan']
            self.skill_stats['Cooldown'] = [f'{self.cooldown / 1000:.1f}s', 'white']

    def display_info(self, screen, mouse_pos):
        if self.skill_rect.collidepoint(mouse_pos):
            self.hovered = True
        else:
            self.hovered = False

        # text = [
        #     self.skill_name,
        #     self.skill_stats,
        #     self.skill_desc
        # ]

        self.update_stat_info()

        if self.hovered:
            from button import DisplaySkillInfo
            self.info_bubble = DisplaySkillInfo(
                image_path=text_box_img,
                pos=mouse_pos,  # Will be updated based on skill icon position
                skill_name=self.skill_name,
                skill_icon_path=self.skill_img,
                stats=self.skill_stats,
                info_text=self.skill_desc,
                font_path=global_vars.FONT_PATH,
                font_size=font_size * 1.2,
                anchor='midbottom'
            )
            # info_bubble = ImageBro(
            #         image_path=text_box_img,
            #         pos=mouse_pos,
            #         text=text,
            #         font_path=global_vars.FONT_PATH,
            #         font_size=font_size * 1.05,
            #         text_color='green',
            #         player_info=True,
            #         text_scale=1.3,  # Full size
            #         anchor='midbottom'
            #     )
                
            # info_bubble.drawing_info(screen)

    def update(self, screen, mana, special=0, player_type=0, player=None, skill_name='', skill_desc='', mouse_pos=None):
        self.draw_skill_icon(screen, mana, special, player_type, player=player)
        self.draw_mana_cost(screen, mana)
        # self.display_info(screen, mouse_pos, self.skill_count)

class Attack_Display(pygame.sprite.Sprite): #The Attack_Display class should handle the visual representation and animation of an attack. Here's the corrected version:
   
    """
        This class represents the attack display and its properties.
        It contains the attack's animation frames, duration, and other attributes.
        It also handles the attack's position and movement.

        Attack_Display Class Parameter Descriptions:

        1. x (int): 
        - The initial horizontal position (x-coordinate) of the attack on the screen.

        2. y (int): 
        - The initial vertical position (y-coordinate) of the attack on the screen.

        3. frames (list of Surface): 
        - A list of images (frames) that represent the attack's animation.

        4. frame_duration (int): 
        - Duration in milliseconds each frame is displayed before switching to the next one.

        5. repeat_animation (int): 
        - Number of times the animation should loop. After the final loop, the attack ends.

        6. speed (int): 
        - Horizontal movement speed of the attack. If zero, the attack is stationary.

        7. dmg (int): 
        - The amount of damage dealt per hit or frame, depending on other flags.

        8. final_dmg (int): 
        - Damage that is applied at the end of the animation (used for finishers or strong final hits).

        9. who_attacks (object): 
        - The entity (e.g. player or enemy) initiating the attack.

        10. who_attacked (object): 
            - The target of the attack, to receive damage or effects.

        11. moving (bool): 
            - If True, the attack moves horizontally according to 'speed'. If False, it's static.

        12. heal (bool): 
            - If True, instead of dealing damage, the attack heals the one who cast it.

        13. continuous_dmg (bool): 
            - If True, the attack deals damage continuously every frame while colliding with the target.

        14. per_end_dmg (tuple(bool, bool)): 
            - Two boolean flags:
                * [0] – Enables damage to occur at the end of each animation cycle.
                * [1] – Applies damage when animation ends, regardless of collision. (1 set of damage)

        15. disable_collide (bool): 
            - If True, the attack does not deal damage upon direct collision.

        16. stun (tuple(bool, int)): 
            - A tuple that enables stun and defines its duration:
                * [0] – Enables/disables stun logic.
                * [1] – Stun duration or intensity (custom logic may vary).

        17. sound (tuple(bool, Sound, Sound, Sound)): 
            - A tuple that defines if sound plays and includes up to 3 sound objects:
                * [0] – Enables/disables sound playback.
                * [1-3] – Sound effects to play when animation ends.

        18. kill_collide (bool): 
            - If True, the attack sprite disappears instantly upon colliding with the target.

        19. follow (tuple(bool, bool)):
            - Controls if the attack should follow another sprite:
                * [0] – If True, the attack will stick to the enemy upon collision and follow them.
                * [1] – If True, the attack always follows the enemy, even without collision.
                
        19.1 follow_self (bool):
            - Make the follow logic for self

        19.2 follow_offset (tuple(int,int)):
            - Position of the follow in x and y (positive/negative values)

        20. delay (tuple(bool, int)):
            - Delays the attack’s animation and effect:
                * [0] – If True, delay is enabled.
                * [1] – Time in milliseconds to wait before the attack becomes active (e.g. (True, 1000) delays by 1 second).

        UPDATE

        21. stop_movement (bool, int, int)
            - Prevents enemy from moving (and using skills)
                * [0] – If True, activates status.
                * [1] – Status
                    1 - Freeze
                    2 - Root
                    3 - Slow
                    4 - Silence
                * [2] – Status mode/type
                    1 - While collides player, effect active, else none (collision only)
                    2 - When collides player, effect active, until attack ends (if hit once)
                    3 - Effect active, until attack ends (full duration)
                * [3] – Slow Rate
                    < 1.0 (ex. 0.8 for 20% slow)
                    - Only if Status is slow

        ? damage_mode - no use for now
        '''
        """

    def __init__(self, x, y, frames:pygame.Surface=list, frame_duration=100, repeat_animation=1, dmg=0, final_dmg=0, who_attacks:object=None, who_attacked:object=None,
                speed=0,  
                moving=False, 
                heal=False,
                continuous_dmg=False, 
                per_end_dmg=(False, False),
                disable_collide=False, 
                stun=(False, 0),
                sound=(False, None, None, None), 
                kill_collide=False,
                follow=(False, False), delay=(False, 0), follow_offset=(0, 0), repeat_sound=False, follow_self=False, use_live_position_on_delay=False,
                hitbox_scale_x=0.6, hitbox_scale_y=0.6,
                hitbox_offset_x=0, hitbox_offset_y=0, heal_enemy=False, self_kill_collide=False, self_moving=False,
                consume_mana=[False, 0],
                stop_movement=(False, 0, 0, 1.0),
                spawn_attack:dict=None, periodic_spawn:dict=None,
                add_mana=False, add_mana_to_enemy=False, mana_mult=1,
                reduce_mana=0,
                damage_mode='single'#no use for now
                ,is_basic_attack=False#used to identify basic attacks for crit
                ):
        super().__init__()
        self.x = x
        self.y = y
        self.frames = frames
        self.frame_duration = frame_duration
        self.repeat_animation = repeat_animation
        self.speed = speed
        self.dmg = dmg
        self.final_dmg = final_dmg
        self.who_attacks = who_attacks
        # print(who_attacked, type(who_attacked))
        # Always store as a list to handle multiple enemies
        if type(who_attacked) == list:
            self.who_attacked = who_attacked.copy()  # Make a copy to avoid modifying the original list
        else:
            self.who_attacked = [who_attacked] if who_attacked is not None else []
        
        # Track collision and damage state per enemy
        # Dictionary: enemy -> {'colliding': bool, 'damaged': bool, 'following': bool}
        self.enemy_states = {}
        for enemy in self.who_attacked:
            if enemy is not None:
                self.enemy_states[enemy] = {
                    'colliding': False,
                    'damaged': False,
                    'following': False
                }
        # Track which enemies this attack actually affected (for symmetric removal)
        self.affected_enemies = set()
        self.moving = moving
        self.heal = heal
        self.continuous_dmg = continuous_dmg
        self.per_end_dmg = per_end_dmg
        self.disable_collide = disable_collide
        self.stun = stun
        self.sound = sound
        self.kill_collide = kill_collide
        self.follow = follow
        self.delay = delay
        self.follow_offset = follow_offset
        self.repeat_sound = repeat_sound
        self.follow_self = follow_self
        self.use_live_position_on_delay = use_live_position_on_delay
        self.heal_enemy = heal_enemy
        self.self_kill_collide = self_kill_collide
        self.self_moving = self_moving # applies some logic to moving to self
        self.consume_mana = consume_mana # [0] = bool, [1] = how much mana (still same as how dmg is applied)
        if len(stop_movement) == 4:
            self.stop_movement = stop_movement
        else: #just in case if the status is not slow
            self.stop_movement = list(stop_movement)
            self.stop_movement.insert(4, 1.0)
        

        self.spawn_attack = spawn_attack # dict or callable
        self.periodic_spawn = periodic_spawn # dict or None

        self.add_mana = add_mana
        self.add_mana_to_enemy = add_mana_to_enemy
        self.mana_mult = mana_mult
        self.is_basic_attack = is_basic_attack

        self.reduce_mana = reduce_mana

        self.frame_index = 0
        self.last_update_time = pygame.time.get_ticks()

        if not delay[0]:
            self.image = self.frames[self.frame_index]
        else:
            self.image = pygame.Surface((1, 1), pygame.SRCALPHA)  # Invisible placeholder
        
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_done = False

        self.current_repeat = 0

        # some logic flags
        self.damaged = False
        self.damaged_detect = self.damaged

        self.following_target = False  # set to True when collided if follow[0] is true
        

        self.delay_start_time = pygame.time.get_ticks()
        self.delay_triggered = False

        self.hitbox_offset_x = hitbox_offset_x
        self.hitbox_offset_y = hitbox_offset_y

        self.hitbox_scale_x = hitbox_scale_x
        self.hitbox_scale_y = hitbox_scale_y

        self.hitbox_width = int(self.rect.width * hitbox_scale_x)
        self.hitbox_height = int(self.rect.height * hitbox_scale_y)


        self.hitbox_rect = pygame.Rect(self.x, self.y, self.hitbox_width, self.hitbox_height)
        
        #spawn attack
        self._has_spawned_on_collide = False
        self._last_periodic_spawn = pygame.time.get_ticks()
        self._periodic_spawn_count = 0





    def update_hitbox(self):
        self.hitbox_rect.center = self.rect.center
        # self.hitbox_rect.x = self.rect.x - self.hitbox_offset_x
        # self.hitbox_rect.y = self.rect.y + self.hitbox_offset_y


    def draw_hitbox(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox_rect, 2)  # Red outline for debugging
        # print("Hitbox drawn")
        # print(self.rect.width)

    def kill_self(self): # Remove attack and cleanup status effects
        # remove only this attack's status from all affected enemies
        if self.stop_movement[0]:
            status_type = self.stop_movement[1]
            # iterate the set of enemies this attack applied the status to
            for enemy in list(getattr(self, 'affected_enemies', set())):
                if enemy is None:
                    continue
                try:
                    enemy.remove_movement_status(status_type, source=self)
                except Exception:
                    pass  # Enemy might have already been removed
            # clear the set to avoid double removal
            try:
                self.affected_enemies.clear()
            except Exception:
                pass
        # finally kill the sprite
        self.kill()

    def _apply_damage(self, enemy, damage_amount, is_final=False):
        """Helper method to apply damage with all effects (mana, special, lifesteal) to a specific enemy."""
        # Host-authority: in LAN mode only Player 1 (host) computes and applies
        # combat effects (including RNG crits). Player 2 receives the authoritative
        # results via state snapshots, so it must not run damage logic itself.
        if global_vars.active_net_client is not None and global_vars.active_net_client.my_player_type == 2:
            return
        if enemy is None:
            return
        
        # Apply crit for basic attacks only
        if self.is_basic_attack:
            if hasattr(self.who_attacks, 'crit_chance') and hasattr(self.who_attacks, 'crit_damage'):
                crit_roll = random.random()
                if crit_roll < self.who_attacks.crit_chance:
                    damage_amount += damage_amount * self.who_attacks.crit_damage


            if damage_amount > 0: # bug fix: only burn if damage > 0
                if self.who_attacks.mana_burn_flat[0] > 0: # burns mana at provided amount 
                        enemy.take_mana_burn(enemy, self.who_attacks.mana_burn_flat[0], self.who_attacks.mana_burn_flat[1])
                
                if self.who_attacks.mana_burn_per[0] > 0: # burns mana based on percentage of damage dealt (ex. dmg 5 -> 50% - 2.5 burn mana)
                    enemy.take_mana_burn(enemy, damage_amount * self.who_attacks.mana_burn_per[0], self.who_attacks.mana_burn_per[1])
        
            if self.who_attacks.lifesteal > 0 and not self.who_attacks.is_dead():
                lifesteal_amount = damage_amount * self.who_attacks.lifesteal
                self.who_attacks.take_heal(abs(lifesteal_amount))

            elif self.who_attacks.lifesteal < 0 and not self.who_attacks.is_dead():
                # damages the attacker if lifesteal is less than 0
                lifesteal_amount = damage_amount * self.who_attacks.lifesteal
                self.who_attacks.take_damage(abs(lifesteal_amount))
                
        enemy.take_damage(
            damage_amount,
            add_mana_to_self=True if self.add_mana else False,
            enemy=self.who_attacks,
            add_mana_to_enemy=self.add_mana_to_enemy,
            mana_multiplier=self.mana_mult
        )
        self.who_attacks.take_special(damage_amount * SPECIAL_MULTIPLIER)
        # damages self 
        if self.who_attacks.health_cost > 0 and not self.who_attacks.is_dead():
            # damages the attacker if lifesteal is less than 0
            health_cost_amount = damage_amount * self.who_attacks.health_cost
            self.who_attacks.take_damage(abs(health_cost_amount))

        # spell lifesteal, health attacker only spells
        if self.who_attacks.spell_lifesteal > 0 and not self.who_attacks.is_dead():
            spell_lifesteal_amount = damage_amount * self.who_attacks.spell_lifesteal
            self.who_attacks.take_heal(abs(spell_lifesteal_amount))
        
        
    def _apply_heal(self, heal_amount):
        """Helper method to apply healing with special gain."""
        # Host-authority: only the host applies heals; P2 mirrors via snapshots.
        if global_vars.active_net_client is not None and global_vars.active_net_client.my_player_type == 2:
            return
        self.who_attacks.take_heal(heal_amount)
        self.who_attacks.take_special(heal_amount * SPECIAL_MULTIPLIER)
    
    def _check_and_set_follow(self, enemy):
        """Helper method to check and set following_target flag for a specific enemy."""
        if enemy is None:
            return
        if enemy not in self.enemy_states:
            return
        if self.follow[0] and not self.enemy_states[enemy]['following']:
            self.enemy_states[enemy]['following'] = True
    
    def _check_collision(self, enemy):
        """Check if attack collides with a specific enemy. Returns True if colliding."""
        if enemy is None or enemy not in self.enemy_states:
            return False
        return self.hitbox_rect.colliderect(enemy.hitbox_rect)
    
    def _get_colliding_enemies(self):
        """Get all enemies that are currently colliding with the attack."""
        colliding = []
        for enemy in self.who_attacked:
            if enemy is not None and self._check_collision(enemy):
                colliding.append(enemy)
                # Update collision state
                if enemy in self.enemy_states:
                    self.enemy_states[enemy]['colliding'] = True
            elif enemy is not None and enemy in self.enemy_states:
                # Enemy is no longer colliding
                self.enemy_states[enemy]['colliding'] = False
        return colliding

    def update(self):
        if global_vars.SHOW_HITBOX:
            
            self.draw_hitbox(screen)
        self.update_hitbox()
        
        '''
        Update the attack display's position and animation.
        This method is called every frame to update the attack display's state.
        It handles the animation frames, movement, and collision detection.
        It also plays the attack sound if specified.
        The method checks for collisions with the target and applies damage if necessary.
        The method also handles the stun effect if specified.
        The method is designed to be used with Pygame and integrates with the Pygame sprite system.
        The method is called by the main game loop to update the attack display's state.
        '''
        # print(self.following_target)
        # print(self.detect_collision())
        """Update the attack animation and position."""
        current_time = pygame.time.get_ticks()

        #delay logic
        if self.delay[0] and not self.delay_triggered:
            if current_time - self.delay_start_time < self.delay[1]:
                return
            else:
                if self.use_live_position_on_delay:
                    self.x = self.who_attacks.x_pos + self.follow_offset[0]
                    self.y = self.who_attacks.y_pos + self.follow_offset[1]

                self.image = self.frames[self.frame_index]
                self.rect = self.image.get_rect(center=(self.x - self.hitbox_offset_x, self.y + self.hitbox_offset_y))

                self.hitbox_width = int(self.rect.width * self.hitbox_scale_x)
                self.hitbox_height = int(self.rect.height * self.hitbox_scale_y)
                self.hitbox_rect = pygame.Rect(self.x, self.y, self.hitbox_width, self.hitbox_height)

                if self.sound[0] == True and not self.repeat_sound:
                    if self.sound[1] != None:
                        self.sound[1].play()
                    if self.sound[2] != None:
                        self.sound[2].play()
                    if self.sound[3] != None:
                        self.sound[3].play()

                self.delay_triggered = True

        elif not self.delay[0] and not self.delay_triggered:
            if self.sound[0] == True and not self.repeat_sound:
                if self.sound[1] != None:
                    self.sound[1].play()
                if self.sound[2] != None:
                    self.sound[2].play()
                if self.sound[3] != None:
                    self.sound[3].play()

            self.delay_triggered = True

        # Get all currently colliding enemies
        colliding_enemies = self._get_colliding_enemies()
        has_collision = len(colliding_enemies) > 0

        if self.delay_triggered:
            # MAIN LOGIC 1
            # Every frame tick (uses current fps)
            
            # Must at be the top (bug)
            # Spawn attack when collide
            # 'use_attack_onhit_pos': bool, spawns attack when enemy collides with the attack
            if has_collision and self.spawn_attack and not self._has_spawned_on_collide:
                spec = self.spawn_attack
                if callable(spec):
                    new = spec(self)
                    if new:
                        attack_display.add(new)
                else:
                    ak = spec.get('attack_kwargs', {}).copy()
                    # pick the first actual colliding enemy (the one that triggered the spawn)
                    collided_enemy = colliding_enemies[0] if len(colliding_enemies) > 0 else None
                    if spec.get('use_attack_onhit_pos', True):
                        ak['x'], ak['y'] = self.rect.center
                    # If we have an actual collided enemy, ensure the spawned attack targets that enemy
                    if collided_enemy is not None:
                        try:
                            # ensure who_attacked is set to the collided enemy (Attack_Display accepts single or list)
                            ak['who_attacked'] = collided_enemy
                        except Exception:
                            pass
                        # If follow_offset exists, avoid picking a large random positive vertical offset
                        # which can push the spawned attack below ground. Respect the provided offset
                        # but clamp it relative to the target hitbox size.
                        fo = ak.get('follow_offset', None)
                        if fo and isinstance(fo, (tuple, list)) and len(fo) >= 2:
                            try:
                                fx, fy = fo[0], fo[1]
                                max_h = max(1, collided_enemy.hitbox_rect.height)
                                # Limit the vertical offset to half the target hitbox height in magnitude
                                limit = max_h // 2
                                if abs(fy) > limit:
                                    fy = limit if fy > 0 else -limit
                                ak['follow_offset'] = (fx, fy)
                            except Exception:
                                pass
                    attack_display.add(Attack_Display(**ak))
                self._has_spawned_on_collide = True

            # Spawns attack periodically
            # 'interval': int, spaws attack between intervals
            # 'repeat_count': int, total attack(s) to spawn
            # 'use_attack_pos': bool, uses current pos of attack and spawns attack every interval
            if self.periodic_spawn:
                now = pygame.time.get_ticks()
                interval = self.periodic_spawn.get('interval', 2000)
                max_times = self.periodic_spawn.get('repeat_count', None)
                if now - self._last_periodic_spawn >= interval:
                    ak = self.periodic_spawn.get('attack_kwargs', {}).copy()
                    if self.periodic_spawn.get('use_attack_pos', False):
                        ak['x'], ak['y'] = self.rect.center
                    attack_display.add(Attack_Display(**ak))
                    self._last_periodic_spawn = now
                    self._periodic_spawn_count += 1
                    if max_times is not None and self._periodic_spawn_count >= max_times:
                        self.periodic_spawn = None



            # apply type 3 freeze/root first only once to all enemies
            if self.stop_movement[0] and self.stop_movement[2] == 3 and not getattr(self, "status_applied", False):
                for enemy in self.who_attacked:
                    if enemy is not None:
                        try:
                            enemy.movement_status(self.stop_movement[1], source=self, slow_rate=self.stop_movement[3])
                            try:
                                self.affected_enemies.add(enemy)
                            except Exception:
                                pass
                        except:
                            pass
                self.status_applied = True

            if current_time - self.last_update_time > self.frame_duration:
                self.last_update_time = current_time
                self.frame_index += 1
                
                # print('reducing dmg')

                if self.frame_index < len(self.frames):
                    self.image = self.frames[self.frame_index]

                # Every attack frame (depends on frame duration)
                elif self.frame_index >= len(self.frames): # kind of 'else' in my s.py
                    self.frame_index = 0
                    self.current_repeat += 1

                    # EVERY FRAME ATTACK LOGIC --------------------------

                    if self.per_end_dmg[0]:
                        # Reset damaged state for all enemies
                        for enemy in self.who_attacked:
                            if enemy is not None and enemy in self.enemy_states:
                                self.enemy_states[enemy]['damaged'] = False
                        self.damaged_detect = False 
                        self.damaged = False
                        
                    # normal logic, damages enemy anywhere
                    if not self.heal and not self.heal_enemy:
                        if self.per_end_dmg[1]:  # removed self.damaged check - per_end_dmg[1] should damage every repeat
                            if not self.continuous_dmg:
                                # Apply damage to all colliding enemies (per_end_dmg[1] = damage at end of animation cycle)
                                # Get current colliding enemies at this frame
                                current_colliding = self._get_colliding_enemies()
                                
                                # If disable_collide is True, damage who_attacked directly (bypassing collision)
                                if self.disable_collide:
                                    for enemy in self.who_attacked:
                                        if enemy is not None and enemy in self.enemy_states:
                                            self._apply_damage(enemy, self.dmg)
                                else:
                                    for enemy in current_colliding:
                                        if enemy is not None and enemy in self.enemy_states:
                                            if not self.enemy_states[enemy]['damaged']:
                                                self._apply_damage(enemy, self.dmg)
                                                self.enemy_states[enemy]['damaged'] = True
                    else:
                        if self.per_end_dmg[1]:  # removed self.damaged check
                            if not self.continuous_dmg:
                                self._apply_heal(self.dmg)







                    # MAIN LOGIC 2
                    # Final animation end
                    if self.current_repeat >= self.repeat_animation:
                        # warning: inside these block of codes only runs per frames, not fps frames, 
                        # which might prone to errors if not read carefully.
                        
                                
                        #dmg animation
                        self.animation_done = True
                        self.kill_self() # Remove the sprite from the group  

                    # EVERY END FRAME ATTACK LOGIC -----------------------------
                        
                    if self.sound[0] == True and self.repeat_sound:
                        if self.sound[1] != None:
                            self.sound[1].play()
                        if self.sound[2] != None:
                            self.sound[2].play()
                        if self.sound[3] != None:
                            self.sound[3].play()

                    #final dmg - apply to all colliding enemies
                    for enemy in colliding_enemies:
                        if enemy is not None and enemy in self.enemy_states:
                            if not self.enemy_states[enemy]['damaged']:
                                self._check_and_set_follow(enemy)
                                if not self.disable_collide: # end animation will do the damaging
                                    self._apply_damage(enemy, self.final_dmg, is_final=True)

                    


                    
                            








            # EVERY FRAME ATTACK LOGIC --------------------------

                # EVERY GAME FPS ATTACK LOGIC --------------------------
                
                #dmg per every frame (too fast)  <-- indent  

                # stun logic
                if not self.heal and not self.heal_enemy:
                    
                                
                    #dmg per frame

                    # main atk logic - iterate over all colliding enemies
                    for enemy in colliding_enemies:
                        if enemy is None or enemy not in self.enemy_states:
                            continue
                        
                        enemy_state = self.enemy_states[enemy]
                        
                        # Only apply damage if this enemy hasn't been damaged yet (for moving attacks)
                        if not enemy_state['damaged'] and not self.disable_collide:
                            if not self.continuous_dmg:
                                self._check_and_set_follow(enemy)
                                self._apply_damage(enemy, self.dmg)
                                
                                # Mark as damaged if it's a moving attack (fireball style)
                                if self.moving:
                                    enemy_state['damaged'] = True
                        
                    # continuous dmg logic - damage all colliding enemies continuously
                    if self.continuous_dmg:
                        for enemy in colliding_enemies:
                            if enemy is not None and enemy in self.enemy_states:
                                self._check_and_set_follow(enemy)
                                self._apply_damage(enemy, self.dmg)

                    #for per_end_dmg logic - only applies to colliding enemies
                    # NOW WHY TF DOES THIS WORK SUDDENLY? this is .... good?
                    if self.per_end_dmg[0] and self.disable_collide:
                        for enemy in colliding_enemies:
                            if enemy is None or enemy not in self.enemy_states:
                                continue
                            
                            enemy_state = self.enemy_states[enemy]
                            
                            if not enemy_state['damaged']:
                                self._check_and_set_follow(enemy)
                                if not self.continuous_dmg:
                                    self._apply_damage(enemy, self.dmg)

                                if self.damaged_detect:
                                    enemy_state['damaged'] = True

                    #whenn collide, kill
                    if has_collision:
                        if self.kill_collide:
                            self.rect.x += 10000
                            self.kill_self()
                    if self.hitbox_rect.colliderect(self.who_attacks.hitbox_rect):
                        if self.self_kill_collide:
                            self.rect.x += 10000
                            self.kill_self()

                    

                # heal logic
                else:
                    if self.self_moving:
                        if self.hitbox_rect.colliderect(self.who_attacks.hitbox_rect):
                            if self.heal_enemy:
                                # Heal all colliding enemies
                                if self.continuous_dmg:
                                    for enemy in colliding_enemies:
                                        if enemy is None or enemy not in self.enemy_states:
                                            continue
                                        self._check_and_set_follow(enemy)
                                        enemy.take_heal(self.dmg)
                                        self.who_attacks.take_special(self.dmg * SPECIAL_MULTIPLIER)
                                else:
                                    for enemy in colliding_enemies:
                                        if enemy is None or enemy not in self.enemy_states:
                                            continue
                                        enemy_state = self.enemy_states[enemy]
                                        if not enemy_state['damaged']:
                                            self._check_and_set_follow(enemy)
                                            enemy.take_heal(self.dmg)
                                            self.who_attacks.take_special(self.dmg * SPECIAL_MULTIPLIER)
                                            enemy_state['damaged'] = True
                            else:
                                if not self.damaged:
                                    self._check_and_set_follow(self.who_attacks) if self.who_attacks in self.enemy_states else None
                                    self._apply_heal(self.dmg)
                                    self.damaged = True

                    else:#normal stuff
                        if self.heal_enemy:
                            # Heal all colliding enemies
                            if self.continuous_dmg:
                                for enemy in colliding_enemies:
                                    if enemy is None or enemy not in self.enemy_states:
                                        continue
                                    self._check_and_set_follow(enemy)
                                    enemy.take_heal(self.dmg)
                                    self.who_attacks.take_special(self.dmg * SPECIAL_MULTIPLIER)
                            else:
                                for enemy in colliding_enemies:
                                    if enemy is None or enemy not in self.enemy_states:
                                        continue
                                    enemy_state = self.enemy_states[enemy]
                                    if not enemy_state['damaged']:
                                        self._check_and_set_follow(enemy)
                                        enemy.take_heal(self.dmg)
                                        self.who_attacks.take_special(self.dmg * SPECIAL_MULTIPLIER)
                                        enemy_state['damaged'] = True
                        else:
                            if not self.damaged and self.hitbox_rect.colliderect(self.who_attacks.hitbox_rect):
                                self._check_and_set_follow(self.who_attacks) if self.who_attacks in self.enemy_states else None
                                self._apply_heal(self.dmg)


                if self.consume_mana[0]:
                    self.who_attacks.take_mana(self.consume_mana[1])

            # ALWAYS AFFECTED
            
            if self.moving: # moving logic
                # Move the attack
                self.rect.x += self.speed #(Theres a bug where you use water princess special skill 4 on left border so it moves enemy outside border, that has freeze effect, after it goes back to screen, still frozen. Fix the player movement statuses if bug persists.)
                if self.rect.x > width + 2000 or self.rect.x < -2000: # (the 2nd part might be the culprit...)
                    self.kill_self()  # Remove the sprite if it goes off-screen
                    # (There, fixed, but somethings wrong with removing effect on kill self)

            #stun logic - apply to all colliding enemies
            for enemy in colliding_enemies:
                if enemy is None or enemy not in self.enemy_states:
                    continue
                self._check_and_set_follow(enemy)
                if self.stun[0]:
                    try:
                        enemy.stun(self.stun, self.rect.centerx, self.rect.centery, self.stun[1])
                    except:
                        pass

            #follow logic - follow the first enemy that was set to follow
            if not self.follow_self:
                followed_enemy = None
                # Check if any enemy should be followed
                for enemy in self.who_attacked:
                    if enemy is None or enemy not in self.enemy_states:
                        continue
                    if self.follow[1]:  # FOLLOW ENEMY always
                        followed_enemy = enemy
                        break
                    elif self.follow[0] and self.enemy_states[enemy]['following']:
                        followed_enemy = enemy
                        break
                
                if followed_enemy is not None:
                    self.rect.centerx = followed_enemy.rect.centerx + self.follow_offset[0]
                    self.rect.centery = followed_enemy.rect.centery + self.follow_offset[1]
                    # Prevent followed attacks from going below ground level
                    try:
                        if self.rect.centery > global_vars.DEFAULT_Y_POS:
                            self.rect.centery = int(global_vars.DEFAULT_Y_POS) - 2
                    except Exception:
                        pass

            else:
                if self.follow[1]: # FOLLOW SELF
                    self.rect.centerx = self.who_attacks.rect.centerx + self.follow_offset[0]
                    self.rect.centery = self.who_attacks.rect.centery + self.follow_offset[1]
                elif self.follow[0] and self.following_target:
                    self.rect.centerx = self.who_attacks.rect.centerx + self.follow_offset[0]
                    self.rect.centery = self.who_attacks.rect.centery + self.follow_offset[1]
                    # Clamp to ground so attacks following the caster don't sink below the floor
                    try:
                        if self.rect.centery > global_vars.DEFAULT_Y_POS:
                            self.rect.centery = int(global_vars.DEFAULT_Y_POS) - 2
                    except Exception:
                        pass

            # print(self.follow_self)

            #freeze and root - apply to all colliding enemies
            # [0] = enable
            # [1] = status type (freeze/root)
            # [2] = type
            if self.stop_movement[0]: # enable status
                if self.stop_movement[2] in (1,2): # if either type == 1 or 2
                    # type 2 - apply when colliding
                    # always run code below if type == 2
                    # print(self.stop_movement)
                    for enemy in colliding_enemies:
                        if enemy is None or enemy not in self.enemy_states:
                            continue
                        try:
                            enemy.movement_status(self.stop_movement[1], source=self, slow_rate=self.stop_movement[3])
                            # record that this attack affected that enemy so we can remove symmetrically
                            try:
                                self.affected_enemies.add(enemy)
                            except Exception:
                                pass
                        except Exception:
                            pass
                    # type 1 
                    # run code below if type == 1
                    if self.stop_movement[2] == 1:
                        # removes status from enemies that are no longer colliding
                        # iterate over the enemies we actually applied the status to
                        for enemy in list(getattr(self, 'affected_enemies', set())):
                            if enemy is None:
                                continue
                            if enemy not in colliding_enemies and enemy in self.enemy_states:
                                try:
                                    enemy.remove_movement_status(self.stop_movement[1], source=self)
                                except:
                                    pass
                                # forget that we applied to this enemy
                                try:
                                    self.affected_enemies.discard(enemy)
                                except:
                                    pass

            if self.current_repeat >= self.repeat_animation:
                if self.stop_movement[0]:
                    status_type = self.stop_movement[1]
                    mode = self.stop_movement[2]
                    if mode in (1, 2, 3):  # remove for modes that persist until attack end
                        # remove status only from enemies this attack actually affected
                        for enemy in list(getattr(self, 'affected_enemies', set())):
                            if enemy is None:
                                continue
                            try:
                                enemy.remove_movement_status(status_type, source=self)
                            except Exception:
                                pass
                        try:
                            self.affected_enemies.clear()
                        except Exception:
                            pass

            
            

            

            



'''
Hero Stats



Fire Wizard:

Strength: 40
Intelligence: 40
Agility: 27



Wanderer Magician:

Strength: 40
Intelligence: 36
Agility: 32



Fire Knight:

Strength: 40
Intelligence: 40
Agility: 65



Wind Hashashin:

Strength: 38
Intelligence: 40
Agility: 12

'''


















import hero_codes.fire_wizard as fire_wizard
Fire_Wizard = fire_wizard.Fire_Wizard

        


        

        
# MULT = 0.7

import hero_codes.wanderer_magician as wanderer_magician
Wanderer_Magician = wanderer_magician.Wanderer_Magician
        


    
import hero_codes.fire_knight as fire_knight
Fire_Knight = fire_knight.Fire_Knight

        

         





import hero_codes.wind_hashashin as wind_hashashin
Wind_Hashashin = wind_hashashin.Wind_Hashashin










import hero_codes.water_princess as water_princess
Water_Princess = water_princess.Water_Princess






import hero_codes.forest_ranger as forest_ranger
Forest_Ranger = forest_ranger.Forest_Ranger



import hero_codes.yurei as yurei
Yurei = yurei.Yurei





import hero_codes.chthulu as chthulu
Chthulu = chthulu.Chthulu


import hero_codes.phantom_assassin as phantom_assassin
Phantom_Assassin = phantom_assassin.Phantom_Assassin


# #-------------------------------------
# #if have time to make, make the players more centralized

# #inside player class
# def set_opponent(self, opponent):
#     self.opponent = opponent

# #call after initializing both heroes
# PLAYER_1_SELECTED_HERO.set_opponent(PLAYER_2_SELECTED_HERO)
# PLAYER_2_SELECTED_HERO.set_opponent(PLAYER_1_SELECTED_HERO)

# # simplify/modify attack logic inside input, attack.
# who_attacked=self.opponent,

# #instead of this :l
# who_attacked=PLAYER_1_SELECTED_HERO if self.player_type == 2 else PLAYER_2_SELECTED_HERO,

# #----------------------------------------------------
# Declaration of the object sprites (Single instance)

# fire_wizard_copy = Fire_Wizard(2)

# fire_wizard = Fire_Wizard(PLAYER_1)
# wanderer_magician = Wanderer_Magician(PLAYER_2)

# # Group of objects sprites (Multiple instances)
# fire_wizard_group = pygame.sprite.Group()
# fire_wizard_group.add(fire_wizard)

# wanderer_magician_group = pygame.sprite.Group()
# wanderer_magician_group.add(wanderer_magician)


# fire_wizard = None
# wanderer_magician = None

# fire_wizard_group = None
# wanderer_magician_group = None

# def detect_collision():
#     for attack in wanderer_magician_group:  # Loop through each sprite in the group
#         if pygame.sprite.spritecollide(attack, fire_wizard_group, False):
#             return True
#     return False



















# {
#       "name": "Enrichment Booster",
#       "image_path": "assets/item icons/new items/2 Icons with back/Icons_42.png",
#       "bonus_type": ["all_stats_flat", "hp_regen_per", "mana_regen_per", "mana_refund_per", "lifesteal_per", "dmg_reduce_per", "dmg_return_per", "move_speed_per", "spell_dmg_per", "cd_reduce_per", "mana_reduce_per"],
#       "bonus_value": [2, 0.02, 0.02, 0.2, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02]
#     },

# {
#       "name": "Enrichment Booster",
#       "image_path": "assets/item icons/new items/2 Icons with back/Icons_42.png",
#       "bonus_type": ["lifesteal_per", "mana_refund_per", "hp_regen_per", "mana_regen_per"],
#       "bonus_value": [0.06, 0.3, 0.05, 0.05]
#     },




from gameloop import game
from gameloop import reset_all
from gameloop import menu
from gameloop import fade
import loader



scale = 0.8
center_pos = (width / 2, height / 2)

item_data = "item_data.json"

item_data = loader.loadFile(item_data)

# print(item_data["items"])

class Item:
    def __init__(self, name, image_path, bonus_type, bonus_value, description="", cooldown=0, attack_frames=None, attack_count=None, attack_frame_duration=100, attack_repeat=1, starts_at_zero=False, size=1, sound_path=None, frame_type="frames"):
        self.name = name
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (75, 75))
        self.bonus_type = bonus_type  # list, e.g., ["str_per", "str_flat", "hp_regen_per"]
        self.bonus_value = [float(v) for v in bonus_value]  # Always floats for consistency
        self.rect = self.image.get_rect(center=center_pos)
        self.description = description  # Optional description
        self.cooldown = cooldown  # in seconds
        self.last_used = -self.cooldown if self.cooldown > 0 else 0  # timestamp in seconds

        # for items with ability
        self.last_used_time = -cooldown  # raw pygame.time.get_ticks() value when used
        self._last_used_paused_total = 0   # global_vars.PAUSED_TOTAL_DURATION snapshot at use


        # Attack display properties
        if attack_frames is not None: # load frames if provided
            if attack_count == "immortality_count": # THERES NO OTHER WAY :(
                attack_count = (5, 10)
            elif attack_count == "temp_hp_count":
                attack_count = (5, 9)
            elif attack_count == "spawn_flame_count":
                attack_count = (8, 8)
            self.attack_frames = self.load_img_frames_v2(attack_frames, attack_count, starts_at_zero, size, frame_type)
        self.attack_frame_duration = attack_frame_duration
        self.attack_repeat = attack_repeat

        self.info = {t: v for t, v in zip(self.bonus_type, self.bonus_value)}

        # Auto-generate display_info (user-friendly strings)
        self.display_info = self.generate_display_info()

    
    def load_img_frames_v2(self, folder:str, count:int | tuple, starts_at_zero=False, size=1, typ='frames', flipped=False, rotate=0):
        ''' Can be used as loading attack frames and loading a spritesheet, provided that count is tuple
        
        - folder: path of single frame, without the numbering.
        
                if spritesheet, provide the spritesheet path (typ != 'frames')
        - count: int if typ == 'frames' (frame count)

                tuple if typ == 'spritesheet' (column, rows)
        '''
        if typ == "frames":
            print(count, typ)
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
    
    def time_since_use(self):
        """Return milliseconds elapsed since last use, excluding paused durations."""
        paused_total = global_vars.PAUSED_TOTAL_DURATION
        if global_vars.PAUSED and global_vars.PAUSED_START is not None:
            paused_total += pygame.time.get_ticks() - global_vars.PAUSED_START
        effective_now = pygame.time.get_ticks() - paused_total
        effective_last = self.last_used_time - self._last_used_paused_total
        return effective_now - effective_last

    def generate_display_info(self):
        display_map = {
            # Primary stats
            "str_per": "Strength",
            "str_flat": "Strength",
            "int_per": "Intelligence",
            "int_flat": "Intelligence",
            "agi_per": "Agility",
            "agi_flat": "Agility",
            "all_stats_per": "All Stats",
            "all_stats_flat": "All Stats",

            # Ability
            "heal_when_low": "Convalescent",
            "extra_temp_hp": "Absorption",
            "immortality": "Immortality",
            "temp_hp_increase": "Safeguard",

            # Health / Mana
            "hp_per": "Max HP",
            "hp_flat": "Max HP",
            "hp_regen_per": "HP Regen",
            "hp_regen_flat": "HP Regen",
            "mana_per": "Max Mana",
            "mana_flat": "Max Mana",
            "mana_regen_per": "Mana Regen",
            "mana_regen_flat": "Mana Regen",
            "mana_refund_per": "Mana Steal",
            "mana_reduce_per": "Mana Cost Reduction",

            # Attack / Damage / Speed
            "atk_per": "Attack Damage",
            "atk_flat": "Attack Damage",
            "atk_speed_flat": "Attack Speed",   # Flat
            "atk_speed_per": "Attack Speed",    # Percentage
            "spell_dmg_per": "Spell Damage",
            "crit_chance_per": "Critical Chance",
            "crit_dmg_per": "Critical Damage",

            # Defensive / Utility / Special
            "dmg_reduce_per": "Damage Reduction",
            "dmg_increase_per": "Damage Taken Increase",
            "dmg_return_per": "Damage Return",
            "lifesteal_per": "Lifesteal",
            "health_cost_per": "Health Cost",
            "move_speed_per": "Move Speed",
            "cd_reduce_per": "Cooldown Reduction",
            "sp_increase_per": "Special Increase",
            "mana_burn_per": "Mana Burn",
            "mana_burn_per_dmg": "Mana Burn to Damage",
            "mana_burn_flat": "Mana Burn",
            "mana_burn_flat_dmg_per": "Mana Burn to Damage", # force display at percentage
            "spell_lifesteal_per": "Spell Lifesteal",
            "spawn_flame": "Heat Wave"
        }
        
        # Types that are abilities and should not show values
        ability_types = {
            "heal_when_low": "passive",
            "immortality": "passive",
            "temp_hp_increase": "passive",
            "spawn_flame": "passive"
            }
        
        info_list = []
        for typ, val in self.info.items():
            nice_name = display_map.get(typ, typ.replace("_", " ").title())  # Fallback to capitalized type
            if typ in ability_types:
                info_list.append(f"{nice_name} - {ability_types[typ]} ability")
            else:
                sign = "+" if val > 0 else ""
                if "_per" in typ:  # Percentage
                    formatted_val = f"{sign}{val * 100:.0f}%"
                else:  # Flat
                    formatted_val = f"{sign}{val:g}"  # :g trims decimals
                info_list.append(f"{nice_name}: {formatted_val}")
        return info_list

    def draw_icon(self, center_pos, small=False, hero_sp=False):
        """
        Draw item icon with cooldown display for equipped items.
        """
        if small == 'smallest':
            profile = pygame.transform.scale(self.image, (25, 25))
        else:
            profile = self.image
        rect = profile.get_rect(center=center_pos)
        screen.blit(profile, rect)

        # Display cooldown if applicable
        if hasattr(self, 'cooldown') and self.cooldown > 0 and not global_vars.PAUSED:
            current_time = pygame.time.get_ticks() / 1000 - global_vars.PAUSED_TOTAL_DURATION / 1000
            remaining = self.cooldown - (current_time - self.last_used)
            if remaining > 0:
                font = global_vars.get_font(15)
                text = font.render(f"{math.ceil(remaining)}", True, red)
                screen.blit(text, (center_pos[0] - text.get_width()//2, center_pos[1] - 30))
            else:
                font = global_vars.get_font(15)
                text = font.render("ready", True, green)
                screen.blit(text, (center_pos[0] - text.get_width()//2, center_pos[1] - 30))

    def update(self, position, line_break_every=100, use_literal=False, character_limit=1000):
        '''line_break_every = simply dont put arrow at the bonus.'''
        if use_literal:
            # Option 1: Literal values (no %)
            stats_lines = [f"{key.replace('_', ' ').title()}: {'' if val < 0 else '+'}{val:g}" for key, val in self.info.items()]
        else:
            # Option 2: User-friendly
            stats_lines = self.display_info

        # Auto-wrap long lines (every N items)
        if line_break_every > 0:
            wrapped = []
            for i in range(0, len(stats_lines), line_break_every):
                chunk = stats_lines[i:i+line_break_every]
                # Prepend '@-> ' to all but the first in the chunk
                chunk = [chunk[0]] + [f"@-> {entry}" for entry in chunk[1:]]
                wrapped.append(' '.join(chunk))
            stats_lines = wrapped  # Now list of grouped strings

        # Build full lines list: Name first, then stats, then desc (each as separate lines)
        full_lines = [self.name] + stats_lines
        if self.description:
            full_lines += [""]  # Empty line spacer
            # Split desc into lines if long (e.g., every 40 chars)
            desc_words = self.description.split()
            desc_lines = []
            current_line = ""
            for word in desc_words:
                if len(current_line) + len(word) + 1 > character_limit:  # Char limit per line
                    desc_lines.append(current_line.strip())
                    current_line = word
                else:
                    current_line += " " + word
            if current_line:
                desc_lines.append(current_line.strip())
            full_lines += desc_lines

        info_bubble_item = ImageBro(
            image_path=text_box_img,
            # pos=(position[0]*0.6, position[1]),  # Your custom position
            pos=position,
            text=full_lines,
            font_path=global_vars.FONT_PATH,
            font_size=font_size * 1.05,
            text_color='white',
            # fixed_size=(250, 200 + (len(full_lines) * font_size)),  # Keep your dynamic height
            text_scale=1.3,  # <-- Makes text 80% size → looks cleaner in tall box
            anchor='bottomleft'  # Or 'center', etc.
        )
        info_bubble_item.drawing_info(screen)

    # def draw(self, pos):
    #     self.decor = pygame.draw.rect(screen, black, self.decor_rect)
    #     screen.blit(self.image, pos)
        
        
    
# Update log for items

# Nerf:
# Crimson Crystal: 10% spell dmg, 5% mana reduce, 5% cd reduce -> 10% spell dmg, 3% mana reduce, 3% cd reduce
# Red Crystal: 20% mana reduce, 5% cd reduce, 3% spell dmg -> 15% mana reduce, 3% cd reduce, 2% spell dmg
# Ruby: 20% cd reduce, 5% mana reduce, 3% spell dmg -> 15% cd reduce, 3% mana reduce, 2% spell dmg

# Update:
# Emblem Necklace: 8% mana -> 10%, 4% mana regen -> 5%, removed 8 mana -> 4 int flat
# Buff:
# Elixir: 6% all effect ->  7%
# War Helmet: 5% str -> 10%, 4% hp regen -> 5%
# Spirit Feather: removed 3 agi flat

# Update:
# so many (buffs)


# Update:
# improved crystals by 5% (2% for spell dmg)
# princess necklace mana reduce 5% -> 10%

#update 
# error war helmet was only at 1 str bug

# Update:
# modified all crystals to have 15%/5% value

items = []


for item in item_data["items"]:
    # print(item)
    # print(item["image_path"])
    items.append(Item(
        name=item.get("name", "Unnamed Item"),
        image_path=item.get("image_path", ""),
        bonus_type=item.get("bonus_type", "Unknown Bonus"),
        bonus_value=item.get("bonus_value", "Unknown Bonus Value"),
        description=item.get("description", ""),
        cooldown=item.get("cooldown", 0),
        attack_frames=item.get("attack_frames"),
        attack_count=item.get("attack_count"),
        attack_frame_duration=item.get("attack_frame_duration", 100),
        attack_repeat=item.get("attack_repeat", 1),
        starts_at_zero=item.get("starts_at_zero", False),
        size=item.get("size", 1),
        sound_path=item.get("sound_path"),
        frame_type=item.get("frame_type")
    ))


def get_items_by_names(names_list):
    """Returns a list of cloned Item instances of the given item names."""
    item_map = {item.name: item for item in items}
    item_names = []
    for name in names_list:
        if name in item_map:
            item_names.append(copy.copy(item_map[name]))
    return item_names


# items = [
#     Item("War Helmet", r"assets\item icons\in use\Icons_40.png", 
#          ["str_per", "str_flat", "hp_regen_per"], [0.1, 1.0, 0.08]),  # Stats clear → no desc needed

#     Item("Tough Stone", r"assets\item icons\in use\Icons_14.png", 
#          ['dmg_reduce_per', 'hp_flat', "move_speed_per"], [0.15, 5.0, -0.1],
#          description="Reduces damage taken@but lowers movement speed."),

#     Item("Undead Marrow", r"assets\item icons\new items\2 Icons with back\Icons_40.png", 
#          ["lifesteal_per"], [0.15]),  # Simple → no desc

#     Item("Spoon", r"assets\item icons\new items\2 Icons with back\Icons_19.png", 
#          ['hp_flat', 'mana_flat', 'agi_flat', 'cd_reduce_per'], [30.0, -30.0, 5.0, 0.05],
#          description="Gains HP and agility@but loses mana.@Reduces skill cooldowns."),

#     Item("Vitality Booster", r"assets\item icons\new items\2 Icons with back\Icons_23.png", 
#          ["hp_per", "hp_flat"], [0.1, 5.0]),  # Clear → no desc

#     Item("Mysterious Mushroom", r"assets\item icons\in use\Icons_08.png", 
#          ["hp_regen_per", "mana_regen_per"], [-0.3, 0.3],
#          description="Greatly increases mana regeneration@at the cost of health regeneration."),



#     Item("Crimson Hearthstone", r"assets\item icons\gems\Icons_15.png", 
#          ['hp_flat', 'dmg_reduce_per', 'hp_regen_per'], [25.0, 0.05, 0.05]),  # Clear → no desc

#     Item("Azure Myststone", r"assets\item icons\gems\Icons_11.png", 
#          ['mana_flat', 'spell_dmg_per', 'mana_regen_per'], [25.0, 0.05, 0.05]),  # Clear → no desc

#     Item("Verdant Fury", r"assets\item icons\gems\Icons_03.png", 
#          ['atk_flat', 'atk_speed_per', 'move_speed_per'], [0.25, 0.05, 0.05]),  # Clear → no desc

#     Item("Elixir", r"assets\item icons\in use\Icons_30.png", 
#          ["hp_regen_per", "mana_regen_per", "move_speed_per"], [0.07, 0.07, 0.07]),  # Balanced → no desc

#     Item("Energy Booster", r"assets\item icons\new items\2 Icons with back\Icons_12.png", 
#          ["str_flat", "int_flat", "agi_flat"], [4.0, 4.0, 3.0]),  # Clear → no desc

#     Item("Mana Essence", r"assets\item icons\new items\2 Icons with back\Icons_26.png", 
#          ['mana_refund_per'], [0.75],
#          description="Refunds 75% of mana spent on skills."),



#     Item("Crimson Crystal", r"assets\item icons\new items\2 Icons with back\Icons_24.png", 
#          ['spell_dmg_per', 'mana_reduce_per', 'cd_reduce_per'], [0.15, 0.05, 0.05]),  # Clear → no desc

#     Item("Red Crystal", r"assets\item icons\new items\2 Icons with back\Icons_06.png", 
#          ['mana_reduce_per', 'cd_reduce_per', 'spell_dmg_per'], [0.15, 0.05, 0.05]),  # Clear → no desc

#     Item("Ruby", r"assets\item icons\new items\2 Icons with back\Icons_07.png", 
#          ['cd_reduce_per', 'mana_reduce_per', 'spell_dmg_per'], [0.15, 0.05, 0.05]),  # Clear → no desc

#     Item("Princess Necklace", r"assets\item icons\new items\2 Icons with back\Icons_34.png", 
#          ['mana_flat', 'mana_reduce_per', 'spell_dmg_per'], [40.0, 0.05, 0.05]),  # Clear → no desc

#     Item("Corrupted Booster", r"assets\item icons\new items\2 Icons with back\Icons_35.png", 
#          ['health_cost_per', "spell_dmg_per"], [-0.15, 0.25],
#          description="Greatly increases spell damage@but reduces max health."),

#     Item("Emblem Amulet", r"assets\item icons\in use\Icons_26.png", 
#          ["int_per", "int_flat", "mana_regen_per"], [0.1, 4.0, 0.08]),  # Clear → no desc



#     Item("Old Axe", r"assets\item icons\in use\Icons_09.png", 
#          ["atk_per", "hp_flat", "agi_flat"], [0.1, 5.0, 2.0]),  # Clear → no desc

#     Item("Spirit Feather", r"assets\item icons\in use\Icons_11.png", 
#          ["move_speed_per", "atk_speed_flat"], [0.1, 150.0]),  # Clear → no desc

#     Item("Cheese", r"assets\item icons\2 Icons with back\Icons_12.png", 
#          ['sp_increase_per', 'all_stats_per'], [0.40, 0.5],
#          description="Special meter fills 40% faster."),

#     Item("The Great Hilt", r"assets\item icons\2 Icons with back\Icons_23.png", 
#          ['atk_flat', "move_speed_per", 'atk_speed_flat'], [0.1, 0.05, 50.0]),  # Clear → no desc

#     Item("Flower Locket", r"assets\item icons\in use\Icons_13.png", 
#          ["hp_regen_per", "mana_regen_per", "move_speed_per", "atk_speed_flat", "int_flat"], [0.02, 0.02, 0.02, 100.0, 4.0]),  # Many stats → no desc

#     Item("Machete", r"assets\item icons\new items\2 Icons with back\Icons_27.png", 
#          ["crit_chance_per", "crit_dmg_per"], [0.2, 0.7],
#          description="Grants each attack a 20%@chance to deal 70% more damage."),



#     Item("Curse of Warlord", r"assets\item icons\new items\2 Icons with back\Icons_15.png", 
#          ['dmg_return_per'], [0.20],
#          description="Returns 20% of damage taken to attacker."),

#     Item("Last Breath", r"assets\item icons\new items\2 Icons with back\Icons_04.png", 
#          ['heal_when_low', 'all_stats_flat'], [1.0, 1], 
#          description="When health falls below 10%, instantly@restores health equal@to Strength.@@Cooldown: 120s",
#          cooldown=120,
#          attack_frames=r'assets\attacks_item\Last Breath\image_',
#          attack_count=8,
#          attack_frame_duration=125,
#          attack_repeat=5,
#          starts_at_zero=True,
#          size=2,
#          sound_path='pass muna bro'),

#     Item("Unwavering banner", r"assets\item icons\new items\2 Icons with back\Icons_05.png", 
#          ['extra_temp_hp'], [50.0], 
#          description="Grants 50 temporary HP that absorbs@damage before affecting real health."),

     
# ]




"""# MAX CHAR LENGTH (including spaces):
\n# -> 32"""

# doc
#
'''
War Helmet: 10% str, 1 str flat, 0.02 hp regen
Emblem Necklace: 12% int, 8 mana flat, 0.04 mana regen
Old Axe: 7% atk, 3 hp flat
Spirit Feather: 5% move speed, 150 attack speed, 3 agi flat
Vitality Booster: 15% hp, 10 hp flat
Mysterious Mushroom: -35% hp regen, 35% mana regen
Elixir: 8% hp regen, 8% mana regen, 4% move speed
Flower Locket: 12% hp regen, 12% mana regen
Energy Booster: 3 str flat, 3 int flat, 3 agi flat
'''
# Hero display info cache - populated once at startup to avoid expensive hero instantiation
HERO_DISPLAY_CACHE = {}

def build_hero_display_cache():
    """
    Pre-compute hero display info cache to avoid expensive instantiation on hover.
    This is called once at startup to populate the cache.
    """
    hero_data = {
        "Fire Wizard": {"str": 40, "int": 40, "agi": 26, "base_atk": 0.1, "atk_time": 1750, "atk_spd_mod": 0.5, "atk_spd": 100, "hp_regen": 0.8, "mana_regen": 5.3, "move_speed": 2.2, "icon": fire_wizard_icon},
        "Wanderer Magician": {"str": 40, "int": 36, "agi": 35, "base_atk": 0.2, "atk_time": 1600, "atk_spd_mod": 0.5, "atk_spd": 100, "hp_regen": 0.6, "mana_regen": 6.75, "move_speed": 2.2, "icon": wanderer_magician_icon},
        "Fire Knight": {"str": 42, "int": 36, "agi": 33, "base_atk": 3.4, "atk_time": 1800, "atk_spd_mod": 0.5, "atk_spd": 60, "hp_regen": 0.85, "mana_regen": 4.85, "move_speed": 1.76, "icon": fire_knight_icon},
        "Wind Hashashin": {"str": 38, "int": 40, "agi": 24, "base_atk": 0.0, "atk_time": 1700, "atk_spd_mod": 0.6, "atk_spd": 105, "hp_regen": 0.82, "mana_regen": 5.1, "move_speed": 2.64, "icon": wind_hashashin_icon},
        "Water Princess": {"str": 38, "int": 48, "agi": 20, "base_atk": 0.0, "atk_time": 3700, "atk_spd_mod": 0.4, "atk_spd": 60, "hp_regen": 0.8, "mana_regen": 6.05, "move_speed": 2.035, "icon": water_princess_icon},
        "Forest Ranger": {"str": 32, "int": 52, "agi": 30, "base_atk": 0.1, "atk_time": 1800, "atk_spd_mod": 1.1, "atk_spd": 100, "hp_regen": 0.8, "mana_regen": 5.0, "move_speed": 2.53, "icon": forest_ranger_icon},
        "Yurei": {"str": 36, "int": 40, "agi": 37, "base_atk": 0.5, "atk_time": 1500, "atk_spd_mod": 0.55, "atk_spd": 100, "hp_regen": 0.75, "mana_regen": 5.5, "move_speed": 2.31, "icon": yurei_icon},
        "Chthulu": {"str": 40, "int": 40, "agi": 25, "base_atk": 2.5, "atk_time": 1900, "atk_spd_mod": 0.5, "atk_spd": 100, "hp_regen": 0.9, "mana_regen": 4.9, "move_speed": 1.1, "icon": chthulu_icon},
        "Phantom Assassin": {"str": 40, "int": 40, "agi": 30, "base_atk": 0.3, "atk_time": 1600, "atk_spd_mod": 1.2, "atk_spd": 110, "hp_regen": 0.8, "mana_regen": 5.5, "move_speed": 2.42, "icon": phantom_assassin_icon},
    }
    
    STR_MULT = 5  # From Player class
    INT_MULT = 5  # From Player class
    AGI_MULT = 0.1  # From Player class
    
    for hero_name, data in hero_data.items():
        str_val = data["str"]
        int_val = data["int"]
        agi_val = data["agi"]
        base_atk = data["base_atk"]
        atk_time = data["atk_time"]
        atk_spd_mod = data["atk_spd_mod"]
        atk_spd = data["atk_spd"]
        hp_regen = data["hp_regen"]
        mana_regen = data["mana_regen"]
        move_speed = data["move_speed"]
        hero_icon = data["icon"]
        
        # Calculate derived stats (matching Player class logic)
        max_health = str_val * STR_MULT
        max_mana = int_val * INT_MULT
        basic_damage = base_atk + (agi_val * AGI_MULT)
        
        # Extract trait from HERO_INFO
        trait_text = ""
        if hero_name in HERO_INFO:
            info_str = HERO_INFO[hero_name]
            if "Trait: " in info_str:
                trait_text = info_str.split("Trait: ")[-1]
        
        # Build stats dictionary with colors (organized in display order)
        stats = {
            'Strength': (f"{str_val}", 'red'),
            'Intelligence': (int_val, 'cyan'),
            'Agility': (agi_val, 'green'),
            'Move Speed': (round(move_speed, 2), 'white'),
            'Health': (int(max_health), 'red'),
            'Mana': (int(max_mana), 'cyan'),
            'Health Regen': (round(hp_regen + str_val/100, 2), 'green'),
            'Mana Regen': (round(mana_regen + int_val/100, 2), 'cyan'),
            'Attack Speed': (atk_spd, 'white'),
            'Base Attack Time': (f"{atk_time//100/10}s", 'white'),
            'Attack Speed Modifier': (atk_spd_mod, 'white'),
            'Attack Damage': (round(basic_damage, 2), 'red'),
        }
        
        HERO_DISPLAY_CACHE[hero_name] = (stats, "Trait:@" + trait_text, hero_icon)

def get_hero_display_info(hero_class):
    """
    Get cached hero display information (O(1) lookup, no instantiation).
    
    Args:
        hero_class: The hero class (e.g., Fire_Wizard)
    
    Returns:
        tuple: (stats_dict, trait_text, icon_path) from cache
    """
    hero_name = hero_class.__name__.replace("_", " ")
    cached = HERO_DISPLAY_CACHE.get(hero_name, ({}, "", None))
    return cached


HERO_INFO = { # Agility on display based on total damage around 5-6 seconds, compared with data is above forest ranger class
    "Fire Wizard": f"Strength: 40, Intelligence: 40, Agility: 26, , Trait: 10% Spell Damage",
    "Wanderer Magician": f"Strength: 40, Intelligence: 36, Agility: 37, , Trait: 20%->30% Mana Regen",
    "Fire Knight": f"Strength: 42, Intelligence: 36, Agility: 33, , Trait: 15% Base Health Regen",
    "Wind Hashashin": f"Strength: 38, Intelligence: 40, Agility: 24, , Trait: 15% Mana@Reduction",
    "Water Princess": f"Strength: 40, Intelligence: 48, Agility: 20, , Trait: 15%/20% Mana@Cost and Delay",
    "Forest Ranger": f"Strength: 32, Intelligence: 52, Agility: 30, , Trait: 10% Lifesteal@20% Base Attack Speed@200% Mana as Damage",
    "Yurei": f"Strength: 36, Intelligence: 40, Agility: 37, , Trait: 15% Cooldown Reduction",
    "Chthulu": f"Strength: 40, Intelligence: 40, Agility: 25, , Trait: 5%/10% Stat Increase",
    "Phantom Assassin": f"Strength: 40, Intelligence: 40, Agility: 30, , Trait: 0",
}

# Initialize hero display cache (called once after HERO_INFO is defined for performance)
build_hero_display_cache()

# HERO_INFO = { # Agility on display based on total damage around 5-6 seconds, compared with data is above forest ranger class
#     "Fire Wizard": "Strength: 40, Intelligence: 40, Agility: 27 (26 dmg), HP: 200, Mana: 200, Damage: 5.4 , Attack Speed: -200, , Trait: 20% spell dmg",
#     "Wanderer Magician": "Strength: 40, Intelligence: 36, Agility: 32 (19 dmg), HP: 200, Mana: 180, Damage: 3.2 , Attack Speed: -500, , Trait: 20%->30% mana, regen",
#     "Fire Knight": "Strength: 44, Intelligence: 40, Agility: 65 (26 dmg), HP: 220, Mana: 200, Damage: 6.4 , Attack Speed: -700, , Trait: 15% hp regen",
#     "Wind Hashashin": "Strength: 38, Intelligence: 40, Agility: 13 (28 dmg), HP: 190, Mana: 200, Damage: 2.6 , Attack Speed: 0, , Trait: 15% mana, reduce",
#     "Water Princess": "Strength: 40, Intelligence: 48, Agility: 20 (30 dmg), HP: 200, Mana: 240, Damage: 2.0*(1.5/5), Attack Speed: -3200, , Trait: 15%->20% mana, cost/delay",
#     "Forest Ranger": "Strength: 32, Intelligence: 52, Agility: 35 (18 dmg), HP: 160, Mana: 260, Damage: 3.6, Attack Speed: -880, , Trait: 10% lifesteal, 20% atk speed, 200%+ mana refund",
#     "Yurei": "Strength: 36, Intelligence: 40, Agility: 23 (23 dmg), HP: 180, Mana: 200, Damage: 2.3, Attack Speed: -180, , Trait: 15% cd reduce",
#     "Chthulu": "Strength: 40, Intelligence: 40, Agility: 35 (31 dmg), HP: 220, Mana: 220, Damage: 5.2, Attack Speed: -300, , Trait: 5-10% stat,potency"
# }


class EquippedItem:
    '''
    scudge
    '''
    def __init__(self, items_list):
        self.item = []
        self.items_list = items_list  # List of Item instances


    def add(self, item):
        indexed = len(self.item)
        if indexed < MAX_ITEM:
            self.item.append(item)

    def populate_random_items(self, max_items=MAX_ITEM, ):
        """
        Randomly equip items from the available items list.
        This method randomly selects and equips items up to max_items count.
        
        Args:
            max_items: Maximum number of items to randomly equip (default: MAX_ITEM)
        """
        if not self.items_list or len(self.items_list) == 0:
            return

        for item in self.items_list:
            item.selected = False
        self.item.clear()
        
        # Randomly select how many items to equip (1 to max_items)
        num_items_to_equip = min(max_items, len(self.items_list))
        
        # Randomly select items from the available items list
        selected_items = random.sample(self.items_list, num_items_to_equip)
        
        # Add the randomly selected items to the equipped items
        for item in selected_items:
            self.add(item)
            # Mark as selected so update() won't remove them
            item.selected = True

    def update(self):
        for i in self.item:
            if i.selected == False:
                self.item.remove(i)
        # print("updating")
        for i, item in enumerate(self.item):
            
            
            item.set_position((item_equip_hashmap[i], height-50))    


class PlayerSelector:
    """
    Clickable selector for heroes, items, or maps with smooth movement on select.
    """
    # Default sizes
    PROFILE_SIZE = (width * 0.05859375, width * 0.05859375)        # Heroes 75, 75
    INGAME_SIZE = (width * 0.0390625, width * 0.0390625)         # Items (your old size)
    DECOR_SIZE_LARGE = (width * 0.06640625, width * 0.06640625)    
    DECOR_OFFSET_LARGE = (width * 0.0328125, width * 0.0328125)
    DECOR_SIZE_SMALL = (width * 0.046875, width * 0.046875)
    DECOR_OFFSET_SMALL = (width * 0.0234375, width * 0.0234375) # 30, 30
    DECOR_SIZE_SMALLEST = (width * 0.0234375, width * 0.0234375)  # 30, 30

    DESELECT_Y_OFFSET = - (height * 0.0625)

    def __init__(self, image, center_pos, class_item, small=False, custom_size=None, custom_border=(15,15), static_pos:tuple=(1,1)):
        """
        Args:
            image: str path or Surface
            center_pos: (x, y) tuple
            class_item: Hero class or Item instance
            small: True for item-sized icons (50x50)
            custom_size: (w, h) tuple for maps/other special sizes (overrides small)
            custom_border: (w, h) if custom_size is used. (for decor)
        """
        self.class_item = class_item

        if isinstance(image, str):
            original = pygame.image.load(image).convert_alpha()
        else:
            original = image

        # Determine size
        if custom_size:
            profile_size = custom_size
            decor_size = (custom_size[0] + custom_border[0], custom_size[1] + custom_border[0])  # rough border
            decor_offset = (decor_size[0] // 2, decor_size[1] // 2)
        elif small:
            profile_size = self.INGAME_SIZE
            decor_size = self.DECOR_SIZE_SMALL
            decor_offset = self.DECOR_OFFSET_SMALL
        else:
            profile_size = self.PROFILE_SIZE
            decor_size = self.DECOR_SIZE_LARGE
            decor_offset = self.DECOR_OFFSET_LARGE

        self.profile = pygame.transform.scale(original, profile_size)
        self.ingame_profile = pygame.transform.scale(original, (25, 25))  # always keep small version

        self.profile_rect = self.profile.get_rect(center=center_pos)
        self.decor_rect = pygame.Rect(
            self.profile_rect.centerx - decor_offset[0],
            self.profile_rect.centery - decor_offset[1],
            *decor_size
        )

        self.can_move_back = False
        self.can_move = True
        self.hovered = False
        self.selected = False
        self.move_variable = False
        self.move_back_variable = False

        self.original_pos = center_pos
        self.target_pos = center_pos

        self.static_pos_2 = center_pos

        
        self.static_pos_1 = static_pos


        self.move_speed = 0.1
        # print(self.original_pos)
        self.highlight_offset = (0, -50)  # Move right 10, up 20 when selected
        self.back_button = ImageButton(
            image_path=text_box_img,
            pos=(self.profile_rect.centerx, self.profile_rect.top + self.DESELECT_Y_OFFSET),
            scale=0.5,
            text='Deselect',
            font_path=global_vars.FONT_PATH,
            font_size=font_size * 0.75,
            text_color='white',
            text_anti_alias=global_vars.TEXT_ANTI_ALIASING
        )

        
    def set_position(self, new_center, instant=False):
        """
        Move the selector to a new center position.
        
        Args:
            new_center (tuple): New (x, y) center.
            instant (bool): If True, snap immediately (bypass lerp).
        """
     
        if instant:
            self.target_pos = new_center
            self._apply_position(new_center)
        else:
            self.target_pos = new_center

    def _apply_position(self, center):
        """Internal: Sync all rects to given center."""
        dx = center[0] - self.profile_rect.centerx
        dy = center[1] - self.profile_rect.centery
        # print(dx, dy)

        self.profile_rect.center = center
        self.decor_rect.move_ip(dx, dy)
        self.back_button.set_position((center[0], center[1] + self.DESELECT_Y_OFFSET))  # Assuming ImageButton has set_position # Full (x, y) with offset
        # If associated item needs to follow (e.g., for tooltip alignment)
        if hasattr(self.class_item, 'set_position'):
            self.class_item.set_position(center)


    def enable_movement(self):
        """Allow movement after animation completes."""
        while self.move_variable:
            if not self.can_move and not self.can_move_back:
                        self.can_move_back = True
            self.move_variable = False

        while self.move_back_variable:
            if not self.can_move_back and not self.can_move:
                        self.can_move = True
            self.move_back_variable = False
            print(self.can_move, self.can_move_back)



    def update(self, mouse_pos, mouse_pressed, other_selectors, max_selected=MAX_ITEM):
        # Smooth movement toward target
        
        if self.profile_rect.center != self.target_pos:
            
            current = [float(self.profile_rect.centerx), float(self.profile_rect.centery)]
            dx = self.target_pos[0] - current[0]
            dy = self.target_pos[1] - current[1]

            # If very close, snap exactly to avoid drift
            if abs(dx) <= 2 and abs(dy) <= 2:
                # print("Snapped")
                self._apply_position(self.target_pos)
                self.enable_movement()

            else:
                # Normal smooth movement
                # print(dx, dy)
                if abs(dx) > 10:
                    
                    current[0] += (dx * self.move_speed)
                else:
                    current[0] += (dx * 0.3)
                if abs(dy) > 10:
                    
                    current[1] += (dy * self.move_speed)
                else:
                    current[1] += (dy * 0.3)
                
                self._apply_position((round(current[0]), round(current[1])))
        
        # Draw base
        self.draw()

        # Selection logic
        selected_count = sum(1 for s in other_selectors if s.selected)
        can_select = selected_count < max_selected

        if not self.selected:
            if self.decor_rect.collidepoint(mouse_pos) and can_select and self.can_move:
                self.hovered = True
                if mouse_pressed[0]:

                    self.can_move = False
                    self.selected = True


                    self.move_variable = True
                    


                    highlight_pos = (
                        self.original_pos[0] + self.highlight_offset[0],
                        self.original_pos[1] + self.highlight_offset[1]
                    )
                    self.set_position(highlight_pos)
                    self.hovered = False
            else:
                self.hovered = False
        else:
            # Show and handle deselect button
            self.back_button.draw(screen, mouse_pos)
            if mouse_pressed[0] and self.back_button.is_clicked(mouse_pos) and self.can_move_back:
                self.move_back_variable = True
                self.can_move_back = False
                print(self.can_move_back)
                self.set_position(self.original_pos)
                self.selected = False
                print(self.target_pos)
                
                    
    def draw(self):
        """Draw border and profile image based on state."""
        color = gold if self.selected else white if self.hovered else black
        pygame.draw.rect(screen, color, self.decor_rect)
        screen.blit(self.profile, self.profile_rect)

    def draw_icon(self, center_pos, small=False, hero_sp=False):
        """
        Draw small or large icon with black border (used in-game).
        
        Args:
            center_pos (tuple): Center position for the icon.
            small (bool): If True, use ingame size (25x25).
        """
        profile = self.ingame_profile if small else self.profile
        size = self.INGAME_SIZE if small else self.PROFILE_SIZE
        offset = self.DECOR_OFFSET_SMALL if small else self.DECOR_OFFSET_LARGE
        border = self.DECOR_SIZE_SMALL if small else self.DECOR_SIZE_LARGE
        if small == 'smallest':
            offset = (15, 15)
            border = self.DECOR_SIZE_SMALLEST

        if hero_sp:
            color = gold
        elif hero_sp == 'item':
            color = cyan2
        else:
            color = black

        rect = profile.get_rect(center=center_pos)
        decor = pygame.Rect(rect.centerx - offset[0], rect.centery - offset[1], border[0], border[1])
        pygame.draw.rect(screen, color, decor)
        screen.blit(profile, rect)

        # Display cooldown if applicable
        if hasattr(self.class_item, 'cooldown') and self.class_item.cooldown > 0 and not global_vars.PAUSED:
            current_time = pygame.time.get_ticks() / 1000 - global_vars.PAUSED_TOTAL_DURATION / 1000
            remaining = self.class_item.cooldown - (current_time - self.class_item.last_used)
            if remaining > 0:
                font = global_vars.get_font(15)
                text = font.render(f"{math.ceil(remaining)}", True, red)
                screen.blit(text, (center_pos[0] - text.get_width()//2, center_pos[1] - 30))
            else:
                font = global_vars.get_font(15)
                text = font.render("ready", True, green)
                screen.blit(text, (center_pos[0] - text.get_width()//2, center_pos[1] - 30))

    
    
    def is_selected(self):
        return self.selected

    def get_associated(self):
        """Return the associated hero class or item."""
        return self.class_item

    def show_hover_tooltip(self, position):
        """Display hero info tooltip on hover with detailed stats and trait."""
        if (self.hovered and
            isinstance(self.class_item, type) and
            issubclass(self.class_item, Player)):
            hero_name = self.class_item.__name__.replace("_", " ")
            if hero_name in HERO_INFO:
                # Get detailed hero stats and trait
                stats, trait_text, icon_path = get_hero_display_info(self.class_item)
                
                # Create and display info bubble using DisplaySkillInfo
                from button import DisplaySkillInfo
                info_bubble = DisplaySkillInfo(
                    image_path=text_box_img,
                    pos=position,
                    skill_name=hero_name,
                    skill_icon_path=icon_path,  # Could add hero portrait if desired
                    stats=stats,
                    info_text=trait_text,
                    font_path=global_vars.FONT_PATH,
                    font_size=font_size * 1.2,
                    text_color='white',
                    anchor='midbottom',
                    text_scale=1.1,
                    columns=3
                )
                info_bubble.drawing_info(screen)
        

       
# class PlayerSelector:
#     def __init__(self, image_path:str, position:tuple, value:object, size:int=(75, 75), decorxsize:int=85, decorysize:int=85, offsetdecor:int=(42, 42)):
#         self.position = position
#         self.value = value # item_class or hero_class

#         self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), size)
#         self.image_rect = self.image.get_rect(center = self.position)
        
#         self.button_rect = pygame.Rect(self.image_rect.centerx - offsetdecor[0], self.image_rect.centery - offsetdecor[1], decorxsize, decorysize)




class ImageBro:
    """
    Flexible tooltip:
    - fixed_size for manual control (items)
    - text_scale to make text smaller/bigger independently
    """
    def __init__(self, image_path, pos, text, font_path, font_size, text_color='white',
                 padding=(20, 20), min_size=(150, 100), player_info=False, anchor='topleft',
                 fixed_size=None, text_scale=1.0):  # <-- NEW: text_scale
        """
        Args:
            text_scale: float multiplier for font_size (e.g., 0.8 = 80% size)
            fixed_size: (w, h) for manual background size
        """
        self.original_bg = pygame.image.load(image_path).convert_alpha()
        
        # Effective font size
        effective_font_size = int(font_size * text_scale)
        self.font = global_vars.get_font(effective_font_size)
        self.text_color = text_color
        self.padding = padding

        # Text processing
        # handles , and @ separator
        self.text_lines = []
        def parse_block(block):
            """Split one block into sublines using @"""
            return block.split('@') if isinstance(block, str) else [str(block)]

        if isinstance(text, str):
            # Major sections split by comma
            sections = text.split(',')
            for sec in sections:
                self.text_lines.extend(parse_block(sec.strip()))

        elif isinstance(text, (list, tuple)):
            for entry in text:
                self.text_lines.extend(parse_block(entry))

        # Space after title if multi-line
        if len(self.text_lines) > 1:
            self.text_lines.insert(1, '')

        self.rendered_lines = [
            self.font.render(line, global_vars.TEXT_ANTI_ALIASING, text_color)
            for line in self.text_lines
        ]

        # Size logic
        if fixed_size:
            final_w, final_h = fixed_size
            self.background = pygame.transform.smoothscale(self.original_bg, (int(final_w), int(final_h)))
        else:
            # Auto-size with better width
            if self.rendered_lines:
                content_w = max(line.get_width() for line in self.rendered_lines)
                content_h = sum(line.get_height() for line in self.rendered_lines) + 10 * (len(self.rendered_lines) - 1)
            else:
                content_w = content_h = 0
            
            needed_w = content_w + padding[0] * 2
            needed_h = content_h + padding[1] * 2
            
            # Wider default for better readability
            final_w = max(needed_w, min_size[0] + 50, self.original_bg.get_width())  # +50 for comfort
            final_h = max(needed_h, min_size[1], self.original_bg.get_height())
            
            self.background = pygame.transform.smoothscale(self.original_bg, (int(final_w), int(final_h)))

        # Positioning
        self.rect = self.background.get_rect()
        setattr(self.rect, anchor, pos)
        self.rect.clamp_ip(screen.get_rect())

    def drawing_info(self, screen):
        screen.blit(self.background, self.rect)
        
        y = self.rect.top + self.padding[1]
        for line_surf in self.rendered_lines:
            x = self.rect.left + self.padding[0]
            screen.blit(line_surf, (x, y))
            y += line_surf.get_height() + 10


font_size = int(height * 0.02) # = 100
scale = 0.8
center_pos = (width / 2, height / 2)



#new vvvv
menu_button = ImageButton(
    image_path=menu_button_img,
    pos=(60, 25),
    scale=0.9,
    text='',
    font_path=resource_path('assets/font/slkscr.ttf'),  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

loading = ImageButton(
    image_path=loading_button_img,
    pos=center_pos,
    scale=0.8,
    text='',
    font_path=global_vars.FONT_PATH,  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

fight = ImageButton(
    image_path=text_box_img,
    pos=(width/2, height*0.9),
    scale=0.8,
    text='FIGHT!',
    font_path=global_vars.FONT_PATH,  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

done = ImageButton(
    image_path=text_box_img,
    pos=(width/2, height*0.9),
    scale=0.8,
    text='select',
    font_path=global_vars.FONT_PATH,  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING
)

def create_title(text, font=None, scale=1, y_offset=100, color=white, angle=0, modify_xpos=False):
    title = pygame.transform.rotozoom(font.render(f'{text}', global_vars.TEXT_ANTI_ALIASING, color), angle, scale)
    title_rect = title.get_rect(center = (width / 2, y_offset))
    if modify_xpos != False:
        title_rect.x = modify_xpos
    screen.blit(title, title_rect)
    # print(title_rect)


slot = ImageButton(
    image_path=resource_path('assets/UI/slot.png'),
    pos=(400, height - 20),
    scale=1,
    text='',
    font_path=resource_path('assets/font/slkscr.ttf'),  # or any other font path
    font_size=font_size,  # dynamic size ~29 at 720p
    text_color='white',
    text_anti_alias=global_vars.TEXT_ANTI_ALIASING,
    hover_move=0
)
# print('opening player selection')
# print(global_vars.SMOOTH_BG)

def auto_align(instant=True):
    for i in p1_items:
        i.original_pos = i.static_pos_1
        if not i.selected:
            i.set_position(i.original_pos, instant)

    for i in p2_items:
        i.original_pos = i.static_pos_1
        if not i.selected:
            i.set_position(i.original_pos, instant)


item_spacing_w = 7
item_max_y = 4
def paginating(move:bool, instant:bool = False, max_height = item_max_y):
        auto_align(instant)
        global item_page
        # print(f"Current Page = {item_page}")
        baseline = item_spacing_w * max_height
        total_page = ((len(p1_items)-1)//(baseline)) + 1
        # print(f"Baseline = {baseline}")
        # print(f" p1 items = {len(p1_items)}")
        # print(f" total page {total_page}")
        
        if move:
            if item_page < total_page:
                item_page += 1
        elif not move:
            if item_page > 1:
                item_page -= 1
        
                # p1_items[i].target_pos = p1_items[i].static_pos_1
            
        for i in range(baseline * (item_page-1), baseline * item_page):
            try:
                p1_items[i].original_pos = p1_items[i].static_pos_2
                # p1_items[i].target_pos = p1_items[i].static_pos_1
                if not p1_items[i].selected:
                    # print("this item is not selected")
                    # print(p1_items[i].static_pos_2)
                    # print(p1_items[i].original_pos)
                    p1_items[i].set_position(p1_items[i].original_pos)
                else:
                    print("selected item")
            except:
                print("out of bound")
                break

        for i in range(baseline * (item_page-1), baseline * item_page):
            try:
                p2_items[i].original_pos = p2_items[i].static_pos_2
                # p1_items[i].target_pos = p1_items[i].static_pos_1
                if not p2_items[i].selected:
                    # print("this item is not selected")
                    # print(p1_items[i].static_pos_2)
                    # print(p1_items[i].original_pos)
                    p2_items[i].set_position(p2_items[i].original_pos)
                else:
                    print("selected item")
            except:
                print("out of bound")
                break


def cleanup_networking():
    """Disconnect client and stop server to prevent port conflicts."""
    if global_vars.active_net_client is not None:
        try:
            global_vars.active_net_client.disconnect()
        except:
            pass
        global_vars.active_net_client = None
    import net_server
    try:
        net_server.stop_server()
    except:
        pass
    import net_client
    try:
        net_client.stop_lan_scanning()
    except:
        pass


def lan_connect(host_ip, port=5555, room_name=''):
    """Connect to host_ip:port as a client. Returns a reason why it got disconnected."""
    print('host ip: ', host_ip, ' port: ', port)
    from net_client import NetClient
    global_vars.active_net_client = NetClient(host_ip, port)
    try:
        global_vars.active_net_client.connect()
    except Exception as e:
        print(f"[CLIENT] Failed to connect: {e}")
        # Show a quick failure screen
        font = global_vars.get_font(40)
        t0 = pygame.time.get_ticks()
        while pygame.time.get_ticks() - t0 < 1500:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); exit()
            screen.fill((0, 0, 0))
            Animate_BG.smooth_waterfall_night_bg.display(screen, speed=50)
            txt = font.render(f"Failed to connect to {host_ip}", global_vars.TEXT_ANTI_ALIASING, red)
            screen.blit(txt, (width//2 - txt.get_width()//2, height//2))
            pygame.display.update()
            clock.tick(30)
        cleanup_networking()
        return 'fail'

    font = global_vars.get_font(30)
    cancel_btn = ImageButton(
        image_path=text_box_img,
        pos=(width // 2, int(height * 0.75)),
        scale=scale * 1.2,
        text='Cancel',
        font_path=r'assets\font\slkscr.ttf',
        font_size=font_size,
        text_color='white',
        text_anti_alias=global_vars.TEXT_ANTI_ALIASING
    )

    while global_vars.active_net_client.phase == 'connecting':
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global_vars.active_net_client.disconnect()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                cleanup_networking()
                return 'back_to_menu'
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if cancel_btn.is_clicked(event.pos):
                    cleanup_networking()
                    return 'back'

        screen.fill((0, 0, 0))
        Animate_BG.smooth_waterfall_night_bg.display(screen, speed=50)
        
        # Translucent Container
        box_w, box_h = int(width * 0.6), int(height * 0.45)
        box = pygame.Rect(width // 2 - box_w // 2, int(height * 0.22), box_w, box_h)
        overlay = pygame.Surface((box.width, box.height), pygame.SRCALPHA)
        overlay.fill((10, 10, 15, 220))
        screen.blit(overlay, box.topleft)
        pygame.draw.rect(screen, (80, 80, 100), box, 3)

        # Title
        txt = font.render(f"Room name: {room_name}", global_vars.TEXT_ANTI_ALIASING, white)
        screen.blit(txt, (width//2 - txt.get_width()//2, box.y + 60))

        # Show Host LAN IP
        if global_vars.active_net_client.my_player_type == 1:
            local_ip = _get_local_ip()
            ip_txt = global_vars.get_font(30).render(f"Your IP: {local_ip}", global_vars.TEXT_ANTI_ALIASING, (120, 220, 120))
            share_txt = global_vars.get_font(22).render("Share this address with the other player", global_vars.TEXT_ANTI_ALIASING, (160, 160, 160))
            screen.blit(ip_txt, (width // 2 - ip_txt.get_width() // 2, box.y + 130))
            screen.blit(share_txt, (width // 2 - share_txt.get_width() // 2, box.y + 180))
        else:
            conn_txt = global_vars.get_font(30).render(f"Connected. Waiting for game to start...", global_vars.TEXT_ANTI_ALIASING, (120, 220, 120))
            screen.blit(conn_txt, (width // 2 - conn_txt.get_width() // 2, box.y + 140))

        dots = "." * ((pygame.time.get_ticks() // 500) % 4)
        status_txt = global_vars.get_font(26).render(f"Waiting for opponent{dots}", global_vars.TEXT_ANTI_ALIASING, (200, 200, 200))
        screen.blit(status_txt, (width // 2 - status_txt.get_width() // 2, box.y + 240))

        cancel_btn.draw(screen, mouse_pos)
        pygame.display.update()
        clock.tick(60)

    if global_vars.active_net_client.phase == 'disconnected':
        cleanup_networking()
        return 'fail'

    result = player_selection(net_client=global_vars.active_net_client)
    print("player_selection returned:", result)

    # Always tear the client/server down on every exit path so the player who
    # leaves (host or joiner) actually drops the socket. The server's finally
    # block then notifies the remaining player with 'opponent_left'.
    cleanup_networking()
    if result == 'opponent_left':
        return 'opponent_left'
    elif result == 'back_to_menu':
        return 'back_to_menu'
    else:
        print('its me :)')
        return 'done'



def _get_local_ip():
    """Best-effort LAN IP of this machine (to show the host so the joiner can connect)."""
    import socket as _socket
    s = _socket.socket(_socket.AF_INET, _socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))  # no packets sent; just picks the outbound interface
        return s.getsockname()[0]
    except Exception:
        return '127.0.0.1'
    finally:
        s.close()


def _mp_draw_bg(title):
    screen.fill((0, 0, 0))
    Animate_BG.smooth_waterfall_night_bg.display(screen, speed=50)
    t = global_vars.get_font(80).render(title, global_vars.TEXT_ANTI_ALIASING, white)
    screen.blit(t, (width // 2 - t.get_width() // 2, int(height * 0.12)))


def _mp_text(text, size, color, cy):
    surf = global_vars.get_font(size).render(text, global_vars.TEXT_ANTI_ALIASING, color)
    rect = surf.get_rect(center=(width // 2, cy))
    screen.blit(surf, rect)
    return rect


def prompt_room_name(default_name="", max_chars=14):
    """Ask the host for a room name using the reusable TextInputField. Returns the
    typed name, or None if the player cancelled (ESC / Cancel button)."""
    from text_input_field import TextInputField

    field = TextInputField(
        x=width // 2 - int(width * 0.25), y=int(height * 0.44),
        width=int(width * 0.5), height=70,
        font=global_vars.get_font(40),
        max_chars=max_chars,
        text=default_name,
        placeholder="Enter room name",
        active=True,
    )

    host_btn = ImageButton(
        image_path=text_box_img,
        pos=(width // 2 - 140, int(height * 0.65)),
        scale=1.2, text='Host',
        font_path=r'assets\font\slkscr.ttf',
        font_size=font_size, text_color='white',
        text_anti_alias=global_vars.TEXT_ANTI_ALIASING,
    )
    cancel_btn = ImageButton(
        image_path=text_box_img,
        pos=(width // 2 + 140, int(height * 0.65)),
        scale=1.2, text='Cancel',
        font_path=r'assets\font\slkscr.ttf',
        font_size=font_size, text_color='white',
        text_anti_alias=global_vars.TEXT_ANTI_ALIASING,
    )

    while True:
        dt = clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            result = field.handle_event(event)
            if result == 'submit':
                return field.get_text().strip()
            if result == 'cancel':
                return None
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if host_btn.is_clicked(event.pos):
                    return field.get_text().strip()
                elif cancel_btn.is_clicked(event.pos):
                    return None

        field.update(dt)
        _mp_draw_bg("HOST GAME")
        _mp_text("Room Name", 30, (200, 200, 200), int(height * 0.38))
        field.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        host_btn.draw(screen, mouse_pos)
        cancel_btn.draw(screen, mouse_pos)
        pygame.display.update()


def host_game():
    """Start the relay server in-process and connect to it as Player 1 (host).
    Once we're the host we stop LAN scanning so we never also appear as / act as
    a joiner of another room."""
    import net_client
    net_client.stop_lan_scanning()

    # Ask for a room name first; cancelling backs out to the lobby.
    room_name = prompt_room_name()
    if room_name is None:
        return None

    cleanup_networking()
    import net_server
    thread, bound_port = net_server.start_background_server(room_name=room_name)
    if thread is None:
        print("[HOST] No free port available to host.")
        return 'fail'
    return lan_connect('127.0.0.1', bound_port, room_name=room_name)


def join_game():
    """Minecraft-style 'Direct Connect': type the host's IP, then connect as Player 2."""
    cleanup_networking()
    info_font_size = 30
    scale_btn = 1.2

    from text_input_field import TextInputField
    ip_field = TextInputField(
        x=width // 2 - int(width * 0.5) // 2,  # same as: width//2 - box_w//2
        y=int(height * 0.44),                   # same y
        width=int(width * 0.5),                 # same box_w
        height=70,                              # same box_h
        font=global_vars.get_font(40),          # same font
        # text="127.0.0.1",                       # pre-filled default
        max_chars=21,                           # matches len(ip) < 21 guard
        allowed_chars="0123456789.",            # same char whitelist
        text_color=white,                       # (255,255,255)
        bg_color=(25, 25, 25),                  # same fill
        border_color=(200, 200, 200),           # same inactive border
        active_border_color=(255, 215, 0),      # gold highlight when focused
        border_width=3,                         # same border thickness
        padding_x=18,                           # matches midleft offset of 18
        active=True,                            # always focused (same as original)
        placeholder="127.0.0.1",                 
    )

    connect_btn = ImageButton(
        image_path=text_box_img,
        pos=(width // 2 - 140, int(height * 0.65)),
        scale=scale_btn,
        text='Connect',
        font_path=r'assets\font\slkscr.ttf',
        font_size=font_size,
        text_color='white',
        text_anti_alias=global_vars.TEXT_ANTI_ALIASING
    )
    cancel_btn = ImageButton(
        image_path=text_box_img,
        pos=(width // 2 + 140, int(height * 0.65)),
        scale=scale_btn,
        text='Cancel',
        font_path=r'assets\font\slkscr.ttf',
        font_size=font_size,
        text_color='white',
        text_anti_alias=global_vars.TEXT_ANTI_ALIASING
    )

    while True:
        # print(ip)
        dt = clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()

            result = ip_field.handle_event(event)
            if result == 'submit':
                if ip_field.get_text().strip():
                    return lan_connect(ip_field.get_text().strip())
            if result == 'cancel':
                return None
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if connect_btn.is_clicked(event.pos):
                    if connect_btn.is_clicked(event.pos):
                        if ip_field.get_text().strip():
                            return lan_connect(ip_field.get_text().strip())
                elif cancel_btn.is_clicked(event.pos):
                    return None

        _mp_draw_bg("JOIN GAME")
        _mp_text("Host Address", info_font_size, (200, 200, 200), int(height * 0.38))

        ip_field.draw(screen, global_vars.TEXT_ANTI_ALIASING)
        ip_field.update(dt) 

        connect_btn.draw(screen, mouse_pos)
        cancel_btn.draw(screen, mouse_pos)
        pygame.display.update()


def multiplayer_menu(notice=None):
    """YOMIH-style multiplayer lobby menu: displays a list of active LAN games,
    and buttons to Host, Direct Connect, Play Local PvP, or Back.

    `notice` shows a transient banner at the top of the menu. It is set when the
    player is returned here because a session ended (e.g. 'opponent_left' ->
    'Opponent Left'). It is never set when the menu is opened normally."""
    import net_client
    cleanup_networking()
    net_client.start_lan_scanning()

    # Map a session-end reason to the banner text shown at the top of the menu.
    _NOTICE_TEXT = {'opponent_left': 'Opponent Left', 'disconnected': 'Disconnected'}
    notice_text = _NOTICE_TEXT.get(notice)
    notice_start = pygame.time.get_ticks() if notice_text else None
    NOTICE_DURATION = 5000  # ms

    scale_btn = 1.2 
    host_btn = ImageButton(
        image_path=text_box_img,
        pos=(int(width * 0.75), int(height * 0.35)),
        scale=scale_btn,
        text='Host LAN Game',
        font_path=r'assets\font\slkscr.ttf',
        font_size=font_size,
        text_color='white',
        text_anti_alias=global_vars.TEXT_ANTI_ALIASING
    )
    direct_btn = ImageButton(
        image_path=text_box_img,
        pos=(int(width * 0.75), int(height * 0.48)),
        scale=scale_btn,
        text='Direct Connect',
        font_path=r'assets\font\slkscr.ttf',
        font_size=font_size,
        text_color='white',
        text_anti_alias=global_vars.TEXT_ANTI_ALIASING
    )
    local_btn = ImageButton(
        image_path=text_box_img,
        pos=(int(width * 0.75), int(height * 0.61)),
        scale=scale_btn,
        text='Local PvP',
        font_path=r'assets\font\slkscr.ttf',
        font_size=font_size,
        text_color='white',
        text_anti_alias=global_vars.TEXT_ANTI_ALIASING
    )
    back_btn = ImageButton(
        image_path=text_box_img,
        pos=(int(width * 0.75), int(height * 0.74)),
        scale=scale_btn,
        text='Back to Menu',
        font_path=r'assets\font\slkscr.ttf',
        font_size=font_size,
        text_color='white',
        text_anti_alias=global_vars.TEXT_ANTI_ALIASING
    )

    import net_server
    while True:
        mouse_pos = pygame.mouse.get_pos()
        my_ip = _get_local_ip()
        # Hide only THIS host's own beacon (ip:port). Other hosts on the same
        # machine use a different port and must stay visible/joinable.
        my_key = f"{my_ip}:{net_server.get_server_port()}" if global_vars.active_net_client else None
        servers = {k: v for k, v in net_client.get_active_servers().items() if k != my_key}
        # print(servers)

        # If we're currently hosting, we must NOT be able to join another host
        # (host-to-host). The browser still SHOWS other rooms (so the host can
        # see who else is up), but their entries are disabled/non-clickable.
        am_hosting = (
            global_vars.active_net_client is not None
            and global_vars.active_net_client.my_player_type == 1
        )

        panel_rect = pygame.Rect(int(width * 0.08), int(height * 0.28), int(width * 0.44), int(height * 0.52))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                net_client.stop_lan_scanning()
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    net_client.stop_lan_scanning()
                    cleanup_networking()
                    return 'back_to_menu'
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Launch a LAN session. If it ends because the opponent left,
                # stay in this menu and show a banner; otherwise leave the menu.
                global_vars.SINGLE_MODE_ACTIVE = False # fix bug where selecting single player, then leaving, sets the SINGLE_MODE_ACTIVE to true, even in multiplayer LAN.
                session = None
                if host_btn.is_clicked(event.pos):
                    net_client.stop_lan_scanning()
                    session = host_game()
                elif direct_btn.is_clicked(event.pos):
                    net_client.stop_lan_scanning()
                    session = join_game()
                elif local_btn.is_clicked(event.pos):
                    net_client.stop_lan_scanning()
                    
                    return player_selection(net_client=None)
                elif back_btn.is_clicked(event.pos):
                    net_client.stop_lan_scanning()
                    cleanup_networking()
                    return 'back_to_menu'
                elif not am_hosting:
                    # Check server browser clicks. Disabled entirely while hosting
                    # so a host can never join another host.
                    room_y = panel_rect.y + 60
                    for key, (name, ip, port) in list(servers.items())[:5]:
                        btn_rect = pygame.Rect(panel_rect.x + 20, room_y, panel_rect.width - 40, 60)
                        if btn_rect.collidepoint(event.pos):
                            net_client.stop_lan_scanning()
                            session = lan_connect(ip, port)
                            break
                        room_y += 75

                if session in ('opponent_left', 'disconnected', 'back'):
                    # Survivor returns to the lobby with a transient notice.
                    notice_text = _NOTICE_TEXT.get(session)
                    notice_start = pygame.time.get_ticks()
                    cleanup_networking()
                    net_client.start_lan_scanning()
                    break  # re-evaluate the loop fresh with the banner armed
                elif session is not None:
                    # back_to_menu / done / fail / None -> leave the lobby.
                    return session

        _mp_draw_bg("MULTIPLAYER LOBBY")

        # Draw Right Panel buttons
        host_btn.draw(screen, mouse_pos)
        direct_btn.draw(screen, mouse_pos)
        local_btn.draw(screen, mouse_pos)
        back_btn.draw(screen, mouse_pos)

        # Draw Left Panel Container
        pygame.draw.rect(screen, (15, 15, 20), panel_rect)
        pygame.draw.rect(screen, (80, 80, 100), panel_rect, 2)

        # Title of Left Panel
        panel_title = global_vars.get_font(26).render("ACTIVE LAN SESSIONS", global_vars.TEXT_ANTI_ALIASING, (180, 180, 220))
        screen.blit(panel_title, (panel_rect.x + 20, panel_rect.y + 15))

        # Draw active rooms inside panel
        room_y = panel_rect.y + 60
        if not servers:
            blink_scan = (pygame.time.get_ticks() // 400) % 4
            scan_text = "Scanning for LAN lobbies" + ("." * blink_scan)
            txt_surf = global_vars.get_font(20).render(scan_text, global_vars.TEXT_ANTI_ALIASING, (140, 140, 140))
            screen.blit(txt_surf, (panel_rect.centerx - txt_surf.get_width() // 2, panel_rect.centery))
        else:
            for key, (name, ip, port) in list(servers.items())[:5]:
                btn_rect = pygame.Rect(panel_rect.x + 20, room_y, panel_rect.width - 40, 60)
                # While hosting, rooms are shown but greyed out (not joinable).
                is_hovered = btn_rect.collidepoint(mouse_pos) and not am_hosting

                # Draw room button
                if am_hosting:
                    bg_color = (20, 20, 24)
                    border_color = (45, 45, 55)
                    text_color = (110, 110, 120)
                else:
                    bg_color = (45, 50, 65) if is_hovered else (25, 28, 35)
                    border_color = gold if is_hovered else (60, 65, 80)
                    text_color = white

                pygame.draw.rect(screen, bg_color, btn_rect)
                pygame.draw.rect(screen, border_color, btn_rect, 2)

                # Text inside: show the broadcast room name (falls back to
                # "Game ip:port" when the host didn't set one), then the address.
                label = f"{name} - {ip}"#:{port}"
                room_text = global_vars.get_font(22).render(label, global_vars.TEXT_ANTI_ALIASING, text_color)
                screen.blit(room_text, (btn_rect.x + 20, btn_rect.centery - room_text.get_height() // 2))
                room_y += 75

        # Transient banner shown only when we were returned here after a session
        # ended (opponent left / disconnected). Auto-clears after NOTICE_DURATION.
        if notice_text and notice_start is not None:
            if pygame.time.get_ticks() - notice_start < NOTICE_DURATION:
                banner = global_vars.get_font(40).render(notice_text, global_vars.TEXT_ANTI_ALIASING, red)
                screen.blit(banner, (width // 2 - banner.get_width() // 2, int(height * 0.04)))
            else:
                notice_text = None
                notice_start = None

        pygame.display.update()
        clock.tick(60)





def wait_screen(condition_func, text="Waiting for something...", background=None, font=25):
    wait_font = global_vars.get_font(font)
    while not condition_func():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        _nc = global_vars.active_net_client
        if _nc is None or _nc.phase == 'disconnected' or _nc.opponent_left:
            return 'opponent_left'          
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((0, 0, 0))

        wait_text = wait_font.render(text, True, white)
        screen.blit(wait_text, (width // 2 - wait_text.get_width() // 2, height // 2))
        pygame.display.update()
        clock.tick(30)

# from global_vars import quick_run_hero1, quick_run_hero2
def player_selection(net_client=None):
    global map_selected
    # print('player selection opened')
    # print(global_vars.SMOOTH_BG)
    global PLAYER_1_SELECTED_HERO, PLAYER_2_SELECTED_HERO, hero1, hero2, hero1_group, hero2_group, bot, bot_group, hero3_group, hero3
    global p1_select, p2_select, p1_items, p2_items
    # global_vars.SMOOTH_BG = not global_vars.SMOOTH_BG
    background = pygame.transform.scale(
        pygame.image.load(resource_path('assets/backgrounds/12.png')).convert(), (width, height))

    font = global_vars.get_font(50)
    default_size = (((width*0.2) * DEFAULT_HEIGHT) / ((height*0.2) * DEFAULT_WIDTH))

    #upper position PlayerSelector(wind_hashashin_icon, (75, height - 75 * 3), Wind_Hashashin)
    #p1
    addd=int(width * 0.0079)#10 
    # yposlower=75
    # yposupper=200

    yposlower=int(height * 0.10417 ) #75
    yposupper=int(height * 0.2778) #200

    xpos1=width - int(yposlower * 7)+addd # 535
    xpos2=width - int(yposlower * 5.5)+addd # 422
    xpos3=width - int(yposlower * 4)+addd #310
    xpos4=width - int(yposlower * 2.5)+addd #197
    xpos5=width - int(yposlower)+addd #85

    #difference 112.5
    # last is only 75 position for xpos4

    #p2
    temp_icon = resource_path('assets/hero profiles/temp.jpg')
    
    # Heroes (large icons — default size)

    p1_select = []

    p1_select = [
        PlayerSelector(fire_wizard_icon, (xpos1, height - yposlower), Fire_Wizard),
        PlayerSelector(wanderer_magician_icon, (xpos2, height - yposlower), Wanderer_Magician),
        PlayerSelector(fire_knight_icon, (xpos3, height - yposlower), Fire_Knight),
        PlayerSelector(phantom_assassin_icon, (xpos4, height - yposlower), Phantom_Assassin),
        PlayerSelector(chthulu_icon, (xpos5, height - yposlower), Chthulu),


        PlayerSelector(wind_hashashin_icon, (xpos3, height - yposupper), Wind_Hashashin),
        PlayerSelector(water_princess_icon, (xpos2, height - yposupper), Water_Princess),
        PlayerSelector(forest_ranger_icon, (xpos1, height - yposupper), Forest_Ranger),
        PlayerSelector(yurei_icon, (xpos4, height - yposupper), Yurei),
    ]

    p2_select = [
        PlayerSelector(fire_wizard_icon, (xpos1, height - yposlower), Fire_Wizard),
        PlayerSelector(wanderer_magician_icon, (xpos2, height - yposlower), Wanderer_Magician),
        PlayerSelector(fire_knight_icon, (xpos3, height - yposlower), Fire_Knight),
        PlayerSelector(phantom_assassin_icon, (xpos4, height - yposlower), Phantom_Assassin),
        PlayerSelector(chthulu_icon, (xpos5, height - yposlower), Chthulu),

        PlayerSelector(wind_hashashin_icon, (xpos3, height - yposupper), Wind_Hashashin),
        PlayerSelector(water_princess_icon, (xpos2, height - yposupper), Water_Princess),
        PlayerSelector(forest_ranger_icon, (xpos1, height - yposupper), Forest_Ranger),
        PlayerSelector(yurei_icon, (xpos4, height - yposupper), Yurei),
    ]
    

    # positioning
    upper=height * 0.76
    item_gap_x = width * 0.05859375
    item_gap_y = 100

   
    def position_alignnment_Y(max_width:int, indexed:int, max_height:int = item_max_y, height_gap = upper, item_gap_x = item_gap_x, item_gap_y = item_gap_y):
        baseline = (max_height * max_width)
        indexed = indexed - 1
        indexed = indexed % baseline

        new_indexed = 1 + (indexed - (max_width) * ((indexed) // (max_width)))
        # print(f"{indexed} - ({max_width}) * ({indexed}) // ({1+ max_width})")
        # print(f"{item_gap_x} - {new_indexed}, {height} - ({upper} - ({item_gap_y} * ({indexed}) // (1 + {max_width})))))")
        return ((item_gap_x * new_indexed),height - (height_gap - (item_gap_y * ((indexed) // (max_width)))))

    



    # Items (small icons — use small=True)
    p1_items = []
    for x,y in enumerate(items):
        p1_items.append(PlayerSelector(
            y.image, 
            position_alignnment_Y(item_spacing_w, x+1), 
            y, 
            small=True,
            static_pos = (width - (width * 1.1),position_alignnment_Y(item_spacing_w, x+1)[1]))
            )

    p2_items = []
    for x,y in enumerate(items):
        p2_items.append(PlayerSelector(
            y.image, 
            position_alignnment_Y(item_spacing_w, x+1), 
            y, 
            small=True,
            static_pos = (width - (width * 1.1),position_alignnment_Y(item_spacing_w, x+1)[1]))
            )

    # Maps (custom large size)
    map_select = [
        PlayerSelector(waterfall_icon, (width*0.1172, height - (75*6)), Animate_BG.waterfall_bg, custom_size=(200, 125)),
        PlayerSelector(lava_icon, (width/2 - (55 * 3), height - (75*6)), Animate_BG.lava_bg, custom_size=(200, 125)),
        PlayerSelector(dark_forest_icon, (width/2 + (55 * 3), height - (75*6)), Animate_BG.dark_forest_bg, custom_size=(200, 125)),
        PlayerSelector(trees_icon, (width * 0.8828, height - (75*6)), Animate_BG.trees_bg, custom_size=(200, 125)),
        PlayerSelector(global_vars.mountains_icon, (width*0.1172, height - (75*3)), Animate_BG.mountains_bg, custom_size=(200, 125)),
        PlayerSelector(global_vars.sunset_icon, (width/2 - (width*0.1289), height - (75*3)), Animate_BG.sunset_bg, custom_size=(200, 125)),
        PlayerSelector(global_vars.city_icon, (width/2 + (width*0.1289), height - (75*3)), Animate_BG.city_bg, custom_size=(200, 125)),
    ]


    equipped_items = EquippedItem(p1_items)
    equipped_items_p2 = EquippedItem(p2_items)

    player_1_choose = True
    player_2_choose = False
    map_choose = False

    map_selected = Animate_BG.dark_forest_bg # Default

    # ── Phase 2: map name ↔ Animate_BG lookup for LAN sync ──
    _map_name_to_bg = {
        'waterfall': Animate_BG.waterfall_bg,
        'lava': Animate_BG.lava_bg,
        'dark_forest': Animate_BG.dark_forest_bg,
        'trees': Animate_BG.trees_bg,
        'mountains': Animate_BG.mountains_bg,
        'sunset': Animate_BG.sunset_bg,
        'city': Animate_BG.city_bg,
    }
    _bg_to_map_name = {v: k for k, v in _map_name_to_bg.items()}

    go = False

    immediate_run = IMMEDIATE_RUN # for dev option only

    from button import RectButton
    all_items_button = RectButton((width/2), height*0.8, global_vars.FONT_PATH, int(height * 0.025), (0, 255, 0), "All Items")
    x2_bot = RectButton((width/2), height*0.5, global_vars.FONT_PATH, int(height * 0.025), (0, 255, 0), "2x Bot")
    random_p1 = RectButton((width/2), height*0.7, global_vars.FONT_PATH, int(height * 0.025), (0, 255, 0), "Random Hero")
    random_p2 = RectButton((width/2), height*0.7, global_vars.FONT_PATH, int(height * 0.025), (0, 255, 0), "Random Hero")

    random_p1_item = RectButton((width/2), height*0.6, global_vars.FONT_PATH, int(height * 0.025), (0, 255, 0), "Random Item")
    random_p2_item = RectButton((width/2), height*0.6, global_vars.FONT_PATH, int(height * 0.025), (0, 255, 0), "Random Item")


    next_page_button = RectButton((width/3.5), height*0.75, global_vars.FONT_PATH, int(height * 0.025), (0, 255, 0), ">", height_position=0)
    back_page_button = RectButton((width/6), height*0.75, global_vars.FONT_PATH, int(height * 0.025), (0, 255, 0), "<", height_position=0)

    toggle_bot_button = RectButton((width/2), height*0.8, global_vars.FONT_PATH, int(height * 0.025), (0, 255, 0), "Toggle Bot")
    # chosen hero will be the name
    def get_name(v:str):
        r = v.split('_')
        if len(r) == 2:
            return r[0] + (' '  + r[1])
        elif len(r) == 3:
            return r[0] +  (' ' + r[1]) +  (' ' + r[2])
        else:
            return r[0]
    paginating(False, True)
    
    while True:
        if immediate_run: # DEV OPTION ONLY
            PLAYER_1_SELECTED_HERO = Phantom_Assassin
            PLAYER_2_SELECTED_HERO = Wind_Hashashin
            map_selected = Animate_BG.city_bg # Default
            bot = create_bot(Wanderer_Magician, hero1, hero1) if global_vars.SINGLE_MODE_ACTIVE else None
            player_1_choose = False
            map_choose = True
            go = True
        

        # LAN: auto-skip the turn that doesn't belong to this client
        if global_vars.active_net_client is not None:
            if global_vars.active_net_client.my_player_type == 1 and player_2_choose:
                # P1 has picked, now waiting — skip P2 UI, go straight to map
                player_2_choose = False
                map_choose = True
                go = False
            elif global_vars.active_net_client.my_player_type == 2 and player_1_choose:
                # P2 skips P1 UI, goes straight to picking their own hero
                player_1_choose = False
                player_2_choose = True
                go = False
        # check if opponent disconnected
        if global_vars.active_net_client is not None and global_vars.active_net_client.opponent_left:
            # global_vars.active_net_client.opponent_left = False
            # global_vars.active_net_client.disconnect()
            # print("Opponent left detected in player_selection")
            return 'opponent_left'
        # print('running')
        # print(global_vars.MAIN_VOLUME)
        # return
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()

        screen.fill((0, 0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if global_vars.active_net_client is not None:
                    global_vars.active_net_client.disconnect()
                pygame.quit()
                exit()   
            if keys[pygame.K_ESCAPE]:
                if global_vars.active_net_client is not None and global_vars.active_net_client.opponent_left:
                    # global_vars.active_net_client.opponent_left = False
                    # print(f'I am leaving good luck everybody')
                    # print("Opponent left detected in player_selection")
                    return 'opponent_left'
                else:
                    print('going back to menu?')
                    return 'back_to_menu'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.is_clicked(event.pos):
                    if global_vars.active_net_client is not None and global_vars.active_net_client.opponent_left:
                        # global_vars.active_net_client.opponent_left = False
                        # print(f'I am leaving good luck everybody')
                        # print("Opponent left detected in player_selection")
                        return 'opponent_left'
                    else:
                        print('going back to menu?')
                        return 'back_to_menu'

                if all_items_button.is_clicked(event.pos):
                    if player_2_choose:
                        global_vars.all_items = all_items_button.toggle(global_vars.all_items)
                if x2_bot.is_clicked(event.pos):
                    if player_2_choose:
                        global_vars.toggle_hero3 = x2_bot.toggle(global_vars.toggle_hero3)
                if random_p1.is_clicked(event.pos):
                    if player_1_choose:
                        global_vars.random_pick_p1 = random_p1.toggle(global_vars.random_pick_p1)
                if random_p2.is_clicked(event.pos):
                    if player_2_choose:
                        global_vars.random_pick_p2 = random_p2.toggle(global_vars.random_pick_p2)
                if toggle_bot_button.is_clicked(event.pos):
                    if player_1_choose:
                        global_vars.HERO1_BOT = toggle_bot_button.toggle(global_vars.HERO1_BOT)
                if random_p1_item.is_clicked(event.pos):
                    if player_1_choose:
                        global_vars.random_item_pick_p1 = random_p1_item.toggle(global_vars.random_item_pick_p1)
                if random_p2_item.is_clicked(event.pos):
                    if player_2_choose:
                        global_vars.random_item_pick_p2 = random_p2_item.toggle(global_vars.random_item_pick_p2)
                if next_page_button.is_clicked(event.pos):
                    paginating(True)
                if back_page_button.is_clicked(event.pos):
                    paginating(False)

        # screen.blit(background, (0, 0))
        Animate_BG.waterfall_night_bg.display(screen, speed=50) if not global_vars.SMOOTH_BG else Animate_BG.smooth_waterfall_night_bg.display(screen, speed=50)
        if not go:
            create_title('Hero Selection', font, default_size, height * 0.1, modify_xpos=width*0.05) if not map_choose else None
        else:
            create_title('Item Selection', font, default_size, height * 0.1, modify_xpos=width*0.05) if not map_choose else None
        menu_button.draw(screen, mouse_pos)
        slot.draw(screen, mouse_pos) if not map_choose else None

        if player_1_choose and (global_vars.active_net_client is None or global_vars.active_net_client.my_player_type == 1): 
            if not go:                  
                create_title('PLAYER 1', font, default_size, height * 0.1, modify_xpos=width*0.5) #height*0., default_size - 0.55
            else: #display selected hero name
                create_title(get_name(PLAYER_1_SELECTED_HERO.__name__), font, default_size, height * 0.1, modify_xpos=width*0.5)
                
            # hero1 bot Option (has all_items) draws hard mode option
            toggle_bot_button.update(mouse_pos, global_vars.HERO1_BOT)
            toggle_bot_button.draw(screen, global_vars.TEXT_ANTI_ALIASING)
            
            random_p1.update(mouse_pos, global_vars.random_pick_p1)
            random_p1.draw(screen, global_vars.TEXT_ANTI_ALIASING)
            random_p1_item.update(mouse_pos, global_vars.random_item_pick_p1)
            random_p1_item.draw(screen, global_vars.TEXT_ANTI_ALIASING)

            # print(pygame.mouse.get_pressed())
            
            # fire_wizard_select.update(mouse_pos, mouse_press)
            # wanderer_magician_select.update(mouse_pos, mouse_press)

            for selector in p1_select:
                selector.update(mouse_pos, mouse_press, p1_select, max_selected=1)
                


            for selector in p1_select:
                if selector.hovered:
                    selector.show_hover_tooltip(mouse_pos)
                    # selector.the_info((width + (width * 0.322), height - 525)) #previous position
                if selector.is_selected(): # when hero selection
                    PLAYER_1_SELECTED_HERO = selector.get_associated()
                    create_title(f"{item_page}", font, 0.5, height * 0.78, modify_xpos=width*0.24)
                    next_page_button.update(mouse_pos, (True if next_page_button.is_clicked(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] else False))
                    next_page_button.draw(screen, global_vars.TEXT_ANTI_ALIASING)

                    back_page_button.update(mouse_pos, (True if back_page_button.is_clicked(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] else False))
                    back_page_button.draw(screen, global_vars.TEXT_ANTI_ALIASING)

                    if selector.selected:
                        selector.set_position((75, height- (height * 0.07)))

                    # Draw item selection
                    for item in p1_items:
                        item.update(mouse_pos, mouse_press, p1_items, max_selected=MAX_ITEM)
                        if item.selected:
                            if item in equipped_items.item:
                                continue
                            indexed = len(equipped_items.item)
                            item.set_position((item_equip_hashmap[indexed], height-(height * 0.139)))
                            equipped_items.add(item)
                            
                        equipped_items.update()
                        # print(equipped_items.item)

                            # print(item.original_pos)    
                            # print(item.target_pos)
                            
                    for item in p1_items:
                        item.draw()


                    for item in p1_items:
                        if item.hovered:
                            # item.class_item.update((width + (width * 0.322), height - 500))
                            item.class_item.update(mouse_pos)


                    # randoms = [1,5,7,8]
                    # p1_items[randoms[0]].selected = True


                    
                    # print(selector.get_associated())
                    go = True
                    break  # Only one can be selected
                else:
                    go = False
                    

            if go:
                done.draw(screen, mouse_pos)
                if pygame.mouse.get_pressed()[0] and done.is_clicked(mouse_pos) or keys[pygame.K_SPACE]:
                    loading.draw(screen, pygame.mouse.get_pos())
                    pygame.display.update()
                    pygame.time.delay(100)

                    player_1_choose = False
                    player_2_choose = True
                    go = False


        if player_2_choose and (global_vars.active_net_client is None or global_vars.active_net_client.my_player_type == 2):
            if not go:
                create_title('PLAYER 2', font, default_size, height * 0.1, modify_xpos=width*0.5)
            else:
                create_title(get_name(PLAYER_2_SELECTED_HERO.__name__), font, default_size, height * 0.1, modify_xpos=width*0.5)
            
            # Hard Bot Option (has all_items) draws hard mode option
            if global_vars.SINGLE_MODE_ACTIVE:
                all_items_button.update(mouse_pos, global_vars.all_items)
                all_items_button.draw(screen, global_vars.TEXT_ANTI_ALIASING)
                x2_bot.update(mouse_pos, global_vars.toggle_hero3)
                x2_bot.draw(screen, global_vars.TEXT_ANTI_ALIASING)
            random_p2.update(mouse_pos, global_vars.random_pick_p2)
            random_p2.draw(screen, global_vars.TEXT_ANTI_ALIASING)
            random_p2_item.update(mouse_pos, global_vars.random_item_pick_p2)
            random_p2_item.draw(screen, global_vars.TEXT_ANTI_ALIASING)

            for selector in p2_select:
                selector.update(mouse_pos, mouse_press, p2_select, max_selected=1)

            for selector in p2_select:
                if selector.hovered:
                    selector.show_hover_tooltip(mouse_pos)
                if selector.is_selected():
                    create_title(f"{item_page}", font, 0.5, height * 0.78, modify_xpos=width*0.24)
                    PLAYER_2_SELECTED_HERO = selector.get_associated()
                    next_page_button.update(mouse_pos, (True if next_page_button.is_clicked(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] else False))
                    next_page_button.draw(screen, global_vars.TEXT_ANTI_ALIASING)

                    back_page_button.update(mouse_pos, (True if back_page_button.is_clicked(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] else False))
                    back_page_button.draw(screen, global_vars.TEXT_ANTI_ALIASING)

                    if selector.selected:
                        selector.set_position((75, height-50))

                
        



                    for item in p2_items:
                        item.update(mouse_pos, mouse_press, p2_items, max_selected=MAX_ITEM)
                        if item.selected:
                            if item in equipped_items_p2.item:
                                continue
                            indexed = len(equipped_items_p2.item)
                            item.set_position((item_equip_hashmap[indexed], height-100))
                            equipped_items_p2.add(item)
                            
                        equipped_items_p2.update()
                        

                    for item in p2_items:
                        item.draw()

            
                    for item in p2_items:
                        if item.hovered:
                            item.class_item.update(mouse_pos)
                            # item.class_item.update((-(width * 0.0001), height - 500)) #previous position
                

                    
                    
                    
                    # print(PLAYER_2_SELECTED_HERO)
                    go = True
                    break
                else:
                    go = False
                    
                    

            if go:
                done.draw(screen, mouse_pos)
                if pygame.mouse.get_pressed()[0] and done.is_clicked(mouse_pos) or keys[pygame.K_SPACE]:
                    loading.draw(screen, pygame.mouse.get_pos())
                    pygame.display.update()
                    pygame.time.delay(100)

                    player_2_choose = False
                    map_choose = True
                    go = False


        if map_choose:
            # ── Phase 2: LAN P2 waits for host map selection ──
            if global_vars.active_net_client is not None and global_vars.active_net_client.my_player_type == 2:
                # waiting_font = global_vars.get_font(40)
                result = wait_screen(
                    condition_func=lambda: global_vars.active_net_client.map_selected is not None,
                    text="Waiting for host to start...",
                    background=background,
                    font=40
                )

                if result == 'opponent_left':
                    return 'opponent_left'

                map_selected = _map_name_to_bg.get(
                    global_vars.active_net_client.map_selected,
                    Animate_BG.dark_forest_bg
                )
                # Skip map UI, go straight to fight
                go = True
            else:
                # Normal map selection UI (local mode or LAN host)
                create_title('MAP SELECT', font, default_size, height * 0.1)
                for selector in map_select:
                    selector.update(mouse_pos, mouse_press, map_select, max_selected=1)

                for selector in map_select:
                    # if selector.hovered:
                    #     selector.the_info((-(width * 0.0001), height - 500))
                    if selector.is_selected():
                        map_selected = selector.get_associated()

                        

                        # # Draw item selection
                        # for item in p2_items:
                        #     item.update(mouse_pos, mouse_press, p2_items, max_selected=MAX_ITEM)
                        # for item in p2_items:
                        #     item.draw()

                        # for item in p2_items:
                        #     if item.hovered:
                        #         item.class_item.update((-(width * 0.0001), height - 500))
  
                        # print(PLAYER_2_SELECTED_HERO)
                        go = True
                        break
                    elif not immediate_run:
                        go = False
                
            if go:
                fight.draw(screen, mouse_pos)
                is_p2_lan = global_vars.active_net_client is not None and global_vars.active_net_client.my_player_type == 2
                if is_p2_lan or (pygame.mouse.get_pressed()[0] and fight.is_clicked(mouse_pos)) or keys[pygame.K_SPACE] or immediate_run:
                    
                    # ── Phase 2: LAN host sends map choice ──
                    # if global_vars.active_net_client is not None and global_vars.active_net_client.my_player_type == 1:
                    #     _map_name = _bg_to_map_name.get(map_selected, 'dark_forest')
                    #     global_vars.active_net_client.send_map(_map_name)

                    screen.blit(background, (0, 0))
                    loading.draw(screen, pygame.mouse.get_pos())
                    pygame.display.update()
                    # pygame.time.delay(500)  # Wait for 2 seconds before showing the player selection screen

                    # for random hero selection if toggled
                    heroes = (Fire_Wizard, Wanderer_Magician,
                              Fire_Knight, Wind_Hashashin,
                              Water_Princess, Forest_Ranger,
                              Yurei, Chthulu)
                    # Player type seems to be phased out but is still being used
                    # ── LAN: use server-confirmed hero classes ──
                    _hero_map = {
                        'Fire_Wizard': Fire_Wizard,
                        'Wanderer_Magician': Wanderer_Magician,
                        'Fire_Knight': Fire_Knight,
                        'Wind_Hashashin': Wind_Hashashin,
                        'Water_Princess': Water_Princess,
                        'Forest_Ranger': Forest_Ranger,
                        'Yurei': Yurei,
                        'Chthulu': Chthulu,
                        'Phantom_Assassin': Phantom_Assassin,
                    }

                    

                    if global_vars.active_net_client is not None:

                        # send map (P1 only)
                        if global_vars.active_net_client.my_player_type == 1:
                            _map_name = _bg_to_map_name.get(map_selected, 'dark_forest')
                            global_vars.active_net_client.send_map(_map_name)

                        # load my hero
                        if global_vars.active_net_client.my_player_type == 1:
                            hero1 = PLAYER_1_SELECTED_HERO(PLAYER_1, hero2) if not global_vars.random_pick_p1 else random.choice(heroes)(PLAYER_1, hero2)
                        else:
                            hero2 = PLAYER_2_SELECTED_HERO(PLAYER_2, hero1) if not global_vars.random_pick_p2 else random.choice(heroes)(PLAYER_2, hero1)

                        my_hero_name = (PLAYER_1_SELECTED_HERO.__name__ 
                                        if global_vars.active_net_client.my_player_type == 1 
                                        else PLAYER_2_SELECTED_HERO.__name__)

                        # Handle random item selection BEFORE collecting names, then send
                        if global_vars.active_net_client.my_player_type == 1:
                            if global_vars.random_item_pick_p1:
                                equipped_items.populate_random_items(MAX_ITEM)
                            my_item_names = [item.get_associated().name for item in p1_items if item.is_selected()]
                        else:
                            if global_vars.random_item_pick_p2:
                                equipped_items_p2.populate_random_items(MAX_ITEM)
                            my_item_names = [item.get_associated().name for item in p2_items if item.is_selected()]

                        # send hero + items, wait for both_ready
                        global_vars.active_net_client.send_hero_ready(my_hero_name, my_item_names)
                        result = wait_screen(lambda: global_vars.active_net_client.both_ready, text="Waiting for opponent...")
                        if result == 'opponent_left':
                            return 'opponent_left'
                        
                        # identify opponent hero
                        PLAYER_1_SELECTED_HERO = _hero_map.get(global_vars.active_net_client.p1_hero, PLAYER_1_SELECTED_HERO)
                        PLAYER_2_SELECTED_HERO = _hero_map.get(global_vars.active_net_client.p2_hero, PLAYER_2_SELECTED_HERO)
                        
                        # both heroes are not ready again since will load the opponent hero
                        # global_vars.active_net_client.send_hero_not_ready()
                        # result = wait_screen(lambda: global_vars.active_net_client.opponent_ready, text="Loading opponent hero...")
                        # if result == 'opponent_left':
                        #     return 'opponent_left'
                        
                        # load opponent hero
                        if global_vars.active_net_client.my_player_type == 1:
                            hero2 = PLAYER_2_SELECTED_HERO(PLAYER_2, hero1) if not global_vars.random_pick_p2 else random.choice(heroes)(PLAYER_2, hero1)
                        elif global_vars.active_net_client.my_player_type == 2:
                            hero1 = PLAYER_1_SELECTED_HERO(PLAYER_1, hero2) if not global_vars.random_pick_p1 else random.choice(heroes)(PLAYER_1, hero2)
                            
                        # global_vars.active_net_client.send_hero_ready(my_hero_name) # opponent hero done loading
                        global_vars.active_net_client.send_load_opponent_hero_ready(my_hero_name)
                        result = wait_screen(lambda: global_vars.active_net_client.ready_to_battle, text="Waiting for opponent...")
                        if result == 'opponent_left':
                            return 'opponent_left'

                        # Equip items for both heroes in LAN
                        hero1.items = get_items_by_names(global_vars.active_net_client.p1_items)
                        hero2.items = get_items_by_names(global_vars.active_net_client.p2_items)
                        hero1.apply_item_bonuses()
                        hero2.apply_item_bonuses()
                        



                    else: # Local mode 
                        if global_vars.active_net_client is None or global_vars.active_net_client.my_player_type == 1:
                            hero1 = PLAYER_1_SELECTED_HERO(PLAYER_1, hero2) if not global_vars.random_pick_p1 else random.choice(heroes)(PLAYER_1, hero2)
                        if global_vars.active_net_client is None or global_vars.active_net_client.my_player_type == 2:
                            hero2 = PLAYER_2_SELECTED_HERO(PLAYER_2, hero1) if not global_vars.random_pick_p2 else random.choice(heroes)(PLAYER_2, hero1)
                        # print(hero1.enemy)
                        # print(hero2.enemy)
                        # hero3 = Wind_Hashashin(PLAYER_1, hero2)
                    

                        if global_vars.SINGLE_MODE_ACTIVE:
                            if global_vars.HERO1_BOT:
                                bot1_class = create_bot(PLAYER_1_SELECTED_HERO if not global_vars.random_pick_p1 else random.choice(heroes), PLAYER_1, hero2)
                                hero1 = bot1_class(hero2, hero2)  # pass live hero2 reference

                            bot2_class = create_bot(PLAYER_2_SELECTED_HERO if not global_vars.random_pick_p2 else random.choice(heroes), PLAYER_2, hero1)
                            hero2 = bot2_class(hero1, hero1)  # pass live hero1 reference (first is for bot reference, second is for player reference)
                            
                            if global_vars.toggle_hero3: # Create a third enemy (hero3) for single player mode
                                bot3_class = create_bot(PLAYER_2_SELECTED_HERO if not global_vars.random_pick_p2 else random.choice(heroes), PLAYER_2, hero1)
                                hero3 = bot3_class(hero1, hero1)  # pass live hero1 reference (both enemies target the player)
                                # Position hero3 slightly offset from hero2 so they don't overlap
                                from global_vars import DEFAULT_X_POS, DEFAULT_Y_POS
                                hero3.x_pos = DEFAULT_X_POS - 50  # Offset hero3 slightly to the left of hero2
                                hero3.y_pos = DEFAULT_Y_POS
                                hero3.player_1_y += 150
                                hero3.player_2_y += 150 
                                
                            if global_vars.HERO1_BOT:
                                hero1.player = hero2 # modify hero1 live reference for hero2 to real referenced object

                    
                        for item in equipped_items.item:
                            # if item.is_selected():
                                hero1.items.append(item.get_associated())

                        for item in equipped_items_p2.item:
                            # if item.is_selected():
                                hero2.items.append(item.get_associated())
                                # Also apply to hero3 in single player mode
                                if global_vars.SINGLE_MODE_ACTIVE:
                                    if global_vars.toggle_hero3:
                                        hero3.items.append(item.get_associated())


                        # === AUTO-EQUIP RANDOM ITEMS IF TOGGLE IS ON ===
                        if global_vars.random_item_pick_p1:
                            equipped_items.populate_random_items(MAX_ITEM)
                        
                        if global_vars.random_item_pick_p2:
                            equipped_items_p2.populate_random_items(MAX_ITEM)

                    # --- Create sprite groups (shared by LAN and local) ---
                    hero1_group = pygame.sprite.Group()
                    # hero1_group.add(hero3)

                    hero2_group = pygame.sprite.Group()
                    

                    if global_vars.active_net_client is None and global_vars.SINGLE_MODE_ACTIVE:
                        if global_vars.toggle_hero3:
                            hero2_group.add(hero3)

                    # ------------------------------
                    # --- Create bots for both teams ---
                    hero1_group.add(
                        *(create_bot(PLAYER_1_SELECTED_HERO if not global_vars.random_pick_p1 else random.choice(heroes), PLAYER_1, [])(None, []) for _ in range(0))
                    )

                    hero2_group.add(
                        *(create_bot(PLAYER_2_SELECTED_HERO if not global_vars.random_pick_p2 else random.choice(heroes), PLAYER_2, [])(None, []) for _ in range(0))
                    )

                    hero1_group.add(hero1)
                    hero2_group.add(hero2)
                    # --- Assign enemies ---
                    for h in hero1_group:
                        h.enemy = list(hero2_group)
                    for h in hero2_group:
                        h.enemy = list(hero1_group)

                    if global_vars.active_net_client is None:
                        # --- Apply items to team 1 (local mode only; LAN uses get_items_by_names) ---
                        for h in hero1_group:
                            # If all_items is on and this is a bot, don't clear/override items
                            # uncomment to allow player1 bots to have same settings as player2 bots
                            # if not (global_vars.all_items and hasattr(h, 'botkey_skill1')):
                            #     h.items = []
                            h.items = []
                        for item in p1_items:
                            if item.is_selected():
                                for h in hero1_group:
                                    # If all_items is on and this is a bot, skip (it already has all items)
                                    if not (global_vars.all_items and hasattr(h, 'botkey_skill1')):
                                        h.items.append(copy.copy(item.get_associated()))
                        for h in hero1_group:
                            h.apply_item_bonuses()

                        # --- Apply items to team 2 (local mode only) ---
                        for h in hero2_group:
                            # If all_items is on and this is a bot, don't clear/override items
                            if not (global_vars.all_items and hasattr(h, 'botkey_skill1')):
                                h.items = []

                        for item in p2_items:
                            if item.is_selected():
                                for h in hero2_group:
                                    # If all_items is on and this is a bot, skip (it already has all items)
                                    if not (global_vars.all_items and hasattr(h, 'botkey_skill1')):
                                        h.items.append(copy.copy(item.get_associated()))

                        for h in hero2_group:
                            h.apply_item_bonuses()

                    pygame.mixer.music.fadeout(1000)
                    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

                    reset_all()
                    
                    while True:
                        game_end_result = fade(background, lambda: game(net_client=global_vars.active_net_client if global_vars.active_net_client else None)) #lez go it worked
                        # print('game end result from player_selection:', game_end_result)
                        if game_end_result in ("rematch", "restart"):
                            continue
                        else:
                            # print('break!', game_end_result)
                            break

                    return game_end_result

        pygame.display.update()
        clock.tick(FPS)

    
bot = object




# ONLY PLACE HOLDER VALUE, CHANGES LATER
# fire_wizard = Fire_Wizard(PLAYER_1)
# wanderer_magician = Wanderer_Magician(PLAYER_2)

# fire_wizard_select = PlayerSelector(fire_wizard_icon, (75, height -75), Fire_Wizard)
# wanderer_magician_select = PlayerSelector(wanderer_magician_icon, (75*3, height -75), Wanderer_Magician)

# p1_select_icon = [
#         PlayerSelector(fire_wizard_icon, (75, height - 75), Fire_Wizard),
#         PlayerSelector(wanderer_magician_icon, (75 * 3, height - 75), Wanderer_Magician),
#         PlayerSelector(fire_knight_icon, (75 * 5, height - 75), Fire_Knight),
#         PlayerSelector(wind_hashashin_icon, (75, height - 75 * 3), Wind_Hashashin)
#     ]




        # self.player_death = self.load_attack_class(
        #     filepath=r"PYTHON WITH KIM  NEW!\characters\skeleton\craftpix-net-957123-free-skeleton-pixel-art-sprite-sheets\Skeleton_Warrior\Dead.png",
        #     frame_width=192, 
        #     frame_height=192, 
        #     rows=1, 
        #     columns=4, 
        #     scale=1, 
        #     rotation=0,
        #     frame_duration=100
        # )
    




bot = object




# ONLY PLACE HOLDER VALUE, CHANGES LATER
# fire_wizard = Fire_Wizard(PLAYER_1)
# wanderer_magician = Wanderer_Magician(PLAYER_2)

# fire_wizard_select = PlayerSelector(fire_wizard_icon, (75, height -75), Fire_Wizard)
# wanderer_magician_select = PlayerSelector(wanderer_magician_icon, (75*3, height -75), Wanderer_Magician)

# p1_select_icon = [
#         PlayerSelector(fire_wizard_icon, (75, height - 75), Fire_Wizard),
#         PlayerSelector(wanderer_magician_icon, (75 * 3, height - 75), Wanderer_Magician),
#         PlayerSelector(fire_knight_icon, (75 * 5, height - 75), Fire_Knight),
#         PlayerSelector(wind_hashashin_icon, (75, height - 75 * 3), Wind_Hashashin)
#     ]




        # self.player_death = self.load_attack_class(
        #     filepath=r"PYTHON WITH KIM  NEW!\characters\skeleton\craftpix-net-957123-free-skeleton-pixel-art-sprite-sheets\Skeleton_Warrior\Dead.png",
        #     frame_width=192, 
        #     frame_height=192, 
        #     rows=1, 
        #     columns=4, 
        #     scale=1, 
        #     rotation=0,
        #     frame_duration=100
        # )
    

# NEXT TO DO IS TO CONTINUE WORKING ON THE SKILLS
from gameloop import main_menu, menu
if __name__ == '__main__':
    main_menu()
    menu()
