import pygame

import json
import os
import global_vars as g
   


data = {
"skill_1_p1" : (pygame.K_z,"Z"),
"skill_2_p1" : (pygame.K_x,"X"),
"skill_3_p1" : (pygame.K_c,"C"),
"skill_4_p1" : (pygame.K_v,"V"),
"basic_atk_p1" : (pygame.K_e,"E"),
"sp_skill_p1" : (pygame.K_f,"F"),

"jump_p1" : (pygame.K_w,"W"),
"left_move_p1" : (pygame.K_a,"A"),
"right_move_p1" : (pygame.K_d,"D"),



"skill_1_p2" : (pygame.K_u,"U"),
"skill_2_p2" : (pygame.K_i,"I"),
"skill_3_p2" : (pygame.K_o,"O"),
"skill_4_p2" : (pygame.K_p,"P"),

"basic_atk_p2" : (pygame.K_l,"L"),
"sp_skill_p2" : (pygame.K_k,"K"),

"jump_p2" : (pygame.K_UP,"UP"),
"left_move_p2" : (pygame.K_LEFT,"LEFT"),
"right_move_p2" : (pygame.K_RIGHT,"RIGHT"),


}










status = [
    # === Letters A-Z ===




    pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d,
    pygame.K_e, pygame.K_f, pygame.K_g, pygame.K_h,
    pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l,
    pygame.K_m, pygame.K_n, pygame.K_o, pygame.K_p,
    pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t,
    pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x,
    pygame.K_y, pygame.K_z,

    # === Top-Row Numbers ===
    pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3,
    pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7,
    pygame.K_8, pygame.K_9,

    # === Symbols (unshifted) ===
    pygame.K_MINUS,
    pygame.K_EQUALS,
    pygame.K_LEFTBRACKET,
    pygame.K_RIGHTBRACKET,
    pygame.K_BACKSLASH,
    pygame.K_SEMICOLON,
    pygame.K_QUOTE,
    pygame.K_COMMA,
    pygame.K_PERIOD,
    pygame.K_SLASH,
    pygame.K_BACKQUOTE,

    # === Space & Special Keys ===
    pygame.K_SPACE,
    pygame.K_TAB,
    pygame.K_BACKSPACE,
    pygame.K_SCROLLLOCK,
    pygame.K_NUMLOCK,
    pygame.K_PAUSE,

    # === Arrow Keys ===
    pygame.K_LEFT,
    pygame.K_RIGHT,
    pygame.K_UP,
    pygame.K_DOWN,

    # === Numpad Numbers (with NumLock ON) ===
    pygame.K_KP0, pygame.K_KP1, pygame.K_KP2,
    pygame.K_KP3, pygame.K_KP4, pygame.K_KP5,
    pygame.K_KP6, pygame.K_KP7, pygame.K_KP8,
    pygame.K_KP9,

    # === Numpad Operations ===
    pygame.K_KP_PLUS,
    pygame.K_KP_MINUS,
    pygame.K_KP_MULTIPLY,
    pygame.K_KP_DIVIDE,
    pygame.K_KP_PERIOD,

    # === Modifier Keys ===
    pygame.K_LSHIFT,
    pygame.K_RSHIFT,
    pygame.K_LCTRL,
    pygame.K_RCTRL,
    pygame.K_LALT,
    pygame.K_RALT,

    # === Media / Extra Keys ===
    pygame.K_INSERT,
    pygame.K_HOME,
    pygame.K_END,
    pygame.K_PAGEUP,
    pygame.K_PAGEDOWN,
    pygame.K_DELETE,
]

os.makedirs("key_settings", exist_ok=True)
filename = f"key_settings/keybinds_{g.user_id}.json"

    

def read_settings():

    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                Main_Keybinds = json.load(f)      # Load existing dictionary
            except json.JSONDecodeError:
                print("Error") 
                Main_Keybinds = data
                        # If file empty or invalid, start fresh
    else:
        Main_Keybinds = data

    return Main_Keybinds

def write_settings():
    if os.path.exists(filename):
        return None
    else:
        with open(filename, "w") as f:
            json.dump(data, f, indent = 4)





    



detect_key_skill = {
"read_skill_1_p1" : False,
"read_skill_2_p1" : False,
'read_skill_3_p1' : False,
"read_skill_4_p1" : False,

"read_basic_atk_p1" : False,
"read_sp_skill_p1" : False,

"read_jump_p1" : False,
"read_left_move_p1" : False,
"read_right_move_p1" : False,





"read_skill_1_p2" : False,
"read_skill_2_p2" : False,
'read_skill_3_p2' : False,
"read_skill_4_p2" : False,

"read_basic_atk_p2" : False,
"read_sp_skill_p2" : False,

"read_jump_p2" : False,
"read_left_move_p2" : False,
"read_right_move_p2" : False


}






























# pygame.init()
# fps = 60
# screen = pygame.display.set_mode((100, 100))
# clock = pygame.time.Clock()

# a = pygame.K_a
# b = pygame.K_b
# print(a)
# lists = {
# pygame.K_a : "A"
# }


# def main():
#     while True:
#         keys = pygame.key.get_pressed()
#         # mouse_pos = pygame.mouse.get_pos()
#         # mouse_press = pygame.mouse.get_pressed()
#         # key_press = pygame.key.get_pressed()

#         screen.fill((0, 255, 0))
#         # event ---------------------
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 exit() 
#             # if event.type == pygame.MOUSEBUTTONDOWN:
#             #     if menu_button.is_clicked(event.pos):
#             #         menu() 
#             #         return
#         if keys[lists['skl_1']]:
#             # print(len(keys))
#             print(pygame.K_b)



#         # enter ur logic here -----------------
#         for index,key_type in enumerate(keys):
#             if key_type == True:
#                 break


#         # end ------------------
#         pygame.display.update()
#         clock.tick(fps)
# main()  

