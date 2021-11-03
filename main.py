import arcade
import os
import time

from arcade import Sprite
from arcade.experimental.lights import Light, LightLayer

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "The Dark Platforms"

# Constants used to scale our sprites from their original size
TILE_SCALING = 2
CHARACTER_SCALING = TILE_SCALING * 1
COIN_SCALING = 0.5
POWER_SCALING = TILE_SCALING
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 7
GRAVITY = 1.5
PLAYER_JUMP_SPEED = 20

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 720
RIGHT_VIEWPORT_MARGIN = 720
BOTTOM_VIEWPORT_MARGIN = 100
TOP_VIEWPORT_MARGIN = 150

# 512
PLAYER_START_X = SPRITE_PIXEL_SIZE * TILE_SCALING * 2
# 3072
PLAYER_START_Y = SPRITE_PIXEL_SIZE * TILE_SCALING * 12

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

HEALTHBAR_WIDTH = 25
HEALTHBAR_HEIGHT = 3
HEALTHBAR_OFFSET_Y = -10

HEALTH_NUMBER_OFFSET_X = -10
HEALTH_NUMBER_OFFSET_Y = -25

POWER_SPEED = 5
POWER_1_SPEED = 10

AMBIENT_COLOR = (10, 10, 10)
UPDATES_PER_FRAME = 6

# time
start_time = time.time()
end_time = time.time()
duration = int(end_time - start_time)
time_limit = 5
plight = 1

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]

class InstructionView(arcade.View):
    """ View to show instructions """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()

        self.texture = arcade.load_texture("Assets/gamescreen.PNG")

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
        self.selected = 1

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()

        arcade.draw_text("The Dark Platforms", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click To Play", self.window.width / 2, self.window.height / 2 - 75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("This Game is quite hard (prepare to take on my challenge)", self.window.width / 2, self.window.height / 2 - 355,
                         arcade.color.WHITE, font_size=20, anchor_x="center")


    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = GameView()
        game_view.setup(1)
        self.window.show_view(game_view)


class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        self.texture = arcade.load_texture("Assets/gamescreen.png")

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
        self.selected = 1

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()

        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)

        # takes you to menu
        if self.selected == 1:
            arcade.draw_text("Menu", 485, 285, arcade.csscolor.WHITE, 75)
        else:
            arcade.draw_text("Menu", 500, 300, arcade.csscolor.WHITE, 50)

        # takes you to quit the game
        if self.selected == 2:
            arcade.draw_text("Quit", 505, 215, arcade.csscolor.WHITE, 75)
        else:
            arcade.draw_text("Quit", 520, 230, arcade.csscolor.WHITE, 50)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        # selection keys
        if key == arcade.key.ENTER:
            if self.selected == 1:
                game_view = InstructionView()
                self.window.show_view(game_view)
            elif self.selected == 2:
                arcade.close_window()
        if key == arcade.key.DOWN:
            self.selected += 1
            if self.selected > 2:
                self.selected = 1
        if key == arcade.key.UP:
            self.selected -= 1
            if self.selected < 1:
                self.selected = 2

    # mouse click and motion tracking for selection
    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if 285 <= y <= 285 + 75 and 450 <= x <= 450 + 200:
            self.selected = 1
        elif 230 <= y <= 230 + 75 and 500 <= x <= 500 + 200:
            self.selected = 2

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if 285 <= y <= 285 + 75 and 450 <= x <= 450 + 200:
            game_view = InstructionView()
            self.window.show_view(game_view)
        elif 230 <= y <= 230 + 75 and 500 <= x <= 500 + 200:
            arcade.close_window()

class GameWinView(arcade.View):
    """ View to show when game is won """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        self.texture = arcade.load_texture("Assets/gamescreen.png")

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
        self.selected = 1

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()

        arcade.draw_text("You Beat The Game You must be good!", 485, 300, arcade.csscolor.WHITE, 75)

        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)

        # takes you to menu
        if self.selected == 1:
            arcade.draw_text("Menu", 485, 285, arcade.csscolor.WHITE, 75)
        else:
            arcade.draw_text("Menu", 500, 300, arcade.csscolor.WHITE, 50)

        # takes you to quit the game
        if self.selected == 2:
            arcade.draw_text("Quit", 505, 215, arcade.csscolor.WHITE, 75)
        else:
            arcade.draw_text("Quit", 520, 230, arcade.csscolor.WHITE, 50)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.ENTER:
            if self.selected == 1:
                game_view = InstructionView()
                self.window.show_view(game_view)
            elif self.selected == 2:
                arcade.close_window()
        if key == arcade.key.DOWN:
            self.selected += 1
            if self.selected > 2:
                self.selected = 1
        if key == arcade.key.UP:
            self.selected -= 1
            if self.selected < 1:
                self.selected = 2

    # mouse click and motion tracking for selection
    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        if 285 <= y <= 285 + 75 and 450 <= x <= 450 + 200:
            self.selected = 1
        elif 230 <= y <= 230 + 75 and 500 <= x <= 500 + 200:
            self.selected = 2

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if 285 <= y <= 285 + 75 and 450 <= x <= 450 + 200:
            game_view = InstructionView()
            self.window.show_view(game_view)
        elif 230 <= y <= 230 + 75 and 500 <= x <= 500 + 200:
            arcade.close_window()


class PlayerCharacter(arcade.Sprite):
    """ Player Sprite"""

    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        # Track our state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

        # --- Load Textures ---
        # main_path = ""

        # Load textures for idle standing
        for i in range(1):
            self.idle_texture_pair = load_texture_pair(f"Character/char idle{i}.png")
        self.jump_texture_pair = load_texture_pair("Character/char Jump.png")
        self.fall_texture_pair = load_texture_pair("Character/char Fall.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(4):
            texture = load_texture_pair(f"Character/char Walk{i}.png")
            self.walk_textures.append(texture)

        # Load textures for climbing
        self.climbing_textures = []
        for i in range(1):
            texture = load_texture_pair(f"Character/char climb{i}.png")
            self.climbing_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[1]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
        self.set_hit_box(self.texture.hit_box_points)

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Climbing animation
        if self.is_on_ladder:
            self.climbing = True
        if not self.is_on_ladder and self.climbing:
            self.climbing = False
        if self.climbing and abs(self.change_y) > 1:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
        # if self.climbing:
            # self.texture = self.climbing_textures[self.cur_texture // 4]
            # return

        # Jumping animation
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_texture_pair[self.character_face_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 3 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        self.texture = self.walk_textures[frame][self.character_face_direction]

class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        """
        Initializer for the game
        """
        super().__init__()

        # Call the parent class and set up the window

        # Set the path to start with this program
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.health_texture = arcade.load_texture("Tiles/Health/Heart.png")

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.coin_list = None
        self.obstacle_list = None
        self.wall_list = None
        self.decor_list = None
        self.backgroundb_list = None
        self.ladder_list = None
        self.enemy_list = None
        self.player_list = None
        self.power_list = None
        self.dont_touch_list = None
        self.lava_list = None
        self.breakable_list = None
        self.do_touch_list = None

        # lights
        self.light_layer = None
        self.item_light = None
        self.player_light = None
        self.lava_light = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our 'physics' engine
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        self.end_of_map = 0

        # Keep track of the score
        self.score = 0

        # Load sounds
        self.collect_coin_sound = arcade.load_sound("Assets/coin1.mp3")
        self.activate_sound = arcade.load_sound("Assets/coin1.mp3")
        self.jump_sound = arcade.load_sound("Assets/Jump.wav")
        self.game_over = arcade.load_sound("Assets/gameover1.mp3")
        self.gun_sound = arcade.load_sound("Assets/pew.mp3")

        self.level = 4

    def setup(self, level):
        """ Set up the game here. Call this function to restart the game. """

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 4

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.backgroundb_list = arcade.SpriteList()
        self.decor_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.power_list = arcade.SpriteList()

        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite = PlayerCharacter()

        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_list.append(self.player_sprite)

        self.light_layer = LightLayer(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.light_layer.set_background_color(arcade.color.BLACK)

        radius = 400
        mode = 'soft'
        color = arcade.csscolor.WHITE
        self.player_light = Light(0, 0, radius, color, mode)

        radius = 100
        mode = 'soft'
        color = arcade.csscolor.WHITE
        self.item_light = Light(0, 0, radius, color, mode)

        radius = 150
        mode = 'soft'
        color = arcade.csscolor.ORANGE
        self.lava_light = Light(0, 0, radius, color, mode)

        x = 500
        y = 3072
        radius = 100
        mode = 'soft'
        color = arcade.csscolor.WHITE
        light = Light(x, y, radius, color, mode)
        self.light_layer.add(light)

        # --- Load in a map from the tiled editor ---

        # Name of the layer in the file that has our platforms/walls
        platforms_layer_name = 'Platforms'
        moving_platforms_layer_name = 'Moving Platforms'

        # Name of the layer that has items for pick-up
        coins_layer_name: str = 'coins'

        obstacle_layer_name: str = 'coins'

        # Map name
        map_name = f"Maps/level_{self.level}.tmx"

        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        # Calculate the right edge of the my_map in pixels
        self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE

        # -- Platforms
        self.wall_list = arcade.tilemap.process_layer(my_map,
                                                      platforms_layer_name,
                                                      TILE_SCALING,
                                                      use_spatial_hash=True)

        # -- Moving Platforms
        moving_platforms_list = arcade.tilemap.process_layer(my_map, moving_platforms_layer_name, TILE_SCALING)
        for sprite in moving_platforms_list:
            self.wall_list.append(sprite)

        # -- Background objects
        self.backgroundb_list = arcade.tilemap.process_layer(my_map,
                                                            "Background",
                                                            scaling=TILE_SCALING,
                                                            use_spatial_hash=True)

        # -- Background objects
        self.decor_list = arcade.tilemap.process_layer(my_map,
                                                       "decor",
                                                       scaling=TILE_SCALING,
                                                       use_spatial_hash=True)

        # -- Background objects
        self.ladder_list = arcade.tilemap.process_layer(my_map,
                                                        "Ladders",
                                                        scaling=TILE_SCALING,
                                                        use_spatial_hash=True)

        # -- Coins
        self.coin_list = arcade.tilemap.process_layer(my_map, coins_layer_name,
                                                      TILE_SCALING,
                                                      use_spatial_hash=True)

        self.obstacle_list = arcade.tilemap.process_layer(my_map, obstacle_layer_name,
                                                          TILE_SCALING,
                                                          use_spatial_hash=True)

        # -- Don't Touch Layer
        self.dont_touch_list = arcade.tilemap.process_layer(my_map,
                                                            "dont touch",
                                                            TILE_SCALING,
                                                            use_spatial_hash=True)

        self.do_touch_list = arcade.tilemap.process_layer(my_map,
                                                          "do touch",
                                                          TILE_SCALING,
                                                          use_spatial_hash=True)

        self.lava_list = arcade.tilemap.process_layer(my_map,
                                                      "lava",
                                                      TILE_SCALING,
                                                      use_spatial_hash=True)

        self.breakable_list = arcade.tilemap.process_layer(my_map,
                                                           "breakable",
                                                           TILE_SCALING,
                                                           use_spatial_hash=True)

        # --- Other stuff
        # Set the background color
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             gravity_constant=GRAVITY,
                                                             ladders=self.ladder_list)

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        with self.light_layer:
            self.backgroundb_list
            self.ladder_list.draw()
            self.player_list.draw()
            self.power_list.draw()
            self.coin_list.draw()
            self.enemy_list.draw()
            self.obstacle_list.draw()
            self.do_touch_list.draw()
            self.dont_touch_list.draw()
            self.lava_list.draw()
            self.decor_list.draw()
            self.wall_list.draw()
            self.breakable_list.draw()

        self.light_layer.draw(ambient_color=AMBIENT_COLOR)
        if self.score == 4:
            self.health_texture = arcade.load_texture("Tiles/Health/Heart.png")
        elif self.score == 3:
            self.health_texture = arcade.load_texture("Tiles/Health/Heart1.png")
        elif self.score == 2:
            self.health_texture = arcade.load_texture("Tiles/Health/Heart2.png")
        elif self.score == 1:
            self.health_texture = arcade.load_texture("Tiles/Health/Heart3.png")
        else:
            pass

        if self.level == 1:
            arcade.draw_text("Its To Dark Press A & D to walk and find a Light they also give you more hp", 500, 3072, arcade.csscolor.WHITE, 20)
            arcade.draw_text("Step On The Switch To Open This Door!", 1500, 2500, arcade.csscolor.WHITE, 20)
            arcade.draw_text("Jump Over The Spike or You Lose hp!", 2400, 2000, arcade.csscolor.WHITE, 20)
            arcade.draw_text("Here Is The Way Out!", 2900, 2000, arcade.csscolor.WHITE, 20)
        if self.level == 2:
            arcade.draw_text("To Beat The Game You Must Find A Portal in This Huge Map", 500, 3072, arcade.csscolor.WHITE, 20)
            arcade.draw_text("The Torch is here", 800, 2950, arcade.csscolor.WHITE, 20)


        # Draw our health on the screen, scrolling it with the character
        self.health_texture.draw_sized(100 + self.view_left, 40 + self.view_bottom, 200, 80)

        # Draw hit boxes.
        # for wall in self.wall_list:
        #     wall.draw_hit_box(arcade.color.BLACK, 3)
        #
        # self.player_sprite.draw_hit_box(arcade.color.RED, 3)

    def on_resize(self, width, height):
        """ User resizes the screen. """

        # --- Light related ---
        # We need to resize the light layer to
        self.light_layer.resize(width, height)

    def process_keychange(self):
        """
        Called when we change a key up/down or we move on/off a ladder.
        """
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif self.physics_engine.can_jump(y_distance=10) and not self.jump_needs_reset:
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

        # Process up/down when on a ladder and no movement
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite.change_y = 0

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.SPACE or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.SPACE or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        self.process_keychange()

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Move the player with the physics engine
        self.physics_engine.update()

        # Update animations
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True

        if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
            self.player_sprite.is_on_ladder = True
            self.process_keychange()
        else:
            self.player_sprite.is_on_ladder = False
            self.process_keychange()

        self.coin_list.update_animation(delta_time)
        self.obstacle_list.update_animation(delta_time)
        self.backgroundb_list.update_animation(delta_time)
        self.player_list.update_animation(delta_time)
        self.player_light.position = self.player_sprite.position

        # Update walls, used with moving platforms
        self.wall_list.update()

        # See if the moving wall hit a boundary and needs to reverse direction.
        for wall in self.wall_list:

            if wall.boundary_right and wall.right > wall.boundary_right and wall.change_x > 0:
                wall.change_x *= -1
            if wall.boundary_left and wall.left < wall.boundary_left and wall.change_x < 0:
                wall.change_x *= -1
            if wall.boundary_top and wall.top > wall.boundary_top and wall.change_y > 0:
                wall.change_y *= -1
            if wall.boundary_bottom and wall.bottom < wall.boundary_bottom and wall.change_y < 0:
                wall.change_y *= -1

        # See if we hit any coins
        coin_hit_list: list[Sprite] = arcade.check_for_collision_with_list(self.player_sprite,
                                                                           self.coin_list)
        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:

            # Adding light when touches the light item
            if 'points' not in coin.properties:

                start_time
                print(start_time)
                print("Light added.")
                self.light_layer.add(self.player_light)
                self.score += 1

            # Remove the coin
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)

        # Track if we need to change the viewport
        changed_viewport = False

        # --- Manage Scrolling ---

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed_viewport = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed_viewport = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed_viewport = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed_viewport = True

        if changed_viewport:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

        obstacle_hit_list: list[Sprite] = arcade.check_for_collision_with_list(self.player_sprite,
                                                                               self.obstacle_list)

        # If we hit an obstacle
        for obstacle in obstacle_hit_list:

            # Figure out if obstacle has properties
            if 'Obstacle' not in obstacle.properties:
                print("Its a Coin not an Obstacle or no obstacle found.")
            else:
                # succesfully switched
                switch = int(obstacle.properties['Obstacle'])
                print("Switched:", switch)
                for wall in self.wall_list:
                    # check for wall
                    if "Obstacle" not in wall.properties:
                        pass
                    else:
                        # remove the sprite
                        if int(wall.properties['Obstacle']) == switch:
                            wall.remove_from_sprite_lists()

            obstacle.remove_from_sprite_lists()
            arcade.play_sound(self.activate_sound)

        # Did the player fall off the map?
        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
            arcade.play_sound(self.game_over)

            # Did the player touch something they should not?
        if arcade.check_for_collision_with_list(self.player_sprite,
                                                self.dont_touch_list):

            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
            arcade.play_sound(self.game_over)
            self.score -= 1
            if self.score <= 0:
                view = GameOverView()
                self.window.show_view(view)

        if arcade.check_for_collision_with_list(self.player_sprite,
                                                self.lava_list):
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
            arcade.play_sound(self.game_over)
            self.score -= 1
            if self.score <= 0:
                view = GameOverView()
                self.window.show_view(view)

        # See if the user got to the end of the level
        if arcade.check_for_collision_with_list(self.player_sprite,
                                                self.do_touch_list):

            # if you beat the last level
            if self.level == 4:
                view = GameWinView()
                self.window.show_view(view)

            # Advance to the next level
            if self.level == 1:
                self.level += 1

                # Load the next level
                self.setup(self.level)

            if self.level == 2:
                self.level += 1

                # Load the next level
                self.setup(self.level)

            if self.level == 3:
                self.level += 1

                # Load the next level
                self.setup(self.level)

            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True

        # Update the player based on the physics engine
        if not self.game_over:
            # Move the enemies
            self.enemy_list.update()

            # Check each enemy
            for enemy in self.enemy_list:
                # If the enemy hit a wall, reverse
                if len(arcade.check_for_collision_with_list(enemy, self.wall_list)) > 0:
                    enemy.change_x *= -1
                # If the enemy hit the left boundary, reverse
                elif enemy.boundary_left is not None and enemy.left < enemy.boundary_left:
                    enemy.change_x *= -1
                # If the enemy hit the right boundary, reverse
                elif enemy.boundary_right is not None and enemy.right > enemy.boundary_right:
                    enemy.change_x *= -1

            # Update the player using the physics engine
            self.physics_engine.update()

            # See if the player hit a worm. If so, game over.
            if len(arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)) > 0:
                self.game_over = True

def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
