# Daniel Xue
# dlx3ud
# Programming Project Checkpoint 2

"""
Baseline Project idea: Bullet-Hell Style Space Shooter
(a la Galaga, the Touhou Project, and/or Space Invaders at a minimum)
Implementation of required features detailed in code below:
Priority of planned optional features:
Bullets - basic is done
Enemies - basic is done, mover is done (needs some more customization options with phase, amplitude, etc.)
Health Bar - is mostly done, code to reset game is done
Collectibles - not done or started, but i-frame indicator is made
Scrolling Level - done
Animation - nope
Score Board - nope
More levels, hi-score boards, etc. - nope
Note: still also need to make a win condition / add score
Note: my invincibility frames code just stopped working, so that's no fun
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
# eventually replaced with relevant ship image at the end with a death animation if HP drops to 0


def make_player(color, size, hp):
    """
    Creates a square player character middle of the bottom of the screen
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
    player.hurt_timer = 0       # initializes a value for a timer for invincibility frames


# Enemy Sprites
# green boxes moving in from the top that can move, shoot at the player or both
# will be destroyed if the player causes enough damage, playing an explosion animation
enemies = {
    "basic": [],
    "mover": []
}
# initializes an empty dict to store list of gameboxes for each kind of enemy


def make_enemy(kind, x, y, color, width, height, hp):
    """
    Spawns an enemy of a given kind at a given location with a given color, width, and height
    :param hp: int starting hit points of the enemy
    :param kind: a string indicating that enemy's kind (a key in the dictionary of lists)
    :param x: x coordinate of the enemy's initial location
    :param y: y coordinate of the enemy's initial location
    :param color: string indicating that enemy's color
    :param width: int pixel width of said enemy
    :param height: int pixel height of said enemy
    :return: nothing
    """
    enemy = gamebox.from_color(x, y, color, width, height)
    # creates a gamebox with the given parameters
    enemy.hp = hp
    # sets enemy hp to the hp given
    enemies[kind].append(enemy)
    # appends said value a list in the dictionary of projectiles


def make_basic_enemy(x, y):
    """
    Spawns a basic enemy that neither moves nor shoots at the given location
    :param x: x coordinate of the enemy's initial location
    :param y: y coordinate of the enemy's initial location
    :return: nothing
    """
    make_enemy("basic", x, y, "green", 30, 30, 1)   # basic enemies have an hp of 1


# different types possible (e.g. more health, different moving patterns, bosses possible)


def make_mover_enemy(x, y):
    """
    Spawns a basic enemy that neither moves nor shoots at the given location
    :param x: x coordinate of the enemy's initial location
    :param y: y coordinate of the enemy's initial location
    :return: nothing
    """
    make_enemy("mover", x, y, "dark green", 30, 30, 1)   # mover enemies have an hp of 1 for testing
    enemies["mover"][-1].move_timer = 0     # initializes a value for timer to dictate behavior


# Bullets and other Projectiles
# green and white rectangles that shoot in lines and do damage
projectiles = {
    "player bullet": [],
    "enemy bullet": []
}
# initializes an empty dictionary to store list of gameboxes for each kind of projectile


def make_projectile(kind, x, y, color, size, speedx=0, speedy=0):
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
    # sets bullet speed to be player speed by going up a certain amount
    projectiles[kind].append(projectile)
    # appends said value a list in the dictionary of projectiles


def make_player_bullet():
    """
    Spawns a player bullet at the player's location that goes up
    :return: nothing
    """
    make_projectile("player bullet", player.x, player.y, "white", 5, speedy=player.speedy - bullet_speed)


# may also make different types if I have time
# e.g. rockets that do AoE damage, homing missiles, laser beams, etc.

# Collectibles
# power-ups to health, speed, power, dropped by enemies when killed; may also increase score
power_up_indicators = []
# initializes an empty list to store power-ups


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
    hp_remaining = gamebox.from_color(0, 0, "red", total_hp.width, player.hp / init_player_hp * total_hp.height)
    # creates red rectangle with length corresponding to player health
    hp_remaining.bottomleft = total_hp.bottomleft
    # matches the bottomleft corner of health remaining with the total health
    HUD.append(outline)
    HUD.append(total_hp)
    HUD.append(hp_remaining)
    # adds all elements to HUD


# Health bar starting at 10 on the bottom left that decreases when player gets hit


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
controls_text = "WASD to move\nLeft-click to shoot\nP to pause/unpause"
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
begin = gamebox.from_text(camera.x, text_position + 54, "Press space to begin", 36, "white")
# creates a line below all that describing how to begin
start_screen.append(begin)  # also adds that to the start screen text

# ------- LEVEL/STAGE DESIGNS -------
# "levels" that contain a preset sequence of enemies, pickups, and bosses


def level_one():
    """
    The preset sequence of enemies, pickups, and bosses that make up level one
    :return: nothing
    """
    make_player(player_color, player_size, init_player_hp)    # makes basic player
    make_basic_enemy(100, 100)
    make_basic_enemy(300, 100)
    make_mover_enemy(200, 50)
    make_mover_enemy(200, -50)
    for i in range(-100, -1000, -100):
        make_basic_enemy(random.randint(50, 150), i + random.randint(-20, 20))
        make_basic_enemy(random.randint(250, 350), i + random.randint(-20, 20))
        make_mover_enemy(200, i - 50)


# ------- INITIAL CONDITIONS --------
game_on = False  # keeps the game from turning on
bullet_speed = 10  # initializes the bullet speed to be 10

# Player
player_color = "white"  # sets player color
player_size = 40        # sets player size
init_player_hp = 10     # sets initial player hp
player_move_speed = 5  # sets initial value for player move speed
player_fire_rate = 5    # determines how often the player can shoot when holding down left click
player_invincibility_frames = 60    # determines how long the player is invincible after getting hit

# Enemy
enemy_move_speed = 5  # sets initial value for enemy move speed

# Scroll Speed
scroll_speed = 2    # sets magnitude of scroll speed


def tick(keys):
    """
    Animation, input, collision detection, scoring, drawing...
    anything that happens every second, you name it, and
    it's probably mentioned somewhere in this function. Go figure.
    """
    # documentation format stolen from the pong lab, thank you for the help!
    # ----- GLOBAL VARIABLES -----
    global game_on
    global projectiles
    global enemies
    global HUD
    global power_up_indicators

    # ----- THINGS THAT SHOULD BE CLEARED EVERY TICK (BETTER NAME PENDING) -----
    HUD = []
    power_up_indicators = []

    # ----- MOVEMENT/SCROLL -----
    if game_on:
        # checks that the game is on
        player.move_speed()
        # moves the player by a designated speed if the game is turned on

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

        level_one()  # loads player, enemies, and other relevant assets for level one
        # may include condition to check for save/other progress if time

    # ------- USER INPUT ---------
    if pygame.K_SPACE in keys and not game_on:
        # turns the game on when space is pressed
        game_on = True

    if game_on:
        # checks that the game is on
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
                # some destruction animation might play
                enemy_kind.remove(enemy)    # the enemy is destroyed
                # the player gets some score increase

    # note that basic enemies don't shoot or move

    for enemy in enemies["mover"]:
        enemy.x = 100 * math.sin(math.pi / 60 * enemy.move_timer) + 200
        # amplitude is 100, phase is 120 ticks (or 4 seconds), initial position is 200
        # this can be modified later as needed (or in the original function
        enemy.move_timer += 1
        # increases move timer
        if enemy.move_timer == 120:
            enemy.move_timer = 0
            # resets move timer after reach 120 so we don't have to store so much data
    # moves side to side sinusoidally with the power of math

    # tougher enemies may move and shoot more often

    # boss enemies will stay in place at the top and shoot more bullets

    # ----- COLLISION DETECTION -----
    # if an enemy bullet collides with the player
    # the bullet is destroyed and the player takes damage
    # if the player is out of HP, the player explodes
    # and level restarts if they have lives
    # if no lives, game over

    for enemy_kind in enemies.values():
        for enemy in enemy_kind:
            # for all enemies in all lists:
            if player.touches(enemy):
                # if a player touches any enemy
                if player.hurt_timer % player_invincibility_frames:
                    # if their hurt timer is not at a multiple of their i-frames
                    player.hurt_timer += 1
                    # increase hurt timer by one
                else:
                    player.hp -= 1
                    # decrease hp if their hurt time is at a multiple of their i-frames
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

    if 0 < player.hurt_timer % player_invincibility_frames < (player_invincibility_frames - 10):
        show_invincible(player)

    if player.hp <= 0:
        # if player hp drops to 0
        game_on = False
        # resets the game

    for bullet in projectiles["player bullet"]:
        # loops over player bullets
        for enemy_kind in enemies.values():
            for enemy in enemy_kind:
                # for all enemies in all enemy lists
                if bullet.touches(enemy):
                    # if the bullet touches the enemy
                    projectiles["player bullet"].remove(bullet)
                    # the bullet is destroyed
                    enemy.hp -= 1
                    # the enemy loses one hp

    # ----- SCORING ------
    # arbitrary values are assigned for each enemy killed
    # and then shown in the upper left

    # if the player kills a lot of enemies without being hit
    # a multiplier may be added to the score

    # ----- HUD Elements -----
    # where HUD elements are recreated every tick for accurate information
    make_health_bar()

    # ----- SCROLLING LEVEL -----
    # where appropriate elements are moved up with the camera
    if game_on:
        camera.y -= scroll_speed
        player.y -= scroll_speed
        for element in HUD:
            element.y -= scroll_speed
        for indicator in power_up_indicators:
            indicator.y -= scroll_speed

    # moves the camera, player, HUD Elements and power-up indicators up

    # ----- DRAW METHODS --------
    camera.clear("black")
    # where everything above is actually drawn and displayed
    if not game_on:
        for element in start_screen:
            camera.draw(element)
    # draws all active start screen elements if the game has not started

    camera.draw(player)
    # draws the the player

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

    for element in HUD:
        camera.draw(element)
    # draws all HUD elements

    camera.display()

    # ---- CHECKING FOR WIN ----
    # checks that the player beat the boss and/or got to the end of the level
    # may record score in external file
    # and then request the player for a name to go with a score


ticks_per_second = 30

gamebox.timer_loop(ticks_per_second, tick)
