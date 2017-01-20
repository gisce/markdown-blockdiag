from __future__ import absolute_import, unicode_literals

import os
import tempfile

from blockdiag import parser, builder, drawer


def random_filename():
    return os.path.basename(tempfile.mkstemp('-diagram.png')[1])


def draw_blockdiag(content, filename=None):
    tree = parser.parse_string(content)
    diagram = builder.ScreenNodeBuilder.build(tree)

    draw = drawer.DiagramDraw('png', diagram, filename=filename)
    draw.draw()

    return draw.save()
