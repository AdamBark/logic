# This file is part of logic.

# logic is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# logic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with logic.  If not, see <http://www.gnu.org/licenses/>.

import os
import pyglet
from pyglet.window import key
from pyglet.gl import *


def main():
    pyglet.resource.path = ["data"]
    pyglet.resource.reindex()
    window = pyglet.window.Window(512, 512)
    gluOrtho2D(-0.25, 0.25, -0.25, 0.25)
    block = pyglet.resource.image("logic_block.png")
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    sprite = pyglet.sprite.Sprite(block, x=64, y=64)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    selector = pyglet.sprite.Sprite(
        pyglet.resource.image("selector.png"), x=0, y=0)
    grid = pyglet.resource.image("grid2.png")
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    @window.event
    def on_draw():
        window.clear()
        grid.blit(0, 0)
        sprite.draw()
        selector.draw()

    @window.event
    def on_key_press(symbol, modifier):
        if symbol == key.UP:
            selector.y = min(112, selector.y + 16)
        elif symbol == key.DOWN:
            selector.y = max(0, selector.y - 16)
        elif symbol == key.LEFT:
            selector.x = max(0, selector.x - 16)
        elif symbol == key.RIGHT:
            selector.x = min(112, selector.x + 16)
    pyglet.app.run()
