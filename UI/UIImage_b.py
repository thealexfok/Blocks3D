import numpy as np
import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from OpenGL.arrays import vbo
from OpenGL.GL import shaders

import UI.UICommon as UICommon
from PIL import Image


class UIImage():
    def __init__(self, path="", x=0, y=UICommon.ScreenSize[1], xoffset=0, yoffset=0, align="left", valign="top", visible=True):
        self.path = path
        # origin in bottom left
        self.align, self.valign = align, valign
        self.x, self.y = x, y
        self.xoffset, self.yoffset = xoffset, yoffset
        self.visible = visible
        self.image = pygame.image.load(path)
        self.width, self.height = self.image.get_width(), self.image.get_height()

        # self.image = Image.open(path)
        # text color, bg color
        # self.imageData = np.array(list(self.image.getdata()), np.int8)
        self.imageData = pygame.image.tostring(self.image, "RGBA", 1)
        self.imageID = glGenTextures(1)
        # glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        # glBindTexture(GL_TEXTURE_2D, self.imageID)
        # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        # glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width,
                     self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.imageData)

        # self.image.close()
        # Get width and height

    def Update(self, deltaTime):
        pass

    def Render(self, screen):
        if self.align == "left":
            self.x = 0 + self.xoffset
        elif self.align == "center":
            self.x = UICommon.ScreenSize[0]//2-self.width//2 + self.xoffset
        elif self.align == "right":
            self.x = UICommon.ScreenSize[0] - self.width + self.xoffset
        if self.valign == "top":
            self.y = UICommon.ScreenSize[1] - self.height + self.yoffset
        elif self.valign == "center":
            self.y = UICommon.ScreenSize[1]//2-self.height//2 + self.yoffset
        elif self.valign == "bottom":
            self.y = 0 + self.yoffset

        glWindowPos2d(self.x, self.y)
        # glRasterPos3d(self.x,self.y,self.x)
        # print(self.x,self.y)
        if self.visible:
            #
            # glTranslate(*self.pos)
            # self._DrawBlock()
            # glLoadMatrixf(m)
            glEnable(GL_TEXTURE_2D)

            glBegin(GL_QUADS)
            glTexCoord2f(0, 0)
            glVertex3f(-4, -4, 0)
            glTexCoord2f(0, 1)
            glVertex3f(-4, 4, 0)
            glTexCoord2f(1, 1)
            glVertex3f(4, 4, 0)
            glTexCoord2f(1, 0)
            glVertex3f(4, -4, 0)
            glEnd()
            glDisable(GL_TEXTURE_2D)
