'''
Tests for my CISC108 final project.

Change log:
  - 0.0.2: Fixed typo with assert_equal
  - 0.0.1: Initial version
'''

__VERSION__ = '0.0.2'
import arcade, math, random
from cisc108 import assert_equal
from cisc108_game import assert_type


################################################################################
# Game import
# Rename this to the name of your project file.
from project_starter import *

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

def make_test_world() -> World:
    return {
    'x': 500,
    'y': 750,
    'x1': 1020,
    'y1': 750,
    'moving?': True,
    'backwards': [False, False, True, False, False, True, False],
    'score': 0,
    'player': AVATAR,
    'enemy': ENEMY,
    'enemy_list': arcade.SpriteList(),
    'coin_list': arcade.SpriteList(),
    'wall_x': WALL_X,
    'wall_y': WALL_Y,
    'engine': None,
    'wall_list': arcade.SpriteList(),
    'state': True,
    'win': None
    }
################################################################################
## Testing <name of function>

# Describe this test here, then run whatever code is necessary to
# perform the tests

#Testing Losing and Winning
lost = {'state': True, 'win': None}
lose(lost)
assert_equal(lost, {'state': False, 'win': False})
won = {'state': True, 'win': True}
win(won)
assert_equal(won, {'state': False, 'win': True})

#Testing Key Releases
Left_Release = handle_release(World, arcade.key.A or arcade.key.LEFT)
assert_equal(Left_Release, 0, 0)
Right_Release = handle_release(World, arcade.key.D or arcade.key.RIGHT)
assert_equal(Right_Release, 0, 0)
Up_Release = handle_release(World, arcade.key.W or arcade.key.UP)
assert_equal(Up_Release, 0, 0)
Down_Release = handle_release(World, arcade.key.S or arcade.key.DOWN)
assert_equal(Down_Release, 0, 0)

#Testing Key Presses
Left_Press = handle_key(World, arcade.key.A or arcade.key.LEFT)
assert_equal(Left_Press, 0, 0)
Right_Press = handle_key(World, arcade.key.D or arcade.key.RIGHT)
assert_equal(Right_Press, 0, 0)
Up_Press = handle_key(World, arcade.key.W or arcade.key.UP)
assert_equal(Up_Press, 3, 3)
Down_Press = handle_key(World, arcade.key.S or arcade.key.DOWN)
assert_equal(Down_Press, -3, -3)


