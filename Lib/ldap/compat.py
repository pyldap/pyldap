"""Compatibility wrappers for Py2/Py3."""

import sys

if sys.version_info[0] < 3:
    from UserDict import UserDict
    from urllib import quote
    from urllib import unquote as urllib_unquote
    from urlparse import urlparse

    def unquote(uri):
        """Specialized unquote that uses UTF-8 for parsing."""
        uri = uri.encode('ascii')
        unquoted = urllib_unquote(uri)
        return unquoted.decode('utf-8')
else:
    from collections import UserDict
    from urllib.parse import quote, unquote, urlparse
