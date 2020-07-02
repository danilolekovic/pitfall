#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Pitfall v1.0
By Danilo Lekovic for Game Design 12

screen.py

Multi-screen system. Game file.
"""

import pygame
import random
from pygame.locals import *

# This in particular is why Python 3 is so great!
# perfect, seamless abstract classes!

from abc import ABC, abstractmethod

from player import Player
from entity import *
from filemanager import *
import os

# Using Pygame's built-in vector system
# for coordinates

vec = pygame.math.Vector2


# Screen manager dictates what screen we are in
# Also handles saving in case of crash

class ScreenManager:

    def __init__(self):
        self.currentScreen = None

    def set(self, screen):
        self.currentScreen = screen

    def get(self):
        return self.currentScreen

    # Saves game

    def saveAll(self):
        if isinstance(self.currentScreen, Play):
            FileManager.edit('Coins', FileManager.readOption('Coins')
                             + self.currentScreen.player.coins)
            FileManager.edit('2x Coins',
                             self.currentScreen.available2xCoins)
            FileManager.edit('4x Coins',
                             self.currentScreen.available4xCoins)
            FileManager.edit('Dead Zone',
                             self.currentScreen.availableDeadZone)
            FileManager.edit('Extra Life',
                             self.currentScreen.availableExtraLives)

            if self.currentScreen.highScore \
                < self.currentScreen.player.score:
                FileManager.edit('High Score',
                                 self.currentScreen.player.score)


# Screen abstract class
# All screens extend from this class
# This is why I used Python 3 Mr. Blake ;)
# It's a lot better this way

class Screen(ABC):

    def __init__(self, screenManager):
        self.screenManager = screenManager

    # Every screen needs to draw

    @abstractmethod
    def draw(game):
        pass

    # Every screen needs to handle keys

    @abstractmethod
    def keyDownEvent(event):
        pass

    # Every screen needs to handle mouse clicks
    # (Although never really used this)

    @abstractmethod
    def mouseClickEvent(event):
        pass


# Level elements are entities found in game

class LevelElement:

    def __init__(
        self,
        image,
        pos,
        type,
        index,
        ):
        self.image = image
        self.pos = pos
        self.type = type
        self.index = index


# Item elements are things you can purchase in stores

class ItemElement:

    def __init__(
        self,
        name,
        cost,
        image,
        ):
        self.name = name
        self.cost = cost
        self.image = image

    def getAmount(self):
        return FileManager.readOption(self.name)

    def getText(self, font, setAmount=None):
        if setAmount == None:
            amount = self.getAmount()
            return font.render(str(amount), True, (255, 255, 255))
        else:
            amount = setAmount
            return font.render(str(amount), True, (255, 255, 255))


# The store of the game
# Allows the player to buy many different
# power ups

class Store(Screen):

    def __init__(self, screenManager):
        super(Store, self).__init__(self)
        self.screenManager = screenManager
        self.background = \
            pygame.image.load('Sprites/Store/Background.png')
        self.greenButton = \
            pygame.image.load('Sprites/Store/GreenButton.png')
        self.greenPlacer = \
            pygame.image.load('Sprites/Store/NumberHolder.png')

        # Fonts

        self.font = pygame.font.Font(os.path.join('Pitfall.ttf'), 24)
        self.coins = FileManager.readOption('Coins')

        # Sound effects

        self.soundEnter = pygame.mixer.Sound('Sounds/boom.wav')
        self.soundWhoosh = pygame.mixer.Sound('Sounds/whoosh.wav')

        self.selects = 1

        # Money song psychologically convinces player to buy stuff
        # Pay-to-win system ;) $$$$???

        pygame.mixer.music.load('Sounds/money.wav')
        pygame.mixer.music.play(-1)

        # All items and their prices

        self.items = [ItemElement('2x Coins', 250,
                      pygame.image.load('Sprites/Store/2xCoins.png')),
                      ItemElement('4x Coins', 500,
                      pygame.image.load('Sprites/Store/4xCoins.png')),
                      ItemElement('Dead Zone', 100,
                      pygame.image.load('Sprites/Store/DeadZone.png')),
                      ItemElement('Extra Life', 100,
                      pygame.image.load('Sprites/Store/ExtraLife.png'))]

    def draw(self, screen):
        coinText = self.font.render(str(self.coins), True, (255, 255,
                                    255))

        screen.fill((0, 0, 0))
        screen.blit(self.background, (0, 0))
        screen.blit(coinText, (57, 657))

        # 3 currently visible items are added

        screen.blit(self.items[0].image, (15, 12))
        screen.blit(self.greenPlacer, (15, 142))
        text0 = self.items[0].getText(self.font)
        screen.blit(text0, (15 + 60 / 2 - text0.get_width() / 2, 142
                    + 61 / 2 - text0.get_height() / 2))

        screen.blit(self.items[1].image, (15, 216))
        screen.blit(self.greenPlacer, (15, 346))
        text1 = self.items[1].getText(self.font)
        screen.blit(text1, (15 + 60 / 2 - text1.get_width() / 2, 346
                    + 61 / 2 - text1.get_height() / 2))

        screen.blit(self.items[2].image, (15, 420))
        screen.blit(self.greenPlacer, (15, 550))
        text2 = self.items[2].getText(self.font)
        screen.blit(text2, (15 + 60 / 2 - text2.get_width() / 2, 550
                    + 61 / 2 - text2.get_height() / 2))

        # Buy buttom rotates through selected item

        if self.selects == 1:
            screen.blit(self.greenButton, (469, 41))
        elif self.selects == 2:
            screen.blit(self.greenButton, (469, 245))
        else:
            screen.blit(self.greenButton, (469, 449))

    def keyDownEvent(self, event):

        # Items go down, list gets popped
        # Bottom item goes to the top of the list

        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.selects += 1
            self.soundWhoosh.play()

            if self.selects == 4:
                first = self.items.pop(0)
                self.items.append(first)
                self.selects = 3
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:

        # Items go up
        # Top item goes to the bottom of the list

            self.selects -= 1
            self.soundWhoosh.play()

            if self.selects == 0:
                last = self.items[3]
                self.items = self.items[:-1]
                self.items.insert(0, last)
                self.selects = 1
        elif event.type == pygame.KEYUP and event.key == pygame.K_e:

        # Go back to the main menu

            self.soundEnter.play()
            self.screenManager.set(MainMenu(self.screenManager))
        elif event.type == pygame.KEYDOWN and event.key \
            == pygame.K_RETURN:

        # Buy an item

            self.soundEnter.play()
            if self.coins - self.items[self.selects - 1].cost >= 0:
                self.coins = self.coins - self.items[self.selects
                        - 1].cost
                self.items[self.selects - 1]

                # Coins is saved

                FileManager.edit('Coins', self.coins)
                FileManager.edit(self.items[self.selects - 1].name,
                                 self.items[self.selects
                                 - 1].getAmount() + 1)

    def mouseClickEvent(self, event):
        pass


# This screen appears when you lose

class Lose(Screen):

    def __init__(
        self,
        screenManager,
        score,
        highScore,
        totalCoins,
        coins,
        ):
        super(Lose, self).__init__(self)
        self.screenManager = screenManager
        self.background = pygame.image.load('Sprites/LoseMenu.png')
        self.font = pygame.font.Font(os.path.join('Pitfall.ttf'), 24)
        self.text = self.font.render('Score: {}'.format(score), True,
                (255, 255, 255))
        self.text0 = \
            self.font.render('High Score: {}'.format(highScore), True,
                             (255, 255, 255))
        self.text1 = \
            self.font.render('Coins: {} +{}'.format(totalCoins, coins),
                             True, (255, 255, 255))
        self.soundEnter = pygame.mixer.Sound('Sounds/boom.wav')

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.background, (0, 0))

        # Center all text

        screen.blit(self.text, (1080 / 2 - self.text.get_width() / 2,
                    35))
        screen.blit(self.text0, (1080 / 2 - self.text0.get_width() / 2,
                    67))
        screen.blit(self.text1, (1080 / 2 - self.text1.get_width() / 2,
                    98))

    def keyDownEvent(self, event):
        if event.type == pygame.KEYUP and event.key == pygame.K_m:
            self.screenManager.set(MainMenu(self.screenManager))
            self.soundEnter.play()
        if event.type == pygame.KEYUP and event.key == pygame.K_s:
            self.screenManager.set(Store(self.screenManager))
            self.soundEnter.play()
        elif event.type == pygame.KEYUP and event.key == pygame.K_p:
            self.screenManager.set(Play(self.screenManager))
            self.soundEnter.play()

    def mouseClickEvent(self, event):
        pass


# Game screen

class Play(Screen):

    def __init__(self, screenManager):
        super(Play, self).__init__(self)
        self.screenManager = screenManager
        self.player = Player(60, 400)
        self.backgroundGame = pygame.image.load('Sprites/Background.png')
        self.spriteFloor = \
            pygame.image.load('Sprites/Environment/Floor.png')
        self.coin = pygame.image.load('Sprites/Environment/Coin/1.png')
        self.qKey = pygame.image.load('Sprites/Environment/QKey.png')
        self.eKey = pygame.image.load('Sprites/Environment/EKey.png')
        self.enterKey = \
            pygame.image.load('Sprites/Environment/EnterKey.png')
        self.healthBar = [
            pygame.image.load('Sprites/Player/Health/1.png'),
            pygame.image.load('Sprites/Player/Health/2.png'),
            pygame.image.load('Sprites/Player/Health/3.png'),
            pygame.image.load('Sprites/Player/Health/4.png'),
            pygame.image.load('Sprites/Player/Health/5.png'),
            pygame.image.load('Sprites/Player/Health/6.png'),
            ]
        self.greenPlacer = \
            pygame.image.load('Sprites/Store/Icons/IconPlacer.png')

        # Dictates what elements will be in the level (this is all changed below)

        self.possiblePits = 1
        self.possibleLadders = 1
        self.possibleWalls = 1
        self.possibleBarrels = 2
        self.possibleCoins = 3
        self.possibleCoinsUnderground = 2
        self.possibleGhosts = 0
        self.possibleRats = 1
        self.possibleSnakes = 1

        # Sound effects

        self.soundCoin = pygame.mixer.Sound('Sounds/coin.wav')
        self.soundDead = pygame.mixer.Sound('Sounds/dead.wav')
        self.soundPowerUp = pygame.mixer.Sound('Sounds/power.wav')
        self.soundJump = pygame.mixer.Sound('Sounds/jump.wav')
        self.soundDamage = pygame.mixer.Sound('Sounds/damage.wav')
        self.soundWhoosh = pygame.mixer.Sound('Sounds/whoosh.wav')

        # Coins / scores

        self.currentCoins = FileManager.readOption('Coins')
        self.coinAppend = 10
        self.highScore = FileManager.readOption('High Score')

        # Power-ups

        self.available2xCoins = FileManager.readOption('2x Coins')
        self.available4xCoins = FileManager.readOption('4x Coins')
        self.availableExtraLives = FileManager.readOption('Extra Life')
        self.availableDeadZone = FileManager.readOption('Dead Zone')
        self.noMoreLives = False

        self.icon2XCoins = \
            pygame.image.load('Sprites/Store/Icons/2xCoins.png')
        self.icon4XCoins = \
            pygame.image.load('Sprites/Store/Icons/4xCoins.png')
        self.iconExtralife = \
            pygame.image.load('Sprites/Store/Icons/ExtraLife.png')
        self.iconDeadZone = \
            pygame.image.load('Sprites/Store/Icons/DeadZone.png')

        self.powerIndex = 0
        self.powerIcons = [self.icon2XCoins, self.icon4XCoins,
                           self.iconExtralife, self.iconDeadZone]
        self.usedPowerups = []

        # Fonts

        self.font = pygame.font.Font(os.path.join('Pitfall.ttf'), 24)
        self.sFont = pygame.font.Font(os.path.join('Pitfall.ttf'), 16)

        # Snow feature! Very cool, thank you!

        self.snowing = False
        self.listSnow = []

        if self.snowing:
            for i in range(100):
                x = random.randrange(0, 1080)
                y = random.randrange(0, 720)
                self.listSnow.append([x, y])

        # Creates level randomly

        self.level = []
        self.createLevel()

        # Plays background music, this is A+ material

        pygame.mixer.music.load('Sounds/background.wav')
        pygame.mixer.music.play(-1)

    # Creates level
    # 4 different kinds of levels to add some variety

    def createLevel(self):
        kindOfLevel = random.randrange(1, 4)

        if kindOfLevel is 1:
            self.possibleLadders = 1
            self.possiblePits = 0
            self.possibleWalls = 1
            self.possibleBarrels = 0
            self.possibleSnakes = 0
            self.possibleRats = 3
            self.possibleGhosts = 0
        elif kindOfLevel is 2:
            self.possibleLadders = 1
            self.possiblePits = 0
            self.possibleWalls = 1
            self.possibleBarrels = 2
            self.possibleSnakes = 0
            self.possibleRats = 0
            self.possibleGhosts = 2
        elif kindOfLevel is 3:
            self.possibleLadders = 0
            self.possiblePits = 0
            self.possibleWalls = 1
            self.possibleBarrels = 1
            self.possibleSnakes = 2
            self.possibleRats = 0
            self.possibleGhosts = 0
        elif kindOfLevel is 4:
            self.possibleLadders = 0
            self.possiblePits = 1
            self.possibleWalls = 0
            self.possibleBarrels = 0
            self.possibleSnakes = 0
            self.possibleRats = 5
            self.possibleGhosts = 0

        # Eliminates all animals using Dead Zone powerup

        if 3 in self.usedPowerups:
            self.possibleSnakes = 0
            self.possibleRats = 0
            self.possibleGhosts = 0

        # Every for loop here works the same:
        #   - Loops through number to generate
        #   - Creates random X coordinate
        #   - Checks if anything is touching this previously
        #   - If it is, create new coordinate. repeat
        #   - If not, add to level

        # pit y has to be 485

        for i in range(self.possiblePits):
            pitX = random.randint(140, 555)
            pit = Pit(pitX, 485)

            for t in self.level:
                while pit.rect.colliderect(t.rect):
                    pitX = random.randint(140, 555)
                    pit = Pit(pitX, 485)

            self.level.append(pit)

        # ladder y has to be 492

        for i in range(self.possibleLadders):
            holeX = random.randint(140, 1010)
            ladder = Ladder(holeX, 492)

            for t in self.level:
                while ladder.rect.colliderect(t.rect):
                    holeX = random.randint(140, 1010)
                    ladder = Ladder(holeX, 492)

            self.level.append(ladder)

        # barrel y has to be 474

        for i in range(self.possibleBarrels):
            barrelX = random.randint(340, 1010)
            barrel = Barrel(barrelX, 474)

            for t in self.level:
                while barrel.rect.colliderect(t.rect):
                    barrelX = random.randint(140, 1010)
                    barrel = Barrel(barrelX, 474)

            self.level.append(barrel)

        # wall y has to be 584

        for i in range(self.possibleWalls):
            wallX = random.randint(140, 1010)
            wall = Wall(wallX, 584)

            for t in self.level:
                while wall.rect.colliderect(t.rect):
                    wallX = random.randint(140, 1010)
                    wall = Wall(wallX, 584)

            self.level.append(wall)

        # coin y has to be 483

        for i in range(self.possibleCoins):
            coinX = random.randint(140, 1010)
            coin = Coin(coinX, 483)

            for t in self.level:
                while coin.rect.colliderect(t.rect):
                    coinX = random.randint(140, 1010)
                    coin = Coin(coinX, 483)

            self.level.append(coin)

        # underground coin y has to be 670

        for i in range(self.possibleCoinsUnderground):
            coinX = random.randint(140, 1010)
            coin = Coin(coinX, 670)

            for t in self.level:
                while coin.rect.colliderect(t.rect):
                    coinX = random.randint(140, 1010)
                    coin = Coin(coinX, 670)

            self.level.append(coin)

        # ghost y has to be 605

        for i in range(self.possibleGhosts):
            ghostX = random.randint(140, 1010)
            ghost = Ghost(ghostX, 605)

            for t in self.level:
                while ghost.rect.colliderect(t.rect):
                    ghostX = random.randint(140, 1010)
                    ghost = Ghost(ghostX, 605)

            self.level.append(ghost)

        # rat y has to be 679

        for i in range(self.possibleRats):
            ratX = random.randint(140, 1010)
            rat = Rat(ratX, 679)

            for t in self.level:
                while rat.rect.colliderect(t.rect):
                    ratX = random.randint(140, 1010)
                    rat = Rat(ratX, 679)

            self.level.append(rat)

        # snake y has to be 466

        for i in range(self.possibleSnakes):
            snakeX = random.randint(140, 1010)
            snake = Snake(snakeX, 466)

            for t in self.level:
                while snake.rect.colliderect(t.rect):
                    snakeX = random.randint(140, 1010)
                    snake = Snake(snakeX, 466)

            self.level.append(snake)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.backgroundGame, (0, 0))
        screen.blit(self.spriteFloor, (0, 474))
        screen.blit(self.coin, (60, 90))
        coinText = self.font.render(str(self.currentCoins
                                    + self.player.coins), True, (255,
                                    255, 255))
        screen.blit(coinText, (104, 90))
        screen.blit(self.qKey, (280, 46))
        screen.blit(self.eKey, (377, 46))

        screen.blit(self.powerIcons[self.powerIndex], (323, 37))
        screen.blit(self.greenPlacer, (350, 65))

        # Draws the power up switcher
        # Shows '!' if powerup is in use
        # Also shows number of powerups

        if self.powerIndex == 0:
            text0 = self.sFont.render(str(self.available2xCoins), True,
                    (255, 255, 255))

            if self.powerIndex in self.usedPowerups:
                text0 = self.sFont.render('!', True, (255, 255, 255))

            screen.blit(text0, (350 + 24 / 2 - text0.get_width() / 2,
                        65 + 24 / 2 - text0.get_height() / 2))
        elif self.powerIndex == 1:
            text0 = self.sFont.render(str(self.available4xCoins), True,
                    (255, 255, 255))

            if self.powerIndex in self.usedPowerups:
                text0 = self.sFont.render('!', True, (255, 255, 255))

            screen.blit(text0, (350 + 24 / 2 - text0.get_width() / 2,
                        65 + 24 / 2 - text0.get_height() / 2))
        elif self.powerIndex == 2:
            text0 = self.sFont.render(str(self.availableExtraLives),
                    True, (255, 255, 255))

            if self.powerIndex in self.usedPowerups:
                text0 = self.sFont.render('!', True, (255, 255, 255))

            screen.blit(text0, (350 + 24 / 2 - text0.get_width() / 2,
                        65 + 24 / 2 - text0.get_height() / 2))
        elif self.powerIndex == 3:
            text0 = self.sFont.render(str(self.availableDeadZone),
                    True, (255, 255, 255))

            if self.powerIndex in self.usedPowerups:
                text0 = self.sFont.render('!', True, (255, 255, 255))

            screen.blit(text0, (350 + 24 / 2 - text0.get_width() / 2,
                        65 + 24 / 2 - text0.get_height() / 2))

        # Handles collision for every element in game

        for element in self.level:
            if isinstance(element, Coin):
                element.update()
                screen.blit(element.image, (element.pos.x,
                            element.pos.y))

                if element.rect.colliderect(self.player.rect):
                    self.level.remove(element)
                    self.player.coins += self.coinAppend
                    self.soundCoin.play()
            elif isinstance(element, Barrel) or isinstance(element,
                    Ghost) or isinstance(element, Snake) \
                or isinstance(element, Rat):

                element.update()
                screen.blit(element.image, (element.pos.x,
                            element.pos.y))

                if element.rect.colliderect(self.player.rect):
                    self.level.remove(element)
                    self.player.health -= 1
                    self.soundDamage.play()
            elif isinstance(element, Pit):
                element.update()

                if element.drawing:
                    screen.blit(element.image, (element.pos.x,
                                element.pos.y))

                    if element.rect.colliderect(self.player.rect):
                        self.player.health = 1
                        self.soundDamage.play()
            else:
                screen.blit(element.image, (element.pos.x,
                            element.pos.y))

            continue

        # Creates next stage when player reaches end

        if self.player.pos.x >= 1060:
            self.player.pos.x = 0
            self.level = []
            self.createLevel()
            self.player.score += 100

        # Updates animation

        self.player.animationTimer += 1

        # This 4-branch conditional statement works like this:
        #   - Checks player state
        #   - Draws depending on the state and handles all
        #     major changes the player is having

        if self.player.currentState is self.player.STANCE:
            self.player.stop()
            self.player.doubled = False

            if self.player.animationIndex \
                >= len(self.player.animations['Idle']) - 1:
                self.player.animationIndex = 0

            self.player.changeSprite('Idle')
            self.player.draw(screen, (self.player.pos.x,
                             self.player.pos.y))

            if self.player.animationTimer >= 2:
                self.player.animationTimer = 0

                if self.player.animationIndex \
                    >= len(self.player.animations['Idle']) - 1:
                    self.player.animationIndex = 0
                    self.player.backwardsAnimation = True
                else:
                    self.player.animationIndex = \
                        self.player.animationIndex + 1
        elif self.player.currentState is self.player.RUNNING:
            if self.player.animationIndex \
                >= len(self.player.animations['Running']) - 1:
                self.player.animationIndex = 0

            self.player.doubled = False

            canMoveRight = True
            canMoveLeft = True

            for element in self.level:
                if isinstance(element, Wall):
                    if element.rect.colliderect(self.player.rect):
                        if element.pos.x < self.player.pos.x:
                            canMoveLeft = False
                            canMoveRight = True
                        elif element.pos.x > self.player.pos.x:
                            canMoveRight = False
                            canMoveLeft = True
                    break

            if self.player.orientation is self.player.RIGHT:
                if canMoveRight:
                    self.player.right()
                else:
                    self.player.stop()
            else:
                if canMoveLeft:
                    self.player.left()
                else:
                    self.player.stop()

            self.player.changeSprite('Running')
            self.player.draw(screen, (self.player.pos.x,
                             self.player.pos.y))

            if self.player.animationTimer >= 0:
                self.player.animationTimer = 0

                if self.player.animationIndex \
                    >= len(self.player.animations['Running']) - 1:
                    self.player.animationIndex = 0
                else:
                    self.player.animationIndex += 1
        elif self.player.currentState is self.player.CLIMBING:
            if self.player.animationIndex \
                >= len(self.player.animations['Climbing']) - 1:
                self.player.animationIndex = 0

            self.player.doubled = False

            self.player.changeSprite('Climbing')
            self.player.draw(screen, (self.player.pos.x,
                             self.player.pos.y))

            self.player.pos.y -= 17

            if self.player.pos.y <= 400:
                self.player.currentState = self.player.STANCE

            if self.player.animationTimer >= 1:
                self.player.animationTimer = 0

                if self.player.animationIndex \
                    >= len(self.player.animations['Climbing']) - 1:
                    self.player.animationIndex = 0
                else:
                    self.player.animationIndex += 1
        elif self.player.currentState is self.player.JUMPING:
            if self.player.animationIndex \
                >= len(self.player.animations['Jumping']) - 1:
                self.player.animationIndex = 0

            self.player.changeSprite('Jumping')
            self.player.draw(screen, (self.player.pos.x,
                             self.player.pos.y))

            if self.player.animationTimer >= 1:
                self.player.animationTimer = 0

                if self.player.animationIndex \
                    >= len(self.player.animations['Jumping']) - 1:
                    self.player.animationIndex = 0
                else:
                    self.player.animationIndex += 1

        # Updates player positions and sprites

        self.player.update()

        # Snow feature!

        if self.snowing:
            for i in range(len(self.listSnow)):
                pygame.draw.circle(screen, (255, 255, 255),
                                   self.listSnow[i], 2)

                self.listSnow[i][1] += 1

                if self.listSnow[i][1] > 500:
                    y = random.randrange(-50, -10)
                    self.listSnow[i][1] = y
                    x = random.randrange(0, 1080)
                    self.listSnow[i][0] = x

        # Handles player health and changes health bar
        # Also handles Extra Life powerup

        if self.player.health is 6:
            screen.blit(self.healthBar[0], (28, 28))
        elif self.player.health is 5:
            screen.blit(self.healthBar[1], (28, 28))
        elif self.player.health is 4:
            screen.blit(self.healthBar[2], (28, 28))
        elif self.player.health is 3:
            screen.blit(self.healthBar[3], (28, 28))
        elif self.player.health is 2:
            screen.blit(self.healthBar[4], (28, 28))
        elif self.player.health is 1 and 2 not in self.usedPowerups:

            # Handles death
            # Loads sad music and final info

            screen.blit(self.healthBar[5], (28, 28))
            self.soundDead.play()
            totalCoins = FileManager.readOption('Coins') \
                + self.player.coins
            self.screenManager.set(Lose(self.screenManager,
                                   self.player.score, self.highScore,
                                   totalCoins, self.player.coins))
            pygame.mixer.music.stop()
            pygame.mixer.music.load('Sounds/sadness.wav')
            pygame.mixer.music.play(0)
            FileManager.edit('Coins', totalCoins)
            FileManager.edit('2x Coins', self.available2xCoins)
            FileManager.edit('4x Coins', self.available4xCoins)
            FileManager.edit('Dead Zone', self.availableDeadZone)
            FileManager.edit('Extra Life', self.availableExtraLives)

            if self.highScore < self.player.score:
                FileManager.edit('High Score', self.player.score)
        elif self.player.health is 1 and 2 in self.usedPowerups and not noMoreLives:
            self.player.pos.x = 60
            self.player.health = 6
            self.noMoreLives = True
            if self.availableExtraLives > 0:
                self.availableExtraLives -= 1

        # Current score and high score

        text = self.font.render(str(self.player.score), True, (255,
                                255, 255))
        screen.blit(text, (1000 - text.get_width(), 28))

        HStext = self.font.render(str(self.highScore), True, (255, 213,
                                  0))
        screen.blit(HStext, (1000 - HStext.get_width(), 58))

    # Handles movement

    def keyDownEvent(self, event):

        # This area of code works the same:
        #   - Check KEYDOWN/KEYUP
        #   - Switch player state and orientation

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.player.currentState = self.player.RUNNING
            self.player.orientation = self.player.RIGHT
        elif event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            self.player.currentState = self.player.STANCE
        elif event.type == pygame.KEYDOWN and event.key \
            == pygame.K_LEFT:
            self.player.currentState = self.player.RUNNING
            self.player.orientation = self.player.LEFT
        elif event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            self.player.currentState = self.player.STANCE
        elif event.type == pygame.KEYDOWN and event.key \
            == pygame.K_SPACE:
            if self.player.currentState == self.player.JUMPING:
                if not self.player.doubled:
                    self.player.doubled = True
                    self.player.jump()
            else:
                self.player.currentState = self.player.JUMPING
                self.player.jump()
                self.soundJump.play()
        elif event.type == pygame.KEYDOWN and event.key \
            == pygame.K_DOWN:
            for element in self.level:
                if isinstance(element, Ladder):
                    if element.rect.colliderect(self.player.rect):
                        self.player.currentState = self.player.CLIMBING
                        self.player.fall()
                    break
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            for element in self.level:
                if isinstance(element, Ladder):
                    if element.rect.colliderect(self.player.rect):
                        self.player.currentState = self.player.CLIMBING
                        self.player.rise()
                    break
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            if self.powerIndex == 0:
                self.powerIndex = len(self.powerIcons) - 1
            else:
                self.powerIndex -= 1

            self.soundWhoosh.play()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            if self.powerIndex == len(self.powerIcons) - 1:
                self.powerIndex = 0
            else:
                self.powerIndex += 1

            self.soundWhoosh.play()
        elif event.type == pygame.KEYDOWN and event.key \
            == pygame.K_RETURN:

        # Handles powerups being used

            if self.powerIndex not in self.usedPowerups:
                if self.powerIndex == 0 and self.available2xCoins > 0:
                    self.usedPowerups.append(self.powerIndex)
                    self.soundPowerUp.play()
                    self.coinAppend = self.coinAppend * 2
                    self.available2xCoins -= 1
                elif self.powerIndex == 1 and self.available4xCoins > 0:
                    self.usedPowerups.append(self.powerIndex)
                    self.soundPowerUp.play()
                    self.coinAppend = self.coinAppend * 4
                    self.available4xCoins -= 1
                elif self.powerIndex == 2 and self.availableExtraLives \
                    > 0:
                    self.usedPowerups.append(self.powerIndex)
                    self.soundPowerUp.play()
                    self.availableExtraLives -= 1
                elif self.powerIndex == 3 and self.availableDeadZone \
                    > 0:
                    self.usedPowerups.append(self.powerIndex)
                    self.soundPowerUp.play()
                    self.availableDeadZone -= 1

                    # Eliminates all animals

                    for element in self.level:
                        if isinstance(element, Ghost) \
                            or isinstance(element, Snake) \
                            or isinstance(element, Rat):
                            self.level.remove(element)

    def mouseClickEvent(self, event):
        pass


# Main menu!

class MainMenu(Screen):

    def __init__(self, screenManager):
        super(MainMenu, self).__init__(self)
        self.screenManager = screenManager
        self.backgroundMenu = pygame.image.load('Sprites/Menu.png')
        self.buttonPlay = pygame.image.load('Sprites/Menu/Play.png')
        self.buttonPlaySelected = \
            pygame.image.load('Sprites/Menu/Play-Selected.png')
        self.buttonStore = pygame.image.load('Sprites/Menu/Store.png')
        self.buttonStoreSelected = \
            pygame.image.load('Sprites/Menu/Store-Selected.png')
        self.buttonQuit = pygame.image.load('Sprites/Menu/Quit.png')
        self.buttonQuitSelected = \
            pygame.image.load('Sprites/Menu/Quit-Selected.png')
        self.soundEnter = pygame.mixer.Sound('Sounds/boom.wav')
        self.soundWhoosh = pygame.mixer.Sound('Sounds/whoosh.wav')
        self.selectedIndex = 1

        # ENTER SANDMAN!
        # An A is deserved for this

        pygame.mixer.music.load('Sounds/metallica.wav')
        pygame.mixer.music.play(-1)

    # Buttons are drawn based on selection

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.backgroundMenu, (0, 0))
        screen.blit(self.buttonPlay, (467, 417))
        screen.blit(self.buttonStore, (452, 499))
        screen.blit(self.buttonQuit, (466, 576))

        if self.selectedIndex is 1:
            screen.blit(self.buttonPlaySelected, (467, 417))
        elif self.selectedIndex is 2:
            screen.blit(self.buttonStoreSelected, (452, 499))
        elif self.selectedIndex is 3:
            screen.blit(self.buttonQuitSelected, (466, 576))

    # Buttons rotate and are selected and handled

    def keyDownEvent(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.soundWhoosh.play()
            if self.selectedIndex is 3:
                self.selectedIndex = 1
            else:
                self.selectedIndex += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.soundWhoosh.play()
            if self.selectedIndex is 1:
                self.selectedIndex = 3
            else:
                self.selectedIndex -= 1
        elif event.type == pygame.KEYDOWN and event.key \
            == pygame.K_RETURN:
            pygame.mixer.music.stop()

            self.soundEnter.play()
            if self.selectedIndex is 1:
                self.screenManager.set(Play(self.screenManager))
            elif self.selectedIndex is 2:
                self.screenManager.set(Store(self.screenManager))
            elif self.selectedIndex is 3:
                pygame.quit()

    def mouseClickEvent(self, event):
        pass