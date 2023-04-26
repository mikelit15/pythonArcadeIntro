'''
In this game, you are playing as a blue hen avatar. Your goal is to go throughout the maze
and collect five coins that are generated in specific spots. Once you have collected all
five coins, you have won the game and will be greeted with a game over screen. But watch,
out there are Villanova wildcats roaming the parts of the maze, and if one of them catches
you, you lose the game and will be greeted with a game over screen.

Change log:
  - 0.0.2: Added support for handle_release
  - 0.0.1: Initial version
'''
__VERSION__ = '0.0.2'

import arcade, math, random
from cisc108_game import Cisc108Game

################################################################################
## Game Constants

WINDOW_WIDTH = 1020
WINDOW_HEIGHT = 750
BACKGROUND_COLOR = arcade.color.BLACK
GAME_TITLE = "Top-Down Adventure"

AVATAR = arcade.Sprite("hen.png")
left_hen = arcade.load_texture("hen.png", mirrored=True)
right_hen = arcade.load_texture("hen.png", mirrored=False)
ENEMY = arcade.Sprite("nova.png")
COIN = arcade.Sprite("coin.png")
LOSE = arcade.load_texture("hen.png")
WALL_X = arcade.Sprite("wall_x.png")
WALL_Y = arcade.Sprite("wall_y.png")

PLAYER_SPEED = 4
ENEMY_SPEED = 2

################################################################################
## Record definitions

World = {
    'x': int,
    'y': int,
    'x1': int,
    'y1': int,
    'moving?': bool,
    'backwards?': bool,
    'score': int,
    'player': arcade.Sprite,
    'enemy': arcade.Sprite,
    'coin_list': arcade.SpriteList,
    'wall_x': arcade.Sprite,
    'wall_y': arcade.Sprite,
    'engine': arcade.PhysicsEngineSimple,
    'wall_list': arcade.SpriteList,
    'state': bool,
    'win': bool
    # Remember to explain each field!
}

INITIAL_WORLD = {
    'x': 500,
    'y': 750,
    'x1': 1020,
    'y1': 750,
    'moving?': True,
    'backwards?': False,
    'score': 0,
    'player': AVATAR,
    'enemy': ENEMY,
    'coin_list': arcade.SpriteList(),
    'wall_x': WALL_X,
    'wall_y': WALL_Y,
    'engine': None,
    'wall_list': arcade.SpriteList(),
    'state': True,
    'win': None
    # And update your INITIAL_WORLD accordingly!
}
INITIAL_WORLD['engine'] = arcade.PhysicsEngineSimple(INITIAL_WORLD['player'], INITIAL_WORLD['wall_list'])
INITIAL_WORLD['player'].center_x = 35
INITIAL_WORLD['player'].center_y = 45
INITIAL_WORLD['enemy'].center_x = 75
INITIAL_WORLD['enemy'].center_y = 270

################################################################################
# Drawing functions

def draw_level(world: World):
    """
    Each time the world is drawn, a player avatar, an enemy, a list of coins, and a list
    of walls is created.
    
    Args:
        world (World): The current world to draw
    """

    AVATAR.draw()
    ENEMY.draw()
    world['coin_list'].draw()
    world['wall_list'].draw()

def draw_world(world: World):
    """
    When the game is started, the state is checked in order to draw the level. If the game
    state is false after the player wins or loses, the game checks if the player has lost or
    won and provides the respective game over screen. *If the player loses, a reset button is
    offered to allow another attempt.

    Args:
        world (World): The current world to draw
    """
    if world['state'] == True:
        draw_level(INITIAL_WORLD)
    if world['state'] == False:
        if world['win'] == True:
            draw_game_win(INITIAL_WORLD)
        elif world['win'] == False:
            draw_game_lose(INITIAL_WORLD)


def draw_game_lose(world: World):
    """
    This function draws the game over screen which is called once the player loses
    by hitting an enemy.

    Args:
        world (World): The current world to draw
    """
    score_text = f"Game Over \n\n   Score: {world['score']}"
    arcade.draw_text(score_text, 295, 325, arcade.color.WHITE, 70)

def draw_game_win(world: World):
    """
    This function draws the game over screen which is called once the player wins
    by collecting all five of the coins.

    Args:
        world (World): The current world to draw
    """
    score_text = f"Congratulations \n\n       Score: {world['score']}"
    arcade.draw_text(score_text, 225, 325, arcade.color.WHITE, 70)

################################################################################
# World manipulating functions

def update_world(world: World):
    """
    During every update, the game checks if the player has collided with an enemy or a
    coin. The enemy movement is also updated in order for it to continue moving on its own
    within the bounds.
    
    Args:
        world (World): The current world to update.
    """
    world['engine'].update()

    if 380 <= (world['enemy'].center_x + world['enemy'].width / 2):
        world['backwards?'] = True

    elif (world['enemy'].center_x - world['enemy'].width / 2) <= 70:
        world['backwards?'] = False

    if world['moving?'] and not world['backwards?']:
        world['enemy'].center_x = world['enemy'].center_x + ENEMY_SPEED

    else:
        world['enemy'].center_x = world['enemy'].center_x - ENEMY_SPEED

    hit_enemy = arcade.check_for_collision(AVATAR, ENEMY)

    hit_coin = arcade.check_for_collision_with_list(AVATAR, world['coin_list'])

    if hit_enemy:
        world['state'] = False
        world['win'] = False

    for coin in hit_coin:
        world['score'] += 1
        coin.remove_from_sprite_lists()
        if world['score'] == 5:
            world['state'] = False
            world['win'] = True

def handle_key(world: World, key: int):
    """
    Once the key on the keyboard is pressed, the player image begins to move in
    the given direction. This is done by changing the x coordinate value by the
    given movement speed.
    
    Args:
        world (World): Current state of the world.
        key (int): The ASCII value of the pressed keyboard key (use ord and chr).
    """
    if key == arcade.key.A or key == arcade.key.LEFT:
        world['player'].texture = left_hen
        world['player'].change_x = -PLAYER_SPEED
    elif key == arcade.key.D or key == arcade.key.RIGHT:
        world['player'].texture = right_hen
        world['player'].change_x = PLAYER_SPEED
    elif key == arcade.key.W or key == arcade.key.UP:
        world['player'].change_y = PLAYER_SPEED
    elif key == arcade.key.S or key == arcade.key.DOWN:
        world['player'].change_y = -PLAYER_SPEED


def handle_mouse(world: World, x: int, y: int, button: str):
    """
    <Describe how your game responds to mouse clicks.>
    
    Args:
        world (World): Current state of the world.
        x (int): The x-coordinate of the mouse when the button was clicked.
        y (int): The y-coordinate of the mouse when the button was clicked.
        button (str): The button that was clicked ('left', 'right', 'middle')
    """

def handle_motion(world: World, x: int, y: int):
    """
    <Describe how your game responds to the mouse being moved.>
    
    Args:
        world (World): Current state of the world.
        x (int): The x-coordinate of where the mouse was moved to.
        y (int): The x-coordinate of where the mouse was moved to.
    """

def handle_release(world: World, key: int):
    """
    Once the key on the keyboard is released, the movement speed in the given
    direction is set to 0.

    Args:
        world (World): Current state of the world.
        key (int): The ASCII value of the released keyboard key (use ord and chr).
    """
    if key == arcade.key.A or key == arcade.key.LEFT:
        world['player'].change_x = 0
    elif key == arcade.key.D or key == arcade.key.RIGHT:
        world['player'].change_x = 0
    elif key == arcade.key.W or key == arcade.key.UP:
        world['player'].change_y = 0
    elif key == arcade.key.S or key == arcade.key.DOWN:
        world['player'].change_y = 0

def coin_gen(x: int, y: int):
    """
        This function creates a new coin image that is passed in and is returned on the
        coordinate plane based off of the x and y input values.

        Args:
            x (int): The x coordinate value.
            y (int): The y coordinate value.
    """
    coin = arcade.Sprite("coin.png")
    coin.center_x = x
    coin.center_y = y
    return coin

def coins(world: World):
    """
        This function creates appends coins into the coin list that can be placed anywhere
        on the map.

        Args:
         world (World): Current state of the world.
    """
    world['coin_list'].append(coin_gen(95, 195))
    world['coin_list'].append(coin_gen(585, 120))
    world['coin_list'].append(coin_gen(665, 120))
    world['coin_list'].append(coin_gen(265, 640))
    world['coin_list'].append(coin_gen(500, 715))



def wall_y(x: int, y: int):
    """
        This function creates a new vertical wall image that is passed in and is returned on the
        coordinate plane based off of the x and y input values.

        Args:
            x (int): The x coordinate value.
            y (int): The y coordinate value.
    """
    wall = arcade.Sprite("wall_y.png")
    wall.center_x = x
    wall.center_y = y
    return wall

def wall_x(x: int, y: int):
    """
        This function creates a new horizontal wall image that is passed in and is returned on the
        coordinate plane based off of the x and y input values.

        Args:
            x (int): The x coordinate value.
            y (int): The y coordinate value.
    """
    wall = arcade.Sprite("wall_x.png")
    wall.center_x = x
    wall.center_y = y
    return wall

def walls(world: World):
    """
        This function creates appends walls into the wall list that can be placed anywhere
        on the map.

        Args:
         world (World): The current state of the world.
    """
    #Left Perimeter
    world['wall_list'].append(wall_y(0, 0))
    world['wall_list'].append(wall_y(0, 75))
    world['wall_list'].append(wall_y(0, 150))
    world['wall_list'].append(wall_y(0, 225))
    world['wall_list'].append(wall_y(0, 300))
    world['wall_list'].append(wall_y(0, 375))
    world['wall_list'].append(wall_y(0, 450))
    world['wall_list'].append(wall_y(0, 525))
    world['wall_list'].append(wall_y(0, 600))
    world['wall_list'].append(wall_y(0, 675))
    world['wall_list'].append(wall_y(0, 750))

    # Right Perimeter
    world['wall_list'].append(wall_y(1020, 0))
    world['wall_list'].append(wall_y(1020, 75))
    world['wall_list'].append(wall_y(1020, 150))
    world['wall_list'].append(wall_y(1020, 225))
    world['wall_list'].append(wall_y(1020, 300))
    world['wall_list'].append(wall_y(1020, 375))
    world['wall_list'].append(wall_y(1020, 450))
    world['wall_list'].append(wall_y(1020, 525))
    world['wall_list'].append(wall_y(1020, 600))
    world['wall_list'].append(wall_y(1020, 675))
    world['wall_list'].append(wall_y(1020, 750))

    #Maze Vertical Walls
    world['wall_list'].append(wall_y(225, 195))
    world['wall_list'].append(wall_y(145, 120))
    world['wall_list'].append(wall_y(65, 195))
    world['wall_list'].append(wall_y(305, 120))
    world['wall_list'].append(wall_y(305, 195))
    world['wall_list'].append(wall_y(65, 270))
    world['wall_list'].append(wall_y(545, 125))
    world['wall_list'].append(wall_y(625, 125))
    world['wall_list'].append(wall_y(65, 340))
    world['wall_list'].append(wall_y(545, 195))
    world['wall_list'].append(wall_y(785, 195))
    world['wall_list'].append(wall_y(385, 195))
    world['wall_list'].append(wall_y(385, 270))
    world['wall_list'].append(wall_y(865, 125))
    world['wall_list'].append(wall_y(865, 195))
    world['wall_list'].append(wall_y(468, 270))
    world['wall_list'].append(wall_y(468, 340))
    world['wall_list'].append(wall_y(543, 340))
    world['wall_list'].append(wall_y(623, 345))
    world['wall_list'].append(wall_y(785, 270))
    world['wall_list'].append(wall_y(945, 270))
    world['wall_list'].append(wall_y(65, 490))
    world['wall_list'].append(wall_y(145, 415))
    world['wall_list'].append(wall_y(225, 415))
    world['wall_list'].append(wall_y(225, 340))
    world['wall_list'].append(wall_y(307, 342))
    world['wall_list'].append(wall_y(623, 415))
    world['wall_list'].append(wall_y(785, 343))
    world['wall_list'].append(wall_y(865, 415))
    world['wall_list'].append(wall_y(945, 490))
    world['wall_list'].append(wall_y(785, 490))
    world['wall_list'].append(wall_y(708, 490))
    world['wall_list'].append(wall_y(543, 492))
    world['wall_list'].append(wall_y(387, 490))
    world['wall_list'].append(wall_y(65, 640))
    world['wall_list'].append(wall_y(145, 640))
    world['wall_list'].append(wall_y(145, 565))
    world['wall_list'].append(wall_y(145, 565))
    world['wall_list'].append(wall_y(225, 640))
    world['wall_list'].append(wall_y(387, 640))
    world['wall_list'].append(wall_y(465, 568))
    world['wall_list'].append(wall_y(465, 713))
    world['wall_list'].append(wall_y(543, 640))
    world['wall_list'].append(wall_y(623, 568))
    world['wall_list'].append(wall_y(785, 640))
    world['wall_list'].append(wall_y(945, 568))
    world['wall_list'].append(wall_y(865, 640))

    #Top Perimeter
    world['wall_list'].append(wall_x(0, 750))
    world['wall_list'].append(wall_x(80, 750))
    world['wall_list'].append(wall_x(160, 750))
    world['wall_list'].append(wall_x(240, 750))
    world['wall_list'].append(wall_x(320, 750))
    world['wall_list'].append(wall_x(400, 750))
    world['wall_list'].append(wall_x(480, 750))
    world['wall_list'].append(wall_x(560, 750))
    world['wall_list'].append(wall_x(640, 750))
    world['wall_list'].append(wall_x(720, 750))
    world['wall_list'].append(wall_x(800, 750))
    world['wall_list'].append(wall_x(880, 750))
    world['wall_list'].append(wall_x(960, 750))
    world['wall_list'].append(wall_x(1040, 750))

    #Bottom Perimeter
    world['wall_list'].append(wall_x(0, 0))
    world['wall_list'].append(wall_x(80, 0))
    world['wall_list'].append(wall_x(160, 0))
    world['wall_list'].append(wall_x(240, 0))
    world['wall_list'].append(wall_x(320, 0))
    world['wall_list'].append(wall_x(400, 0))
    world['wall_list'].append(wall_x(480, 0))
    world['wall_list'].append(wall_x(560, 0))
    world['wall_list'].append(wall_x(640, 0))
    world['wall_list'].append(wall_x(720, 0))
    world['wall_list'].append(wall_x(800, 0))
    world['wall_list'].append(wall_x(880, 0))
    world['wall_list'].append(wall_x(960, 0))
    world['wall_list'].append(wall_x(1040, 0))

    #Maze Horizontal Walls
    world['wall_list'].append(wall_x(185, 160))
    world['wall_list'].append(wall_x(105, 230))
    world['wall_list'].append(wall_x(105, 160))
    world['wall_list'].append(wall_x(265, 85))
    world['wall_list'].append(wall_x(105, 305))
    world['wall_list'].append(wall_x(185, 305))
    world['wall_list'].append(wall_x(185, 85))
    world['wall_list'].append(wall_x(105, 85))
    world['wall_list'].append(wall_x(35, 85))
    world['wall_list'].append(wall_x(345, 160))
    world['wall_list'].append(wall_x(425, 85))
    world['wall_list'].append(wall_x(505, 85))
    world['wall_list'].append(wall_x(585, 85))
    world['wall_list'].append(wall_x(665, 85))
    world['wall_list'].append(wall_x(745, 85))
    world['wall_list'].append(wall_x(825, 85))
    world['wall_list'].append(wall_x(905, 85))
    world['wall_list'].append(wall_x(975, 85))
    world['wall_list'].append(wall_x(425, 160))
    world['wall_list'].append(wall_x(665, 160))
    world['wall_list'].append(wall_x(745, 160))
    world['wall_list'].append(wall_x(585, 230))
    world['wall_list'].append(wall_x(665, 230))
    world['wall_list'].append(wall_x(345, 305))
    world['wall_list'].append(wall_x(505, 230))
    world['wall_list'].append(wall_x(905, 160))
    world['wall_list'].append(wall_x(505, 380))
    world['wall_list'].append(wall_x(585, 305))
    world['wall_list'].append(wall_x(745, 305))
    world['wall_list'].append(wall_x(825, 305))
    world['wall_list'].append(wall_x(905, 305))
    world['wall_list'].append(wall_x(185, 380))
    world['wall_list'].append(wall_x(27, 530))
    world['wall_list'].append(wall_x(345, 380))
    world['wall_list'].append(wall_x(585, 450))
    world['wall_list'].append(wall_x(505, 450))
    world['wall_list'].append(wall_x(425, 450))
    world['wall_list'].append(wall_x(265, 450))
    world['wall_list'].append(wall_x(665, 380))
    world['wall_list'].append(wall_x(825, 380))
    world['wall_list'].append(wall_x(985, 380))
    world['wall_list'].append(wall_x(905, 450))
    world['wall_list'].append(wall_x(905, 528))
    world['wall_list'].append(wall_x(825, 528))
    world['wall_list'].append(wall_x(747, 450))
    world['wall_list'].append(wall_x(585, 528))
    world['wall_list'].append(wall_x(185, 528))
    world['wall_list'].append(wall_x(265, 528))
    world['wall_list'].append(wall_x(345, 528))
    world['wall_list'].append(wall_x(425, 528))
    world['wall_list'].append(wall_x(105, 678))
    world['wall_list'].append(wall_x(265, 675))
    world['wall_list'].append(wall_x(265, 605))
    world['wall_list'].append(wall_x(425, 605))
    world['wall_list'].append(wall_x(345, 675))
    world['wall_list'].append(wall_x(505, 675))
    world['wall_list'].append(wall_x(665, 675))
    world['wall_list'].append(wall_x(585, 675))
    world['wall_list'].append(wall_x(665, 605))
    world['wall_list'].append(wall_x(745, 675))
    world['wall_list'].append(wall_x(905, 675))
    world['wall_list'].append(wall_x(985, 675))

############################################################################
# Set up the game
# Don't need to change any of this

if __name__ == '__main__':
    walls(INITIAL_WORLD)
    coins(INITIAL_WORLD)
    Cisc108Game(World, WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE, INITIAL_WORLD,
                draw_world, update_world, handle_key, handle_mouse,
                handle_motion, handle_release)
    arcade.set_background_color(BACKGROUND_COLOR)
    arcade.run()
