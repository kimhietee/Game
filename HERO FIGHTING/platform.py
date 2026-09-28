import pygame
import os
from path_helper import resource_path

class Platform(pygame.sprite.Sprite):
    """A fully configurable platform for the Hero Fighting game.
    
    Supports custom positioning, sizing, image rendering modes, adjustable hitboxes,
    and per-level design attributes like friction, bounce, breakability, and movement.
    
    Image Modes:
        - "normal"  : Draw at original size, centered. Clipped if larger, color-filled if smaller.
        - "stretch" : Scale to exactly fill width x height (may distort).
        - "crop"    : Draw at original size, clipped to platform rect.
        - "tile"    : Repeat the image across the platform area.
        - "fit"     : Scale to fit inside width x height, preserving aspect ratio.
    
    Platform Types:
        - "solid"        : Normal solid platform (can't pass through from any direction).
        - "pass_through" : Can jump through from below, land on top.
        - "one_way"      : Same as pass_through (alias).
        - "breakable"    : Breaks after a number of landings.
        - "moving"       : Moves along a path of waypoints.
        - "slippery"     : Reduces player friction (ice-like).
        - "bouncy"       : Bounces the player upward on landing.
    
    Usage Example:
        platform = Platform(
            x=400, y=400, width=200, height=20,
            image_path='assets/platforms/stone.png',
            image_mode='tile',
            platform_type='solid'
        )
        
        # In your level setup:
        import global_vars
        global_vars.active_platforms.append(platform)
    """

    def __init__(self,
                 # === Core positioning & size ===
                 x=0, y=0,
                 width=200, height=20,
                 anchor="topleft",

                 # === Image & appearance ===
                 image_path=None,
                 image_mode="stretch",
                 color=(100, 100, 100),
                 opacity=255,
                 visible=True,

                 # === Hitbox customization ===
                 hitbox_offset_x=0,
                 hitbox_offset_y=0,
                 hitbox_width=None,
                 hitbox_height=10,
                 landing_tolerance=8.0,
                 edge_forgiveness=5.0,

                 # === Platform behavior ===
                 platform_type="solid",
                 friction=1.0,
                 bounce_force=0,

                 # === Breakable settings ===
                 breakable_hp=0,
                 break_delay=0,
                 respawn_time=0,

                 # === Moving platform settings ===
                 move_path=None,
                 move_speed=1.0,
                 move_loop=True,

                 # === Misc ===
                 active=True,
                 z_order=0,
                 debug_show_hitbox=False
                 ):
        super().__init__()

        # ─── Core ────────────────────────────────────────────
        self.width = width
        self.height = height
        self.anchor = anchor

        # Convert anchor to topleft internally
        self.x, self.y = self._anchor_to_topleft(x, y, anchor)

        # ─── Image & Appearance ──────────────────────────────
        self.image_path = image_path
        self.image_mode = image_mode
        self.color = color
        self.opacity = opacity
        self.visible = visible

        # Load the source image (if provided)
        self._source_image = None
        if image_path:
            self._load_source_image(image_path)

        # Build the rendered surface
        self._surface = None
        self._rebuild_surface()

        # pygame.sprite.Sprite requirements
        self.image = self._surface
        self.rect = self._surface.get_rect(topleft=(self.x, self.y))

        # ─── Hitbox ──────────────────────────────────────────
        self.hitbox_offset_x = hitbox_offset_x
        self.hitbox_offset_y = hitbox_offset_y
        self.hitbox_width = hitbox_width if hitbox_width is not None else width
        self.hitbox_height = hitbox_height
        self.landing_tolerance = landing_tolerance
        self.edge_forgiveness = edge_forgiveness

        self.hitbox_rect = self._build_hitbox()

        # ─── Platform Behavior ───────────────────────────────
        self.platform_type = platform_type
        self.friction = friction
        self.bounce_force = bounce_force

        # ─── Breakable ───────────────────────────────────────
        self.breakable_hp = breakable_hp
        self._max_breakable_hp = breakable_hp
        self.break_delay = break_delay
        self.respawn_time = respawn_time
        self._breaking = False
        self._break_timer = 0
        self._broken = False
        self._respawn_timer = 0

        # ─── Moving ─────────────────────────────────────────
        self.move_path = move_path if move_path else []
        self.move_speed = move_speed
        self.move_loop = move_loop
        self._move_index = 0
        self._move_forward = True
        self._origin_x = self.x
        self._origin_y = self.y
        # If move_path is set, insert starting position as first waypoint
        if self.move_path and (self.x, self.y) != tuple(self.move_path[0]):
            self.move_path.insert(0, (self.x, self.y))

        # ─── Misc ───────────────────────────────────────────
        self.active = active
        self.z_order = z_order
        self.debug_show_hitbox = debug_show_hitbox

    # ═══════════════════════════════════════════════════════
    #  ANCHOR HELPERS
    # ═══════════════════════════════════════════════════════

    def _anchor_to_topleft(self, x, y, anchor):
        """Convert an anchor-relative position to topleft coordinates."""
        if anchor == "center":
            return x - self.width // 2, y - self.height // 2
        elif anchor == "midtop":
            return x - self.width // 2, y
        elif anchor == "midbottom":
            return x - self.width // 2, y - self.height
        else:  # "topleft" or default
            return x, y

    # ═══════════════════════════════════════════════════════
    #  IMAGE LOADING & SURFACE BUILDING
    # ═══════════════════════════════════════════════════════

    def _load_source_image(self, path):
        """Load the source image from disk."""
        try:
            resolved = resource_path(path)
            self._source_image = pygame.image.load(resolved).convert_alpha()
        except (FileNotFoundError, pygame.error) as e:
            print(f"[Platform] Warning: Could not load image '{path}': {e}")
            self._source_image = None

    def _rebuild_surface(self):
        """Build the final rendered surface based on image_mode."""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        if self._source_image is None:
            # No image — solid color fill
            surface.fill(self.color)
        else:
            # Fill background color first (visible in "normal" and "fit" modes)
            surface.fill(self.color)

            if self.image_mode == "stretch":
                scaled = pygame.transform.scale(self._source_image, (self.width, self.height))
                surface.blit(scaled, (0, 0))

            elif self.image_mode == "normal":
                # Center the image at its original size
                img_w, img_h = self._source_image.get_size()
                blit_x = (self.width - img_w) // 2
                blit_y = (self.height - img_h) // 2
                surface.blit(self._source_image, (blit_x, blit_y))

            elif self.image_mode == "crop":
                # Draw from the top-left of the image, clipped to platform size
                surface.blit(self._source_image, (0, 0),
                             area=pygame.Rect(0, 0, self.width, self.height))

            elif self.image_mode == "tile":
                img_w, img_h = self._source_image.get_size()
                if img_w > 0 and img_h > 0:
                    for tx in range(0, self.width, img_w):
                        for ty in range(0, self.height, img_h):
                            # Clip the last tile if it overflows
                            clip_w = min(img_w, self.width - tx)
                            clip_h = min(img_h, self.height - ty)
                            surface.blit(self._source_image, (tx, ty),
                                         area=pygame.Rect(0, 0, clip_w, clip_h))

            elif self.image_mode == "fit":
                img_w, img_h = self._source_image.get_size()
                if img_w > 0 and img_h > 0:
                    scale_x = self.width / img_w
                    scale_y = self.height / img_h
                    scale = min(scale_x, scale_y)
                    new_w = int(img_w * scale)
                    new_h = int(img_h * scale)
                    scaled = pygame.transform.scale(self._source_image, (new_w, new_h))
                    blit_x = (self.width - new_w) // 2
                    blit_y = (self.height - new_h) // 2
                    surface.blit(scaled, (blit_x, blit_y))

        # Apply opacity
        if self.opacity < 255:
            surface.set_alpha(self.opacity)

        self._surface = surface

    def set_image(self, image_path, image_mode=None):
        """Change the platform's image at runtime.
        
        Args:
            image_path: Path to the new image file.
            image_mode: Optionally change the rendering mode too.
        """
        self.image_path = image_path
        if image_mode is not None:
            self.image_mode = image_mode
        self._load_source_image(image_path)
        self._rebuild_surface()
        self.image = self._surface

    def set_image_mode(self, mode):
        """Change the image rendering mode and rebuild the surface.
        
        Args:
            mode: One of "normal", "stretch", "crop", "tile", "fit".
        """
        self.image_mode = mode
        self._rebuild_surface()
        self.image = self._surface

    # ═══════════════════════════════════════════════════════
    #  HITBOX
    # ═══════════════════════════════════════════════════════

    def _build_hitbox(self):
        """Build the collision hitbox rect based on current settings."""
        hx = self.x + (self.width - self.hitbox_width) // 2 + self.hitbox_offset_x
        hy = self.y + self.hitbox_offset_y
        return pygame.Rect(hx, hy, self.hitbox_width, self.hitbox_height)

    def get_hitbox(self):
        """Return the current hitbox rect (updated position)."""
        return self.hitbox_rect

    def set_hitbox(self, offset_x=None, offset_y=None, width=None, height=None,
                   landing_tolerance=None, edge_forgiveness=None):
        """Modify hitbox parameters at runtime.
        
        Only pass the values you want to change; others stay unchanged.
        
        Args:
            offset_x: Shift collision zone left/right relative to platform center.
            offset_y: Shift collision zone up/down.
            width: Override collision width.
            height: Collision zone thickness.
            landing_tolerance: Max downward velocity for catching the platform.
            edge_forgiveness: Extra margin pixels on left/right edges.
        """
        if offset_x is not None:
            self.hitbox_offset_x = offset_x
        if offset_y is not None:
            self.hitbox_offset_y = offset_y
        if width is not None:
            self.hitbox_width = width
        if height is not None:
            self.hitbox_height = height
        if landing_tolerance is not None:
            self.landing_tolerance = landing_tolerance
        if edge_forgiveness is not None:
            self.edge_forgiveness = edge_forgiveness
        self.hitbox_rect = self._build_hitbox()

    def set_position(self, x, y, anchor=None):
        """Move the platform to a new position.
        
        Args:
            x: New x coordinate.
            y: New y coordinate.
            anchor: Anchor point ("topleft", "center", "midtop", "midbottom").
                    If None, uses the anchor set during construction.
        """
        if anchor is not None:
            self.anchor = anchor
        self.x, self.y = self._anchor_to_topleft(x, y, self.anchor)
        self.rect.topleft = (self.x, self.y)
        self.hitbox_rect = self._build_hitbox()

    def set_size(self, width, height):
        """Resize the platform and rebuild its surface and hitbox.
        
        Args:
            width: New width in pixels.
            height: New height in pixels.
        """
        self.width = width
        self.height = height
        # Update hitbox width if it was tracking platform width
        if self.hitbox_width == self.width:
            self.hitbox_width = width
        self._rebuild_surface()
        self.image = self._surface
        self.rect = self._surface.get_rect(topleft=(self.x, self.y))
        self.hitbox_rect = self._build_hitbox()

    # ═══════════════════════════════════════════════════════
    #  COLLISION DETECTION
    # ═══════════════════════════════════════════════════════

    def check_landing(self, player):
        """Determine if a player should land on this platform.
        
        This uses smart collision that prevents the "magnet" effect:
        - Only catches the player when falling downward
        - Respects landing_tolerance to avoid snapping at high speeds
        - Uses edge_forgiveness for natural edge behavior
        - For pass-through platforms, only catches from above
        
        Args:
            player: A Player instance with x_pos, y_pos, y_velocity, hitbox_rect.
            
        Returns:
            True if the player should land on this platform, False otherwise.
        """
        if not self.active or self._broken:
            return False

        # Player must be falling (positive y_velocity = moving downward)
        if player.y_velocity <= 0:
            return False

        # For pass-through / one-way platforms, player must be coming from above
        if self.platform_type in ("pass_through", "one_way"):
            # Player's feet must have been above the platform top last frame
            player_feet_prev = player.y_pos - player.y_velocity
            if player_feet_prev > self.hitbox_rect.top:
                return False

        # Check if player's downward velocity is within tolerance
        # (prevents magnet-snapping at extreme speeds)
        if player.y_velocity > self.landing_tolerance * 3:
            # At very high speeds, still allow landing but with stricter checks
            pass

        # Get player's horizontal center (feet position)
        player_center_x = player.x_pos
        player_feet_y = player.y_pos

        # Horizontal overlap check with edge forgiveness
        hitbox = self.hitbox_rect
        left_bound = hitbox.left - self.edge_forgiveness
        right_bound = hitbox.right + self.edge_forgiveness

        if player_center_x < left_bound or player_center_x > right_bound:
            return False

        # Vertical check: player's feet must be crossing the platform top
        # (within one frame of movement)
        platform_top = hitbox.top
        player_prev_feet = player_feet_y - player.y_velocity

        # Player was above (or at) platform top last frame, and is now at or below
        if player_prev_feet <= platform_top and player_feet_y >= platform_top:
            # Land the player
            player.y_pos = platform_top
            player.y_velocity = 0
            player.jumping = False
            if player.stunned:
                player.stunned = False
            return True

        # Also check if player is within the hitbox height zone
        # (handles cases where player is exactly on the platform)
        if (platform_top <= player_feet_y <= platform_top + hitbox.height and
                player_prev_feet <= platform_top + hitbox.height):
            player.y_pos = platform_top
            player.y_velocity = 0
            player.jumping = False
            if player.stunned:
                player.stunned = False
            return True

        return False

    def is_player_on(self, player):
        """Check if a player is currently standing on this platform.
        
        Used to detect when a player walks off the edge (should start falling).
        
        Args:
            player: A Player instance.
            
        Returns:
            True if the player is on this platform.
        """
        if not self.active or self._broken:
            return False

        hitbox = self.hitbox_rect
        player_center_x = player.x_pos
        player_feet_y = player.y_pos

        # Check horizontal bounds (with forgiveness)
        left_bound = hitbox.left - self.edge_forgiveness
        right_bound = hitbox.right + self.edge_forgiveness

        # Check if player is on the platform surface
        on_surface = abs(player_feet_y - hitbox.top) <= 2  # Within 2px of surface
        in_bounds = left_bound <= player_center_x <= right_bound

        return on_surface and in_bounds

    # ═══════════════════════════════════════════════════════
    #  EFFECTS
    # ═══════════════════════════════════════════════════════

    def apply_effects(self, player):
        """Apply platform-specific effects to a player standing on it.
        
        Called each frame while the player is on the platform.
        
        Args:
            player: A Player instance.
        """
        # Friction (affects horizontal movement speed)
        if self.friction != 1.0:
            player.speed = player.default_speed * self.friction

        # Bounce
        if self.bounce_force > 0:
            player.y_velocity = -self.bounce_force
            player.jumping = True
            player.on_platform = None
            return  # Don't stay on a bouncy platform

        # Breakable
        if self.breakable_hp > 0 and not self._breaking:
            self.breakable_hp -= 1
            if self.breakable_hp <= 0:
                self._breaking = True
                self._break_timer = pygame.time.get_ticks()
                if self.break_delay == 0:
                    self._do_break()

    def _do_break(self):
        """Actually break the platform (make it inactive)."""
        self._broken = True
        self._breaking = False
        self.active = False
        if self.respawn_time > 0:
            self._respawn_timer = pygame.time.get_ticks()

    def _do_respawn(self):
        """Respawn the platform after it was broken."""
        self._broken = False
        self.active = True
        self.breakable_hp = self._max_breakable_hp

    # ═══════════════════════════════════════════════════════
    #  MOVEMENT
    # ═══════════════════════════════════════════════════════

    def _update_movement(self):
        """Update moving platform position along its path."""
        if not self.move_path or len(self.move_path) < 2:
            return

        # Current target waypoint
        target = self.move_path[self._move_index]
        dx = target[0] - self.x
        dy = target[1] - self.y
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist <= self.move_speed:
            # Arrived at waypoint
            self.x, self.y = target[0], target[1]

            if self.move_loop:
                # Loop: go to next waypoint, wrap around
                self._move_index = (self._move_index + 1) % len(self.move_path)
            else:
                # Ping-pong
                if self._move_forward:
                    self._move_index += 1
                    if self._move_index >= len(self.move_path):
                        self._move_index = len(self.move_path) - 2
                        self._move_forward = False
                else:
                    self._move_index -= 1
                    if self._move_index < 0:
                        self._move_index = 1
                        self._move_forward = True
        else:
            # Move towards target
            move_x = (dx / dist) * self.move_speed
            move_y = (dy / dist) * self.move_speed
            self.x += move_x
            self.y += move_y

        # Update rects
        self.rect.topleft = (int(self.x), int(self.y))
        self.hitbox_rect = self._build_hitbox()

    # ═══════════════════════════════════════════════════════
    #  MAIN UPDATE & DRAW
    # ═══════════════════════════════════════════════════════

    def update(self):
        """Update platform state (movement, break timers, respawn timers).
        
        Call this every frame from the game loop.
        """
        current_time = pygame.time.get_ticks()

        # Handle break delay
        if self._breaking and self.break_delay > 0:
            if current_time - self._break_timer >= self.break_delay:
                self._do_break()

        # Handle respawn
        if self._broken and self.respawn_time > 0:
            if current_time - self._respawn_timer >= self.respawn_time:
                self._do_respawn()

        # Handle movement
        if self.move_path:
            self._update_movement()

    def draw(self, screen):
        """Draw the platform to the screen.
        
        Args:
            screen: The pygame display surface.
        """
        if not self.visible or self._broken:
            return

        screen.blit(self._surface, self.rect)

        # Debug hitbox visualization
        if self.debug_show_hitbox:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox_rect, 2)
            # Draw landing zone (green) - shows where players can land
            landing_zone = pygame.Rect(
                self.hitbox_rect.left - self.edge_forgiveness,
                self.hitbox_rect.top - 2,
                self.hitbox_rect.width + self.edge_forgiveness * 2,
                4
            )
            pygame.draw.rect(screen, (0, 255, 0), landing_zone, 1)

    def __repr__(self):
        return (f"Platform(x={self.x}, y={self.y}, {self.width}x{self.height}, "
                f"type='{self.platform_type}', mode='{self.image_mode}', "
                f"active={self.active})")


# ═══════════════════════════════════════════════════════════
#  HELPER: Manage all platforms in a level
# ═══════════════════════════════════════════════════════════

def update_platforms():
    """Update all active platforms. Call once per frame from the game loop."""
    import global_vars
    for platform in global_vars.active_platforms:
        platform.update()


def draw_platforms(screen, z_order_filter=None):
    """Draw all active platforms. Call from the game loop's render section.
    
    Args:
        screen: The pygame display surface.
        z_order_filter: If set, only draw platforms with this z_order.
                       Use negative z_order for behind-player, positive for in-front.
    """
    import global_vars
    # Sort by z_order so background platforms draw first
    sorted_platforms = sorted(global_vars.active_platforms, key=lambda p: p.z_order)
    for platform in sorted_platforms:
        if z_order_filter is not None and platform.z_order != z_order_filter:
            continue
        platform.draw(screen)


def clear_platforms():
    """Remove all platforms. Call when changing levels."""
    import global_vars
    global_vars.active_platforms.clear()


def load_platforms_from_list(platform_defs):
    """Create platforms from a list of dictionaries.
    
    Each dict should contain keyword arguments for the Platform constructor.
    
    Args:
        platform_defs: List of dicts, each defining a platform.
        
    Returns:
        List of Platform instances created.
        
    Example:
        platforms = load_platforms_from_list([
            {"x": 300, "y": 450, "width": 200, "height": 20, "platform_type": "solid"},
            {"x": 600, "y": 350, "width": 150, "height": 20, "platform_type": "pass_through"},
            {"x": 100, "y": 300, "width": 100, "height": 20, "platform_type": "breakable", "breakable_hp": 3},
        ])
    """
    import global_vars
    created = []
    for pdef in platform_defs:
        p = Platform(**pdef)
        global_vars.active_platforms.append(p)
        created.append(p)
    return created
