# encoding=utf-8
from __future__ import unicode_literals

import unittest
import base64
from xml.sax.saxutils import unescape

from markdown import markdown
from markdown_blockdiag.parser import BlockdiagProcessor
from markdown_blockdiag.utils import draw_blockdiag


BASIC_DIAG_TXT = r"""
blockdiag {
    A -> B -> C;
}
""".strip()


EXTENDED_DIAG_TXT = r"""
blockdiag {
    A [label = "label test A"];
    B [label = "label test B"];
    C [label = "label test C"];

    A -> B -> C  [label = tag];    // comment
}
""".strip()


SEQ_DIAG_TXT = r"""
seqdiag {
    // edge label
    A -> B [label = "call"];
    A <- B [label = "return"];

    // diagonal edge
    A -> B [diagonal, label = "diagonal edge"];
    A <- B [diagonal, label = "return diagonal edge"];

    // color of edge
    A -> B [label = "colored label", color = red];

    // failed edge
    A -> B [label = "failed edge", failed];
}
""".strip()


MARKDOWN_DOC = r"""
# Title

paragraph

{diagram}

paragraph

{diagram}

paragraph
"""


class BlockdiagTest(unittest.TestCase):
    """Testing blockdiag extension
    """

    def test_run(self):
        self.assertTrue(BlockdiagProcessor.RE.match(BASIC_DIAG_TXT))

    def test_basic_blockdiag(self):
        draw = draw_blockdiag(BASIC_DIAG_TXT)

        expected = '<p><img src="data:image/png;base64,{0}" /></p>'.format(
            base64.b64encode(draw)
        )
        result = markdown(
            BASIC_DIAG_TXT,
            extensions=['markdown_blockdiag'],
        )

        self.assertEqual(expected, result)

    def test_svg_blockdiag(self):
        self.maxDiff = None
        draw = draw_blockdiag(BASIC_DIAG_TXT, output_fmt='svg')

        expected = '<p><img src="data:image/svg+xml;utf8,{0}" /></p>'.format(draw)
        result = markdown(
            BASIC_DIAG_TXT,
            extensions=['markdown_blockdiag'],
            extension_configs={'markdown_blockdiag': {'format': 'svg'}}
        )
        result = unescape(result).replace('&quot;', '\"')

        self.assertEqual(expected, result)

    def test_label_blockdiag(self):
        draw = draw_blockdiag(EXTENDED_DIAG_TXT)

        expected = '<p><img src="data:image/png;base64,{0}" /></p>'.format(
            base64.b64encode(draw)
        )
        result = markdown(
            EXTENDED_DIAG_TXT,
            extensions=['markdown_blockdiag'],
        )
        self.assertEqual(expected, result)

    def test_seqdiag(self):
        draw = draw_blockdiag(SEQ_DIAG_TXT)

        expected = '<p><img src="data:image/png;base64,{0}" /></p>'.format(
            base64.b64encode(draw)
        )
        result = markdown(
            SEQ_DIAG_TXT,
            extensions=['markdown_blockdiag'],
        )
        self.assertEqual(expected, result)

    def test_markdown(self):
        draw = draw_blockdiag(EXTENDED_DIAG_TXT)

        expected = '<p><img src="data:image/png;base64,{0}" /></p>'.format(
            base64.b64encode(draw)
        )

        marcdown_doc = MARKDOWN_DOC.format(diagram=EXTENDED_DIAG_TXT)
        result = markdown(
            marcdown_doc,
            extensions=['markdown_blockdiag'],
        )

        self.assertTrue("Title" in result)
        self.assertEqual(2, result.count(expected))
        self.assertEqual(3, result.count("paragraph"))
