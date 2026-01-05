import pygame
from player import Player
from heroes import Attacks, Attack_Display, load_attack, load_attack_flipped

import global_vars
from global_vars import (
    # icon
    ICON_WIDTH, ICON_HEIGHT, 
    # positioning
    X_POS_SPACING, START_OFFSET_X, SKILL_Y_OFFSET, SPACING_X, JUMP_DELAY,
    DEFAULT_X_POS, DEFAULT_Y_POS, DEFAULT_JUMP_FORCE,
    TOTAL_WIDTH, ZERO_WIDTH,
    # .
    DEFAULT_CHAR_SIZE, DEFAULT_CHAR_SIZE_2,
    # .
    DEFAULT_SPECIAL_SKILL_COOLDOWN,
    DEFAULT_HEALTH_REGENERATION, DEFAULT_MANA_REGENERATION,
)
class Phantom_Assassin(Player):
    def __init__(self, player_type, enemy):
        super().__init__(player_type, enemy)

        # Character Spritesheet with column and row
        # attack 1 - assets\characters\Phantom Assassin\Attack1.png 6 1
        # attack 2 - assets\characters\Phantom Assassin\Attack2.png 6 1
        # death - assets\characters\Phantom Assassin\Death.png 6 1
        # idle - assets\characters\Phantom Assassin\Idle.png 8 1
        # run - assets\characters\Phantom Assassin\Run.png 8 1
        # jump and fall (combine) - assets\characters\Phantom Assassin\Jump.png 2 1, assets\characters\Phantom Assassin\Fall.png 2 1

        # ----- Core -----
        self.player_type = player_type
        self.name = "Phantom Assasin"
        self.hitbox_rect = pygame.Rect(0, 0, 50, 100)
        self.x = 50
        self.y = 50
        self.width = 200

        # ----- Hero Specifications -----
        # Stats
        self.strength = 40
        self.intelligence = 40
        self.agility = 30

        self.base_health_regen = 0.8
        self.base_mana_regen = 5.3
        self.base_attack_damage = 0.1

        self.base_attack_speed = 100
        self.base_attack_time = 1700
        
        self.base_animation_speed = 120
        
        self.atk1_mana_cost = 20
        self.atk2_mana_cost = 20
        self.atk3_mana_cost = 20
        self.sp_mana_cost = 20
        
        self.atk1_cooldown = 1000
        self.atk2_cooldown = 1000
        self.atk3_cooldown = 1000
        self.sp_cooldown = 1000

        self.sp_atk1_mana_cost = 80
        self.sp_atk2_mana_cost = 70
        self.sp_atk3_mana_cost = 110
        self.sp_atk4_mana_cost = 80

        self.special_atk1_cooldown = 150
        self.special_atk2_cooldown = 120
        self.special_atk3_cooldown = 200
        self.special_atk4_cooldown = 200

        

        # Add more if damage list is not sufficient
        #   - base_damage, attack_frames, *variable
        #       *refer to the Player's existing variables, or create one if not enough
        #   - [0] = damage, [1] = final damage (applies at last frame)
        self.base_damage = {
            'atk1dmg': (10, 0),
            'atk2dmg': (15, 0),
            'atk3dmg': (10, 0),
            'atk4dmg': (10, 0),
            # For projectile damage
            #'sample': 20
        }

        # Sound Effects
        #   - str [0] file path
        #   - int [1] max volume
        sound1 = [r'assets\sound effects\wanderer_magician\shine-8-268901 1.mp3', 0.7]
        sound2 = [r'assets\sound effects\wanderer_magician\wind-chimes-2-199848 2.mp3', 0.7]
        sound3 = [r'assets\sound effects\wanderer_magician\elemental-magic-spell-impact-outgoing-228342 3.mp3', 0.7]
        sound4 = [r'assets\sound effects\wanderer_magician\Rasengan Sound Effect 4.mp3', 0.7]
        self.sound1 = self.load_sound(sound1[0])
        self.sound2 = self.load_sound(sound2[0])
        self.sound3 = self.load_sound(sound3[0])
        self.sound4 = self.load_sound(sound4[0])


        # Character Frame Source (remove the counting number)
        #   - str [0] file path
        #   - int [1] frame count - turn it into tuple to make it column and rows
        #   - bool [2] starts at zero 
        basic_attack_animation = [r'assets\attacks\Basic Attack\wanderer magician\basic atk\basic atk_', 5, False, 'frames']
        jumping_animation = [r'assets\characters\Phantom Assassin\Jump.png', (1,2), False, 'spritesheet']
        falling_animation = [r'assets\characters\Phantom Assassin\Fall.png', (1,2), False, 'spritesheet']

        running_animation = [r'assets\characters\Phantom Assassin\Run.png', (1,8), False, 'spritesheet']
        idle_animation = [r'assets\characters\Phantom Assassin\Idle.png', (1,8), False, 'spritesheet']
        death_animation = [r'assets\characters\Phantom Assassin\Death.png', (1,6), False, 'spritesheet']
        atk1_animation = [r'assets\characters\Phantom Assassin\Attack1.png', (1,6), False, 'spritesheet']
        atk2_animation = [r'assets\characters\Phantom Assassin\Attack2.png', (1,6), False, 'spritesheet']
        atk3_animiation = [r'assets\characters\Phantom Assassin\Attack3.png', (1,6), False, 'spritesheet']
        atk4_animation = [r'assets\characters\Phantom Assassin\Attack4.png', (1,6), False, 'spritesheet']

                
        # Attack Frame Count
        self.attack_frames = {
            'atk1frames': 24,
            'atk2frames': 14,
            'atk3frames': 34,
            'atk4frames': 52,
        }

        # Attack Frame Source (remove the counting number)
        #   - str [0] file path
        #   - int [1] frame count
        #   - bool [2] starts at zero
        atk1 = [r'assets\attacks\Phantom Assassin\atk1\?', 24, False]  # Assuming pathed frames
        atk2 = [r'assets\attacks\Phantom Assassin\atk2\?', 14, False]
        atk3 = [r'assets\attacks\Phantom Assassin\atk3\?', 34, False]
        atk4 = [r'assets\attacks\Phantom Assassin\atk4\?', 52, False]
        
        # Skill Icons Source
        default_skill_size = (ICON_WIDTH, ICON_HEIGHT) #touple type shi
        sk_1 = [r'assets\skill icons\onre\magic-summon-circle-purple-magic-footage-162703660_iconl.jpg', default_skill_size]
        sk_2 = [r'assets\skill icons\onre\person-fade-away-green-fog-260nw-2585215663.jpg', default_skill_size]
        sk_3 = [r'assets\skill icons\onre\a.jpg', default_skill_size]
        sk_4 = [r'assets\skill icons\onre\dark-silhouette-woman-windblown-hair-her-form-dissolving-chaotic-cloud-black-dust-dissolves-violently-particles-393542673.jpg', default_skill_size]
        sp = [r'assets\skill icons\onre\aa.jpg', default_skill_size]
        sp_sk_1 = [r'assets\skill icons\onre\magic-summon-circle-purple-magic-footage-162703660_iconl.jpg', default_skill_size]
        sp_sk_2 = [r'assets\skill icons\onre\person-fade-away-green-fog-260nw-2585215663.jpg', default_skill_size]
        sp_sk_3 = [r'assets\skill icons\onre\a.jpg', default_skill_size]
        sp_sk_4 = [r'assets\skill icons\onre\dark-silhouette-woman-windblown-hair-her-form-dissolving-chaotic-cloud-black-dust-dissolves-violently-particles-393542673.jpg', default_skill_size]

        skill_1_icon = self.load_img_scaled(sk_1[0], sk_1[1])
        skill_2_icon = self.load_img_scaled(sk_2[0], sk_2[1])
        skill_3_icon = self.load_img_scaled(sk_3[0], sk_3[1])
        skill_4_icon = self.load_img_scaled(sk_4[0], sk_4[1])
        special_icon = self.load_img_scaled(sp[0], sp[1])
        special_skill_1_icon = self.load_img_scaled(sp_sk_1[0], sp_sk_1[1])
        special_skill_2_icon = self.load_img_scaled(sp_sk_2[0], sp_sk_2[1])
        special_skill_3_icon = self.load_img_scaled(sp_sk_3[0], sp_sk_3[1])
        special_skill_4_icon = self.load_img_scaled(sp_sk_4[0], sp_sk_4[1])
        
        # Load Attack Frames (use the frame source)
        self.atk1 = self.load_img_frames(atk1[0], atk1[1], atk1[2], DEFAULT_CHAR_SIZE)
        self.atk2 = self.load_img_frames(atk2[0], atk2[1], atk2[2], DEFAULT_CHAR_SIZE)
        self.atk3 = self.load_img_frames(atk3[0], atk3[1], atk3[2], DEFAULT_CHAR_SIZE)
        self.atk4 = self.load_img_frames(atk4[0], atk4[1], atk4[2], DEFAULT_CHAR_SIZE)

        # Load Character Frames (search for the correct method to use in the base class (Player))
        self.player_jump = self.load_img_frames_v2(jumping_animation[0], jumping_animation[1], jumping_animation[2], DEFAULT_CHAR_SIZE, basic_attack_animation[3])
        self.player_jump_flipped = self.load_img_frames_v2(jumping_animation[0], jumping_animation[1], jumping_animation[2], DEFAULT_CHAR_SIZE, basic_attack_animation[3], True)
        self.player_falling = self.load_img_frames_v2(falling_animation[0], falling_animation[1], falling_animation[2], DEFAULT_CHAR_SIZE, falling_animation[3])
        self.player_falling_flipped = self.load_img_frames_v2(falling_animation[0], falling_animation[1], falling_animation[2], DEFAULT_CHAR_SIZE, falling_animation[3], True)  

        self.player_jump = self.player_jump + self.player_falling
        self.player_jump_flipped = self.player_jump_flipped + self.player_falling_flipped
         
        self.player_idle = self.load_img_frames_v2(idle_animation[0], idle_animation[1], idle_animation[2], DEFAULT_CHAR_SIZE, basic_attack_animation[3])
        self.player_idle_flipped = self.load_img_frames_v2(idle_animation[0], idle_animation[1], idle_animation[2], DEFAULT_CHAR_SIZE, basic_attack_animation[3], True)
        self.player_run = self.load_img_frames_v2(running_animation[0], running_animation[1], running_animation[2], DEFAULT_CHAR_SIZE, basic_attack_animation[3])
        self.player_run_flipped = self.load_img_frames_v2(running_animation[0], running_animation[1], running_animation[2], DEFAULT_CHAR_SIZE, basic_attack_animation[3], True)
        self.player_death = self.load_img_frames_v2(death_animation[0], death_animation[1], death_animation[2], DEFAULT_CHAR_SIZE, basic_attack_animation[3])
        self.player_death_flipped = self.load_img_frames_v2(death_animation[0], death_animation[1], death_animation[2], DEFAULT_CHAR_SIZE, basic_attack_animation[3], True)
        self.player_atk1 = self.load_img_frames_v2(atk1_animation[0], atk1_animation[1], atk1_animation[2], DEFAULT_CHAR_SIZE, basic_attack_animation[3])
        self.player_atk1_flipped = self.load_img_frames_v2(atk1_animation[0], atk1_animation[1], atk1_animation[2], DEFAULT_CHAR_SIZE, basic_attack_animation[3], True)
        self.player_atk2 = self.load_img_frames_v2(atk2_animation[0], atk2_animation[1], atk2_animation[2], DEFAULT_CHAR_SIZE, basic_attack_animation[3])
        self.player_atk2_flipped = self.load_img_frames_v2(atk2_animation[0], atk2_animation[1], atk2_animation[2], DEFAULT_CHAR_SIZE, basic_attack_animation[3], True)
        self.player_atk3 = self.load_img_frames_v2(atk3_animiation[0], atk3_animiation[1], atk3_animiation[2], DEFAULT_CHAR_SIZE, basic_attack_animation[3])
        self.player_atk3_flipped = self.load_img_frames_v2(atk3_animiation[0], atk3_animiation[1], atk3_animiation[2], DEFAULT_CHAR_SIZE, basic_attack_animation[3], True)
        self.player_sp = self.load_img_frames_v2(atk4_animation[0], atk4_animation[1], atk4_animation[2], DEFAULT_CHAR_SIZE, basic_attack_animation[3])
        self.player_sp_flipped = self.load_img_frames_v2(atk4_animation[0], atk4_animation[1], atk4_animation[2], DEFAULT_CHAR_SIZE, basic_attack_animation[3], True)
        
        self.player_basic = self.player_atk1
        self.player_basic_flipped = self.player_atk1_flipped

        # Player Image and Rect
        self.image = self.player_idle[self.player_idle_index]
        self.rect = self.image.get_rect(midbottom = (self.x_pos, self.y_pos))

        # Application
        self.max_health = self.strength * self.str_mult
        self.max_mana = self.intelligence * self.int_mult
        self.health = self.max_health
        self.mana = self.max_mana

        self.health_regen = self.calculate_regen(self.base_health_regen, self.hp_regen_per_str, self.strength) #0.8 + 40 * 0.01 = 1.2
        self.mana_regen = self.calculate_regen(self.base_mana_regen, self.mana_regen_per_int, self.intelligence) #5.3 + 40 * 0.01 = 5.7
        self.basic_attack_damage = self.calculate_regen(self.base_attack_damage, self.agi_mult, self.agility, basic_attack=True) # 0.1 + 26 * 0.1 = 2.7

        self.attack_speed = self.calculate_effective_as()
        self.basic_attack_animation_speed = self.base_animation_speed / (self.attack_speed / self.base_attack_speed)
        
        # set to new hp/mana
        self.white_health_p1 = self.health
        self.white_mana_p1 = self.mana   
        self.white_health_p2 = self.health
        self.white_mana_p2 = self.mana 

        # inherited
        self.atk1_damage = (
            self.base_damage['atk1dmg'][0] / self.attack_frames['atk1frames'],
            self.base_damage['atk1dmg'][0])
        self.atk2_damage = (
            self.base_damage['atk2dmg'][0] / self.attack_frames['atk2frames'],
            self.base_damage['atk2dmg'][0])
        self.atk3_damage = (
            self.base_damage['atk3dmg'][0] / self.attack_frames['atk3frames'],
            self.base_damage['atk3dmg'][0])
        self.sp_damage = (
            self.base_damage['atk4dmg'][0] / self.attack_frames['atk4frames'],
            self.base_damage['atk4dmg'][0])
        # For projectile damage
        # self.sample = self.base_damage['atk4dmg'][0]

        # apply Sound Effect Volume
        self.sound1.set_volume(sound1[1])
        self.sound2.set_volume(sound2[1])
        self.sound3.set_volume(sound3[1])
        self.sound4.set_volume(sound4[1])

        # player Icon Rects
        self.setup_skill_icon_rects(
            skill_icons=[
                skill_1_icon,
                skill_2_icon,
                skill_3_icon,
                skill_4_icon
            ],
            special_icon=special_icon,
            special_skill_icons=[
                special_skill_1_icon,
                special_skill_2_icon,
                special_skill_3_icon,
                special_skill_4_icon
            ],
            x_pos_spacing = X_POS_SPACING,
            start_offset_x = START_OFFSET_X,
            spacing_x = SPACING_X,
            skill_y_offset = SKILL_Y_OFFSET,
            default_x_pos = DEFAULT_X_POS,
        )

        # mana values
        self.mana_cost_list = [
            self.atk1_mana_cost,
            self.atk2_mana_cost,
            self.atk3_mana_cost,
            self.sp_mana_cost
        ]
        self.special_mana_cost_list = [
            self.sp_atk1_mana_cost,
            self.sp_atk2_mana_cost,
            self.sp_atk3_mana_cost,
            self.sp_atk4_mana_cost
        ]
        # modify the index on which skill has lowest mana cost
        self.lowest_mana_cost = self.mana_cost_list[0]

        # apply Attacks class (responsible for all skills)
        # --------------- Basic Skills ---------------
        self.attacks = [
            # Skills
            Attacks(
                skill_rect = self.skill_1_rect,
                skill_img = skill_1_icon,
                mana = self.mana,
                # ----------------------
                mana_cost = self.mana_cost_list[0],
                cooldown = self.atk1_cooldown
            ),
            Attacks(
                skill_rect = self.skill_2_rect,
                skill_img = skill_2_icon,
                mana = self.mana,
                # ----------------------
                mana_cost = self.mana_cost_list[1],
                cooldown = self.atk2_cooldown
            ),
            Attacks(
                skill_rect = self.skill_3_rect,
                skill_img = skill_3_icon,
                mana = self.mana,
                # ----------------------
                mana_cost = self.mana_cost_list[2],
                cooldown = self.atk3_cooldown
            ),
            Attacks(
                skill_rect = self.skill_4_rect,
                skill_img = skill_4_icon,
                mana = self.mana,
                # ----------------------
                mana_cost = self.mana_cost_list[3],
                cooldown = self.atk4_cooldown
            ),
            # Basic Attack (icon can be changed)
            Attacks(
                mana_cost=0,
                cooldown=self.basic_attack_cooldown,
                mana=self.mana,
                # ----------------------
                skill_rect=self.basic_icon_rect,
                skill_img=self.basic_icon,   
            ),
            # Special Skill
            Attacks(
                skill_rect=self.special_rect,
                skill_img=special_icon,
                mana=0,
                mana_cost=0,
                special_skill=True,
                # ----------------------
                cooldown=DEFAULT_SPECIAL_SKILL_COOLDOWN,
            )
        ]

        # --------------- Special Skills ---------------
        self.special_attacks = [
            # Skills
            Attacks(
                skill_rect = self.special_skill_1_rect,
                skill_img = special_skill_1_icon,
                mana = self.mana,
                # ----------------------
                mana_cost = self.special_mana_cost_list[0],
                cooldown = self.special_atk1_cooldown
            ),
            Attacks(
                skill_rect = self.special_skill_2_rect,
                skill_img = special_skill_2_icon,
                mana = self.mana,
                # ----------------------
                mana_cost = self.special_mana_cost_list[1],
                cooldown = self.special_atk2_cooldown
            ),
            Attacks(
                skill_rect = self.special_skill_3_rect,
                skill_img = special_skill_3_icon,
                mana = self.mana,
                # ----------------------
                mana_cost = self.special_mana_cost_list[2],
                cooldown = self.special_atk3_cooldown
            ),
            Attacks(
                skill_rect = self.special_skill_4_rect,
                skill_img = special_skill_4_icon,
                mana = self.mana,
                # ----------------------
                mana_cost = self.special_mana_cost_list[3],
                cooldown = self.special_atk4_cooldown
            ),
            # Basic Attack (icon can be changed)
            Attacks(
                mana_cost=0,
                cooldown=self.basic_attack_cooldown,
                mana=self.mana,
                # ----------------------
                skill_rect=self.basic_icon_rect,
                skill_img=self.basic_icon,   
            )
        ]

        self.skill_1 = self.attacks[0]
        self.skill_2 = self.attacks[1]
        self.skill_3 = self.attacks[2]
        self.skill_4 = self.attacks[3]
        self.basic_attack = self.attacks[4]
        self.activate_special = self.attacks[5]

        self.special_skill_1 = self.special_attacks[0]
        self.special_skill_2 = self.special_attacks[1]
        self.special_skill_3 = self.special_attacks[2]
        self.special_skill_4 = self.special_attacks[3]
        self.special_attack = self.special_attacks[4]
        
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
            
        
        if not self.is_jumping():
            if self.is_pressing(hotkey1) and not self.is_busy_attacking():
                if self.is_in_basic_mode():
                    if self.is_skill_ready(self.attacks, self.skill_1):
                        
                        frame_duration, repeat_animation = self.skill_duration(
                            set_mode = ('seconds', 1000),
                            frame_count = self.attack_frames['atk1frames']
                        )
                        attack = Attack_Display(
                            x=self.attack_position(self.rect, 'x', 20, True),
                            y=self.attack_position(self.rect, 'y', 20, False),
                            frames=self.attack_frame_count(self.atk1, self.atk1_flipped),
                            frame_duration=frame_duration,
                            repeat_animation=repeat_animation,
                            speed=6 if self.facing_right else -6,
                            dmg=self.atk1_damage[0],
                            final_dmg=self.atk1_damage[1],
                            who_attacks=self,
                            who_attacked=self.enemy,
                            moving=True,
                            delay=(True, 800),
                            sound=(True, self.atk1_sound, None, None),

                            hitbox_scale_x=0.4,
                            hitbox_scale_y=0.4
                            )
                        
                elif self.is_in_special_mode():
                    if self.is_skill_ready(self.mana, self.special_skill_1):

                        pass

                elif hotkey2 and not self.is_busy_attacking():
                    if self.is_in_basic_mode():
                        if self.is_skill_ready(self.mana, self.skill_2):
                            
                            frame_duration, repeat_animation = self.skill_duration(
                                set_mode = ('seconds', 1000),
                                frame_count = self.attack_frames['atk2frames']
                            )
                            attack = Attack_Display(
                                x=self.attack_position(self.rect, 'x', 20, True),
                                y=self.attack_position(self.rect, 'y', 20, False),
                                frames=self.attack_frame_count(self.atk2, self.atk2_flipped),
                                frame_duration=frame_duration,
                                repeat_animation=repeat_animation,
                                speed=0,
                                dmg=self.atk2_damage[0],
                                final_dmg=self.atk2_damage[1],
                                who_attacks=self,
                                who_attacked=self.enemy,
                                moving=False,
                                delay=(True, 800),
                                sound=(True, self.atk2_sound, None, None),

                                hitbox_scale_x=0.4,
                                hitbox_scale_y=0.4
                                )
                            
                    elif self.is_in_special_mode():
                        if self.is_skill_ready(self.mana, self.special_skill_2):

                            pass