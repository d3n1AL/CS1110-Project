# Daniel Xue
# dlx3ud
# Programming Project Checkpoint 2

"""
Baseline Project idea: Bullet-Hell Style Space Shooter
(a la Galaga, the Touhou Project, and/or Space Invaders at a minimum)
Implementation of required features detailed in code below:
Priority of planned optional features:
Bullets - done
Enemies - basic is done, mover is done
Health Bar - basic is done, code to reset game is done
Collectibles - basic is done, i-frame indicator is also done
Scrolling Level - done
Score Board - done
More levels, hi-score boards, etc. - done
"""

import pygame
import gamebox
import math
import random

# ------- CAMERA -------
camera = gamebox.Camera(400, 600)
# creates camera to view the game, sets dimensions at 400 by 600

# ------- QUALITY OF LIFE FUNCTIONS -------


def out_of_bounds(sprite):
    """
    Indicates whether part of the sprite is outside of the camera range
    :param sprite: a gamebox with the attributes top, bottom, left, and right
    :return: a boolean indicating if part of said sprite is outside the camera
    """
    off_top = sprite.top < camera.top
    # checks whether the sprite is off the top edge
    off_bottom = sprite.bottom > camera.bottom
    # checks whether the sprite is off the bottom edge
    off_right = sprite.right > camera.right
    # checks whether the sprite is off the right edge
    off_left = sprite.left < camera.left
    # checks whether the sprite is off the left edge
    return off_top or off_bottom or off_right or off_left  # returns True if off any edge


def in_camera_range(sprite):
    """
    Indicates whether any part of the sprite is inside of the camera range
    Note: this is NOT the same as not out_of_bounds(sprite) !!
    :param sprite: a gamebox with the attributes top, bottom, left, and right
    :return: a boolean indicating whether all parts of said sprite are inside the camera
    """
    in_top = sprite.bottom >= camera.top
    # checks whether any part of the sprite is below the top edge
    in_bottom = sprite.top <= camera.bottom
    # checks whether any part of the sprite is above the bottom edge
    in_right = sprite.left <= camera.right
    # checks whether any part of the sprite is left of the right edge
    in_left = sprite.right >= camera.left
    # checks whether any part of the sprite is right of the left edge
    return in_top or in_bottom or in_right or in_left


# ------- GRAPHICS/ANIMATIONS -------
# Player Sprites
player = None
# initializes a variable to store a player gamebox
# note: there can only be one!


def make_player(color, size, hp):
    """
    Creates a square player character at the middle of the bottom of the screen
    :param color: a string indicating color
    :param size: an int giving its side length
    :param hp: int giving player's initial hp
    :return: nothing
    """
    global player
    player = gamebox.from_color(camera.x, camera.bottom - size / 2, color, size, size)
    # creates a gamebox at the center of the bottom of the screen with given color and size
    player.hp = hp
    # initializes hp as hp
    player.bullet_timer = 0  # initializes a value for a timer to space bullets apart
    player.hurt_timer = 0  # initializes a value for a timer for invincibility frames
    player.power_up_timer = 0  # initializes a value for a timer for certain power-ups
    player.score = 0    # initializes a value to store player's score
    player.score_multiplier = 1     # initializes a value for a score multiplier that increases for each enemy killed
    # and resets when hit by an enemy
    player.score_saved = False  # initializes a boolean to record whether the player's score has been saved


# Enemy Sprites
# green boxes moving in from the top that can move
# will be destroyed if the player causes enough damage
enemies = {
    "basic": [],
    "mover": []
}
# initializes an empty dict to store list of gameboxes for each kind of enemy


def hp_to_color(hp):
    """
    Returns the enemy's color in a string given its hp as an integer
    :param hp: int hp of said enemy
    :return: a string containing the enemy's color
    """
    if hp <= 1:
        return "dark green"
        # returns dark green when enemy has 1 hp
    if hp <= 5:
        return "yellow"
        # returns yellow when enemy has hp of 2-5
    if hp <= 10:
        return "orange"
        # returns orange when enemy has hp of 6-10
    if hp <= 20:
        return "pink"
        # returns pink when enemy has hp of 11-20
    return "cyan"
    # returns cyan when enemy has hp of greater than 20 (which, for the record, it should not unless it is a boss


def make_enemy(kind, x, y, width, height, hp):
    """
    Spawns an enemy of a given kind at a given location with a given color, width, and height
    :param hp: int starting hit points of the enemy
    :param kind: a string indicating that enemy's kind (a key in the dictionary of lists)
    :param x: x coordinate of the enemy's initial location
    :param y: y coordinate of the enemy's initial location
    :param width: int pixel width of said enemy
    :param height: int pixel height of said enemy
    :return: nothing
    """
    enemy = gamebox.from_color(x, y, hp_to_color(hp), width, height)
    # creates a gamebox with the given parameters
    enemy.hp = hp
    # sets enemy hp to the hp given
    enemy.score = hp * 10
    # sets enemy score to ten times the enemy's initial hp as a default
    enemies[kind].append(enemy)
    # appends said value a list in the dictionary of projectiles


def make_basic_enemy(x, y, hp=1):
    """
    Spawns a basic enemy that neither moves nor shoots at the given location
    :param hp: int starting hit points of the enemy
    :param x: x coordinate of the enemy's initial location
    :param y: y coordinate of the enemy's initial location
    :return: nothing
    """
    make_enemy("basic", x, y, 30, 30, hp)
    # basic enemies have a default hp of 1
    # and give a score of 10 upon dying


# different types possible (e.g. more health, different moving patterns, bosses possible)


def make_mover_enemy(x, y, hp=1, x_amplitude=60, y_amplitude=60, x_period=120, y_period=120, x_phase=0, y_phase=30):
    """
    Spawns an enemy that moves with the given parameters sinusoidally
    :param hp: int initial hp of the enemy
    :param x: int x-coordinate of initial location
    :param y: int y-coordinate of initial location
    :param x_amplitude: int range of x motion
    :param y_amplitude: int range of y motion
    :param x_period: int period of x motion
    :param y_period: int period of y motion
    :param x_phase: int phase of x motion
    :param y_phase: int phase of y motion
    :return: nothing
    """
    make_enemy("mover", x, y, 30, 30, hp)
    enemies["mover"][-1].x_move_timer = 0  # initializes a value for timer to dictate x behavior
    enemies["mover"][-1].y_move_timer = 0   # initializes a similar value for a timer to dictate y behavior
    enemies["mover"][-1].x_amplitude = x_amplitude   # initializes a value for amplitude of motion
    enemies["mover"][-1].x_period = x_period    # initializes value for frequency of motion
    enemies["mover"][-1].x_phase = x_phase      # initializes a value for phase of motion
    enemies["mover"][-1].y_amplitude = y_amplitude  # initializes a value for amplitude of motion
    enemies["mover"][-1].y_period = y_period  # initializes value for frequency of motion
    enemies["mover"][-1].y_phase = y_phase  # initializes a value for phase of motion
    enemies["mover"][-1].x_init = x     # initializes an attribute for initial x position
    enemies["mover"][-1].y_init = y     # initializes an attribute for initial y position
    # note that the defaults make the mover go in small circles


def make_slider_enemy(x, y, hp=1, amplitude=60, period=120, phase=0):
    """Makes a mover enemy that only moves horizontally"""
    make_mover_enemy(x, y, hp, amplitude, 0, period, 120, phase, 0)
    # note 120 is used for y period to avoid division by 0


def make_climber_enemy(x, y, hp=1, amplitude=60, period=120, phase=0):
    """Makes a mover enemy that only moves vertically"""
    make_mover_enemy(x, y, hp, 0, amplitude, 120, period, 0, phase)


# Bullets and other Projectiles
# white rectangles that shoot in lines and do damage
projectiles = {
    "player bullet": []
}
# initializes an empty dictionary to store list of gameboxes for each kind of projectile


def make_projectile(kind, x, y, color, size, speedx=0, speedy=0, pierce=1):
    """
    Spawns a projectile of a given type at a given location with a given color, size, and speed
    :param kind: a string indicating that projectile's kind (a key in the dictionary of lists)
    :param x: int of x coordinate of projectile's initial location
    :param y: int of y coordinate of projectile's initial location
    :param color: string indicating that projectile's color
    :param size: int indicating the side length of the projectile
    :param speedx: int x speed of the bullet (default of 0)
    :param speedy: int y speed of the bullet (default of 0)
    :return: nothing
    """
    projectile = gamebox.from_color(x, y, color, size, size)
    # creates a gamebox with the given parameters
    projectile.speedx = speedx
    projectile.speedy = speedy
    projectile.pierce = pierce
    # creates attributes to store projectile speed and pierce
    projectiles[kind].append(projectile)
    # appends said value a list in the dictionary of projectiles


def make_player_bullet():
    """
    Spawns a player bullet at the player's location that goes up
    :return: nothing
    """
    global has_power_up

    bullet_pierce = 1
    if has_power_up["strength"] or has_power_up["super"]:
        bullet_pierce = 2
    # player bullet pierce is 1 by default, 2 when stronk or super

    bullet_color = "white"
    if has_power_up["strength"]:
        bullet_color = "red"
    elif has_power_up["rapid fire"]:
        bullet_color = "green"
    elif has_power_up["speed"]:
        bullet_color = "blue"
    elif has_power_up["super"]:
        bullet_color = "purple"
    # player bullet color changes depending on what power_up is dropped

    bullet_speedy = -1 * bullet_speed
    if has_power_up["speed"] or has_power_up["super"]:
        bullet_speedy *= 2
    # player bullet speed goes up by the given bullet speed, doubled when speed or super

    make_projectile("player bullet", player.x, player.y, bullet_color, 5, speedy=bullet_speedy, pierce=bullet_pierce)


# may also make different types if I have time
# e.g. rockets that do AoE damage, homing missiles, laser beams, etc.

# Collectibles
# power-ups to health, speed, power, dropped by enemies when killed; may also increase score
# initializes an empty dict of lists to store power-up gameboxes
power_ups = {
    "health": [],
    "strength": [],
    "rapid fire": [],
    "speed": [],
    "super": []
}


def make_power_up(kind, x, y, color, size=10):
    """
    Spawns a power-up of a given kind at a given location with a given color and size
    :param size: int indicating the side length of the power-up
    :param kind: a string indicating the power-up's kind (a key in the dictionary of lists
    :param x: int x-coordinate of the power-up's initial location
    :param y: int y-coordinate of the power-up's initial location
    :param color: string indicating the power-up's color
    :return: nothing
    """
    power_up = gamebox.from_color(x, y, color, size, size)
    # creates a gamebox with the given parameters
    power_up.kind = kind
    # creates a new attribute to store the power-up's kind
    power_ups[kind].append(power_up)


def make_health_power_up(x, y):
    """
    Spawns a gray power-up at the given location to refill the player's health
    :param x: int x-coordinate of the power-up's initial location
    :param y: int y-coordinate of the power-up's initial location
    :return: nothing
    """
    make_power_up("health", x, y, "gray")


def make_strength_power_up(x, y):
    """
    Spawns a red power-up at the given location to increase the pierce of the player's bullets
    :param x: int x-coordinate of the power-up's initial location
    :param y: int y-coordinate of the power-up's initial location
    :return: nothing
    """
    make_power_up("strength", x, y, "red")


def make_rapid_fire_power_up(x, y):
    """
    Spawns a green power-up at the given location to increase the fire rate of the player's bullets
    :param x: int x-coordinate of the power-up's initial location
    :param y: int y-coordinate of the power-up's initial location
    :return: nothing
    """
    make_power_up("rapid fire", x, y, "green")


def make_speed_power_up(x, y):
    """
    Spawns a blue power-up at the given location to increase the speed of the player ship
    :param x: int x-coordinate of the power-up's initial location
    :param y: int y-coordinate of the power-up's initial location
    :return: nothing
    """
    make_power_up("speed", x, y, "blue")


def make_super_power_up(x, y):
    """
    Spawns a purple power-up at the given location to give the effects of strength, rapid fire, and speed
    :param x: int x-coordinate of the power-up's initial location
    :param y: int y-coordinate of the power-up's initial location
    :return: nothing
    """
    make_power_up("super", x, y, "purple")


def make_random_power_up(x, y):
    """
    Spawns a random power-up at the given location based on distribution detailed below
    :param x: int x-coordinate of the power-up's initial location
    :param y: int y-coordinate of the power-up's initial location
    :return: nothing
    """
    power_up_roll = random.randrange(0, 200)
    # rolls a number between 0-199 to determine what power-up is generated
    if power_up_roll < 1:
        make_super_power_up(x, y)
        # if a zero is rolled, make the super power-up
    elif power_up_roll < 6:
        make_strength_power_up(x, y)
        # if a number 1-5 is rolled, make the strength power-up
    elif power_up_roll < 11:
        make_rapid_fire_power_up(x, y)
        # if a number 6-10 is rolled, make the rapid fire power-up
    elif power_up_roll < 16:
        make_speed_power_up(x, y)
        # if a number 11-15 is rolled, make the speed power-up
    elif power_up_roll < 21:
        make_health_power_up(x, y)
        # if a number 16-20 is rolled, make the health power-up
    # if number is greater than 20, don't make anything


def add_power_up(kind):
    """
    Gives the appropriate power-up to the player character based on the kind specified
    :param kind: string indicating what power-up is being added
    :return: nothing
    """
    global has_power_up
    global player_fire_rate
    global player_move_speed

    if kind == "health":
        player.hp = init_player_hp
        # restores the player's hp to full when health is picked up

    else:
        if player.power_up_timer == 0:
            # if their power-up timer is at zero

            if kind == "strength":
                player.color = "red"
                # changes player color to red

            elif kind == "rapid fire":
                player.color = "green"
                player_fire_rate = 2
                # changes player color to green and halves frames between bullets

            elif kind == "speed":
                player.color = "blue"
                player_move_speed *= 2
                # changes player color to blue and doubles move speed

            elif kind == "super":
                player.color = "purple"
                player_fire_rate = 2
                player_move_speed *= 2
                # changes player color to purple, halves frames between bullets and doubles move speed

            has_power_up[kind] = True
            # adds relevant bullet effects by switching on a power_up in the dictionary

            player.power_up_timer += 1
            # increase the timer by 1

        elif player.power_up_timer % player_power_up_frames:
            # if their power_up timer is not a multiple of the pu frames
            player.power_up_timer += 1
            # increase the timer by 1

        elif player.power_up_timer == player_power_up_frames:
            # if their power_up_timer has reached its limit
            player.color = player_color

            if kind == "rapid fire" or kind == "super":
                player_fire_rate = 5
                # resets player fire rate back to 5

            if kind == "speed" or kind == "super":
                player_move_speed //= 2
                # resets player move speed by halving it

            has_power_up[kind] = False
            # turns off relevant bullet effects by switching off a power_up in the dictionary

            player.power_up_timer = 0
            # resets the player power up timer


power_up_indicators = []
# initializes an empty list to store indicators for power-ups and/or other properties


def show_invincible(sprite):
    """
    Adds the letter "i" in black over the sprite to indicate invincibility frames
    :param sprite: some gamebox
    :return: nothing
    """
    invincible = gamebox.from_text(sprite.x, sprite.y, "i", 36, "black", bold=True)
    power_up_indicators.append(invincible)


# HUD Elements (Timer, Health Bar, etc.)
HUD = []
# initializes an empty list to store HUD elements


def make_health_bar():
    """
    Creates a health bar in the bottom left that displays player health
    :return: nothing
    """
    outline = gamebox.from_color(0, 0, "white", 20, 150)
    # creates a white rectangle
    outline.center = (camera.left + outline.width / 2, camera.bottom - outline.height / 2)
    # centers outline in the bottom left
    total_hp = gamebox.from_color(0, 0, "black", 16, 146)
    # creates smaller black rectangle
    total_hp.center = outline.center
    # centers total health in the same place as outline
    try:
        hp_remaining = gamebox.from_color(0, 0, "red", total_hp.width, player.hp / init_player_hp * total_hp.height)
        # creates red rectangle with length corresponding to player health
    except:
        hp_remaining = gamebox.from_color(0, 0, "red", total_hp.width, total_hp.height)
        # creates red rectangle with the same length of total hp if no player is created
    hp_remaining.bottomleft = total_hp.bottomleft
    # matches the bottomleft corner of health remaining with the total health
    HUD.append(outline)
    HUD.append(total_hp)
    HUD.append(hp_remaining)
    # adds all elements to HUD


def make_scoreboard():
    """
    Creates a scoreboard in the upper left that displays the player score
    :return: nothing
    """
    try:
        scoreboard = gamebox.from_text(0, 0, "Score: " + str(int(player.score)), 30, "white")
        # creates a text box displaying the player's score
        multiplier = gamebox.from_text(0, 0, "Multiplier: " + str(int(100 * player.score_multiplier) / 100) + "x", 30, "white")
        # creates a text box displaying the player's score multiplier to the nearest hundredth
    except:
        scoreboard = gamebox.from_text(0, 0, "Score: 0", 30, "white")
        # creates a text box displaying a score of 0
        multiplier = gamebox.from_text(0, 0, "Multiplier: 1.0x", 30, "white")
        # creates a text box displaying a multiplier of 1.0
    scoreboard.topleft = camera.topleft
    # moves the scoreboard such that its top left corner is the camera's top left corner
    multiplier.topleft = scoreboard.bottomleft
    # positions the multiplier text under the scoreboard
    HUD.append(scoreboard)
    HUD.append(multiplier)
    # adds elements to HUD to be drawn


def show_high_score():
    """
    Shows the high score for the level in the upper right
    :return: nothing
    """
    try:
        high_score = level_high_score
        # sets the high score to the level_high_score gotten at the beginning
        if player.score > high_score:
            high_score = player.score
            # changes it to the player score if greater
    except:
        high_score = 0
        # if no high_score found
    high_score_display = gamebox.from_text(0, 0, "High Score: " + str(high_score), 30, "white")
    # creates a text box displaying said high score
    high_score_display.topright = camera.topright
    # positions the high_score display in the camera's top right corner
    HUD.append(high_score_display)
    # adds element to the HUD to be drawn


def make_you_win():
    """
    Creates a big "YOU WIN" statement to indicate that the player has completed the level
    :return: nothing
    """
    you_win = gamebox.from_text(camera.x, camera.y, "YOU WIN", 60, "white")
    # creates a big text box saying "you win" in the center of the screen
    restart = gamebox.from_text(camera.x, 0, "Press space to return to start", 30, "white")
    # creates a text box to tell player how to restart
    restart.top = you_win.bottom
    # positions restart statement under the "you win" statement
    HUD.append(you_win)
    HUD.append(restart)
    # adds element to HUD to be drawn


def make_game_over():
    """
    Creates a big "GAME OVER" statement to indicate that the player has lost said level
    :return: nothing
    """
    game_over = gamebox.from_text(camera.x, camera.y, "GAME OVER", 60, "white")
    # create a big text box saying "game over" in the center of the screen
    restart = gamebox.from_text(camera.x, 0, "Press space to return to start", 30, "white")
    # creates a text box to tell player how to restart
    restart.top = game_over.bottom
    # positions restart statement under the "game over" statement
    HUD.append(game_over)
    HUD.append(restart)
    # adds element to HUD to be drawn


# Additional lives may also be listed as "level restarts"
# and a score board may also be added in the top left
# with high score displayed at the top (basically like galaga)

# if additional bullet types are included, they will also be listed
# in the bottom right

# ------- START SCREEN -------
# creates a start screen with game name, student names (and IDs), and basic game instructions
game_name = gamebox.from_text(camera.x, camera.y - 120, "SUPER SPACE SHOOT", 48, "white")
author = gamebox.from_text(camera.x, camera.y - 84, "By Daniel Xue (dl3xud)", 40, "white")
start_screen = [game_name, author]
# stores relevant start screen elements inside a list for easier drawing

text_position = author.bottom  # initialize a variable to store y position of given text on the page
controls_text = "WASD to move\nLeft-click to shoot"
# controls text stored in a variable
for control_text in controls_text.split("\n"):
    # for each separate instruction
    controls = gamebox.from_text(camera.x, text_position + 18, control_text, 36, "white")
    # create a new gamebox oriented below the last
    start_screen.append(controls)
    # and add it to this list storing the start screen data
    text_position += controls.height
    # increase current text y position by the height of controls
goal_text = "Objective:\nSurvive to the end of the level\nwith the highest score"
for goal in goal_text.split("\n"):
    # for each separate line the state goal
    goal_line = gamebox.from_text(camera.x, text_position + 18, goal, 36, "white")
    # create a new gamebox oriented below the last
    start_screen.append(goal_line)
    # and add it to this list storing the start screen data
    text_position += goal_line.height
    # increase current text y position by the height of controls
begin1 = gamebox.from_text(camera.x, text_position + 54, "Press 1, 2, or T to select", 36, "white")
begin2 = gamebox.from_text(camera.x, text_position + 80, "a level and begin", 36, "white")
# creates a line below all that describing how to begin
start_screen.append(begin1)  # also adds that to the start screen text
start_screen.append(begin2)


# ------- LEVEL/STAGE DESIGNS -------
# "levels" that contain a preset sequence of enemies, pickups, and bosses


def level_select(keys):
    """
    Chooses a level to run based off of what key is pressed
    :param keys: a list that contains various keys when pressed
    :return: nothing
    """
    global curr_level
    curr_level = ""
    # clears curr_level
    if pygame.K_t in keys:
        test_level()  # loads player, enemies, and other relevant assets for a test level
        curr_level = "TEST"  # sets curr_level to test
    elif pygame.K_1 in keys:
        level_one()     # loads level 1
        curr_level = "1"    # sets curr_level to 1
    elif pygame.K_2 in keys:
        level_two()     # loads level 2
        curr_level = "2"    # sets curr_level to 2


def test_level():
    """
    The preset sequence of enemies, pickups, and bosses that make up a test level
    :return: nothing
    """
    make_player(player_color, player_size, init_player_hp)  # makes basic player
    make_basic_enemy(100, 100)
    make_basic_enemy(300, 100)
    make_mover_enemy(200, 50)
    make_mover_enemy(200, -50)
    for i in range(-100, -3000, -100):
        make_basic_enemy(random.randint(50, 150), i + random.randint(-20, 20))
        make_basic_enemy(random.randint(250, 350), i + random.randint(-20, 20))
        make_mover_enemy(200, i - 50)


def level_one():
    """
    The preset sequence of enemies, pickups, and bosses that make up level one
    :return: nothing
    """
    # screen 0: 600-0, also, blank except for player and a few enemies
    make_player(player_color, player_size, init_player_hp)  # makes basic player
    make_basic_enemy(100, 100)
    make_basic_enemy(300, 100)

    # screen 1: 0 - -600: intro to enemies
    for i in range(15, camera.width, 30):
        make_basic_enemy(i, -100)
        make_basic_enemy(i, -200 - i)
        make_basic_enemy(i, -600 + i)
    # row of enemies followed by an x

    # screen 2: -600 - -1200: intro to movers
    make_slider_enemy(200, -700, 1, 100)
    make_slider_enemy(200, -800, 1, 100, 60)
    # shows off different move periods
    make_climber_enemy(50, -950, 1, 100)
    make_climber_enemy(150, -950, 1, 100, phase=30)
    make_climber_enemy(250, -950, 1, 100, phase=60)
    make_climber_enemy(350, -950, 1, 100, phase=90)
    # fun with different phases
    for i in range(0, 120, 30):
        make_mover_enemy(200, -1200, 1, x_amplitude=100, x_phase=i, y_amplitude=100, y_phase=i+30)
    # enemies kind of move in a circle

    # screen 3: -1200 - -1800: fun with higher hp enemies
    for i in range(15, camera.width, 60):
        make_basic_enemy(i, -1400, 1)
        make_basic_enemy(i + 30, -1400, 2)
    # row of 1 and 2

    for i in range(15, camera.width, 60):
        make_basic_enemy(i, -1500, 2)
        make_basic_enemy(i + 30, -1500, 1)
    # row of 2 and 1

    for i in range(15, camera.width, 120):
        make_basic_enemy(i, -1600, 2)
        make_basic_enemy(i + 30, -1600, 1)
        make_basic_enemy(i + 60, -1600, 6)
        make_basic_enemy(i + 90, -1600, 3)
    # fun times with 1, 2, 6, and 3

    for i in range(15, camera.width, 120):
        make_basic_enemy(i, -1700, 11)
        make_basic_enemy(i + 30, -1700, 21)
    # row of 11 and 21, I suggest you avoid

    for i in range(15, camera.width, 120):
        make_basic_enemy(i, -1800, 1)
        make_basic_enemy(i + 30, -1800, 21)
        make_basic_enemy(i + 60, -1800, 1)
    # another row of 1 and 21's I suggest you avoid

    # screen 4: -1800 - -2400: fun with different move patterns
    for i in range(0, 9):
        make_mover_enemy(200, -1900 - i * 60, 2, int(200 / 9 * (i + 1)), int(100 / 18 * (i + 1)))
    # big wavy stick that I thought was cool

    # screen 5: -2400 - 3000: shoot 'em down!!
    make_rapid_fire_power_up(200, -2500)
    make_strength_power_up(100, -2500)
    make_speed_power_up(300, -2500)
    make_super_power_up(200, -2750)
    # shows off the power_ups if you missed them
    for i in range(15, camera.width, 30):
        for j in range(-2560, -3000, -30):
            make_basic_enemy(i, j, 2)


def level_two():
    """
    The preset sequence of enemies, pickups, and bosses that make up level two
    :return: nothing
    """
    # this level's theme? target practice!

    # screen 0: 600-0, also, blank except for player and a few enemies
    make_player(player_color, player_size, init_player_hp)  # makes basic player

    for i in range(5):
        make_slider_enemy(100, 300 - 60 * i, 1, 100, 120, 24 * i)
        make_slider_enemy(300, 300 - 60 * i, 1, 100, 120, 24 * i)
    # starts off with a few winding snakes to set the mood

    # screen 1: 0 - -600: fun with circles!!!
    for i in range(0, 120, 15):
        make_mover_enemy(100, -200, 3, x_amplitude=50, x_phase=i, y_amplitude=50, y_phase=i+30)
        make_mover_enemy(300, -200, 1, x_amplitude=50, x_phase=i, y_amplitude=50, y_phase=i+30)
    # slow circles to start
    make_speed_power_up(100, -200)
    # speed power-up in the yellow circle
    for i in range(0, 96, 12):
        make_mover_enemy(100, -400, 1, 50, 50, 96, 96, x_phase=i, y_phase=i+24)
        make_mover_enemy(300, -400, 3, 50, 50, 96, 96, x_phase=i, y_phase=i+24)
    # faster circles
    make_rapid_fire_power_up(300, -400)
    # rapid fire power-up in the yellow circle
    for i in range(0, 80, 10):
        make_mover_enemy(100, -600, 3, 50, 50, 80, 80, x_phase=i, y_phase=i+20)
        make_mover_enemy(300, -600, 1, 50, 50, 80, 80, x_phase=i, y_phase=i+20)
    # and they get even faster, sheesh
    make_super_power_up(100, -600)
    # super power-up in the yellow circle

    # screen 2: -600 - -1200: less fun with grids
    for i in range(15, camera.width, 60):
        make_climber_enemy(i, -1000, 2, 200)
        make_climber_enemy(i + 30, -1000, 3, 200, phase=30)

    for i in range(0, 6):
        make_slider_enemy(200, -800 - 60 * i, 1, 200, phase=i*20)
    # combines climbers and sliders

    # screen 3: -1200 - -1800: choices, choices, choices
    for i in range(60, camera.width-45, 30):
        for j in range(-1300, -1700, -30):
            make_basic_enemy(i, j, 5)
    # yellow barrier
    make_health_power_up(15, -1400)
    make_super_power_up(385, -1400)
    make_rapid_fire_power_up(200, -1250)
    make_rapid_fire_power_up(200, -1450)
    make_rapid_fire_power_up(200, -1650)
    # power-ups give you options, hopefully

    # screen 4: -1800 - -2400: Don't get too caught up in the small fries
    for i in range(15, camera.width, 30):
        for j in range(-1800, -2400, -30):
            make_basic_enemy(i, j, 1)
    # lots of nice green

    for i in range(0, 10):
        make_slider_enemy(200, -1800 - 60 * i, 25, 200, phase=12*i)
    # lots of not nice cyan

    # screen 5: -2400 - 3200: Chaos
    for i in range(0, 20):
        make_mover_enemy(200, -2600 - 30 * i, 6, 200 * i // 10, 200 + i, 120 - i, 120 + i, (120 - i) // 14, (120 + i) // 14)
        # makes a cool pattern, plug it into a graph if you have time later


# ------- SAVING/LOADING HIGH SCORES --------
# defines functions to save/load high scores


def save_score():
    """
    Saves a player's score when they complete a level
    :return: nothing
    """
    save_file = open("super_space_shoot_scores.txt", "a")
    # opens a new file to save scores in
    save_file.write(curr_level + "," + str(player.score) + "\n")
    # writes the current level and player score in one line
    save_file.close()
    # closes save file
    player.score_saved = True
    # changes score_saved to indicate that the player's score has been saved


def get_high_score():
    """
    Gets the saved high score when a level is booted
    :return: save high score as an int for the level
    """
    try:
        scores = {}     # initializes a dict to store scores
        with open("super_space_shoot_scores.txt", "r") as f:
            # opens the file to read if it exists
            for line in f.readlines():
                # splits by new line
                clean_line = line.strip()
                # strips line of white space
                if len(clean_line) >= 1:
                    # checks that line has characters in it
                    if clean_line.split(",")[0] in scores.keys():
                        # checks whether there's already an entry in the dict for the level
                        scores[clean_line.split(",")[0]].append(int(clean_line.split(",")[1]))
                        # if so, adds the score as an int to the list
                    else:
                        scores[clean_line.split(",")[0]] = [int(clean_line.split(",")[1])]
                        # otherwise adds a list with the first score to the level's key in the dict
            # f.close() is already implied here

        high_score = 0  # initializes an int to store high score
        for score in scores[curr_level]:
            # loops over scores for that current level
            if score > high_score:
                # if a score is greater than the high score
                high_score = score
                # it's the new high_score
    except:
        high_score = 0
        # if no file is find, the high score is 0 by default

    return high_score


# ------- INITIAL CONDITIONS --------
game_on = False  # keeps the game from turning on
curr_level = ""   # initializes a variable to store current level as a string
level_high_score = 0  # initializes an int to store the level high score
# so the save file doesn't have to be constantly read

# Player
player_color = "white"  # sets player color
player_size = 40  # sets player size
init_player_hp = 10  # sets initial player hp
player_move_speed = 5  # sets initial value for player move speed
player_fire_rate = 10  # determines how often the player can shoot when holding down left click
player_invincibility_frames = 30  # determines how long the player is invincible after getting hit
player_power_up_frames = 60  # determines how long the player's power-ups last
curr_power_up = None  # initializes a variable to store current_power_type

# Enemy
enemy_move_speed = 5  # sets initial value for enemy move speed

# Scroll Speed
scroll_speed = 2  # sets magnitude of scroll speed

# Bullet
bullet_speed = 10  # initializes the bullet speed to be 10
has_power_up = {
    "strength": False,
    "rapid fire": False,
    "speed": False,
    "super": False
}


def tick(keys):
    """
    Animation, input, collision detection, scoring, drawing...
    anything that happens every second, you name it, and
    it's probably mentioned somewhere in this function. Go figure.
    """
    # documentation format stolen from the pong lab, thank you for the help!
    # ----- GLOBAL VARIABLES -----
    global game_on
    global player
    global projectiles
    global enemies
    global HUD
    global power_up_indicators
    global curr_power_up
    global level_high_score

    # ----- THINGS THAT SHOULD BE CLEARED EVERY TICK (BETTER NAME PENDING) -----
    HUD = []
    power_up_indicators = []

    # ----- MOVEMENT/SCROLL -----
    if game_on:
        # checks that the game is on

        for projectile_type in projectiles.values():
            for projectile in projectile_type:
                projectile.move_speed()
        # moves each bullet by its designated speed

        for enemy_kind in enemies.values():
            for enemy in enemy_kind:
                enemy.move_speed()
        # moves each enemy by its designated speed

    else:
        camera.topleft = (0, 0)
        # forces camera position to be at its initial position
        for kind in enemies.keys():
            enemies[kind] = []  # clears all lists of enemies initially
        for kind in projectiles.keys():
            projectiles[kind] = []  # clears all lists of projectiles initially
        for kind in power_ups.keys():
            power_ups[kind] = []  # clears all lists of power_ups initially

        level_select(keys)
        # loads a level depending on what key is pressed

    # ------- USER INPUT ---------
    if curr_level and not game_on:
        # turns the game on when level is selected and the game is off
        game_on = True
        # gets the high score for the current level
        level_high_score = get_high_score()

    if game_on and player:
        # checks that the game is on and that player exists
        if pygame.K_w in keys and player.top > camera.top:
            player.y -= player_move_speed
        if pygame.K_s in keys and player.bottom < camera.bottom:
            player.y += player_move_speed
        if pygame.K_d in keys and player.right < camera.right:
            player.x += player_move_speed
        if pygame.K_a in keys and player.left > camera.left:
            player.x -= player_move_speed
        # WASD to move but only if player is not moving out of camera range in each direction

        if camera.mouseclick:
            # when mouse is clicked
            if player.bullet_timer % player_fire_rate:
                # if the current timer is not divisible by 5
                player.bullet_timer += 1
                # add one to timer
            else:
                # if the current timer is divisible by 5
                make_player_bullet()
                # make a bullet
                player.bullet_timer += 1
                # add one to timer
        else:
            player.bullet_timer = 0
            # sets timer to zero when mouse is not clicked
        # if you hold down the mouse, the ship fires a bullet every five frames
        # but if you mash the mouse button you can shoot more

        # also P for pausing the game

    # ------- BULLET BEHAVIOR ---------
    # defines relevant projectile behavior for all projectiles made
    for projectile_type in projectiles.values():
        # for all lists of projectiles present
        for projectile in projectile_type:
            # loops over each projectile
            if out_of_bounds(projectile):
                # if any are out of bounds
                projectile_type.remove(projectile)
                # they're no longer relevant

    # note that basic player bullets travel up by preset default and aren't included here

    # ------- ENEMY BEHAVIOR ---------
    # where enemy movement, shooting, and other behaviors are defined

    for enemy_kind in enemies.values():
        # for all lists of enemies present
        for enemy in enemy_kind:
            # loops over each enemy in each list
            if enemy.top > camera.bottom:
                # if any are below the bottom of the screen
                enemy_kind.remove(enemy)
                # they're no longer relevant
    # note: above-screen enemies are not drawn instead of completely de-spawned like bullets
    # to allow for good level planning

    for enemy_kind in enemies.values():
        for enemy in enemy_kind:
            if enemy.hp <= 0:
                # if the health of any enemy drops at or below 0
                make_random_power_up(enemy.x, enemy.y)
                # makes a random power up drop from the enemy when killed
                # some destruction animation might play
                enemy_kind.remove(enemy)  # the enemy is destroyed
                if player:
                    # only occurs if the player exists
                    player.score += int(enemy.score * player.score_multiplier)
                    # the player gets some score increase times their current score multiplier
                    player.score_multiplier += enemy.score / 100
                    # score multiplier increases proportional to score increased

    # note that basic enemies don't shoot or move

    for enemy in enemies["mover"]:
        x_scalar = math.sin(2 * math.pi / enemy.x_period * enemy.x_move_timer - enemy.x_phase)
        enemy.x = enemy.x_amplitude * x_scalar + enemy.x_init
        y_scalar = math.sin(2 * math.pi / enemy.y_period * enemy.y_move_timer - enemy.y_phase)
        enemy.y = enemy.y_amplitude * y_scalar + enemy.y_init
        # each enemy moves sinusoidally in the x and y directions with their given amplitudes
        # with scalars storing the result of the sine function to save line space
        # this can be modified later as needed
        enemy.x_move_timer += 1
        enemy.y_move_timer += 1
        # increases move timer
        if enemy.x_move_timer == enemy.x_period:
            enemy.x_move_timer = 0
        if enemy.y_move_timer == enemy.y_period:
            enemy.y_move_timer = 0
            # resets move timer after reaching the period so we don't have to store so much data
    # moves side to side sinusoidally with the power of math

    # tougher enemies may move and shoot more often

    # boss enemies will stay in place at the top and shoot more bullets

    # ----- COLLISION DETECTION -----
    # if an enemy bullet collides with the player
    # the bullet is destroyed and the player takes damage
    # if the player is out of HP, the player explodes
    # and level restarts if they have lives
    # if no lives, game over

    if player:
        # only occurs if player exists

        player_touches_enemy = False
        # initializes a boolean that can stored whether an enemy is touching the player
        # without having to loop any other actions for the enemies present
        for enemy_kind in enemies.values():
            for enemy in enemy_kind:
                # for all enemies in all lists:
                if player.touches(enemy):
                    player_touches_enemy = True

        if player_touches_enemy:
            # if a player exists and touches any enemy
            if player.hurt_timer % player_invincibility_frames:
                # if their hurt timer is not at a multiple of their i-frames
                player.hurt_timer += 1
                # increase hurt timer by one
            else:
                player.hp -= 1
                # decrease hp if their hurt time is at a multiple of their i-frames
                player.score_multiplier = 1
                # resets the player's score multiplier to 1
                player.hurt_timer += 1
                # increase hurt timer by one
        else:
            # if a player does not touch any enemy
            if player.hurt_timer % player_invincibility_frames:
                # if hurt times is not at a multiple of their i-frames
                player.hurt_timer += 1
                # increase hurt timer by one
            else:
                # if at a multiple of their i-frames
                player.hurt_timer = 0
                # reset hurt timer
        # if the player hit the enemy w/o invincibility, they lose hp and are invincible for a time
        # after which they can get hurt again if they are still touching the enemy
        # or their invincibility frames run out and they still have to dodge

        if 0 < player.hurt_timer % player_invincibility_frames < (player_invincibility_frames - 5):
            show_invincible(player)

        if player.hp <= 0:
            # if player hp drops to 0
            if not player.score_saved:
                save_score()
            # saves score if player score has not been saved
            player = None
            # removes the player from the game

    if not player and game_on:
        # if the player is removed but the game is running
        make_game_over()
        # shows game over text
        if pygame.K_SPACE in keys:
            game_on = False
            # resets the game if space is pressed

    for bullet in projectiles["player bullet"]:
        # loops over player bullets
        for enemy_kind in enemies.values():
            for enemy in enemy_kind:
                # for all enemies in all enemy lists
                if bullet.touches(enemy):
                    # if the bullet touches the enemy
                    bullet.pierce -= 1
                    # the bullet loses some pierce
                    enemy.hp -= 1
                    # the enemy loses one hp

    for bullet_list in projectiles.values():
        for bullet in bullet_list:
            # for all bullets
            if bullet.pierce <= 0:
                # when bullet pierce is less than zero
                bullet_list.remove(bullet)
                # remove the bullet

    # ----- POWER-UP BEHAVIOR -----
    # defines relevant power-up behavior for all power-ups made
    player_touches_power_up = False  # initializes a boolean to store whether the player has contact a power-up

    if player:
        # only occurs if the player exists
        for power_up_list in power_ups.values():
            # for all lists of power-ups present
            for power_up in power_up_list:
                # loops over each power_up
                if camera.bottom < power_up.top:
                    # if any are below the camera's bounds
                    power_up_list.remove(power_up)
                    # they're no longer relevant

                if player.touches(power_up) and not player.power_up_timer:
                    # checks whether the player is touching a power_up with a current power_up in effect
                    player_touches_power_up = True
                    # changes this condition to indicate it is
                    curr_power_up = power_up.kind
                    # stores kind of power-up in contact in here
                    power_up_list.remove(power_up)
                    # removes said power-up from play

        if player_touches_power_up or player.power_up_timer:
            add_power_up(curr_power_up)
            # adds power_up effects if the player has just touched the power_up
            # or if their timer has not run out

    # ----- HUD Elements -----
    # where HUD elements are recreated every tick for accurate information
    make_health_bar()
    make_scoreboard()
    show_high_score()

    # ----- SCROLLING LEVEL -----
    # where appropriate elements are moved up with the camera
    if game_on:
        camera.y -= scroll_speed
        if player:
            # checks that player exists
            player.y -= scroll_speed
        for element in HUD:
            element.y -= scroll_speed
        for indicator in power_up_indicators:
            indicator.y -= scroll_speed

    # moves the camera, player, HUD Elements and power-up indicators up

    # ---- CHECKING FOR WIN ----
    # checks that the player got to the end of the level and/or destroyed all enemies
    # may record score in external file
    enemies_present = False
    # initializes variable to check for the presence of enemies
    for enemy_list in enemies.values():
        # loops over lists of all enemy types
        if enemy_list:
            # if the list is not empty
            enemies_present = True
            # set enemies_present to true

    if not enemies_present and game_on and player:
        # if no enemies are present and that the player is alive
        make_you_win()
        # print the win statement
        # record the score in a separate outfile
        if not player.score_saved:
            # checks that the player's score has not been saved
            save_score()
        # make restarting possible
        if pygame.K_SPACE in keys:
            game_on = False

    # ----- DRAW METHODS --------
    camera.clear("black")
    # where everything above is actually drawn and displayed
    if not game_on:
        for element in start_screen:
            camera.draw(element)
    # draws all active start screen elements if the game has not started

    if player:
        camera.draw(player)
        # draws the the player if it exists

    for indicator in power_up_indicators:
        camera.draw(indicator)
    # draw all power_up indicators

    for projectile_list in projectiles.values():
        for projectile in projectile_list:
            camera.draw(projectile)
    # draws all active bullets

    for enemy_list in enemies.values():
        for enemy in enemy_list:
            if in_camera_range(enemy):
                camera.draw(enemy)
    # draws all enemies that are in camera range

    for power_up_list in power_ups.values():
        for power_up in power_up_list:
            if in_camera_range(power_up):
                camera.draw(power_up)
    # draws all power-ups that are in camera range

    for element in HUD:
        camera.draw(element)
    # draws all HUD elements

    camera.display()


ticks_per_second = 30

gamebox.timer_loop(ticks_per_second, tick)
