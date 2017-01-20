from __future__ import unicode_literals, absolute_import
import re
import os

from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
from markdown_blockdiag.utils import draw_blockdiag, random_filename


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

        filename = random_filename()

        draw_path = os.path.join(
            diagram_dir,
            filename
        )

        raw_block = blocks.pop(0)
        diagram = draw_blockdiag(raw_block, draw_path)

        p = etree.SubElement(parent, 'p')
        img = etree.SubElement(p, 'img')
        img.attrib['src'] = '/diagrams/{}'.format(filename)
