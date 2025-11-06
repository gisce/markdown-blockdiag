from markdown.extensions import Extension
from markdown_blockdiag.parser import BlockdiagProcessor


class BlockdiagExtension(Extension):

    def __init__(self, **kwargs):
        self.config = {
            'fontpath': ['', 'Font path to use'],
            'fontantialias': [True, 'Font antialiasing'],
            'format': ['png', 'Format to use (png/svg)'],
            'edge_label_box': [True, 'Show box around edge labels'],
        }
        super(BlockdiagExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md, md_globals=None):
        md.parser.blockprocessors.add(
            'blockdiag', BlockdiagProcessor(md.parser, self), '>indent'
        )
        md.registerExtension(self)
