#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Pitfall v1.0
By Danilo Lekovic for Game Design 12

game.py

Main execution file
"""

import pygame
from pygame.locals import *
from screen import *


class Game:

    # Initialize class

    def __init__(self):

        # Class variables

        self.FPS = 60
        self.width = 1080
        self.height = 720
        self.playing = True

        # Initialize sound system

        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.mixer.init(frequency=44100, size=-16, channels=1,
                          buffer=2 ** 12)

        # Pygame initialization

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Initialize screen manager for switching screens

        self.screenManager = ScreenManager()
        self.screenManager.set(MainMenu(self.screenManager))

    # Game loop

    def loop(self):
        for event in pygame.event.get():

            # Quit game

            if event.type is pygame.QUIT:
                self.playing = False

                # Save game

                self.screenManager.saveAll()

            # Handle screen events

            self.screenManager.get().keyDownEvent(event)
            self.screenManager.get().mouseClickEvent(event)

        # Run drawing function for screen

        self.screenManager.get().draw(self.screen)

        # Update screen

        pygame.display.update()
        self.clock.tick(self.FPS)

    # Handle quit

    def quit(self):
        pygame.quit()

    # Gets current screen

    def getScreen(self):
        return self.screen


game = Game()

while game.playing:
    game.loop()

game.quit()			