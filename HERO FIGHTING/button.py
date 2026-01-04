import pygame
from global_vars import get_font, screen, width, height, white, TEXT_ANTI_ALIASING
import math
import time

def draw_black_screen(opacity, color=(0,0,0), size=(0, 0, width, height)):
    base_opacity = 255 * opacity
    rect = pygame.Rect(pygame.Rect(size[0], size[1], size[2], size[3]))
    overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

    # Fill it with the color + alpha
    overlay.fill((color[0],color[1],color[2], base_opacity))

    # Blit it on the target surface
    screen.blit(overlay, rect.topleft)

def create_title(text, font=None, scale=1, y_offset=100, color=white, angle=0, x_offset=width):
    title = pygame.transform.rotozoom(font.render(f'{text}', TEXT_ANTI_ALIASING, color), angle, scale)
    title_rect = title.get_rect(center = (x_offset / 2, y_offset))

    screen.blit(title, title_rect)


class ImageButton:
    def __init__(self, image_path, pos, scale, text, font_path, font_size, text_color, move_y=0, hover_move=2, fku=False, scale_val=(0,0), alpha=(1,1), text_anti_alias=True, y_margin=0):
        # Load and scale the image
        
        self.hover_pos = pos
        
        self.hover_move = hover_move
        self.fku = fku
        self.scale_val = scale_val
        self.alpha = alpha
        if self.fku:
            self.original_image = pygame.transform.scale(
        pygame.image.load(self.original_image).convert_alpha(), (self.scale_val[0], self.scale_val[1]))
        else:
            self.original_image = pygame.image.load(image_path).convert_alpha()

        self.image = pygame.transform.rotozoom(self.original_image, 0, scale)
        self.image.set_alpha(int(self.alpha[0] * 255))
        self.rect = self.image.get_rect(center=pos)
        self.height_from_B = self.rect[3]
        self.text_anti_alias = text_anti_alias
    
        
        
        
        
        # Text
        self.text = text 
        self.font = get_font(int(font_size*7.142857142857143), font_path) # Font size = 100
        self.text_color = text_color

        text_surf = self.font.render(self.text, self.text_anti_alias, self.text_color)
        text_surf.set_alpha(int(self.alpha[1] * 255))

        self.text_surf = pygame.transform.rotozoom(text_surf, 0, 0.2)
        # self.text_surf = text_surf
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        
        self.y_margin =  y_margin
        
    def draw(self, screen, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.rect.centery = self.hover_pos[1] + self.hover_move 
            self.text_rect.centery = self.hover_pos[1] + self.hover_move
        else:
            self.rect.centery = self.hover_pos[1]
            self.text_rect.centery = self.hover_pos[1]
        
        # Draw the image and text
        screen.blit(self.image, self.rect)
        screen.blit(self.text_surf, self.text_rect)



    def set_position(self, center): # this is the original position 
        dx = center[0] - self.rect.centerx 
        dy = center[1] - self.rect.centery - self.y_margin

        #----------


        self.rect.move_ip(dx, dy)
        self.hover_pos = (center[0], center[1] + self.y_margin)
        # self.text_rect.move_ip(dx, dy)
        #----------

        
        # print(dx, dy)

        self.rect.center = center

        self.hover_pos = (center)
        # self.hover_pos[1] += dy

        self.text_rect.x += dx
        self.text_rect.y += dy



    # Input below can only be checked at pygame.event.MOUSEBUTTON... or any input involving event
    def is_clicked(self, mouse_pos):
        # Check if button is clicked
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
    
    # self.rect.colliderect()
    def is_hovered(self, mouse_pos):
        # Check if button is hovered
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
    

    def animate(self,screen, keyframe):
        self.rect = self.image.get_rect(center=keyframe)
        screen.blit(self.image, self.rect)

        screen.blit(self.text_surf, self.text_rect)



# class Button:
#     def __init__(self, image_path:str, position:tuple[int, int], image_size:int, text:str, font_path:str, text_size:int, text_color:str):
#         self.image = pygame.transform.rotozoom(pygame.image.load(image_path).convert_alpha(), 0, image_size)
#         self.image_rect = self.image.get_rect(center = position)
        
#         font_size = int(text_size*7.142857142857143)
        
#         self.font = get_font(font_size, font_path)

#         # not scaled (font already scaled)
#         text_surf = self.font.render(self.text, self.text_anti_alias, self.text_color)
#         text_scale = 0.2
#         # scaled again
#         self.text_surf = pygame.transform.rotozoom(text_surf, 0, text_scale)
    

    
class ImageInfo:
    def __init__(self, image_path, pos, scale, text, text1, text2, font_path, font_size, text_color, move_y=0, hover_move=2):
        # Load and scale the image
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.rotozoom(self.original_image, 0, scale)
        self.rect = self.image.get_rect(center=pos)

        self.hover_pos = pos
        self.hover_move = hover_move
        
        # Text
        self.text = text
        self.text1 = text1
        self.text2 = text2

        self.font = pygame.font.Font(font_path, int(font_size*7.142857142857143)) # Font size = 100
        self.text_color = text_color

        self.text_surf = pygame.transform.rotozoom(self.font.render(self.text, self.text_anti_alias, self.text_color), 0, 0.2)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        
        self.text_surf1 = pygame.transform.rotozoom(self.font.render(self.text1, self.text_anti_alias, self.text_color), 0, 0.2)
        self.text_rect1 = self.text_surf.get_rect(center=(self.rect.centerx, self.rect.centery + 50))

        self.text_surf2 = pygame.transform.rotozoom(self.font.render(self.text2, self.text_anti_alias, self.text_color), 0, 0.2)
        self.text_rect2 = self.text_surf.get_rect(center=(self.rect.centerx, self.rect.centery + 100))

    def draw(self, screen, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.rect.centery = self.hover_pos[1] + self.hover_move 
            self.text_rect.centery = self.hover_pos[1] + self.hover_move
        else:
            self.rect.centery = self.hover_pos[1]
            self.text_rect.centery = self.hover_pos[1]
        
        # Draw the image and text
        screen.blit(self.image, self.rect)


        screen.blit(self.text_surf, self.text_rect)
        screen.blit(self.text_surf1, self.text_rect1)
        screen.blit(self.text_surf2, self.text_rect2)

    


    def is_clicked(self, mouse_pos):
        # Check if button is clicked
        if self.rect.collidepoint(mouse_pos):
            return True
        return False




class RectButton:
    def __init__(self, x:int, y:int, font:str, font_size:int, color:str, text:str, width:int=40, height:int=40, height_position:int=40):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(font, font_size)
        self.color = color
        self.text = text
        self.height_position = height_position
        self.rect_color = self.color
        self.x = x
        self.y = y
        self.width = width
        self.height_from_B = height + height_position
        self.height = height

        self.button_clicked = False
        self.button_hovered = False

        self.done_clicking = False
        self.enabled = False
    

        

    def set_position(self, pos: tuple):
        self.rect = pygame.Rect(pos[0] - self.width/2, pos[1], self.width, self.height)



    def draw(self, screen:pygame.Surface, text_anti_alias):
        pygame.draw.rect(screen, self.rect_color, self.rect)
        self.text_surf = self.font.render(self.text, text_anti_alias, 'white')
        self.text_rect = self.text_surf.get_rect(center=(self.rect.centerx, self.rect.centery-self.height_position))
        screen.blit(self.text_surf, self.text_rect)
        # pygame.draw.rect(screen, self.rect_color, self.rect)

    def is_clicked(self, mouse_pos): #only detects if the mouse is in the rect
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
    
    def is_switched(self, value=True , switch=True):
        if value and switch:
            self.enabled = not self.enabled
        if not switch:
            self.enabled = value
            print(self.enabled)
        return self.enabled


        return self.enabled
    def is_hovered(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
    def toggle(self, variable):
        return not variable
    
    def change_color(self, default=False, hovered=False, active=False, active_hovered=False):
        if active_hovered: # 200
            self.rect_color = (self.color[0]/1.275, self.color[1]/1.275, self.color[2]/1.275)

        elif active: # 150  
            self.rect_color = (self.color[0]/1.7, self.color[1]/1.7, self.color[2]/1.7)
        elif hovered: # 75
            self.rect_color = (self.color[0]/3.4, self.color[1]/3.4, self.color[2]/3.4)

        elif default:
            self.rect_color = (30,30,30)


     
    def update(self, mouse_pos, variable):
        if self.is_hovered(mouse_pos) and variable:
            self.change_color(active_hovered=True)
   

        elif variable:
            self.change_color(active=True)
  
        elif self.is_hovered(mouse_pos):
            self.change_color(hovered=True)

        else:
            self.change_color(default=True)

        

        # print(default, hovered, active, active_hovered)
    # def associate_value(self):
    #     return self.variable
    # def mouse_pressed(self, mouse_pos, pressed):
    #     return True if pressed else False

    # def update(self, screen:pygame.Surface, text_anti_alias, text, activate, variable=None, lambda_func=None):
    #     self.text = self.font.render(text, text_anti_alias, 'white')
        # for event in pygame.event.get():
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         if button_hovered:
        #             self.button_clicked = not self.button_clicked

        # keys = pygame.key.get_pressed()
        # mouse_pos = pygame.mouse.get_pos()
        # mouse_press = pygame.mouse.get_pressed()
        # key_press = pygame.key.get_pressed()
        # button_hovered = self.rect.collidepoint(mouse_pos)
        # for event in event_handler:

        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         if button_hovered:
        #             self.button_clicked = not self.button_clicked
                # self.do














import global_vars as g






class ModalObject:
    """
    Clickable selector for heroes, items, or maps with smooth movement on select.
    """
    # Default sizes
    PROFILE_SIZE = (75, 75)        # Heroes
    INGAME_SIZE = (50, 50)         # Items (your old size)
    DECOR_SIZE_LARGE = (85, 85)
    DECOR_OFFSET_LARGE = (42, 42)
    DECOR_SIZE_SMALL = (60, 60)
    DECOR_OFFSET_SMALL = (30, 30)
    DECOR_SIZE_SMALLEST = (30, 30)

    DESELECT_Y_OFFSET = -45

    def __init__(self, center_pos, size:tuple=(120,120),  inputobject:list=[], buttons:list=[], button_gap = 0.2, button_bottom_gap = 0.2, Title = "", description = " ", opacity = 1):
        """
        Args:
            image: str path or Surface
            center_pos: (x, y) tuple
            class_item: Hero class or Item instance
            small: True for item-sized icons (50x50)
            custom_size: (w, h) tuple for maps/other special sizes (overrides small)
            custom_border: (w, h) if custom_size is used. (for decor)
        """
        # self.class_item = class_item

        # if isinstance(image, str):
        #     original = pygame.image.load(image).convert_alpha()
        # else:
        # original = (100, 900)

        # Determine size
        self.opacity = opacity
        self.size = size
        profile_size = size
        # decor_size = [size[0], size[1]]
        decor_offset = [12, 12]
        self.description = description
        # self.profile = pygame.transform.scale(original, profile_size)
        # self.ingame_profile = pygame.transform.scale(original, (25, 25))  # always keep small version

    # Create profile rectangle (no image)
        self.profile_rect = pygame.Rect(*center_pos, *profile_size)
        self.profile_rect.center = center_pos

        # Create decor rectangle relative to profile
        self.decor_rect = pygame.Rect(
            self.profile_rect.centerx - decor_offset[0],
            self.profile_rect.centery - decor_offset[1],
            *size
            )

        self.button_gap = button_gap
        self.button_bottom_gap = size[1] * button_bottom_gap
        self.hovered = False
        self.selected = False
        self.disable_action = False

        self.original_pos = center_pos
        self.target_pos = center_pos
        self.move_speed = 0.1
        # print(self.original_pos)
        self.highlight_offset = (0, -50)  # Move right 10, up 20 when selected
        if len(buttons) > 1:
            self.button1 = buttons[0]
            self.button2 = buttons[1]
            
        self.inputobject = inputobject


        self.shake_count = 0
        self.shake_dir = False
        self.title = Title

    def shake_enable(self):
        gap = 0.1 if self.shake_dir else -0.1
        self.target_pos = (self.target_pos[0] * (1 + gap), self.target_pos[1])
        self.shake_dir = not self.shake_dir
        print(gap)
        print(self.target_pos)


    def shake(self, times):
        self.move_speed = 0.5
        print('waw')
        self.shake_count = times
        self.shake_enable()
    
    def set_position(self, new_center, instant=False, selectedval:bool = False):
        """
        Move the selector to a new center position.
        
        Args:
            new_center (tuple): New (x, y) center.
            instant (bool): If True, snap immediately (bypass lerp).
        """
        self.selected = selectedval
        if instant:
            self.target_pos = new_center
            self._apply_position(new_center)
        else:
            self.target_pos = new_center

    def _apply_position(self, center):
        # print(center)
        
        """Internal: Sync all rects to given center."""
        dx = center[0] - self.profile_rect.centerx
        dy = center[1] - self.profile_rect.centery
        # print(dx, dy)

        self.profile_rect.center = center
        self.decor_rect.move_ip(dx, dy)
        self.button1.set_position((center[0] * (1-(self.button_gap/2)), (center[1] + self.size[1]/2 - self.button1.height_from_B) - self.button_bottom_gap))
        self.button2.set_position((center[0] * (1+(self.button_gap/2)), (center[1] + self.size[1]/2 - self.button1.height_from_B) - self.button_bottom_gap)) # Assuming ImageButton has set_position # Full (x, y) with offset
        # If associated item needs to follow (e.g., for tooltip alignment)
        # if hasattr(self.class_item, 'set_position'):
        #     self.class_item.set_position(center)
        print(center[1])
        for num, i in enumerate(self.inputobject):
                i.set_position((center[0], center[1]*0.8 + 100 * num))
                # print((self.profile_rect.centerx, self.profile_rect.centery - 50 * num))
                i.draw(screen, g.TEXT_ANTI_ALIASING)
  
    def update(self, mouse_pos, mouse_pressed, other_selectors, max_selected=g.MAX_ITEM):
        # Smooth movement toward target
        

        if self.profile_rect.center != self.target_pos:
            

            current = [float(self.profile_rect.centerx), float(self.profile_rect.centery)]
            dx = self.target_pos[0] - current[0]
            dy = self.target_pos[1] - current[1]

            # If very close, snap exactly to avoid drift
            if abs(dx) <= 2 and abs(dy) <= 2:
                print("Snapped")
                self.disable_action = self.selected
                self._apply_position(self.target_pos)
                if self.shake_count:
                    self.shake_count -= 1
                    self.shake_enable()

                # self.enable_movement()
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
        # selected_count = sum(1 for s in other_selectors if s.selected)
        # can_select = selected_count < max_selected


        for i in self.inputobject:
                # i.set_position(self.profile_rect.center)
                i.draw(screen, g.TEXT_ANTI_ALIASING)
        # if not self.selected:
        self.button1.draw(g.screen, mouse_pos)
        self.button2.draw(g.screen, mouse_pos)
        # if self.decor_rect.collidepoint(mouse_pos) and self.can_move:
        #         self.hovered = True
        #         if mouse_pressed[0]:
        create_title(self.title, g.get_font(60) , 1, self.profile_rect.centery - (height * 0.2), angle=0, x_offset= self.profile_rect.centerx * 2)
        #             self.can_move = False
        #             self.selected = True
        create_title(self.description, g.get_font(60) , 0.8, self.profile_rect.centery, angle=0, x_offset= self.profile_rect.centerx * 2)

        #             self.move_variable = True
                    

        #             highlight_pos = (
        #                 self.original_pos[0] + self.highlight_offset[0],
        #                 self.original_pos[1] + self.highlight_offset[1]
        #             )
        #             self.set_position(highlight_pos)
        #             self.hovered = False
        # # else:
        # #         self.hovered = False
        # else:
        #     # Show and handle deselect button
            
        if mouse_pressed[0] and self.button1.is_clicked(mouse_pos):
                # self.move_back_variable = True
                # self.can_move_back = False
                # print(self.can_move_back)
                self.move_speed = 0.1
                self.set_position(self.original_pos)
                self.selected = False
                
                # print(self.target_pos)
        if mouse_pressed[0] and self.button2.is_clicked(mouse_pos):
                # self.move_back_variable = True
                # self.can_move_back = False
                # print(self.can_move_back)
                # self.set_position(self.original_pos)
                # self.selected = False
                # print(self.target_pos)
                pass
    






    def draw(self):
        """Draw border and profile image based on state."""
        color = g.gold if self.selected else g.white if self.hovered else g.black
        # pygame.draw.rect(g.screen, color, self.decor_rect)
        # g.screen.blit(self.profile_rect, self.profile_rect)
        # pygame.draw.rect(g.screen, (0, 0, 0, 0), self.profile_rect)
        # draw_black_screen(0.2,size=(width*0.05, height * 0.2, width*0.44, height*0.65))
        overlay = pygame.Surface(self.profile_rect.size, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 255 * self.opacity))  # RGBA (alpha = 120)

        g.screen.blit(overlay, self.profile_rect.topleft)

        
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
            color = g.gold
        elif hero_sp == 'item':
            color = g.cyan2
        else:
            color = g.black

        rect = profile.get_rect(center=center_pos)
        decor = pygame.Rect(rect.centerx - offset[0], rect.centery - offset[1], border[0], border[1])
        pygame.draw.rect(g.screen, color, decor)
        g.screen.blit(profile, rect)

        # Display cooldown if applicable
        if hasattr(self.class_item, 'cooldown') and self.class_item.cooldown > 0 and not g.PAUSED:
            current_time = pygame.time.get_ticks() / 1000 - g.PAUSED_TOTAL_DURATION / 1000
            remaining = self.class_item.cooldown - (current_time - self.class_item.last_used)
            if remaining > 0:
                font = g.get_font(15)
                text = font.render(f"{math.ceil(remaining)}", True, g.red)
                g.screen.blit(text, (center_pos[0] - text.get_width()//2, center_pos[1] - 30))
            else:
                font = g.get_font(15)
                text = font.render("ready", True, g.green)
                g.screen.blit(text, (center_pos[0] - text.get_width()//2, center_pos[1] - 30))

    
    
    def is_selected(self):
        return self.selected

    def get_associated(self):
        """Return the associated hero class or item."""
        return self.class_item

    # def show_hover_tooltip(self, position):
    #     """Display hero info tooltip on hover (if applicable)."""
    #     if (self.hovered and
    #         isinstance(self.class_item, type) and
    #         issubclass(self.class_item, g.Player)):
    #         hero_name = self.class_item.__name__.replace("_", " ")
    #         if hero_name in g.HERO_INFO:
                # info_bubble = ImageBro(
                #     image_path=text_box_img,
                #     pos=position,
                #     scale=2,
                #     text=f"{hero_name}, {HERO_INFO[hero_name]}",
                #     font_path=global_vars.FONT_PATH,
                #     font_size=font_size * 1.05,
                #     text_color='white',
                #     fku=True,
                #     scale_val=(150, 230),
                #     hover_move=0,
                #     player_info=True
                # )
                # info_bubble = ImageBro(
                #     image_path=g.text_box_img,
                #     pos=position,
                #     text=f"{hero_name}, {HERO_INFO[hero_name]}",
                #     font_path=g.FONT_PATH,
                #     font_size=g.font_size * 1.05,
                #     text_color='white',
                #     player_info=True,
                #     text_scale=1.3,  # Full size
                #     anchor='bottomright'
                # )
                # info_bubble.drawing_info(g.screen)
    