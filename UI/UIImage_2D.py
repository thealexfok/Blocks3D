import numpy as np
import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from OpenGL.arrays import vbo
from OpenGL.GL import shaders

import UI.UICommon as UICommon


class UIImage():
    def __init__(self, path="", x=0, y=UICommon.ScreenSize[1], xoffset=0, yoffset=0, align="left", valign="top", visible=True):
        self.path = path
        # origin in bottom left
        self.align, self.valign = align, valign
        self.x, self.y = x, y
        self.xoffset, self.yoffset = xoffset, yoffset
        self.visible = visible
        self.surf = pygame.image.load(path)
        self.width, self.height = self.surf.get_width(), self.surf.get_height()
        self.surf = pygame.transform.scale(
            self.surf, (self.width, self.height))
        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))
        self._CalcRect()

    def _CalcRect(self):
        self.rect.left = self.x
        if self.align == "right":
            self.rect.left -= self.width
        elif self.align == "center":
            self.rect.left -= self.width // 2

        self.rect.top = self.y
        if self.valign == "bottom":
            self.rect.top -= self.height
        elif self.valign == "center":
            self.rect.top -= self.height // 2

        self.rect.width = self.width
        self.rect.height = self.height

    def ProcessEvent(self, event):
        return False

    def Update(self, deltaTime):
        pass

    def Render(self, screen):
        if self.visible and self.surf != None:
            print(self.surf)
            print(self.rect)
            screen.blit(self.surf, self.rect)
            print("rendered")
