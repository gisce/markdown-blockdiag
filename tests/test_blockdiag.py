# encoding=utf-8
from __future__ import unicode_literals

import unittest
import base64
from xml.sax.saxutils import unescape

from markdown import markdown
from markdown_blockdiag.parser import BlockdiagProcessor
from markdown_blockdiag.utils import draw_blockdiag


def join_text(lines):
    return '\n'.join(lines)


TEST_DIAG_TXT = join_text([
    "blockdiag {",
    "    A -> B -> C;",
    "}"
])


class BlockdiagTest(unittest.TestCase):
    """Testing blockdiag extension
    """

    def test_run(self):
        self.assertTrue(BlockdiagProcessor.RE.match(TEST_DIAG_TXT))

    def test_basic_blockdiag(self):
        draw = draw_blockdiag(TEST_DIAG_TXT)

        expected = '<p><img src="data:image/png;base64,{0}" /></p>'.format(
            base64.b64encode(draw)
        )
        result = markdown(
            TEST_DIAG_TXT,
            extensions=['markdown_blockdiag'],
        )

        self.assertEqual(expected, result)

    def test_svg_blockdiag(self):
        self.maxDiff = None
        draw = draw_blockdiag(TEST_DIAG_TXT, output_fmt='svg')

        expected = '<p><img src="data:image/svg+xml;utf8,{0}" /></p>'.format(draw)
        result = markdown(
            TEST_DIAG_TXT,
            extensions=['markdown_blockdiag'],
            extension_configs={'markdown_blockdiag': {'format': 'svg'}}
        )
        result = unescape(result).replace('&quot;', '\"')

        self.assertEqual(expected, result)
