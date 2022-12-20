import numpy as np
import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from OpenGL.arrays import vbo
from OpenGL.GL import shaders

import UI.UICommon as UICommon

from ctypes import sizeof, c_float, c_void_p


class UIImage():
    def __init__(self, path="", x=0, y=UICommon.ScreenSize[1], xoffset=0, yoffset=0, align="left", valign="top", visible=True):
        self.path = path
        # origin in bottom left
        self.align, self.valign = align, valign
        self.x, self.y = x, y
        self.visible = visible
        self.image = pygame.image.load(path)
        # text color, bg color
        # Get width and height
        self.width, self.height = self.image.get_width(), self.image.get_height()

        if self.align == "left":
            self.x = 0 + xoffset
        elif self.align == "center":
            self.x = UICommon.ScreenSize[0]//2-self.width//2 + xoffset
        elif self.align == "right":
            self.x = UICommon.ScreenSize[0] - self.width + xoffset
        if self.valign == "top":
            self.y = UICommon.ScreenSize[1] - self.height + yoffset
        elif self.valign == "center":
            self.y = UICommon.ScreenSize[1]//2-self.height//2 + yoffset
        elif self.valign == "bottom":
            self.y = 0 + yoffset

        self.verts = np.float32(
            [-1, -1, 0, 0,  -1, 1, 0, 1,  1, 1, 1, 1,  -1, -1, 0, 0,  1, 1, 1, 1,  1, -1, 1, 0])

        VERTEX_SHADER = shaders.compileShader("""#version 330
            layout(location = 0) in vec2 pos;
            layout(location = 1) in vec2 uvIn;
            out vec2 uv;
            void main() {
                gl_Position = vec4(pos, 0, 1);
                uv = uvIn;
            }
            """, GL_VERTEX_SHADER)

        FRAGMENT_SHADER = shaders.compileShader("""#version 330
            out vec4 fragColor;
            in vec2 uv;
            uniform sampler2D tex;
            void main() {
                fragColor = texture(tex, uv);
            }
            """, GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(VERTEX_SHADER, FRAGMENT_SHADER)

    def _DrawImage(self):
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.verts, GL_DYNAMIC_DRAW)

        vertex_position_attribute_location = 0
        uv_attribute_location = 1

        glVertexAttribPointer(vertex_position_attribute_location,
                              2, GL_FLOAT, GL_FALSE, sizeof(c_float)*4, c_void_p(0))
        # vertex attributes need to be enabled
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(uv_attribute_location, 2, GL_FLOAT, GL_FALSE, sizeof(
            c_float)*4, c_void_p(sizeof(c_float)*2))
        glEnableVertexAttribArray(1)

        self.image_texture = glGenTextures(1)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.image_texture)

        self.image_data = pygame.image.tostring(self.image, "RGBA", True)

        # load data into the image
        mip_map_level = 0
        glTexImage2D(GL_TEXTURE_2D, mip_map_level, GL_RGBA, self.width,
                     self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.image_data)

        # set the filtering mode for the texture
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glUseProgram(self.shader)
        glDrawArrays(GL_TRIANGLES, 0, 6)

    def Update(self, deltaTime):
        pass

    def Render(self):

        glWindowPos2d(self.x, self.y)

        # print(self.x,self.y)
        if self.visible:
            # print("showing image")z

            glViewport(self.x, self.y, self.width, self.height)
            self._DrawImage()
            glViewport(0, 0, UICommon.ScreenSize[0], UICommon.ScreenSize[1])
