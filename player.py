#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Pitfall v1.0
By Danilo Lekovic for Game Design 12

player.py

Main player
"""

import pygame
from pygame.locals import *

# Using Pygame's built-in vector system for coordinates

vec = pygame.math.Vector2
import os


class Player(pygame.sprite.Sprite):

    # Initialize class

    def __init__(self, x, y):
        super().__init__()
        self.pos = vec(x, y)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)

        # Various states the player can be in
        # This is used to change the players sprite & behavior

        self.STANCE = 0
        self.RUNNING = 1
        self.SWING = 2
        self.JUMPING = 3
        self.LEFT = 4
        self.RIGHT = 5
        self.CLIMBING = 6
        self.currentState = self.STANCE

        # Important values

        self.health = 6
        self.score = 0
        self.coins = 0

        # Double jump

        self.doubled = False

        # Player's orientation
        # This is efficient because now we only have
        # to have one direction for sprites

        self.orientation = self.RIGHT

        # Determines in which directions the player
        # is allowed to move

        self.canMoveRight = True
        self.canMoveLeft = True

        # Animation timers and indexes dictate
        # the current frame and how long each frame
        # should last

        self.animationTimer = 0
        self.animationIndex = 0

        # Animations are loaded from the sprites folder

        self.animations = {}
        self.load()

        # Current sprite is set and rectangle is created
        # for collision detection purposes

        self.image = self.animations['Idle'][0]
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)

    # Changes current sprite and edits rectangle properties

    def changeSprite(self, kind, index=None):
        if index is None:
            index = self.animationIndex

        self.image = self.animations[kind][index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.image.get_width() / 2,
                            self.image.get_height() / 2)

    # Handles jumping by changing the y acceleration to -25.0
    # Also handles double jumping

    def jump(self):
        if self.pos.y < 600:
            self.acceleration.y = -25.0

            if self.acceleration.x > 0.0 and not self.doubled:
                self.acceleration.x = self.acceleration.x * 1.5

            if self.acceleration.x < 0.0 and not self.doubled:
                self.acceleration.x = self.acceleration.x * 1.5
        else:

            self.currentState = self.STANCE

    # Handles player going down ladders
    # by changing the y acceleration to 10.0

    def fall(self):
        self.acceleration.y = 10.0
        self.acceleration.x = 0.0
        self.velocity.x = 0.0
        self.currentState = self.CLIMBING

    # Handles players going up ladders
    # by changing the y acceleration to -5.0

    def rise(self):
        self.acceleration.y = -5.0
        self.acceleration.x = 0.0
        self.velocity.x = 0.0
        self.currentState = self.CLIMBING

    # Updates the player's position in the game loop

    def update(self):

        # Handles behavior for when player is underground

        if self.pos.y > 600:
            self.acceleration.y = 0.0
            self.velocity.y = 0.0
            self.pos.y = 600
            self.currentState = self.STANCE
            self.doubled = False

        # Handles behavior for climbing ladders

        if self.acceleration.y == -5.0 and self.pos.y <= 400:
            self.acceleration.y = 0.0
            self.velocity.y = 0.0
            self.pos.y = 400
            self.currentState = self.STANCE
            self.doubled = False

        # Equations of motion

        self.pos += self.acceleration

        # Does not let player leave left border

        if self.pos.x < 0:
            self.pos.x = 0

        # Updates rectangle for collision purposes

        self.rect.move_ip(self.pos.x, self.pos.y)

        # Handles jumping and physics

        if self.acceleration.y <= -25.0 and self.pos.y <= 300:
            self.acceleration.y = 25.0
        elif self.acceleration.y <= -25.0 and self.pos.y == 604.0:
            self.acceleration.y = 25.0

        if self.acceleration.y >= 25.0 and self.pos.y == 400.0:
            self.acceleration.y = 0.0

            if self.acceleration.x > 0 or self.acceleration.x < 0:
                self.acceleration.x = self.acceleration.x / 1.5
                self.currentState = self.RUNNING
            else:
                self.currentState = self.STANCE

        if self.pos.y >= 690 - self.animations['Idle'][0].get_height() \
            and self.acceleration.y <= -25.0:
            self.currentState = self.STANCE
            self.doubled = False

        if self.pos.y == 400.0 and self.acceleration.y <= -25.0:
            self.acceleration.y = 0.0
            self.velocity.y = 0.0
            self.doubled = False

        if self.acceleration.y <= -25.0 and self.pos.y == 604.0:
            self.acceleration.y = 0.0
            self.velocity.y = 0.0
            self.doubled = False

    # Moves player left by setting x acceleration to -15

    def left(self):
        self.acceleration.x = -15

    # Moves player right by setting x acceleration to +15

    def right(self):
        self.acceleration.x = 15

    # Stops player by setting x acceleration to 0

    def stop(self):
        self.acceleration.x = 0

    # Loads sprites & animations for the player

    def load(self):

        # Checks if player path exists (Should always exist)

        if os.path.exists('Sprites/Player/'):

            # Certain animations are found

            animationNames = ['Climbing', 'Idle', 'Jumping', 'Running']

            # Each sprite is converted to a pygame image and added to the animation dictionary

            for name in animationNames:
                if os.path.exists('Sprites/Player/{}'.format(name)):
                    (path, dirs, files) = \
                        os.walk('Sprites/Player/{}'.format(name)).__next__()
                    self.animations[name] = []
                    bufferArray = []

                    for i in files:
                        if i.endswith('.png'):
                            bufferArray.append(pygame.image.load('Sprites/Player/{}/{}'.format(name,
                                    i)))

                    self.animations[name] = bufferArray

    # Handles player orientation so we can use minimal
    # sprites

    def draw(self, screen, coords):
        if self.orientation is self.LEFT:
            screen.blit(pygame.transform.flip(self.image, True, False),
                        coords)
        else:
            screen.blit(self.image, coords)