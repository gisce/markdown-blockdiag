from __future__ import absolute_import, unicode_literals

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


def draw_blockdiag(content, filename=None, font_path=None, font_antialias=True, output_fmt='png', edge_label_box=True):
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
    
    # Monkey-patch edge_label method to optionally disable edge label box
    # Only blockdiag draws boxes around edge labels (via the 'outline' parameter)
    # Other diagram types either don't use outline or don't have edge labels
    if not edge_label_box and diag_type.strip() == 'blockdiag':
        def edge_label_no_box(edge):
            if edge.label:
                metrics = draw.metrics.edge(edge)
                font = draw.metrics.font_for(edge)
                # Call textarea without outline parameter to remove the box
                draw.drawer.textarea(metrics.labelbox, edge.label, font=font,
                                   fill=edge.textcolor)
        
        draw.edge_label = edge_label_no_box
    
    draw.draw()

    return draw.save()
