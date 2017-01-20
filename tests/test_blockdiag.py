# encoding=utf-8
from __future__ import unicode_literals

import unittest
import tempfile
from contextlib import contextmanager
import shutil

from markdown import markdown
from markdown_blockdiag.parser import BlockdiagProcessor
from markdown_blockdiag.utils import random_filename


def join_text(lines):
    return '\n'.join(lines)


@contextmanager
def patch_mkstemp(patched):
    orig = tempfile.mkstemp
    tempfile.mkstemp = patched
    yield
    tempfile.mkstemp = orig


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

    def test_raise_exception_if_not_configured_dir(self):
        def raised():
            text = join_text([
                "blockdiag {",
                "    A -> B -> C;",
                "}"
            ])
            markdown(text, extensions=['markdown_blockdiag'])

        self.assertRaises(ValueError, raised)

    def test_basic_blockdiag(self):
        text = join_text([
            "blockdiag {",
            "    A -> B -> C;",
            "}"
        ])

        filename = random_filename()

        def patched_mkstemp(*args, **kwargs):
            return 1, filename

        expected = '<p><img src="/diagrams/{0}" /></p>'.format(filename)
        with patch_mkstemp(patched_mkstemp):
            result = markdown(
                text,
                extensions=['markdown_blockdiag'],
                extension_configs={
                    'markdown_blockdiag': {
                        'dir': 'tmp'
                    }
                }
            )
            shutil.rmtree('tmp')

        self.assertEqual(expected, result)
