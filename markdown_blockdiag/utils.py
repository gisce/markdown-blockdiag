from __future__ import absolute_import, unicode_literals

import os
import tempfile


def random_filename():
    return os.path.basename(tempfile.mkstemp('-diagram.png')[1])