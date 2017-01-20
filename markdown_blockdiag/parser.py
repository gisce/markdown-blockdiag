from __future__ import unicode_literals, absolute_import
import re
import os

from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
from markdown_blockdiag.utils import random_filename

from blockdiag import parser, builder, drawer


class BlockdiagProcessor(BlockProcessor):

    RE = re.compile('blockdiag\s+\{')

    def __init__(self, parser, extension):
        super(BlockdiagProcessor, self).__init__(parser)
        self.extension = extension

    def test(self, parent, block):
        return bool(self.RE.match(block))

    def run(self, parent, blocks):
        diagram_dir = self.extension.getConfig('dir')
        if not diagram_dir:
            raise ValueError(
                'No directory is configured for markdown-blockdiag'
            )

        diagram_dir = os.path.join(
            diagram_dir,
            'diagrams'
        )

        if not os.path.exists(diagram_dir):
            os.makedirs(diagram_dir)

        raw_block = blocks.pop(0)
        tree = parser.parse_string(raw_block)
        diagram = builder.ScreenNodeBuilder.build(tree)
        filename = random_filename()
        draw_path = os.path.join(
            diagram_dir,
            filename
        )
        draw = drawer.DiagramDraw('png', diagram, filename=draw_path)
        draw.draw()
        draw.save()
        p = etree.SubElement(parent, 'p')
        img = etree.SubElement(p, 'img')
        img.attrib['src'] = '/diagrams/{}'.format(filename)
