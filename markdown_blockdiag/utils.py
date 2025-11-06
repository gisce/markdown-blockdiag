from __future__ import absolute_import, unicode_literals

import re
import io
from tempfile import NamedTemporaryFile

from nwdiag import parser as nw_parser, builder as nw_builder, drawer as nw_drawer
from seqdiag import parser as seq_parser, builder as seq_builder, drawer as seq_drawer
from actdiag import parser as act_parser, builder as act_builder, drawer as act_drawer
from blockdiag import parser as block_parser, builder as block_builder, drawer as block_drawer
from rackdiag import parser as rack_parser, builder as rack_builder, drawer as rack_drawer
from packetdiag import parser as packet_parser, builder as packet_builder, drawer as packet_drawer

from blockdiag.utils.fontmap import FontMap


DIAG_MODULES = {
    'nwdiag': (nw_parser, nw_builder, nw_drawer),
    'seqdiag': (seq_parser, seq_builder, seq_drawer),
    'actdiag': (act_parser, act_builder, act_drawer),
    'blockdiag': (block_parser, block_builder, block_drawer),
    'rackdiag': (rack_parser, rack_builder, rack_drawer),
    'packetdiag': (packet_parser, packet_builder, packet_drawer),
}


# Cache for pre-fetched remote images
_image_cache = {}


def prefetch_remote_images(content):
    """
    Pre-fetch remote images referenced in diagram content and cache them locally.
    
    This function extracts URLs from background and icon attributes, downloads them,
    and replaces them with local file paths. This ensures diagrams can be rendered
    even in environments with restricted network access after the initial fetch.
    
    Args:
        content: The diagram content string
        
    Returns:
        Modified content with URLs replaced by local file paths
    """
    try:
        from urllib.request import urlopen as orig_urlopen
    except ImportError:
        from urllib2 import urlopen as orig_urlopen
    
    # Pattern to match background = "url" or icon = "url"
    url_pattern = re.compile(r'(background|icon)\s*=\s*"(https?://[^"]+)"')
    
    def replace_url(match):
        attr_name = match.group(1)
        url = match.group(2)
        
        # Check if already cached
        if url in _image_cache:
            return '{} = "{}"'.format(attr_name, _image_cache[url])
        
        # Try to fetch and cache the image
        try:
            with NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
                response = orig_urlopen(url, timeout=10)
                tmpfile.write(response.read())
                tmpfile.flush()
                _image_cache[url] = tmpfile.name
                return '{} = "{}"'.format(attr_name, tmpfile.name)
        except Exception:
            # If fetch fails, keep the original URL and let blockdiag handle it
            return match.group(0)
    
    return url_pattern.sub(replace_url, content)


def draw_blockdiag(content, filename=None, font_path=None, font_antialias=True, output_fmt='png', fetch_remote_images=True):
    # Pre-fetch remote images if enabled
    if fetch_remote_images:
        content = prefetch_remote_images(content)
    
    diag_type, content = content.split(" ", 1)
    parser, builder, drawer = DIAG_MODULES[diag_type.strip()]
    tree = parser.parse_string(content)
    diagram = builder.ScreenNodeBuilder.build(tree)

    fontmap = FontMap()

    if font_path:
        fontmap.set_default_font(font_path)

    draw = drawer.DiagramDraw(
        output_fmt, diagram, filename=filename, font_alias=font_antialias, fontmap=fontmap
    )
    draw.draw()

    return draw.save()
