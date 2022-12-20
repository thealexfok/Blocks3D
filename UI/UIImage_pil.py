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
        self.visible = visible
        self.image = Image.open(path)
        # text color, bg color
        self.imageData = np.array(list(self.image.getdata()))
        self.imageID = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glBindTexture(GL_TEXTURE_2D, self.imageID)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                     self.image.size[0], self.image.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, self.imageData)
        self.image.close()
        # Get width and height

    def Update(self, deltaTime):
        pass

    def Render(self):

        glWindowPos2d(self.x, self.y)

        # print(self.x,self.y)
        if self.visible:
            verts = ((1, 1), (1, -1), (-1, -1), (-1, 1))
            texts = ((1, 0), (1, 1), (0, 1), (0, 0))
            surf = (0, 1, 2, 3)

            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.imageID)

            glBegin(GL_QUADS)
            for i in surf:
                glTexCoord2f(texts[i][0], texts[i][1])
                glVertex2f(self.x + verts[i][0], self.y + verts[i][1])
            glEnd()

            glDisable(GL_TEXTURE_2D)
