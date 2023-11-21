from markdown.extensions import Extension
from markdown_blockdiag.parser import BlockdiagProcessor


class BlockdiagExtension(Extension):

    def __init__(self, **kwargs):
        self.config = {
            'fontpath': ['', 'Font path to use'],
            'fontantialias': [True, 'Font antialiasing'],
            'format': ['png', 'Format to use (png/svg)'],
        }
        super(BlockdiagExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        md.parser.blockprocessors.add(
            'blockdiag', BlockdiagProcessor(md.parser, self), '>indent'
        )
        md.registerExtension(self)
