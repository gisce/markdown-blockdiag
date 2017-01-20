from __future__ import absolute_import, unicode_literals

from blockdiag import parser, builder, drawer


def draw_blockdiag(content, filename=None):
    tree = parser.parse_string(content)
    diagram = builder.ScreenNodeBuilder.build(tree)

    draw = drawer.DiagramDraw('png', diagram, filename=filename)
    draw.draw()

    return draw.save()
