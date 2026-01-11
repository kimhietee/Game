from heroes import hero1, TOTAL_WIDTH, FPS, width, height, screen
from player import Player
from chance import Chance
import pygame
import time
import random
import global_vars

botchance = Chance(0.3)


# from heroes import PLAYER_2_SELECTED_HERO, PLAYER_2




# from heroes import hero2, Fire_Wizard

# hero2 = Fire_Wizard(2)
# print(hero2.__class__)


# hero2 = PLAYER_2_SELECTED_HERO(PLAYER_2)

# MAIN PROBLEM, INHERITANCE, BOT ENHERITS FROM THE SELECTED HERO, THEN USE IT AS A BOT, IM SLEEPING

def create_bot(selected_hero, player_type, enemy):
    global Bot
    class Bot(selected_hero):
        def __init__(self, player, enemy):
            super().__init__(player_type, enemy)
            self.enemy = enemy # Used for player
            self.player = player # Used for bot logic
            # self.strength += self.strength
            # self.intelligence += self.intelligence
            # self.agility += self.agility
            from heroes import items #make a button hard mode
            if global_vars.all_items:
                self.items = items # from heroes.py

            

            # Inputs
            self.botkey_skill1 = self.botkey_skill2 = self.botkey_skill3 = self.botkey_skill4 = False
            self.botkey_right = self.botkey_left = self.botkey_jump = False
            self.botkey_attack = False
            self.botkey_special = False
            self.forcemove_left = self.forcemove_right = False

            # State
            self.state = ''
            self.attack_state = ''

            self.enemy_distance = 0


            self.bot_default_font = pygame.font.SysFont('Serif', 30)

            self.disabled_random_unstuck_direction = False

            # Retargeting config: policy can be 'closest', 'random' or 'focus'
            # You can set `global_vars.BOT_RETARGET_POLICY = 'closest'` to change default.
            self.retarget_policy = getattr(global_vars, 'BOT_RETARGET_POLICY', 'closest')
            self.preferred_target = None
            # initial target (will be validated by ensure_target_alive when update runs)
            try:
                self.target = self.enemy[0] if type(self.enemy) is list and len(self.enemy) > 0 else (self.enemy if self.enemy else None)
            except Exception:
                self.target = None

            self.hero_data = {
                'Fire_Wizard': {
                    'default_timer': 1,
                    'timer_slow_decrease': 2,

                    'cast_special_threshold': self.get_special_threshold,
                    'special_if_sp_skill_ready': True,
                    'special_conditions': [True, 2],

                    'special_threshold': {
                        'health_high_prio': self.max_health * 0.35,
                        'low_prio': 0.9,
                        'high_prio': 0.5
                    },

                    'stuck_logic': {
                        'threshold': 2.5,
                        'detect': 0.5,
                        'duration': 3.0
                    },

                    'edge_escape_logic': {
                        'duration': 2.0,
                        'distance': 300
                    },

                    'took_alot_dmg': {
                        'damage_interval': 0.5,
                        'damage_threshold': 7,
                        'damage_taken_logic': 0.5,
                    },
                    
                    'panic_logic': {
                        'threshold': 0.3,
                        'cooldown': 2.5
                    },

                    'cast_special_threshold_distance': 300,

                    'random_unstuck': 0.0001,
                    'random_edge_escape': 0.000001,

                    'decide_logic': {
                        'chase_distance': 800,
                        'panic_chase_distance': 400,
                        'escape_distance': 240
                    },
                    
                    'skills': {
                        'skill_1': {
                            'cast_range': 150,
                            'min_cast_range': 50,
                            'require_all': False,  # Allow any of these grouped conditions to trigger
                            'conditions': [
                                lambda bot: (not bot.special_active and
                                    bot.enemy_hp_percent() >= 50 and
                                    bot.is_facing_from_enemy() and
                                    bot.mana >= bot.attacks[0].mana_cost * 2 and
                                    not bot.player.sp_attacking and
                                    botchance.update(60)
                                    # random.random() < 0.6
                                ),

                                lambda bot: (not bot.special_active and
                                    (not bot.player.attacking1 and not bot.player.attacking2 and not bot.player.attacking3) and
                                    bot.enemy_hp_percent() < 50 and 
                                    not bot.player.sp_attacking and
                                    bot.is_facing_from_enemy() and(
                                    bot.mana >= bot.attacks[0].mana_cost * 2 or
                                    botchance.update(50)
                                    )
                                ),

                                lambda bot: (not bot.special_active and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    botchance.update(20)
                                ),

                                # sp logic
                                lambda bot: (bot.special_active and
                                    bot.enemy_hp_percent() >= 40 and
                                    bot.is_facing_from_enemy() and
                                    bot.enemy_distance <= 100 and
                                    not bot.player.sp_attacking and
                                    botchance.update(55)
                                ),

                                lambda bot: (bot.special_active and
                                    bot.enemy_hp_percent() <= 40 and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    botchance.update(50)
                                )
                            ]
                        },
                        'skill_2': {
                            'cast_range': 250,
                            'min_cast_range': 200,
                            'require_all': False,
                            'conditions': [
                                lambda bot: (not bot.special_active and
                                    bot.enemy_hp_percent() >= 70 and
                                    self.mana >= self.attacks[1].mana_cost * 1.333 and
                                    not bot.player.sp_attacking and
                                    botchance.update(80)
                                ),

                                lambda bot: (not bot.special_active and
                                    bot.enemy_hp_percent() < 70 and
                                    not bot.player.sp_attacking and
                                    botchance.update(50)
                                ),

                                lambda bot: (not bot.special_active and
                                    bot.enemy_hp_percent() < 50 and
                                    not bot.player.sp_attacking and
                                    botchance.update(50)
                                ),

                                #sp logic
                                lambda bot: (bot.special_active and
                                    bot.enemy_hp_percent() >= 40 and
                                    not bot.player.sp_attacking and
                                    (width / 2 - 150 < bot.x_pos < width / 2 + 150) and
                                    botchance.update(70)
                                ),

                                lambda bot: (bot.special_active and
                                    bot.enemy_hp_percent() <= 40 and
                                    not bot.player.sp_attacking and
                                    (width / 2 - 250 < bot.x_pos < width / 2 + 250) and
                                    botchance.update(70)
                                )
                                
                                
                            ]
                        },
                        'skill_3': {
                            'cast_range': 140, # original cast range: 125
                            'min_cast_range': 80,
                            'require_all': False,
                            'conditions': [
                                lambda bot: (not bot.special_active and
                                    (not bot.player.attacking1 and not bot.player.attacking2 and not bot.player.attacking3) and
                                    bot.enemy_distance <= 125 and
                                    bot.is_facing_from_enemy() and
                                    bot.enemy_hp_percent() >= 40 and
                                    not bot.player.sp_attacking and
                                    bot.mana >= bot.attacks[1].mana_cost * 1.3 and
                                    botchance.update(70)
                                ),

                                lambda bot: (not bot.special_active and
                                    (not bot.player.attacking1 and not bot.player.attacking2 and not bot.player.attacking3) and
                                    bot.enemy_distance <= 125 and
                                    bot.is_facing_from_enemy() and
                                    bot.enemy_hp_percent() < 40 and
                                    not bot.player.sp_attacking and
                                    botchance.update(65)
                                ),

                                lambda bot: (not bot.special_active and
                                    bot.enemy_distance <= 125 and
                                    bot.is_facing_from_enemy() and
                                    bot.bot_hp_percent() < 40 and
                                    not bot.player.sp_attacking and
                                    botchance.update(70)
                                ),

                                # sp logic
                                lambda bot: (bot.special_active and
                                    (not bot.player.attacking1 and not bot.player.attacking2 and not bot.player.attacking3) and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    botchance.update(50)
                                )
                            ]
                        },
                        'skill_4': {
                            'cast_range': 1000, # original cast range: 250
                            'min_cast_range': 200,
                            'require_all': False,
                            'conditions': [
                                lambda bot: (not bot.special_active and
                                    (not bot.player.attacking1 and not bot.player.attacking2 and not bot.player.attacking3) and
                                    bot.enemy_distance <= 250 and
                                    not bot.player.sp_attacking and
                                    bot.is_facing_from_enemy()
                                    ),  # always cast when in range

                                #sp logic
                                lambda bot: (bot.special_active and
                                    not bot.player.sp_attacking and
                                    bot.is_facing_from_enemy()
                                )
                            ]
                        },
                    },
                    'basic_attack': {
                        'atk_range': 100,
                        'min_cast_range': 50,
                    }
                },




                'Wanderer_Magician': {
                    'default_timer': 1,
                    'timer_slow_decrease': 2, # how fast slowly reduce the timer

                    'cast_special_threshold': self.get_special_threshold, # percentage
                    'special_if_sp_skill_ready': False, # decision if always cast special whenever the mana is sufficient for sp  (only use special when sp is not cd) Note: wont use  in sp_skill if its cooldown
                    'special_conditions': [False, 2], # [0] = enable condition: 
                                                        # True = with conditions,
                                                        # False = use skills whenever
                                                        # 
                                                        # [1] = condition type :
                                                        # 0 = enemy weak (will use skills),
                                                        # 1 = enemy strong (will use skills),
                                                        # 2 = don't use skills

                    'special_threshold': {
                        'health_high_prio': self.max_health * 0.7, # if less than the value, then high prio
                        'low_prio': 0.2, # bot will need ??% mana to cast special
                        'high_prio': 0.1 # if less than the hp prio, then ??% is enough to cast special
                    },

                    'stuck_logic': {
                        'threshold': 2.5, # when stuck for __ seconds, unstuck, if still at same pos (detect)
                        'detect': 0.5, # just standing still, how wide the condition, if stuck
                        'duration': 3.0 # how long
                    },

                    'edge_escape_logic': { #default: 2.0, 300, if you modify one, change the other since they're in sync in logic
                        'duration': 2.0, # how long
                        'distance': 300 # how far going away from the edge (if distance too short and duration not ended, if it exceeds distance, the bot just jumps)
                    }, # ...

                    'took_alot_dmg': {
                        'damage_interval': 0.5, # seconds, check if took alot of dmg in that duration (scope) (actually idk what is this)
                        'damage_threshold': 3, # how much health to escape
                        'damage_taken_logic': 0.5, # just standing still, how wide the condition, if bot took ['damage_threshold'] dmg
                    },
                        
                    'panic_logic': {
                        'threshold': 0.3, # if only ['threshold'] percent health, bot panik
                        'cooldown': 2.5 # when panik finish, cd to panik again
                    }, 

                    'cast_special_threshold_distance': 1000, # if enemy is below this distance, cast special, only if special_ready()

                    'random_unstuck': 0.0001, # it just jumps only if idle
                    'random_edge_escape': 0.000001, # same for this one

                    'decide_logic': {
                        'chase_distance': 1000, # chase enemy if below this distance
                        'panic_chase_distance': 400, # same but panik mode
                        'escape_distance': 200, # if enemy below this distance, bot try to escape... # the highest cast range of all skills except skill 4, is skill 2, minus 10

                        # Removed code
                        # 'attack_distance': 800, # basic attack if below this distance 
                    },
                    
                    'skills': { # (not bot.player.attacking1 and not bot.player.attacking2 and not bot.player.attacking3) and
                                # the code above prevent the bot from using skill when the enemy is currently attacking, this can avoid the bot from using skills unneccesarily. only use when needed
                        'skill_1': {
                            'cast_range': 800, # casts the skill if below this distance, only if all conditions are met
                            'min_cast_range': 50, # bot trys to go back when trying to use the skill but below the minimum cast_range (conditions met)
                            'require_all': False,
                            'conditions': [
                                lambda bot: (not bot.special_active and
                                    bot.enemy_hp_percent() >= 70 and
                                    bot.is_facing_from_enemy() and
                                    bot.enemy_distance <= 650 and
                                    bot.player.jumping == True and
                                    bot.mana >= bot.attacks[0].mana_cost * 1.5 and
                                    not bot.player.sp_attacking and
                                    botchance.update(40)
                                ),
                                lambda bot: (not bot.special_active and
                                    (not bot.player.attacking1 and not bot.player.attacking2 and not bot.player.attacking3) and
                                    bot.bot_hp_percent() < 50 and 
                                    not bot.player.sp_attacking and
                                    bot.is_facing_from_enemy() and(
                                    bot.mana >= bot.attacks[0].mana_cost * 2 or
                                    botchance.update(10) or
                                    (bot.player.jumping == True and bot.is_facing_from_enemy()) or
                                    bot.enemy_distance <= 400
                                    )
                                ),
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() < 35 and
                                    bot.is_facing_from_enemy() and
                                    botchance.update(20) and
                                    bot.mana >= bot.attacks[0].mana_cost * 2.2 and
                                    not bot.player.sp_attacking and
                                    bot.enemy_distance <= 200
                                ),

                                # sp logic
                                lambda bot: (bot.special_active and
                                    bot.enemy_hp_percent() > 60 and 
                                    bot.is_facing_from_enemy() and
                                    bot.player.jumping == True and
                                    bot.mana >= bot.attacks[0].mana_cost * 1.3 and
                                    not bot.player.sp_attacking and
                                    bot.enemy_distance <= 200 and
                                    botchance.update(50)
                                ),
                                lambda bot: (bot.special_active and
                                    bot.is_facing_from_enemy() and
                                    bot.player.jumping == True and
                                    bot.enemy_distance <= 150 and
                                    not bot.player.sp_attacking and
                                    botchance.update(75)
                                )

                                
                            ]
                        },
                        'skill_2': {
                            'cast_range': 1050,
                            'min_cast_range': 5,
                            'require_all': False,
                            'conditions': [
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() >= 70 and
                                    bot.bot_hp_percent() < 90 and
                                    bot.enemy_distance >= 700 and
                                    bot.mana >= bot.attacks[0].mana_cost * 1.2 and
                                    botchance.update(5)
                                ),
                                lambda bot: (not bot.special_active and
                                    bot.enemy_hp_percent() < 80 and (
                                        bot.mana >= bot.attacks[0].mana_cost * 1.2 or
                                        botchance.update(10) or
                                        bot.enemy_distance >= 600
                                    )
                                ),
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() < 70 and
                                    botchance.update(20) and
                                    bot.enemy_distance >= 600
                                ),
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() < 40 and (
                                    botchance.update(20) or
                                    bot.enemy_distance >= 500 and
                                    botchance.update(15)
                                    )
                                ),

                                #sp logic
                                lambda bot: (bot.special_active and
                                    bot.bot_hp_percent() <= 60 and
                                    bot.enemy_distance >= 250 and
                                    botchance.update(20)
                                ),
                                lambda bot: (bot.special_active and
                                    bot.bot_hp_percent() <= 35 and
                                    bot.enemy_distance >= 150 and
                                    botchance.update(30)
                                ),
                                lambda bot: (bot.special_active and
                                    bot.bot_hp_percent() <= 20 and
                                    botchance.update(80)
                                )
                            ]
                        },
                        'skill_3': {
                            'cast_range': 1000,
                            'min_cast_range': 10,
                            'require_all': False,
                            'conditions': [
                                lambda bot: (not bot.special_active and
                                    (not bot.player.attacking1 and not bot.player.attacking2 and not bot.player.attacking3) and
                                    bot.bot_hp_percent() >= 75 and
                                    bot.enemy_distance >= 600 and
                                    bot.mana >= bot.attacks[0].mana_cost * 1.3 and
                                    not bot.player.sp_attacking and
                                    botchance.update(40)
                                ),
                                lambda bot: (not bot.special_active and
                                    bot.enemy_hp_percent() < 80 and
                                    bot.mana >= bot.attacks[0].mana_cost * 1.1 and
                                    not bot.player.sp_attacking and
                                    botchance.update(40) and
                                    bot.enemy_distance >= 300
                                ),
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() < 75 and
                                    bot.mana >= bot.attacks[0].mana_cost * 1.3 and
                                    not bot.player.sp_attacking and
                                    botchance.update(30)
                                ),
                                lambda bot: (not bot.special_active and
                                    (not bot.player.attacking1 and not bot.player.attacking2 and not bot.player.attacking3) and
                                    bot.enemy_hp_percent() < 30 and
                                    bot.mana >= bot.attacks[0].mana_cost * 1.2 and
                                    not bot.player.sp_attacking and
                                    botchance.update(30) and
                                    bot.enemy_distance >= 300
                                ),
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() < 40 and
                                    botchance.update(20) and
                                    not bot.player.sp_attacking and
                                    bot.enemy_distance >= 750
                                ),

                                #sp logic
                                lambda bot: (bot.special_active and
                                    bot.enemy_hp_percent() > 40 and
                                    bot.bot_hp_percent() > 50 and
                                    bot.enemy_distance >= 300 and
                                    bot.mana >= bot.attacks[0].mana_cost * 1.2 and
                                    not bot.player.sp_attacking and
                                    botchance.update(15)
                                ),
                                lambda bot: (bot.special_active and
                                    (not bot.player.attacking1 and not bot.player.attacking2 and not bot.player.attacking3) and
                                    bot.enemy_hp_percent() <= 40 and
                                    bot.bot_hp_percent() > 30 and
                                    bot.mana >= bot.attacks[0].mana_cost * 1.1 and
                                    not bot.player.sp_attacking and
                                    botchance.update(30)
                                ),
                                lambda bot: (bot.special_active and
                                    bot.enemy_hp_percent() <= 40 and
                                    bot.bot_hp_percent() <= 30 and
                                    bot.enemy_distance >= 500 and
                                    bot.player.jumping == True and
                                    bot.mana >= bot.attacks[0].mana_cost * 1.2 and
                                    not bot.player.sp_attacking and
                                    botchance.update(40)
                                )
                                
                            ]
                        },
                        'skill_4': {
                            'cast_range': 1070,
                            'min_cast_range': 300,
                            'require_all': False,
                            'conditions': [
                                lambda bot: (not bot.special_active and
                                    bot.enemy_distance > 1000 and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    bot.bot_hp_percent() > 99
                                ),

                                lambda bot: (not bot.special_active and
                                    bot.enemy_hp_percent() > 50 and
                                    bot.is_facing_from_enemy() and
                                    bot.enemy_distance > 800 and
                                    not bot.player.sp_attacking and
                                    botchance.update(90)
                                ),
                                lambda bot: (not bot.special_active and
                                    bot.enemy_hp_percent() < 50 and
                                    bot.is_facing_from_enemy() and
                                    bot.enemy_distance > 600 and
                                    not bot.player.sp_attacking and
                                    botchance.update(70)
                                ),

                                #sp logic
                                lambda bot: (bot.special_active and
                                    bot.enemy_hp_percent() <= 60 and
                                    bot.is_facing_from_enemy() and
                                    bot.enemy_distance > 600 and
                                    not bot.player.sp_attacking and
                                    botchance.update(70)
                                ),
                            ]
                        }
                    },
                    'basic_attack': {
                        'atk_range': 800,
                        'min_cast_range': 160,
                        'disable_min_cast_range_while_special': True
                    }
                },

                'Fire_Knight': {
                    'default_timer': 1,
                    'timer_slow_decrease': 2,

                    'cast_special_threshold': self.get_special_threshold,
                    'special_if_sp_skill_ready': True,
                    'special_conditions': [True, 0],

                    'special_threshold': {
                        'health_high_prio': self.max_health * 0.3,
                        'low_prio': 0.8,
                        'high_prio': 0.55
                    },

                    'stuck_logic': {
                        'threshold': 2,
                        'detect': 0.5,
                        'duration': 2.0
                    },

                    'edge_escape_logic': {
                        'duration': 1.3,
                        'distance': 200
                    }, # ...

                    'took_alot_dmg': {
                        'damage_interval': 0.5,
                        'damage_threshold': 5,
                        'damage_taken_logic': 5,
                    },
                        
                    'panic_logic': {
                        'threshold': 0.25,
                        'cooldown': 2.5
                    }, 

                    'cast_special_threshold_distance': 450,

                    'random_unstuck': 0.0002,
                    'random_edge_escape': 0.000001,

                    'decide_logic': {
                        'chase_distance': 800,
                        'panic_chase_distance': 400,
                        'escape_distance': 200
                    },
                    
                    'skills': {
                        'skill_1': {
                            'cast_range': 100,
                            'min_cast_range': 50,
                            'require_all': False,
                            'conditions': [
                                lambda bot: (not bot.special_active and
                                    all(not bot.attacks[i].is_ready() for i in range(1, 3)) and
                                    not bot.player.sp_attacking and
                                    botchance.update(40)
                                ),

                                #sp logic
                                lambda bot: (bot.special_active and
                                    all(not bot.attacks_special[i].is_ready() for i in range(2, 3)) and
                                    not bot.player.sp_attacking and
                                    botchance.update(40)
                                )
                            ]
                        },
                        'skill_2': {
                            'cast_range': 150,
                            'min_cast_range': 50,
                            'require_all': False,
                            'conditions': [
                                # Combination 1: combo with 2nd skill
                                lambda bot: (not bot.special_active and
                                    (not bot.player.attacking1 and not bot.player.attacking2 and not bot.player.attacking3) and
                                    bot.enemy_hp_percent() >= 60 and
                                    not bot.player.sp_attacking and
                                    bot.attacks[2].is_ready()
                                ),

                                lambda bot: (not bot.special_active and
                                    (not bot.player.attacking1 and not bot.player.attacking2 and not bot.player.attacking3) and
                                    bot.enemy_hp_percent() >= 70 and
                                    bot.mana >= bot.attacks[1].mana_cost * 1.2 and
                                    not bot.player.sp_attacking and
                                    botchance.update(70)
                                ),

                                lambda bot: (not bot.special_active and
                                    bot.enemy_hp_percent() < 70 and
                                    bot.enemy_hp_percent() >= 40 and
                                    bot.mana >= bot.attacks[1].mana_cost * 1.3 and
                                    not bot.player.sp_attacking and
                                    botchance.update(30)
                                ),

                                lambda bot: (not bot.special_active and
                                    bot.enemy_hp_percent() < 40 and
                                    bot.mana >= bot.attacks[1].mana_cost * 1.4 and
                                    not bot.player.sp_attacking and
                                    botchance.update(50)
                                ),

                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() < 50 and
                                    not bot.player.sp_attacking and
                                    botchance.update(60)
                                ),

                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() < 40 and
                                    not bot.player.sp_attacking and
                                    botchance.update(80)
                                ),
                                
                                #sp logic
                                lambda bot: (bot.special_active and
                                    bot.enemy_hp_percent() >= 50 and 
                                    not bot.attacks_special[3].is_ready() and
                                    not bot.player.sp_attacking and
                                    botchance.update(40)
                                ),

                                lambda bot: (bot.special_active and
                                    bot.enemy_hp_percent() < 50 and
                                    not bot.attacks_special[3].is_ready() and
                                    not bot.attacks_special[2].is_ready() and
                                    bot.mana >= bot.attacks[1].mana_cost * 1.2 and
                                    not bot.player.sp_attacking and
                                    botchance.update(40)
                                ),

                                lambda bot: (bot.special_active and
                                    not bot.player.sp_attacking and
                                    bot.bot_hp_percent() < 30 and
                                    botchance.update(80)
                                )
                            ]
                        },
                        'skill_3': {
                            'cast_range': 185,
                            'min_cast_range': 150,
                            'require_all': False,
                            'conditions': [
                                # Combination 1: combo with 2nd skill
                                lambda bot: (not bot.special_active and
                                    (not bot.player.attacking1 and not bot.player.attacking2 and not bot.player.attacking3) and
                                    bot.enemy_hp_percent() >= 60 and
                                    not bot.player.sp_attacking and
                                    not bot.attacks[1].is_ready()
                                ),

                                lambda bot: (not bot.special_active and
                                    bot.enemy_hp_percent() >= 50 and
                                    not bot.attacks[1].is_ready() and
                                    not bot.player.sp_attacking and
                                    bot.mana >= bot.attacks[0].mana_cost * 1.1 and
                                    botchance.update(40)
                                ),

                                lambda bot: (not bot.special_active and
                                    (not bot.player.attacking1 and not bot.player.attacking2 and not bot.player.attacking3) and
                                    bot.enemy_hp_percent() < 50 and
                                    not bot.attacks[1].is_ready() and
                                    not bot.player.sp_attacking and
                                    bot.mana >= bot.attacks[0].mana_cost * 1.2 and
                                    botchance.update(50)
                                ),

                                #sp logic
                                lambda bot: (bot.special_active and
                                    bot.enemy_hp_percent() < 50 and
                                    not bot.player.sp_attacking and
                                    not bot.attacks_special[3].is_ready() and
                                    botchance.update(50)
                                ),

                                lambda bot: (bot.special_active and
                                    bot.bot_hp_percent() < 30 and
                                    not bot.player.sp_attacking and
                                    not bot.attacks_special[3].is_ready() and
                                    botchance.update(70)
                                )
                            ]
                        },
                        'skill_4': {
                            'cast_range': 330,
                            'min_cast_range': 300,
                            'require_all': False,
                            'conditions': [
                                lambda bot: (not bot.special_active and
                                    bot.mana >= bot.attacks[2].mana_cost * 1.05 and
                                    not bot.player.sp_attacking and
                                    not bot.attacks[2].is_ready()
                                ),

                                #sp logic
                                lambda bot: (bot.special_active
                                ) and
                                    not bot.player.sp_attacking
                                

                            ]
                        }
                    },
                    'basic_attack': {
                        'atk_range': 100,
                        'min_cast_range': 40,
                    }
                },
                

                'Wind_Hashashin': {
                    'default_timer': 1.2,
                    'timer_slow_decrease': 1,

                    'cast_special_threshold': self.get_special_threshold,
                    'special_if_sp_skill_ready': True,
                    'special_conditions': [True, 1],
                    

                    'special_threshold': {
                        'health_high_prio': self.max_health * 0.35,
                        'low_prio': 0.75,
                        'high_prio': 0.45
                    },

                    'stuck_logic': {
                        'threshold': 1,
                        'detect': 2,
                        'duration': 4.0
                    },

                    'edge_escape_logic': {
                        'duration': 3.0,
                        'distance': 450
                    },

                    'took_alot_dmg': {
                        'damage_interval': 0.5,
                        'damage_threshold': 3,
                        'damage_taken_logic': 2,
                    },
                    
                    'panic_logic': {
                        'threshold': 0.4,
                        'cooldown': 2.5
                    },

                    'cast_special_threshold_distance': 700,

                    'random_unstuck': 0.0003,
                    'random_edge_escape': 0.000007,

                    'decide_logic': {
                        'chase_distance': 750,
                        'panic_chase_distance': 350,
                        'escape_distance': 270
                    },
                    
                    'skills': {
                        'skill_1': {
                        'cast_range': 1000,
                        'min_cast_range': 20,
                        'require_all': False,
                        # Miscellaneous
                        'not_require_facing_enemy': True, # Cast even not facing the enemy (the code prevents it tho)
                        'allow_while_jumping': True, # Can cast skill while in the air (jumping)
                        'face_away': True, # Will face away from the enemy before using skill
                        'force_escape': True,
                        'disable_random_escape_direction': True, # Disable random escape direction (the bot will always face away from the enemy),  # Let the skill handle the escape logic — don't add random left/right movement
                        # works for every skill (might put it in main bot logic)
                        'conditions': [
                            #for safety measures when the game is starting
                            lambda bot: (not bot.special_active and
                                bot.state == 'escape' and 
                                        bot.bot_hp_percent() >= 85 and
                                        self.mana >= self.attacks[0].mana_cost * 1.3 and
                                        (bot.player.attacking1 or
                                        bot.player.attacking2 or
                                        bot.player.attacking3 or
                                        bot.player.sp_attacking
                                ) and
                                botchance.update(90)
                            ),
                            # Aggressive chase if enemy is low HP and bot is healthy
                            lambda bot: (
                                    not bot.special_active and
                                    bot.state == 'chase' and
                                    bot.enemy_hp_percent() < 40 and
                                    bot.bot_hp_percent() > 60 and
                                    bot.enemy_distance > 500 and
                                    self.mana >= self.attacks[0].mana_cost * 2.5 and
                                    botchance.update(70)
                                ),
                                # Opportunistic attack if enemy is jumping or vulnerable
                                lambda bot: (
                                    not bot.special_active and
                                    bot.state == 'chase' and
                                    bot.player.jumping and
                                    bot.enemy_distance > 500 and
                                    self.mana >= self.attacks[0].mana_cost * 2 and
                                    botchance.update(60)
                                ),
                                # Escape if bot is low HP
                                lambda bot: (
                                    not bot.special_active and
                                    bot.state == 'escape' and
                                    bot.bot_hp_percent() < 30 and
                                    self.mana >= self.attacks[0].mana_cost * 1.8 and
                                    botchance.update(45)
                                ),
                                # Use skill while jumping for mobility
                                # random cast
                                lambda bot: (
                                    not bot.special_active and
                                    bot.player.jumping and
                                    bot.enemy_distance > 100 and
                                    self.mana >= self.attacks[0].mana_cost * 2 and
                                    botchance.update(50)
                                ),
                                # Special active: aggressive chase
                                lambda bot: (
                                    bot.special_active and
                                    bot.state == 'chase' and
                                    bot.enemy_hp_percent() < 60 and
                                    bot.bot_hp_percent() > 40 and
                                    bot.enemy_distance > 200 and
                                    self.mana >= self.attacks[0].mana_cost * 2.2 and
                                    botchance.update(80)
                                ),
                                # Special active: escape if low HP
                                lambda bot: (
                                    bot.special_active and
                                    bot.state == 'escape' and
                                    bot.bot_hp_percent() < 30 and
                                    bot.enemy_distance > 100 and
                                    self.mana >= self.attacks[0].mana_cost * 1.5 and
                                    botchance.update(90)
                                ),
                        ],
                    },
                        'skill_2': {
                            'cast_range': 130,
                            'min_cast_range': 15,
                            'require_all': False,
                            'conditions': [
                                # Use skill 2 for close combat when both are healthy
                                lambda bot: (
                                    not bot.special_active and
                                    bot.enemy_distance <= 80 and
                                    bot.bot_hp_percent() > 50 and
                                    bot.enemy_hp_percent() > 50 and
                                    self.mana >= self.attacks[1].mana_cost * 1.2 and
                                    not bot.player.sp_attacking and
                                    botchance.update(60)
                                ),
                                # Use skill 2 to finish off low HP enemy
                                lambda bot: (
                                    not bot.special_active and
                                    bot.enemy_distance <= 80 and
                                    bot.enemy_hp_percent() < 30 and
                                    self.mana >= self.attacks[1].mana_cost * 1.1 and
                                    not bot.player.sp_attacking and
                                    botchance.update(80)
                                ),
                                # Special active: use skill 2 more aggressively
                                lambda bot: (
                                    bot.special_active and
                                    self.mana >= self.attacks[1].mana_cost * 1.1 and
                                    not bot.player.sp_attacking and
                                    botchance.update(90)
                                )
                            ]
                        },
                        'skill_3': {
                            'cast_range': 140, #125
                            'min_cast_range': 30,#75
                            'require_all': False,
                            'conditions': [
                                # Use skill 3 for mid-range attacks when bot is healthy
                                lambda bot: (
                                    not bot.special_active and
                                    bot.enemy_distance <= 125 and
                                    bot.bot_hp_percent() > 60 and
                                    self.mana >= self.attacks[2].mana_cost * 1.1 and
                                    not bot.player.sp_attacking and
                                    botchance.update(60)
                                ),
                                # death chase
                                lambda bot: (
                                    not bot.special_active and
                                    bot.enemy_distance <= 130 and
                                    bot.bot_hp_percent() <= 60 and
                                    not bot.player.sp_attacking and
                                    botchance.update(70)
                                ),
                                # Special active: use skill 3 for aggressive attacks
                                lambda bot: (
                                    bot.special_active and
                                    bot.bot_hp_percent() >= 30 and
                                    not bot.player.sp_attacking and
                                    botchance.update(50)
                                ),
                                #try to kill
                                lambda bot: (
                                    bot.special_active and
                                    bot.enemy_hp_percent() < 30 and
                                    not bot.player.sp_attacking and
                                    botchance.update(80)
                                )
                            ]
                        },
                        'skill_4': {
                            'cast_range': 1050,
                            'min_cast_range': 100,
                            'require_all': False,
                            'conditions': [
                                # Use skill 4 as a finisher or when enemy is far away
                                lambda bot: (
                                    bot.enemy_distance > 1000 and
                                    bot.enemy_hp_percent() < 30 and
                                    not bot.player.sp_attacking and
                                    botchance.update(90)
                                ),
                                # Use skill 4 to pressure enemy at long range
                                lambda bot: (
                                    bot.enemy_distance > 800 and
                                    bot.enemy_hp_percent() < 60 and
                                    self.mana >= self.attacks[3].mana_cost * 1.1 and
                                    not bot.player.sp_attacking and
                                    botchance.update(70)
                                ),
                                # Always consider skill 4 if enemy is within range
                                lambda bot: (
                                    bot.enemy_distance <= 1000 and
                                    not bot.player.sp_attacking and
                                    botchance.update(50)
                                )
                            ]
                        },
                    },
                    'basic_attack': {
                        'atk_range': lambda bot: 175 if not bot.special_active else 300,
                        'min_cast_range': 30,
                    }
                },

                'Water_Princess': {
                    'default_timer': 1,
                    'timer_slow_decrease': 2,

                    'cast_special_threshold': self.get_special_threshold,
                    'special_if_sp_skill_ready': True,
                    'special_conditions': [True, 2],

                    'special_threshold': {
                        'health_high_prio': self.max_health * 0.4,
                        'low_prio': 0.85,
                        'high_prio': 0.66
                    },

                    'stuck_logic': {
                        'threshold': 2.5,
                        'detect': 0.4,
                        'duration': 3.3
                    },

                    'edge_escape_logic': {
                        'duration': 1.34,
                        'distance': 201
                    },

                    'took_alot_dmg': {
                        'damage_interval': 0.5,
                        'damage_threshold': 6,
                        'damage_taken_logic': 0.5,
                    },
                    
                    'panic_logic': {
                        'threshold': 0.3,
                        'cooldown': 2.5
                    },

                    'cast_special_threshold_distance': 300,

                    'random_unstuck': 0.0001,
                    'random_edge_escape': 0.000001,

                    'decide_logic': {
                        'chase_distance': 800,
                        'panic_chase_distance': 400,
                        'escape_distance': 240
                    },
                    
                    'skills': {
                        'skill_1': {
                            'cast_range': 100,
                            'min_cast_range': 15,
                            'require_all': False,  # Allow any of these grouped conditions to trigger
                            'conditions': [
                                lambda bot: (not bot.special_active and
                                    bot.enemy_hp_percent() >= 70 and
                                    not bot.player.sp_attacking and
                                    not bot.attacks[3].is_ready() and(
                                    bot.mana >= bot.attacks[0].mana_cost * 1.5 or
                                    botchance.update(20)
                                    )
                                ),

                                lambda bot: (not bot.special_active and
                                    bot.enemy_hp_percent() <= 70 and
                                    bot.mana >= bot.attacks[0].mana_cost * 1.30 and
                                    bot.bot_hp_percent() > bot.enemy_hp_percent() and
                                    not bot.player.sp_attacking and
                                    not bot.attacks[3].is_ready() and
                                    botchance.update(60)
                                ),

                                lambda bot: (not bot.special_active and
                                    bot.enemy_hp_percent() <= 40 and
                                    bot.bot_hp_percent() > bot.enemy_hp_percent() and
                                    not bot.player.sp_attacking and
                                    botchance.update(70)
                                ),

                                # sp logic
                                lambda bot: (bot.special_active and
                                    bot.enemy_distance >= 30 and
                                    not bot.player.sp_attacking and
                                    botchance.update(50)
                                )
                            ]
                        },
                        'skill_2': {
                            'cast_range': 650, # 10-700 atk range
                            'min_cast_range': 200,
                            'require_all': False,
                            'conditions': [
                                lambda bot: (not bot.special_active and
                                    bot.enemy_distance <= 500 and
                                    bot.enemy_hp_percent() >= 70 and
                                    self.mana >= self.attacks[1].mana_cost * 1.2 and
                                    not bot.player.sp_attacking and
                                    bot.is_facing_from_enemy() and
                                    not bot.attacks[3].is_ready() and
                                    botchance.update(60)
                                ),

                                lambda bot: (not bot.special_active and
                                    bot.enemy_distance <= 500 and
                                    bot.enemy_hp_percent() < 70 and
                                    bot.is_facing_from_enemy() and
                                    not bot.attacks[3].is_ready() and
                                    not bot.player.sp_attacking and
                                    botchance.update(80)
                                ),

                                #enemy low hp (hit max atk range)
                                lambda bot: (not bot.special_active and
                                    bot.enemy_hp_percent() <= 30 and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    botchance.update(90)
                                ),

                                #sp logic
                                lambda bot: (bot.special_active and
                                    bot.enemy_hp_percent() > 30 and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    botchance.update(70)
                                ),

                                lambda bot: (bot.special_active and
                                    bot.enemy_hp_percent() <= 30 and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    botchance.update(90)
                                )
                                
                            ]# 70 90
                        },
                        'skill_3': {
                            'cast_range': 1500, # original cast range: 125
                            'min_cast_range': 80,
                            'require_all': False,
                            'conditions': [
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() >= 70 and
                                    bot.bot_hp_percent() < 85 and
                                    bot.bot_hp_percent() < bot.enemy_hp_percent() and
                                    bot.enemy_distance >= 250 and
                                    not bot.attacks[3].is_ready() and
                                    botchance.update(70)
                                ),

                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() >= 30 and
                                    bot.bot_hp_percent() < 70 and
                                    bot.bot_hp_percent() < bot.enemy_hp_percent() and
                                    bot.enemy_distance >= 200 and
                                    botchance.update(90)
                                ),

                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() < 30 and
                                    bot.enemy_distance >= 150 and
                                    botchance.update(100)
                                ),

                                # sp logic
                                lambda bot: (bot.special_active and
                                    botchance.update(100)
                                )
                            ]
                        },
                        'skill_4': {
                            'cast_range': 160,
                            'min_cast_range': 90,
                            'require_all': False,
                            'conditions': [
                                lambda bot: (not bot.special_active and
                                    (not bot.player.attacking1 and not bot.player.attacking2 and not bot.player.attacking3) and
                                    bot.enemy_distance <= 150 and
                                    not bot.player.sp_attacking and
                                    bot.is_facing_from_enemy()
                                    ),

                                #sp logic
                                lambda bot: (bot.special_active and
                                    bot.is_facing_from_enemy() and 
                                    not bot.player.sp_attacking
                                )
                            ]
                        },
                    },
                    'basic_attack': {
                        'atk_range': 110,
                        'min_cast_range': 20,
                    }
                },
                
                'Forest_Ranger': {
                    'default_timer': 1,
                    'timer_slow_decrease': 2,

                    'cast_special_threshold': self.get_special_threshold,
                    'special_if_sp_skill_ready': True,
                    'special_conditions': [True, 0],

                    'special_threshold': {
                        'health_high_prio': self.max_health * 0.4,
                        'low_prio': 0.60,
                        'high_prio': 0.30
                    },

                    'stuck_logic': {
                        'threshold': 1,
                        'detect': 2,
                        'duration': 3
                    },

                    'edge_escape_logic': {
                        'duration': 1.5,
                        'distance': 225
                    },

                    'took_alot_dmg': {
                        'damage_interval': 0.3,
                        'damage_threshold': 3.4,
                        'damage_taken_logic': 2,
                    },
                    
                    'panic_logic': {
                        'threshold': 0.4,
                        'cooldown': 5
                    },

                    'cast_special_threshold_distance': 1000,

                    'random_unstuck': 0.0001,
                    'random_edge_escape': 0.000001,

                    'decide_logic': {
                        'chase_distance': 300,
                        'panic_chase_distance': 10, # dont chase at all
                        'escape_distance': 200
                    },
                    
                    'skills': { # (not bot.player.attacking1 and not bot.player.attacking2 and not bot.player.attacking3) and
                                # the code above prevent the bot from using skill when the enemy is currently attacking, this can avoid the bot from using skills unneccesarily. only use when needed
                        'skill_1': {
                            'cast_range': 800,
                            'min_cast_range': 50,
                            'require_all': False,
                            'not_require_facing_enemy': True,
                            'face_away': True,
                            'force_escape': True,
                            'disable_random_escape_direction': True,
                            'conditions': [
                                # Casual buff
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    bot.enemy_distance >= 300 and
                                    botchance.update(70)
                                ),
                                # Immediate buff if enemy is far
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    bot.enemy_distance >= 700
                                ),
                                # Intermediate buff
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    bot.enemy_distance >= 500 and
                                    botchance.update(80)
                                ),
                                # Buff for escape
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() < 50 and
                                    bot.enemy_distance <= 300 and
                                    bot.is_facing_away_from_enemy()
                                ),

                                #sp
                                # Always consider using 1st skill when special active
                                lambda bot: (bot.special_active
                                ),
                            ]
                        },
                            
                        'skill_2': {
                            'cast_range': 1050,
                            'min_cast_range': 5,
                            'require_all': False,
                            'conditions': [
                                # Trick skill while buffed
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    bot.enemy_distance >= 100 and
                                    not bot.player.sp_attacking and
                                    bot.atk_hasted
                                ),
                                # Prefer not to buff
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    bot.enemy_distance >= 300 and
                                    not bot.atk_hasted and
                                    botchance.update(70)
                                ),
                                # If far, try to shoot, and if enemy is casting
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    bot.enemy_distance >= 500 and
                                    (bot.player.attacking1 or bot.player.attacking2 or bot.player.attacking3 or bot.player.sp_attacking) and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    botchance.update(90)
                                ),
                                # Shoot if possible and enemy is while attacking
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() < 50 and
                                    bot.enemy_distance >= 100 and
                                    (bot.player.attacking1 or bot.player.attacking2 or bot.player.attacking3 or bot.player.sp_attacking) and
                                    bot.is_facing_from_enemy() and
                                    botchance.update(90)
                                ),

                                #sp
                                # Trick skill while buffed
                                lambda bot: (bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    bot.enemy_distance >= 100 and
                                    not bot.player.sp_attacking and
                                    bot.atk_hasted
                                ),
                                # Casual skill
                                lambda bot: (bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    bot.enemy_distance >= 100 and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    botchance.update(80)
                                ),
                                # Very casual skill, if enemy is casting
                                lambda bot: (bot.special_active and
                                    bot.bot_hp_percent() < 50 and
                                    bot.is_facing_from_enemy() and
                                    (bot.player.attacking1 or bot.player.attacking2 or bot.player.attacking3 or bot.player.sp_attacking)
                                ),

                                
                            ]
                        },
                            
                        'skill_3': {
                            'cast_range': 300,
                            'min_cast_range': 200,
                            'not_require_facing_enemy': True,
                            'require_all': False,
                            'conditions': [
                                # Try to hit enemy
                               lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    bot.enemy_distance >= 200 and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    botchance.update(80)
                                ),
                                # Slightly far, will try to hit
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() < 50 and
                                    bot.enemy_distance >= 280 and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    botchance.update(90)
                                ),

                                #sp
                                # Cast before enemy go past through back
                                lambda bot: (bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    botchance.update(80)
                                ),
                                # Not preferably far but possible
                                lambda bot: (bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    botchance.update(60)
                                ),
                                # Will cast anyways
                                lambda bot: (bot.special_active and
                                    bot.bot_hp_percent() < 50 and
                                    not bot.player.sp_attacking and
                                    bot.is_facing_from_enemy()
                                ),
                                
                            ]
                        },
                        'skill_4': {
                            'cast_range': 1070,
                            'min_cast_range': 100,
                            'require_all': False,
                            'conditions': [
                                # Casual skill, casts if enemy is using skill (can't be avoided)
                                lambda bot: (not bot.special_active and
                                    ((bot.player.attacking1 or bot.player.attacking2 or bot.player.attacking3 or bot.player.sp_attacking) or
                                    (bot.bot_hp_percent() < 50) or
                                     bot.bot_hp_percent() < 20 and 
                                    not bot.player.sp_attacking
                                    ) 
                                ),
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() < 50
                                ),
                                #sp logic
                                # Enemy is gone
                                lambda bot: (bot.special_active
                                ),
                            ]
                        }
                    },
                    'basic_attack': {
                        'atk_range': 1075,
                        'min_cast_range': 180,
                        'disable_min_cast_range_while_special': True
                    }
                },

                'Yurei': {
                    'default_timer': 1,
                    'timer_slow_decrease': 2,

                    'cast_special_threshold': self.get_special_threshold,
                    'special_if_sp_skill_ready': False,
                    'special_conditions': [True, 0],

                    'special_threshold': {
                        'health_high_prio': self.max_health * 0.6,
                        'low_prio': 0.4,
                        'high_prio': 0.2
                    },

                    'stuck_logic': {
                        'threshold': 1,
                        'detect': 2,
                        'duration': 3
                    },

                    'edge_escape_logic': {
                        'duration': 1.5,
                        'distance': 225
                    },

                    'took_alot_dmg': {
                        'damage_interval': 0.3,
                        'damage_threshold': 3.5,
                        'damage_taken_logic': 1,
                    },
                    
                    'panic_logic': {
                        'threshold': 0.4,
                        'cooldown': 4
                    },

                    'cast_special_threshold_distance': 500,

                    'random_unstuck': 0.0001,
                    'random_edge_escape': 0.000001,

                    'decide_logic': {
                        'chase_distance': 800,
                        'panic_chase_distance': 100,
                        'escape_distance': 300
                    },
                    
                    'skills': { # (not bot.player.attacking1 and not bot.player.attacking2 and not bot.player.attacking3) and
                                # the code above prevent the bot from using skill when the enemy is currently attacking, this can avoid the bot from using skills unneccesarily. only use when needed
                        'skill_1': {
                            'cast_range': 50,
                            'min_cast_range': 10,
                            'require_all': False,
                            'conditions': [
                                # Casual buff
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    not bot.player.sp_attacking and
                                    botchance.update(70)
                                ),
                                # Immediate buff if enemy is far
                                lambda bot: (not bot.special_active and
                                    not bot.player.sp_attacking and
                                    bot.bot_hp_percent() >= 50
                                ),
                                # Intermediate buff
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    not bot.player.sp_attacking and
                                    botchance.update(80)
                                ),
                                # Buff for escape
                                lambda bot: (not bot.special_active and
                                    not bot.player.sp_attacking and
                                    bot.bot_hp_percent() < 50
                                ),

                                #sp
                                # Always consider using 1st skill when special active
                                lambda bot: (bot.special_active
                                ),
                            ]
                        },
                            
                        'skill_2': {
                            'cast_range': 1050,
                            'min_cast_range': 50,
                            'require_all': False,
                            'conditions': [
                                # Trick skill while buffed
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    not bot.player.sp_attacking and
                                    bot.invisible
                                ),
                                # Prefer not to buff
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    bot.enemy_distance <= 500 and
                                    not bot.invisible and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    botchance.update(70)
                                ),
                                # If far, try to shoot, and if enemy is casting
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    bot.enemy_distance >= 500 and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    botchance.update(90)
                                ),
                                # Punish enemy when they are casting/attacking: high priority
                                lambda bot: (not bot.special_active and
                                    (bot.player.sp_attacking or bot.player.attacking1 or bot.player.attacking2 or bot.player.attacking3 or bot.player.basic_attacking) and
                                    bot.enemy_distance >= 100 and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    botchance.update(95)
                                ),
                                # Shoot if possible and enemy is while attacking
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() < 50 and
                                    bot.enemy_distance >= 100 and
                                    (bot.player.attacking1 or bot.player.attacking2 or bot.player.attacking3) and
                                    not bot.player.sp_attacking and
                                    botchance.update(90)
                                ),

                                #sp
                                # Trick skill while buffed
                                lambda bot: (bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    bot.enemy_distance >= 100 and
                                    bot.invisible
                                ),
                                # Casual skill
                                lambda bot: (bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    bot.enemy_distance >= 100 and
                                    bot.is_facing_from_enemy() and
                                    botchance.update(80)
                                ),
                                # Very casual skill, if enemy is casting
                                lambda bot: (bot.special_active and
                                    bot.bot_hp_percent() < 50 and
                                    bot.is_facing_from_enemy()
                                ),

                                
                            ]
                        },
                            
                        'skill_3': {
                            'cast_range': 400,
                            'min_cast_range': 100,
                            'not_require_facing_enemy': True,
                            'require_all': False,
                            'conditions': [
                                # Try to hit enemy
                               lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    bot.enemy_distance <= 300 and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    botchance.update(80)
                                ),
                                # Interrupt enemy casting / special – use silence when enemy is attacking
                                lambda bot: (not bot.special_active and
                                    (bot.player.sp_attacking or bot.player.attacking1 or bot.player.attacking2 or bot.player.attacking3 or bot.player.basic_attacking) and
                                    bot.enemy_distance <= 350 and
                                    botchance.update(95)
                                ),
                                # Slightly far, will try to hit
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() < 50 and
                                    bot.enemy_distance <= 5000 and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    botchance.update(90)
                                ),

                                #sp
                                # Cast before enemy go past through back
                                lambda bot: (bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    botchance.update(80)
                                ),
                                # Not preferably far but possible
                                lambda bot: (bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    botchance.update(60)
                                ),
                                # Will cast anyways
                                lambda bot: (bot.special_active and
                                    bot.bot_hp_percent() < 50 and
                                    not bot.player.sp_attacking and
                                    bot.is_facing_from_enemy()
                                ),
                                
                            ]
                        },
                        'skill_4': {
                            'cast_range': 700,
                            'min_cast_range': 100,
                            'require_all': False,
                            'conditions': [
                                # Casual skill, casts if enemy is using skill (can't be avoided)
                                lambda bot: (not bot.special_active and
                                    (bot.bot_hp_percent() < 50) or
                                     bot.bot_hp_percent() < 20
                                ),
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() < 20
                                ),
                                lambda bot: (not bot.special_active and
                                    botchance.update(60)
                                ),
                                #sp logic
                                # Enemy is gone
                                lambda bot: (bot.special_active and
                                    bot.enemy_distance >= 100
                                ),
                            ]
                        }
                    },
                    'basic_attack': {
                        'atk_range': 40,
                        'min_cast_range': 30
                    }
                },

                'Chthulu': {
                    'default_timer': 1,
                    'timer_slow_decrease': 2,

                    'cast_special_threshold': self.get_special_threshold,
                    'special_if_sp_skill_ready': False,
                    'special_conditions': [False, 0],

                    'special_threshold': {
                        'health_high_prio': self.max_health * 0.4,
                        'low_prio': 0.01,
                        'high_prio': 0.01
                    },

                    'stuck_logic': {
                        'threshold': 100,
                        'detect': 200,
                        'duration': 0
                    },

                    'edge_escape_logic': {
                        'duration': 1.5,
                        'distance': 225
                    },

                    'took_alot_dmg': {
                        'damage_interval': 0.3,
                        'damage_threshold': 300.5,
                        'damage_taken_logic': 1,
                    },
                    
                    'panic_logic': {
                        'threshold': 0.01,
                        'cooldown': 4
                    },

                    'cast_special_threshold_distance': 500,

                    'random_unstuck': 0.0001,
                    'random_edge_escape': 0.000001,

                    'decide_logic': {
                        'chase_distance': 800,
                        'panic_chase_distance': 100,
                        'escape_distance': 300
                    },
                    
                    'skills': { # (not bot.player.attacking1 and not bot.player.attacking2 and not bot.player.attacking3) and
                                # the code above prevent the bot from using skill when the enemy is currently attacking, this can avoid the bot from using skills unneccesarily. only use when needed
                        'skill_1': {
                            'cast_range': 500,
                            'min_cast_range': 10,
                            'require_all': False,
                            'conditions': [
                                # Casual buff
                                lambda bot: (not bot.special_active and
                                    not bot.flying
                                    )
                            ]
                        },
                            
                        'skill_2': {
                            'cast_range': 1050,
                            'min_cast_range': 50,
                            'require_all': False,
                            'conditions': [
                                # Trick skill while buffed
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    not bot.player.sp_attacking
                                ),
                                # Prefer not to buff
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    bot.enemy_distance <= 500 and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    botchance.update(70)
                                ),
                                # If far, try to shoot, and if enemy is casting
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    bot.enemy_distance >= 500 and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    botchance.update(90)
                                ),
                                # Shoot if possible and enemy is while attacking
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() < 50 and
                                    bot.enemy_distance >= 100 and
                                    (bot.player.attacking1 or bot.player.attacking2 or bot.player.attacking3) and
                                    not bot.player.sp_attacking and
                                    botchance.update(90)
                                ),

                                #sp
                                # Trick skill while buffed
                                lambda bot: (bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    bot.enemy_distance >= 100
                                ),
                                # Casual skill
                                lambda bot: (bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    bot.enemy_distance >= 100 and
                                    bot.is_facing_from_enemy() and
                                    botchance.update(80)
                                ),
                                # Very casual skill, if enemy is casting
                                lambda bot: (bot.special_active and
                                    bot.bot_hp_percent() < 50 and
                                    bot.is_facing_from_enemy()
                                ),

                                
                            ]
                        },
                            
                        'skill_3': {
                            'cast_range': 400,
                            'min_cast_range': 100,
                            'not_require_facing_enemy': True,
                            'require_all': False,
                            'conditions': [
                                # Try to hit enemy
                               lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    bot.enemy_distance <= 300 and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    botchance.update(80)
                                ),
                                # Slightly far, will try to hit
                                lambda bot: (not bot.special_active and
                                    bot.bot_hp_percent() < 50 and
                                    bot.enemy_distance <= 5000 and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    botchance.update(90)
                                ),

                                #sp
                                # Cast before enemy go past through back
                                lambda bot: (bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    botchance.update(80)
                                ),
                                # Not preferably far but possible
                                lambda bot: (bot.special_active and
                                    bot.bot_hp_percent() >= 50 and
                                    bot.is_facing_from_enemy() and
                                    not bot.player.sp_attacking and
                                    botchance.update(60)
                                ),
                                # Will cast anyways
                                lambda bot: (bot.special_active and
                                    bot.bot_hp_percent() < 50 and
                                    not bot.player.sp_attacking and
                                    bot.is_facing_from_enemy()
                                ),
                                
                            ]
                        },
                        'skill_4': {
                            'cast_range': 50,
                            'min_cast_range': 2,
                            'require_all': False,
                            'conditions': [
                                # True,
                                # Prefer to use ultimate-like skill when special is ready and enemy is low
                                lambda bot: (not bot.special_active and
                                    (bot.player.attacking1 or bot.player.attacking2 or bot.player.attacking3 or bot.player.sp_attacking) and
                                    botchance.update(95)
                                ),
                                lambda bot: (bot.special_ready() and
                                    bot.enemy_hp_percent() <= 50 and
                                    bot.enemy_distance <= 80 and
                                    botchance.update(90)
                                ),
                                # If special active, try quick follow-up
                                lambda bot: (bot.special_active and
                                    bot.enemy_distance <= 250 and
                                    botchance.update(80)
                                )
                                # Casual skill, casts if enemy is using skill (can't be avoided)
                                # lambda bot: (not bot.special_active and
                                #     (bot.bot_hp_percent() < 50) or
                                #      bot.bot_hp_percent() < 20
                                # ),
                                # lambda bot: (not bot.special_active and
                                #     bot.bot_hp_percent() < 20
                                # ),
                                # lambda bot: (not bot.special_active and
                                #     botchance.update(60)
                                # ),
                                # #sp logic
                                # # Enemy is gone
                                # lambda bot: (bot.special_active and
                                #     bot.enemy_distance >= 100
                                # ),
                            ]
                        }
                    },
                    'basic_attack': {
                        'atk_range': 120,
                        'min_cast_range': 30
                    }
                }
            
            }

            if selected_hero.__name__ == 'Fire_Wizard' and 'Fire_Wizard' in self.hero_data:
                self.hero_bot = 'Fire_Wizard'
            elif selected_hero.__name__ == 'Wanderer_Magician' and 'Wanderer_Magician' in self.hero_data:
                self.hero_bot = 'Wanderer_Magician'
            elif selected_hero.__name__ == 'Fire_Knight' and 'Fire_Knight' in self.hero_data:
                self.hero_bot = 'Fire_Knight'
            elif selected_hero.__name__ == 'Wind_Hashashin' and 'Wind_Hashashin' in self.hero_data:
                self.hero_bot = 'Wind_Hashashin'
            elif selected_hero.__name__ == 'Water_Princess' and 'Water_Princess' in self.hero_data:
                self.hero_bot = 'Water_Princess'
            elif selected_hero.__name__ == 'Forest_Ranger' and 'Forest_Ranger' in self.hero_data:
                self.hero_bot = 'Forest_Ranger'
            elif selected_hero.__name__ == 'Yurei' and 'Yurei' in self.hero_data:
                self.hero_bot = 'Yurei'
            elif selected_hero.__name__ == 'Chthulu' and 'Chthulu' in self.hero_data:
                self.hero_bot = 'Chthulu'
            else:
                # self.hero.bot = selected_hero.__name__
                self.hero_bot = 'Fire_Wizard' # default
                # self.hero_bot = 'Wanderer_Magician'


            self.default_timer = self.hero_data[self.hero_bot]['default_timer'] / FPS
            self.time_reduce_rate = (self.hero_data[self.hero_bot]['timer_slow_decrease'] / FPS)

            # self.not_facing_enemy = self.hero_data[self.hero_bot].get('not_facing_enemy', False)
            
            #decisions
            self.chase_distance = self.hero_data[self.hero_bot]['decide_logic']['chase_distance']
            self.panic_chase_distance = self.hero_data[self.hero_bot]['decide_logic']['panic_chase_distance']
            self.escape_distance = self.hero_data[self.hero_bot]['decide_logic']['escape_distance']

            self.basic_atk_min_range = self.hero_data[self.hero_bot]['basic_attack']['min_cast_range']

            self.random_unstuck = self.hero_data[self.hero_bot]['random_unstuck']
            self.random_edge_escape = self.hero_data[self.hero_bot]['random_edge_escape']
            self.max_atk_range = self.hero_data[self.hero_bot]['basic_attack']['atk_range']
            self.special_in_range = self.enemy_distance <= self.hero_data[self.hero_bot]['cast_special_threshold_distance']

            self.last_hp = self.health
            self.hp_check_timer = 0
            self.hp_check_interval = self.hero_data[self.hero_bot]['took_alot_dmg']['damage_interval']  # seconds
            self.hp_damage_threshold = self.hero_data[self.hero_bot]['took_alot_dmg']['damage_threshold']  # how much damage before triggering escape
            self.detect_pos = self.hero_data[self.hero_bot]['took_alot_dmg']['damage_taken_logic'] # x pos range detect if not moving

            # Unstuck system
            self.prev_x_pos = self.x_pos
            self.stuck_timer = 0
            self.stuck_threshold = self.hero_data[self.hero_bot]['stuck_logic']['threshold']
            self.unstuck_mode = False
            self.unstuck_timer = 0
            self.unstuck_duration = self.hero_data[self.hero_bot]['stuck_logic']['duration']
            self.random_unstuck_direction = 0
            self.unstuck_detect = self.hero_data[self.hero_bot]['stuck_logic']['detect']

            # Edge escape
            self.edge_escape_mode = False
            self.edge_escape_timer = 0
            self.edge_escape_duration = self.hero_data[self.hero_bot]['edge_escape_logic']['duration']

            self.default_edge_distance = self.hero_data[self.hero_bot]['edge_escape_logic']['distance']
            self.edge_distance = 0

            self.last_panic_time = 0
            self.panic_cooldown = self.hero_data[self.hero_bot]['panic_logic']['cooldown']  # seconds

            self.special_threshold = self.hero_data[self.hero_bot]['cast_special_threshold']()
            self.sp_ready_condition = self.hero_data[self.hero_bot]['special_if_sp_skill_ready']
            self.special_conditions = self.hero_data[self.hero_bot]['special_conditions']

            #misc
            self.disable_special_min_atk_range = self.hero_data[self.hero_bot]['basic_attack'].get('disable_min_cast_range_while_special')
            from IntervalExecutor import IntervalExecutor

            self.print_timer = IntervalExecutor(0.5)

            self.enemy_on_right = self.x_pos < self.player.x_pos
            self.enemy_on_left = self.x_pos > self.player.x_pos

            
            
        def panic_mode(self):
            if time.time() - self.last_panic_time < self.panic_cooldown:
                return False
            panic = self.health < self.hero_data[self.hero_bot]['panic_logic']['threshold'] * self.max_health
            if panic:
                self.last_panic_time = time.time()
            #print(f"PANIC: Health={self.health}, Enemy HP%={self.enemy_hp_percent()}, Bot HP%={self.bot_hp_percent()}")
            return panic
        
        def special_ready(self):
            # print(f"Special ready: {self.special == 200 and not self.special_active}")
            # print(f'ads{self.mana >= self.max_mana * self.special_threshold}')
            # print(self.mana)
            # print(self.max_mana * self.special_threshold)
            # print(self.special_threshold)
            return self.special >= 200 and not self.special_active

        # def special_condition_threshold(self, skill):
        #     if self.mana / self.max_mana >= (1 if self.max_mana / self.attacks[skill].mana_cost <= 1 else 2 - self.max_mana / self.attacks[skill].mana_cost):
        #         return 2 - self.max_mana / self.attacks[skill].mana_cost
        #     else:
        #         return 1
        
        def get_special_threshold(self):
            self.health_high_prio = self.hero_data[self.hero_bot]['special_threshold']['health_high_prio']
            type_1 = self.hero_data[self.hero_bot]['special_threshold']['low_prio']
            type_2 = self.hero_data[self.hero_bot]['special_threshold']['high_prio']
            return type_1 if self.health >= self.health_high_prio else type_2

        def enemy_hp_percent(self):
            return (self.player.health / self.player.max_health) * 100 if self.player.max_health > 0 else 100 # Calculate the enemy's health percentage

        def bot_hp_percent(self):
            return (self.health / self.max_health) * 100 if self.max_health > 0 else 100 # Calculate the bot's health percentage

        # def update_self_max_mana(self):
        #     return self.max_mana

        def update_enemy_info(self):
            # print(self.state)
            # print(not self.special_active)
            # print(self.enemy_hp_percent() > 70)
            # print(self.mana >= self.attacks[1].mana_cost * 1.5)
            # print(botchance.update(90))
            # print(f'final result: {(not self.special_active and
            #                         self.enemy_hp_percent() >= 70 and
            #                         self.mana >= self.attacks[1].mana_cost * 1.5 and
            #                         botchance.update(90)
            #                     )}')
            if self.print_timer.should_run():
                
                pass
                # self.hehe()
            # print(self.state)
                # print()
                # print("Bot state:", self.state)
                # print()
                # print('condition 1:')
                # print(f"checking if bot is chase state: {self.state == 'chase'} ")
                # print(f"checking if enemy_hp_percent() <= 70: {self.enemy_hp_percent() <= 70}={self.enemy_hp_percent()}")
                # print(f"checking if  enemy_hp_percent() <  bot_hp_percent(): {self.enemy_hp_percent() < self.bot_hp_percent()}={self.enemy_hp_percent()}, {self.bot_hp_percent()}")
                # print('[CONDITION SATISFIED!!!]') if all([self.state == 'chase', self.enemy_hp_percent() <= 70, self.enemy_hp_percent() < self.bot_hp_percent()]) else print()
                # print('condition 2:')
                # print(f"checking if bot is escape state: {self.state == 'escape'} ")
                # print(f"checking if enemy distance <= 800: {self.enemy_distance <= 800}")
                # print(f"checking if you used any skills: {self.player.attacking1 or self.player.attacking2 or self.player.attacking3 or self.player.sp_attacking}")
                # print('[CONDITION SATISFIED!!!]') if all([self.state == 'escape', any([self.enemy_distance <= 800, self.player.attacking1, self.player.attacking2, self.player.attacking3, self.player.sp_attacking])]) else print()
            # rr = lambda bot: [False if bot.attacks[i].is_ready() else True for i in range(1,4)]
            # print(rr(self))
            #print(self.hero_bot)
            # print(not bot.attacks[3].is_ready())
            # print(self.enemy_distance)
            # print(self.special_active)
            # print(not self.attacks_special[3].is_ready())
            # print(f'not special {not self.special_active}')
            # print('CAST Special' if self.mana / self.max_mana >= (1 if self.max_mana / self.attacks[3].mana_cost <= 1 else 2 - self.max_mana / self.attacks[3].mana_cost) else 'dont', self.mana / self.max_mana, ' >= ', (1 if self.max_mana / self.attacks[3].mana_cost <= 1 else 2 - self.max_mana / self.attacks[3].mana_cost))
            # print((1 if self.max_mana / self.attacks[3].mana_cost <= 1 else 2 - self.max_mana / self.attacks[3].mana_cost))
            # print(self.attacks[3].mana_cost / self.max_mana)
            # print(self.mana / self.max_mana >= self.special_threshold)
            # print(self.special_threshold)
            # print(self.hero_data[self.hero_bot]['special_threshold']['low_prio'])
            # print(self.max_mana / self.attacks[3].mana_cost <= 1)
            # print(self.max_mana / self.attacks[3].mana_cost <= 1)
            # print(0 if self.mana / self.attacks[3].mana_cost >= 1 else 1)
            # Ensure bot always has a valid target
            self.ensure_target()
            target = self.target

            if target is None:
                # No target available; skip updating enemy info
                self.enemy_on_right = False
                self.enemy_on_left = False
                self.enemy_distance = 0
                return

            # Update position & distance relative to target
            self.enemy_on_right = self.x_pos < target.x_pos
            self.enemy_on_left = self.x_pos > target.x_pos
            self.enemy_distance = int(abs(target.x_pos - self.x_pos))

            # Edge detection
            self.left_edge = self.x_pos - self.edge_distance <= self.hitbox_rect.width
            self.right_edge = self.x_pos + self.edge_distance >= (TOTAL_WIDTH - self.hitbox_rect.width)

            # Stuck detection
            if abs(self.prev_x_pos - self.x_pos) < self.unstuck_detect and not self.state in ['idle', 'basic attack']:
                self.stuck_timer += self.default_timer
            else:
                self.stuck_timer = max(0, self.stuck_timer - self.time_reduce_rate)

            self.prev_x_pos = self.x_pos

            # Check stationary damage over interval
            self.hp_check_timer += self.default_timer
            if self.hp_check_timer >= self.hp_check_interval:
                is_still = abs(self.prev_x_pos - self.x_pos) < self.detect_pos and self.state in ['idle', 'basic attack', 'chase']
                hp_lost = self.last_hp - self.health

                if is_still and hp_lost >= self.hp_damage_threshold:
                    # Trigger escape due to damage while standing
                    self.unstuck_mode = True
                    self.unstuck_timer = 0
                    self.random_unstuck_direction = random.choice([-1, 1])

                self.last_hp = self.health
                self.hp_check_timer = 0

            # Activate unstuck if stuck long enough
            if not self.unstuck_mode and self.stuck_timer > self.stuck_threshold and self.state != 'basicattack':
                self.random_unstuck_direction = random.choice([-1, 1])
                self.unstuck_mode = True
                self.unstuck_timer = 0

            # Activate edge escape if too close to edge
            if not self.edge_escape_mode and (self.left_edge or self.right_edge):
                self.edge_escape_mode = True
                self.edge_escape_timer = 0

        def reset_inputs(self):
            
            #print(self.enemy_hp_percent())
            #print(f'thss{self.enemy_hp_percent()}')
            self.botkey_right = self.botkey_left = self.botkey_jump = False
            self.botkey_attack = self.botkey_special = False
            self.botkey_skill1 = self.botkey_skill2 = self.botkey_skill3 = self.botkey_skill4 = False
            self.forcemove_left = self.forcemove_right = False

        def decide_state(self):
            if callable(self.max_atk_range):
                dynamic_atk_range = self.max_atk_range(self)
            else:
                dynamic_atk_range = self.max_atk_range

            # self.last_state = getattr(self, 'last_state', None)
            # if self.state != self.last_state:
            #     print(f"[STATE CHANGE] {self.last_state} → {self.state}")
            # self.last_state = self.state

            #print(self.state, self.unstuck_mode, self.edge_escape_mode, self.random_unstuck_direction)
            #print(self.state, self.random_unstuck_direction, self.edge_distance)
            #print(self.state, not self.unstuck_mode, self.stuck_timer > self.stuck_threshold)
            #print state, edge or unstuck in words
            # print(self.enemy_distance, 'm')
            #print(self.state, self.unstuck_mode, self.edge_escape_mode, self.random_unstuck_direction)
            #print(not self.state in ['basic attack']
            if self.unstuck_mode:
                self.state = 'escape'
            elif self.edge_escape_mode:
                self.state = 'escape'

            elif self.panic_mode():
                if self.enemy_hp_percent() < self.bot_hp_percent():
                    if self.state == 'retreat_for_attack':
                        if self.enemy_on_left:
                            self.forcemove_right = True
                        elif self.enemy_on_right:
                            self.forcemove_left = True
                    elif self.enemy_distance <= dynamic_atk_range and not self.jumping: 
                            self.state = 'basic attack'
                    elif self.enemy_distance <= self.panic_chase_distance: # half of the initial chase distance
                        self.state = 'chase'
                    else:
                        self.state = 'idle'
                else:
                    # Escape only if enemy is strong and close
                    if self.enemy_distance <= self.escape_distance: # IMPORTANT: the highest cast range of all skills except skill 4, is skill 2, minus 10
                        self.state = 'escape'
                        if not self.unstuck_mode:
                            self.unstuck_mode = True
                            self.unstuck_timer = 0
                            self.random_unstuck_direction = random.choice([-1, 1])
                    else:
                        self.state = 'chase'

            # disable retreat when sp basic atk
            elif self.disable_special_min_atk_range and self.special_active and not self.jumping:
                self.state = 'basic attack'
            elif self.enemy_distance < self.basic_atk_min_range:
                if self.disable_special_min_atk_range and self.special_active:
                    pass
                else:
                    self.state = 'retreat_for_attack'

            #def face the enemy
            
            # Set state to basic attack based on dynamic attack range
            elif self.enemy_distance <= dynamic_atk_range and not self.jumping:
                self.state = 'basic attack'
            
            # chase logic
            elif self.enemy_distance <= self.chase_distance: # INITIAL CHASE DISTANCE
                self.state = 'chase'
            elif self.health < self.max_health:
                self.state = 'chase'
            else:
                self.state = 'idle'

        def face_enemy(self):
            if self.enemy_on_left and self.facing_right:
                self.facing_right = False
            elif self.enemy_on_right and not self.facing_right:
                self.facing_right = True

        def unface_enemy(self):
            if self.enemy_on_left and not self.facing_right:
                self.facing_right = True
            elif self.enemy_on_right and self.facing_right:
                self.facing_right = False

        def is_facing_away_from_enemy(self):
            return (self.enemy_on_left and self.facing_right) or (self.enemy_on_right and not self.facing_right)

        def is_facing_from_enemy(self):
            return (self.enemy_on_left and not self.facing_right) or (self.enemy_on_right and self.facing_right)
        
        def handle_movement(self):
            if self.state == 'escape':
                if self.edge_escape_mode:
                    self.unstuck_mode = False
                    self.edge_distance = self.default_edge_distance
                    self.edge_escape_timer += self.default_timer
                    self.botkey_jump = True

                    if self.left_edge:
                        self.botkey_right = True
                    elif self.right_edge:
                        self.botkey_left = True

                    if self.edge_escape_timer >= self.edge_escape_duration:
                        self.edge_distance = 0
                        self.edge_escape_mode = False
                    return
                
                elif self.unstuck_mode:
                    self.unstuck_timer += self.default_timer
                    self.botkey_jump = True

                    if self.disabled_random_unstuck_direction:
                        # Move away from the enemy (player)
                        if self.x_pos < self.player.x_pos:
                            self.botkey_left = True
                        elif self.x_pos > self.player.x_pos:
                            self.botkey_right = True
                    else:
                        # Default random movement
                        if self.random_unstuck_direction == -1:
                            self.botkey_left = True
                        elif self.random_unstuck_direction == 1:
                            self.botkey_right = True

                    if self.unstuck_timer >= self.unstuck_duration:
                        self.unstuck_mode = False
                        self.stuck_timer = 0
                    return


            if self.forcemove_left:
                self.facing_right = False
                self.botkey_left = True
                self.botkey_right = False
            elif self.forcemove_right:
                self.facing_right = True
                self.botkey_right = True
                self.botkey_left = False
            elif self.state == 'chase':
                self.botkey_right = self.enemy_on_right
                self.botkey_left = self.enemy_on_left

        def special_condition(self): # condition whether to continue using skills or not
            if self.special_conditions[0]: # [0] if true or not
                if self.special_conditions[1] == 0 and self.enemy_hp_percent() > self.bot_hp_percent(): # [1] condition type, if enemy is strong, don't use any skills, if enemy is weak, use skills
                    return True
                elif self.special_conditions[1] == 1 and self.enemy_hp_percent() < self.bot_hp_percent(): # [1] condition type, if enemy is weak, don't use any skills, if enemy is strong, use skills
                    return True
                elif self.special_conditions[1] == 2: # [1] condition type, don't use any skills at all
                    return True
                else:
                    return False
            else:
                return False # continue using skills even special is ready until special condition is met
            

        def cast_skills(self):
            # print(self.hero_bot, 'bot')
            # print(selected_hero.__name__, 'kurasu namae')
            debug = False
            self.forcemove_left = False
            self.forcemove_right = False
            if self.special_ready() and self.special_condition():
                if debug:
                    print("[SKIP] Special skill ready & conditions met — saving mana.")
                return
            
            if any([self.attacking1, self.attacking2, self.attacking3, self.sp_attacking]):
                return

            skills = self.hero_data[self.hero_bot]['skills']
            for i in range(4):
                skill_key = f'skill_{i+1}'
                skill = self.attacks_special[i] if self.special_active else self.attacks[i]
                config = skills[skill_key]

                if debug:
                    print(f"\n[SKILL CHECK] Evaluating {skill_key}...")

                # Mana and cooldown
                if self.mana < skill.mana_cost:
                    if debug:
                        print(f"[SKIP] Not enough mana ({self.mana}/{skill.mana_cost})")
                    continue
                if not skill.is_ready():
                    if debug:
                        print(f"[SKIP] Skill is on cooldown.")
                    continue

                min_r = config['min_cast_range']
                max_r = config['cast_range']
                not_facing_enemy = config.get('not_require_facing_enemy', False)
                allow_jump_cast = config.get('allow_while_jumping', False)
                #misc code
                face_enemy_away = config.get('face_away', False)
                force_escape = config.get('force_escape', False)
                self.disabled_random_unstuck_direction = config.get('disable_random_escape_direction', False) 

                # Jumping check
                if self.jumping and not allow_jump_cast:
                    if debug:
                        print(f"[SKIP] Cannot cast {skill_key} while jumping.")
                    continue


                # Evaluate conditions
                require_all = config.get('require_all', True)
                conditions = config.get('conditions', [])

                if callable(require_all):
                    result = require_all(self)
                else:
                    result = require_all

                if debug:
                    print(f"[CONDITIONS] require_all = {result}")
                    for idx, cond in enumerate(conditions):
                        try:
                            cond_result = cond(self) if callable(cond) else cond
                        except Exception as e:
                            print(f"[ERROR] Condition {idx+1} threw error: {e}")
                            cond_result = False
                        print(f"  Condition {idx+1}: {cond_result}")

                passed = (
                    result and all((cond(self) if callable(cond) else cond) for cond in conditions)
                ) or (
                    not result and any((cond(self) if callable(cond) else cond) for cond in conditions)
                )

                if not passed:
                    if debug:
                        print(f"[SKIP] Conditions not met for {skill_key}.")
                    continue

                # Distance handling
                # print(f"[DISTANCE] enemy_distance = {self.enemy_distance}, min_r = {min_r}, max_r = {max_r}")
                # print(f"[DISTANCE] enemy_distance = {self.enemy_distance}")
                if self.enemy_distance < min_r:
                    if debug:
                        print(f"[ACTION] Too close to cast — moving away from enemy.")
                    # self.unface_enemy()
                    self.state = 'retreat_for_attack'
                    if self.enemy_on_left:
                        self.forcemove_right = True
                    elif self.enemy_on_right:
                        self.forcemove_left = True
                    continue
                
                if self.enemy_distance <= max_r:
                    if not not_facing_enemy: # require facing enemy
                        facing_wrong = (
                            (self.enemy_on_left and self.facing_right) or
                            (self.enemy_on_right and not self.facing_right)
                        )
                        if debug:
                            print(f"[FACING] Facing right? {self.facing_right}, Enemy on right? {self.enemy_on_right}")
                        if facing_wrong:
                            if debug:
                                print(f"[ACTION] Turning to face enemy before casting.")
                            self.face_enemy() #DOUBLE CHECK JUST MAKING SURE (IN THE LOGIC FUNC, already face_enemy active, same for unface enemy)
                            self.state = 'chase'
                            return
                    else: # not require facing enemy, if True, then facing enemy is not required (bot no need to face enemy) damn so confusing
                        pass
                    if force_escape:
                        self.state = 'escape'
                    if face_enemy_away:
                        self.forcemove_left = False
                        self.forcemove_right = False
                        # print(f"[DEBUG] Bot facing_right: {self.facing_right}, enemy_on_right: {self.enemy_on_right}, is_facing_away: {self.is_facing_away_from_enemy()}")
                        if debug:
                            print(f"[FACING] Facing enemy away before casting.")
                        self.unface_enemy()
                        if debug:
                            print(f"[CAST] All checks passed. Casting {skill_key}!")
                        setattr(self, f'botkey_skill{i+1}', True)
                        return
                    else:
                        self.forcemove_left = False
                        self.forcemove_right = False
                        if debug:
                            print(f"[CAST] All checks passed. Casting {skill_key}!")
                        setattr(self, f'botkey_skill{i+1}', True)
                        return

                # print(f"[SKIP] Enemy out of cast range for {skill_key}.")
                        
                        

        def handle_attack(self):
            
            # if self.state != 'basic attack':
            #     return
            if callable(self.max_atk_range):
                dynamic_atk_range = self.max_atk_range(self)
            else:
                dynamic_atk_range = self.max_atk_range

            # print(dynamic_atk_range)

            if self.state == 'retreat_for_attack':
                if self.enemy_on_left:
                    self.forcemove_right = True
                elif self.enemy_on_right:
                    self.forcemove_left = True
            elif self.state == 'basic attack': # This code seems redundant
                if (self.enemy_on_left and not self.facing_right) or (self.enemy_on_right and self.facing_right):
                    if self.enemy_distance <= dynamic_atk_range:
                        self.botkey_attack = True

        def handle_special(self):
            if self.special_ready():
                facing_condition = (
                    (self.x_pos > self.player.x_pos and not self.facing_right) or
                    (self.x_pos < self.player.x_pos and self.facing_right)
                )
                # One liner gets me freaking confused, I'm gonna do it normal way bruh
                if (self.special_in_range and facing_condition and (self.mana / self.max_mana >= self.special_threshold)):
                    self.botkey_special = True
                elif self.special_in_range and facing_condition and self.sp_ready_condition:
                    if (self.mana / self.max_mana >= (self.attacks_special[3].mana_cost) / self.max_mana) and self.attacks_special[3].is_ready(): #Always cast special if mana == skill 4 and not special skill 4 if ready
                        self.botkey_special = True

        # def draw_distance(self): # self.enemy_distance = int(abs(self.player.x_pos - self.x_pos))
        #     enemy_distance = self.enemy_distance
        #     enemy_distance_surf = self.bot_default_font.render(str(enemy_distance), 0, 'Red')
        #     screen.blit(enemy_distance_surf, (self.player.x_pos, self.player.y_pos - 120))
        #     line_rect = pygame.rect.Rect((self.player.x_pos if self.x_pos > self.player.x_pos else self.x_pos), self.player.y_pos - 60, enemy_distance, 2)
        #     pygame.draw.rect(screen, 'Red', line_rect)

        def bot_logic(self):
            # print(self.is_facing_away_from_enemy())
            #print(self.enemy_distance)

            #print(self.hero_bot)

            #random unstuck 0.1%
            if random.random() < self.random_unstuck:
                self.unstuck_mode = True
                self.unstuck_timer = 0
                print('Bot is unstuck!')
                
            #random edge escape 0.0001%
            if random.random() < self.random_edge_escape:
                self.edge_escape_mode = True
                self.edge_escape_timer = 0
                print('Bot is edge escaping!')

            if random.random() < 1:
                self.botkey_jump = True
                    
            
            
            # self.draw_distance()
            # print(self.enemy_on_left, self.facing_right)
            # print(self.enemy_on_left and self.facing_right)

            self.reset_inputs()
            self.update_enemy_info()
            self.decide_state()

            if not self.unstuck_mode and not self.edge_escape_mode:
                self.face_enemy()
            #print(self.state)
            #print(self.state, self.unstuck_mode, self.edge_escape_mode)

            if (self.unstuck_mode or self.edge_escape_mode):
                # if not any([self.attacking1, self.attacking2, self.attacking3, self.sp_attacking]):
                #     self.unface_enemy()
                self.cast_skills()
                self.handle_movement()  # Only movement during escape
                
                
                return
            
            self.cast_skills()
            self.handle_attack()
            self.handle_special()
            self.handle_movement()

            

        def inputs(self):
            # print('asdasd')
            # print(self.enemy_hp_percent() < 90)
            # print(random.random() < 0.5)
            # print(self.health < self.max_health * 0.9)
            # print(self.health)
            # print(self.max_health * 0.9)  

            

            self.input(
                self.botkey_skill1,
                self.botkey_skill2,
                self.botkey_skill3,
                self.botkey_skill4,
                self.botkey_right,
                self.botkey_left,
                self.botkey_jump,
                self.botkey_attack,
                self.botkey_special,
            )
        
        def update(self):
            super().update()
            self.ensure_target()
            self.bot_logic()

            



        # debug purposes for print timer
        # def hehe(self):
        #     # print(self.hero_bot, 'bot')
        #     # print(selected_hero.__name__, 'kurasu namae')
        #     debug = True
        #     self.forcemove_left = False
        #     self.forcemove_right = False
        #     if self.special_ready() and self.special_condition():
        #         if debug:
        #             print("[SKIP] Special skill ready & conditions met — saving mana.")
        #         return
            
        #     if any([self.attacking1, self.attacking2, self.attacking3, self.sp_attacking]):
        #         return

        #     skills = self.hero_data[self.hero_bot]['skills']
        #     for i in range(4):
        #         skill_key = f'skill_{i+1}'
        #         skill = self.attacks_special[i] if self.special_active else self.attacks[i]
        #         config = skills[skill_key]

        #         if debug:
        #             print(f"\n[SKILL CHECK] Evaluating {skill_key}...")

        #         # Mana and cooldown
        #         if self.mana < skill.mana_cost:
        #             if debug:
        #                 print(f"[SKIP] Not enough mana ({self.mana}/{skill.mana_cost})")
        #             continue
        #         if not skill.is_ready():
        #             if debug:
        #                 print(f"[SKIP] Skill is on cooldown.")
        #             continue

        #         min_r = config['min_cast_range']
        #         max_r = config['cast_range']
        #         not_facing_enemy = config.get('not_require_facing_enemy', False)
        #         allow_jump_cast = config.get('allow_while_jumping', False)
        #         #misc code
        #         face_enemy_away = config.get('face_away', False)
        #         force_escape = config.get('force_escape', False)
        #         self.disabled_random_unstuck_direction = config.get('disable_random_escape_direction', False) 

        #         # Jumping check
        #         if self.jumping and not allow_jump_cast:
        #             if debug:
        #                 print(f"[SKIP] Cannot cast {skill_key} while jumping.")
        #             continue


        #         # Evaluate conditions
        #         require_all = config.get('require_all', True)
        #         conditions = config.get('conditions', [])

        #         if callable(require_all):
        #             result = require_all(self)
        #         else:
        #             result = require_all

        #         if debug:
        #             print(f"[CONDITIONS] require_all = {result}")
        #             for idx, cond in enumerate(conditions):
        #                 try:
        #                     cond_result = cond(self) if callable(cond) else cond
        #                 except Exception as e:
        #                     print(f"[ERROR] Condition {idx+1} threw error: {e}")
        #                     cond_result = False
        #                 print(f"  Condition {idx+1}: {cond_result}")

        #         passed = (
        #             result and all((cond(self) if callable(cond) else cond) for cond in conditions)
        #         ) or (
        #             not result and any((cond(self) if callable(cond) else cond) for cond in conditions)
        #         )

        #         if not passed:
        #             if debug:
        #                 print(f"[SKIP] Conditions not met for {skill_key}.")
        #             continue

        #         # Distance handling
        #         # print(f"[DISTANCE] enemy_distance = {self.enemy_distance}, min_r = {min_r}, max_r = {max_r}")
        #         # print(f"[DISTANCE] enemy_distance = {self.enemy_distance}")
        #         if self.enemy_distance < min_r:
        #             if debug:
        #                 print(f"[ACTION] Too close to cast — moving away from enemy.")
        #             # self.unface_enemy()
        #             self.state = 'retreat_for_attack'
        #             if self.enemy_on_left:
        #                 self.forcemove_right = True
        #             elif self.enemy_on_right:
        #                 self.forcemove_left = True
        #             continue
                
        #         if self.enemy_distance <= max_r:
        #             if not not_facing_enemy: # require facing enemy
        #                 facing_wrong = (
        #                     (self.enemy_on_left and self.facing_right) or
        #                     (self.enemy_on_right and not self.facing_right)
        #                 )
        #                 if debug:
        #                     print(f"[FACING] Facing right? {self.facing_right}, Enemy on right? {self.enemy_on_right}")
        #                 if facing_wrong:
        #                     if debug:
        #                         print(f"[ACTION] Turning to face enemy before casting.")
        #                     self.face_enemy() #DOUBLE CHECK JUST MAKING SURE (IN THE LOGIC FUNC, already face_enemy active, same for unface enemy)
        #                     self.state = 'chase'
        #                     return
        #             else: # not require facing enemy, if True, then facing enemy is not required (bot no need to face enemy) damn so confusing
        #                 pass
        #             if force_escape:
        #                 self.state = 'escape'
        #             if face_enemy_away:
        #                 self.forcemove_left = False
        #                 self.forcemove_right = False
        #                 # print(f"[DEBUG] Bot facing_right: {self.facing_right}, enemy_on_right: {self.enemy_on_right}, is_facing_away: {self.is_facing_away_from_enemy()}")
        #                 if debug:
        #                     print(f"[FACING] Facing enemy away before casting.")
        #                 self.unface_enemy()
        #                 if debug:
        #                     print(f"[CAST] All checks passed. Casting {skill_key}!")
        #                 setattr(self, f'botkey_skill{i+1}', True)
        #                 return
        #             else:
        #                 self.forcemove_left = False
        #                 self.forcemove_right = False
        #                 if debug:
        #                     print(f"[CAST] All checks passed. Casting {skill_key}!")
        #                 setattr(self, f'botkey_skill{i+1}', True)
        #                 return

        def input(self, hotkey1, hotkey2, hotkey3, hotkey4, right_hotkey, left_hotkey, jump_hotkey, basic_hotkey, special_hotkey):
            super().input(hotkey1, hotkey2, hotkey3, hotkey4, right_hotkey, left_hotkey, jump_hotkey, basic_hotkey, special_hotkey)
    

        # --- Attach retargeting utilities to Bot before returning ---
    def bot_select_target(self, policy=None):
        policy = policy or getattr(self, 'retarget_policy', 'closest')

        enemies = self.enemy if isinstance(self.enemy, list) else [self.enemy]
        enemies = [e for e in enemies if e is not None and not e.is_dead()]

        if not enemies:
            self.target = None
            return None

        if len(enemies) == 1:
            self.target = enemies[0]
            return enemies[0]

        if policy == "focus":
            if getattr(self, "target", None) in enemies:
                return self.target
            self.target = enemies[0]
            return self.target

        if policy == "random":
            self.target = random.choice(enemies)
            return self.target

        # nearest
        sx, sy = self.rect.center
        self.target = min(
            enemies,
            key=lambda e: (e.rect.centerx - sx)**2 + (e.rect.centery - sy)**2
        )
        return self.target


    # def bot_ensure_target(self):
    #     if not hasattr(self, "target") or self.target is None or self.target.is_dead():
    #         bot_select_target(self)


    def bot_ensure_target(self):
        """Ensure the bot always has a valid target."""
        if not hasattr(self, "target") or self.target is None or self.target.is_dead():
            bot_select_target(self)

        
    Bot.select_target = bot_select_target
    Bot.ensure_target = bot_ensure_target

    return Bot

# Change bot policy: (what bot will targets)
#bot.retarget_policy = "focus"

#bot.retarget_policy = "nearest"
#bot.retarget_policy = "random"

#sample usage
# BotClass = create_bot_class(PLAYER_2_SELECTED_HERO)
# bot_instance = BotClass(PLAYER_2)