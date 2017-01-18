from markdown.extensions import Extension
from markdown_blockdiag.parser import BlockdiagProcessor


class BlockdiagExtension(Extension):

    def __init__(self, **kwargs):
        super(BlockdiagExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md, md_globals):
        md.parser.blockprocessors.add(
            'blockdiag', BlockdiagProcessor(md.parser), '>indent'
        )
        md.registerExtension(self)
