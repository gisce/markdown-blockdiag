from __future__ import unicode_literals, absolute_import
import re
import base64

from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
from markdown_blockdiag.utils import draw_blockdiag, DIAG_MODULES


class BlockdiagProcessor(BlockProcessor):

    RE = re.compile(r"""
        ^
        (?P<diagtype>{})
        \s+
        \{{
    """.format("|".join(DIAG_MODULES.keys())), re.VERBOSE)

    def __init__(self, parser, extension):
        super(BlockdiagProcessor, self).__init__(parser)
        self.extension = extension

    def test(self, parent, block):
        return bool(self.RE.match(block))

    def run(self, parent, blocks):
        diag_blocks = []

        for block in blocks:
            block = block.strip()
            diag_blocks.append(block)
            if block.endswith("}"):
                break

        raw_block = "\n".join(diag_blocks)
        del blocks[:len(diag_blocks)]

        font_path = self.extension.getConfig('fontpath')
        output_fmt = self.extension.getConfig('format')
        diagram = draw_blockdiag(raw_block, output_fmt=output_fmt, font_path=font_path)
        if output_fmt == 'png':
            src_data = 'data:image/png;base64,{0}'.format(
                base64.b64encode(diagram)
            )
        else:
            src_data = 'data:image/svg+xml;utf8,{0}'.format(diagram)

        p = etree.SubElement(parent, 'p')
        img = etree.SubElement(p, 'img')
        img.attrib['src'] = src_data
