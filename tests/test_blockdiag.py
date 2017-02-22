# encoding=utf-8
from __future__ import unicode_literals

import unittest
import base64

from markdown import markdown
from markdown_blockdiag.parser import BlockdiagProcessor
from markdown_blockdiag.utils import draw_blockdiag


def join_text(lines):
    return '\n'.join(lines)


class BlockdiagTest(unittest.TestCase):
    """Testing blockdiag extension
    """

    def test_run(self):
        text = join_text([
            "blockdiag {",
            "    A -> B -> C;",
            "}"
        ])
        self.assertTrue(BlockdiagProcessor.RE.match(text))

    def test_basic_blockdiag(self):
        text = join_text([
            "blockdiag {",
            "    A -> B -> C;",
            "}"
        ])

        draw = draw_blockdiag(text)

        expected = '<p><img src="data:image/png;base64,{0}" /></p>'.format(
            base64.b64encode(draw)
        )
        result = markdown(
            text,
            extensions=['markdown_blockdiag']
        )

        self.assertEqual(expected, result)
