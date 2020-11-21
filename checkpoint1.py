# Daniel Xue
# dlx3ud
# Programming Project Checkpoint 1

"""
Baseline Project idea: Bullet-Hell Style Space Shooter
(a la Galaga, the Touhou Project, and/or Space Invaders at a minimum)
Implementation of required features detailed in code belows.
Priority of planned optional features:
Bullets - that shoot from the ship (kind of a must but should be detailed here)
Enemies - that spawn, move, get destroyed after being hit x times
Health Bar - decreases when hitting enemies
Collectibles - mostly power-ups from various enemies
Scrolling Level - for longer, more complex levels
Animation - for the ship, bullets, enemies
Score Board - to track how well you're doing
More levels, hi-score boards, etc. - only if I have time
"""

import pygame
import gamebox

# ------- CAMERA -------
camera = gamebox.Camera(800, 600)
# creates camera to view the game, sets dimensions at 800 by 600
# camera will be centered on the main ship

# ------- GRAPHICS/ANIMATIONS -------
# Player Sprites
# the main player sprite will be a ship that starts at the bottom of the screen
# probably represented by a white rectangle for most of this project
# and then will be replaced at the end with relevant ship image at the end
# with a relevant death animation if HP drops to 0

# Enemy Sprites
# mostly represented by green rectangles that move in from the top of the screen
# and then will sit still and shoot at the character until they pass them
# or the player does enough damage, causing them to explode

# may also make different types if I have time
# e.g. more health, different moving patterns, maybe a boss enemy?

# Bullets and other Projectiles
# mostly green and white moving rectangles for the majority of development
# usually only shoot in straight lines and do a set amount of damage

# may also make different types if I have time
# e.g. rockets that do AoE damage, homing missiles, laser beams, etc.

# Collectibles
# power-ups to health, speed, power, dropped by enemies when killed
# will be represented by red, blue, and yellow boxes for development
# may also increase score

# HUD Elements (Timer, Health Bar, etc.)
# A health bar starting at 100 will be included on the bottom left
# that will dwindle when the player runs into enemy bullets
# Additional lives may also be listed as "level restarts"
# and a score board may also be added in the top left
# with high score displayed at the top (basically like galaga)

# if additional bullet types are included, they will also be listed
# in the bottom right

# ------- START SCREEN -------
# creates a start screen with game name, student names (and IDs), and basic game instructions
# pretty straightforward, Space Shoot (name pending)
# Daniel Xue (dlx3ud)
# WASD to move, mouse to shoot (controls pending)
# objective is to live and shoot down the most enemies for the highest score

# ------- LEVEL/STAGE DESIGNS -------
# defines several "levels" or "stages" for the players to progress through/choose
# a pre-planned sequence of enemy spawns, pickups, and bosses that can be listed here
# probably won't have time for more levels, but they can also be listed
# in separate functions


def tick(keys):
    """
    Animation, input, collision detection, scoring, drawing...
    anything that happens every second, you name it, and
    it's probably mentioned somewhere in this function. Go figure.
    """
    # categories stolen from whoever coded the pong lab, thank you
    # for your help with documenting this project!

    # ----- MOVEMENT/SCROLL -----
    # Camera will continuously scroll up to give player feeling
    # of level progression (subject to change)

    # may also have toggle to check if game has started
    # before moving any players/enemies/bullets/etc.

    # ------- USER INPUT ---------
    # as previously stated, WASD to move
    # and left click to shoot (right for specials)
    # also P for pausing the game

    # ------- ENEMY "AI" ---------
    # where enemy movement and shooting is defined
    # for the time being, normal enemies largely stay in place
    # and may shoot at the player occasionally

    # whereas tougher enemies might move in weird patterns
    # and/or shoot more often

    # boss enemies will probably stay in place at the top of the screen
    # and shoot more bullets

    # ----- COLLISION DETECTION -----
    # if an enemy bullet collides with the player
    # the bullet is destroyed and the player takes damage
    # if the player is out of HP, the player explodes
    # and level restarts if they have lives
    # if no lives, game over

    # if a player bullet hits the enemy
    # the bullet is destroyed, and the enemy takes damage
    # if the enemy is out of HP, the enemy explodes
    # and player score increases
    # and a power-up may drop

    # ----- SCORING ------
    # arbitrary values are assigned for each enemy killed
    # and then shown in the upper left

    # if the player kills a lot of enemies without being hit
    # a multiplier may be added to the score

    # ----- DRAW METHODS --------
    camera.clear("black")
    # where everything above is actually drawn and displayed
    camera.display()

    # ---- CHECKING FOR WIN ----
    # checks that the player beat the boss and/or got to the end of the level
    # may record score in external file
    # and then request the player for a name to go with a score


ticks_per_second = 30

gamebox.timer_loop(ticks_per_second, tick)