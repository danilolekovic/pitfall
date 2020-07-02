#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Pitfall v1.0
By Danilo Lekovic for Game Design 12

entity.py

Class files representing different entities
"""

import pygame as pg

# Using Pygame's built-in vectors

vec = pg.math.Vector2


# Barrel are found above ground
# Player has to jump over these
# Barrels also roll

class Barrel(pg.sprite.Sprite):

    # Initialize class

    def __init__(self, x, y):
        super().__init__()

        # Handles animation

        self.animationTimer = 0
        self.animationIndex = 0
        self.animations = \
            {'All': [pg.image.load('Sprites/Environment/Barrel/1.png'),
             pg.image.load('Sprites/Environment/Barrel/2.png')]}
        self.pos = vec(x, y)
        self.image = self.animations['All'][0].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)

    # Changes sprite

    def changeSprite(self, index=None):
        if index is None:
            index = self.animationIndex

        self.pos = vec(self.pos.x, self.pos.y)
        self.image = self.animations['All'][index].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.pos.x, self.pos.y)

    # Updates in main loop

    def update(self):
        if self.animationIndex == 0:
            self.animationIndex = 1
        else:
            self.animationIndex = 0

        self.changeSprite(self.animationIndex)

        self.pos.x -= 10


# Ghost are found underground
# Player cannot touch these
# Ghosts also move

class Ghost(pg.sprite.Sprite):

    # Initialize class

    def __init__(self, x, y):
        super().__init__()

        # Handle animations

        self.animationTimer = 0
        self.animationIndex = 0
        self.animations = \
            {'All': [pg.image.load('Sprites/Environment/Ghost/1.png'),
             pg.image.load('Sprites/Environment/Ghost/2.png')]}
        self.pos = vec(x, y)
        self.image = self.animations['All'][0].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)

    # Change sprite

    def changeSprite(self, index=None):
        if index is None:
            index = self.animationIndex

        self.pos = vec(self.pos.x, self.pos.y)
        self.image = self.animations['All'][index].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.pos.x, self.pos.y)

    # Update in main loop

    def update(self):
        self.animationTimer += 1

        self.changeSprite(self.animationIndex)
        self.pos.x -= 5

        if self.animationTimer >= 3:
            self.animationTimer = 0

            if self.animationIndex == 0:
                self.animationIndex = 1
            else:
                self.animationIndex = 0


# Rats are found underground
# Player cannot touch these
# Rats also move

class Rat(pg.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.animationTimer = 0
        self.animationIndex = 0
        self.animations = \
            {'All': [pg.image.load('Sprites/Environment/Rat/1.png'),
             pg.image.load('Sprites/Environment/Rat/2.png')]}
        self.pos = vec(x, y)
        self.image = self.animations['All'][0].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)

    def changeSprite(self, index=None):
        if index is None:
            index = self.animationIndex

        self.pos = vec(self.pos.x, self.pos.y)
        self.image = self.animations['All'][index].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.pos.x, self.pos.y)

    def update(self):
        self.animationTimer += 1

        self.changeSprite(self.animationIndex)
        self.pos.x -= 8

        if self.animationTimer >= 3:
            self.animationTimer = 0

            if self.animationIndex == 0:
                self.animationIndex = 1
            else:
                self.animationIndex = 0


# Snakes are found above ground
# Player cannot touch these
# Snakes don't move

class Snake(pg.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.animationTimer = 0
        self.animationIndex = 0
        self.animations = \
            {'All': [pg.image.load('Sprites/Environment/Snake/1.png'),
             pg.image.load('Sprites/Environment/Snake/2.png')]}
        self.pos = vec(x, y)
        self.image = self.animations['All'][0].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)

    def changeSprite(self, index=None):
        if index is None:
            index = self.animationIndex

        self.pos = vec(self.pos.x, self.pos.y)
        self.image = self.animations['All'][index].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.pos.x, self.pos.y)

    def update(self):
        self.animationTimer += 1

        self.changeSprite(self.animationIndex)

        if self.animationTimer >= 5:
            self.animationTimer = 0

            if self.animationIndex == 0:
                self.animationIndex = 1
            else:
                self.animationIndex = 0


# Pits are formed above ground
# Player cannot touch these
# Pits sink and reopen

class Pit(pg.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.animationTimer = 0
        self.animationIndex = 0

        # Full animation

        self.animations = {'All': [
            pg.image.load('Sprites/Environment/Pit/1.png'),
            pg.image.load('Sprites/Environment/Pit/2.png'),
            pg.image.load('Sprites/Environment/Pit/3.png'),
            pg.image.load('Sprites/Environment/Pit/4.png'),
            pg.image.load('Sprites/Environment/Pit/5.png'),
            pg.image.load('Sprites/Environment/Pit/6.png'),
            pg.image.load('Sprites/Environment/Pit/7.png'),
            pg.image.load('Sprites/Environment/Pit/8.png'),
            pg.image.load('Sprites/Environment/Pit/8.png'),
            pg.image.load('Sprites/Environment/Pit/7.png'),
            pg.image.load('Sprites/Environment/Pit/6.png'),
            pg.image.load('Sprites/Environment/Pit/5.png'),
            pg.image.load('Sprites/Environment/Pit/4.png'),
            pg.image.load('Sprites/Environment/Pit/3.png'),
            pg.image.load('Sprites/Environment/Pit/2.png'),
            pg.image.load('Sprites/Environment/Pit/1.png'),
            ]}
        self.pos = vec(x, y)
        self.originalPos = self.pos
        self.image = self.animations['All'][0].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.originalWidth = self.rect.width

        # Disappearing

        self.drawing = True
        self.disappearingTimer = 0

    def changeSprite(self, index=None):
        if index is None:
            index = self.animationIndex

        self.pos = vec(self.pos.x, self.pos.y)
        self.image = self.animations['All'][index].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.pos.x, self.pos.y)

    # Disappears for 40 intervals

    def update(self):
        self.animationTimer += 1

        if not self.drawing:
            self.disappearingTimer += 1

            if self.disappearingTimer >= 40:
                self.drawing = True
                self.disappearingTimer = 0
                self.animationTimer = 0
                self.animationIndex = 8
        else:
            if self.animationIndex == 7:
                self.drawing = False

            if self.animationIndex >= len(self.animations['All']) - 1:
                self.animationIndex = 0

            self.changeSprite(self.animationIndex)
            self.pos.x = self.originalPos.x + self.originalWidth / 2 \
                - self.rect.width / 2

            if self.animationTimer >= 2:
                self.animationTimer = 0

                if self.animationIndex >= len(self.animations['All']) \
                    - 1:
                    self.animationIndex = 0
                else:
                    self.animationIndex += 1


# Walls are found below the ground
# Player can't go through these

class Wall(pg.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.animations = \
            {'All': [pg.image.load('Sprites/Environment/Wall.png')]}
        self.pos = vec(x, y)
        self.image = self.animations['All'][0].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)


# Ladders extend from above the ground to below the ground
# Player can climb these

class Ladder(pg.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.animations = \
            {'All': [pg.image.load('Sprites/Environment/EntireLadder.png'
             )]}
        self.pos = vec(x, y)
        self.image = self.animations['All'][0].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)


# Coins are found above and below the ground
# These are currency

class Coin(pg.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.animationTimer = 0
        self.animationIndex = 0
        self.animations = {'All': [
            pg.image.load('Sprites/Environment/Coin/1.png'),
            pg.image.load('Sprites/Environment/Coin/2.png'),
            pg.image.load('Sprites/Environment/Coin/3.png'),
            pg.image.load('Sprites/Environment/Coin/4.png'),
            pg.image.load('Sprites/Environment/Coin/5.png'),
            pg.image.load('Sprites/Environment/Coin/6.png'),
            pg.image.load('Sprites/Environment/Coin/7.png'),
            pg.image.load('Sprites/Environment/Coin/8.png'),
            ]}
        self.pos = vec(x, y)
        self.image = self.animations['All'][0].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)

    def changeSprite(self, index=None):
        if index is None:
            index = self.animationIndex

        self.image = self.animations['All'][index].convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.pos.x, self.pos.y)

    def update(self):
        self.animationIndex += 1

        if self.animationIndex >= len(self.animations['All']) - 1:
            self.animationIndex = 0

        self.changeSprite(self.animationIndex)

        if self.animationTimer >= 2:
            self.animationTimer = 0

            if self.animationIndex >= len(self.animations['All']) - 1:
                self.animationIndex = 0
            else:
                self.animationIndex += 1



			