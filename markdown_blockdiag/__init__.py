from markdown_blockdiag.extension import BlockdiagExtension


def makeExtension(**kwargs):
    return BlockdiagExtension(**kwargs)
