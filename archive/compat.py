"""
A module for providing backwards compatibility for Python versions.
"""

import sys


IS_PY2 = sys.version_info[0] == 2


if IS_PY2:
    def is_string(obj):
        return isinstance(obj, basestring)
else:
    def is_string(obj):
        return isinstance(obj, str)
