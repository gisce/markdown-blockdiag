from __future__ import absolute_import, unicode_literals

from blockdiag import parser, builder, drawer
from blockdiag.utils.fontmap import FontMap


def draw_blockdiag(content, filename=None, font_path=None):
    tree = parser.parse_string(content)
    diagram = builder.ScreenNodeBuilder.build(tree)

    fontmap = FontMap()

    if font_path:
        fontmap.set_default_font(font_path)

    draw = drawer.DiagramDraw(
        'png', diagram, filename=filename, antialias=True, fontmap=fontmap
    )
    draw.draw()

    return draw.save()
