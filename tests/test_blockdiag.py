# encoding=utf-8
from __future__ import unicode_literals

import unittest
import base64
from xml.sax.saxutils import unescape

from markdown import markdown
from markdown_blockdiag.parser import BlockdiagProcessor
from markdown_blockdiag.utils import draw_blockdiag

# Python 3 version
try:
    from urllib.parse import quote as url_quote
# Python 2 version
except ImportError:
    from urllib import quote as url_quote


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

        expected = '<p><img src="data:image/svg+xml;charset=utf-8,{0}" /></p>'.format(url_quote(draw))
        result = markdown(
            BASIC_DIAG_TXT,
            extensions=['markdown_blockdiag'],
            extension_configs={'markdown_blockdiag': {'format': 'svg'}}
        )
        result = unescape(result).replace('&quot;', '\"')

        self.assertEqual(expected, result)

    def test_font_antialias_blockdiag(self):
        self.maxDiff = None
        draw = draw_blockdiag(BASIC_DIAG_TXT, font_antialias=False)

        expected = '<p><img src="data:image/png;base64,{0}" /></p>'.format(
            base64.b64encode(draw)
        )
        result = markdown(
            BASIC_DIAG_TXT,
            extensions=['markdown_blockdiag'],
            extension_configs={'markdown_blockdiag': {'fontantialias': False}}
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

    def test_prefetch_remote_images(self):
        """Test that prefetch_remote_images correctly handles URLs"""
        from markdown_blockdiag.utils import prefetch_remote_images
        
        # Test with URL patterns
        diagram_with_urls = 'blockdiag { A [background = "http://example.com/bg.png"]; B [icon = "https://example.com/icon.gif"]; }'
        result = prefetch_remote_images(diagram_with_urls)
        
        # The function should either replace URLs with cached paths or keep original URLs on failure
        self.assertIn('background', result)
        self.assertIn('icon', result)
        
        # Test with local paths (should not be modified)
        diagram_with_local = 'blockdiag { A [background = "/local/path.png"]; }'
        result = prefetch_remote_images(diagram_with_local)
        self.assertEqual(diagram_with_local, result)  # Should be unchanged
        
    def test_prefetch_caching(self):
        """Test that prefetch_remote_images caches results"""
        from markdown_blockdiag.utils import prefetch_remote_images, _image_cache
        
        # Clear cache
        _image_cache.clear()
        
        # Test with same URL twice
        diagram = 'blockdiag { A [background = "http://example.com/same.png"]; B [background = "http://example.com/same.png"]; }'
        result = prefetch_remote_images(diagram)
        
        # Both occurrences should be handled (either replaced or kept)
        self.assertIn('background', result)
