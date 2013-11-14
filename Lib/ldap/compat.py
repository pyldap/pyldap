"""Compatibility wrappers for Py2/Py3."""

import sys

if sys.version_info[0] < 3:
    from UserDict import UserDict
    from urllib import quote, unquote
else:
    from collections import UserDict
    from urllib.parse import quote, unquote
