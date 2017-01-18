from __future__ import unicode_literals, absolute_import
import re
import tempfile

from markdown.blockprocessors import BlockProcessor
from markdown.util import etree

from blockdiag import parser, builder, drawer


class BlockdiagProcessor(BlockProcessor):

    RE = re.compile('blockdiag\s+\{')

    def test(self, parent, block):
        return bool(self.RE.match(block))

    def run(self, parent, blocks):
        raw_block = blocks.pop(0)
        tree = parser.parse_string(raw_block)
        diagram = builder.ScreenNodeBuilder.build(tree)
        filename = tempfile.mkstemp('-diagram.png')[1]
        draw = drawer.DiagramDraw('png', diagram, filename=filename)
        draw.draw()
        draw.save()
        p = etree.SubElement(parent, 'p')
        img = etree.SubElement(p, 'img')
        img.attrib['src'] = filename

