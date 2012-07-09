from myproject.settings.common import *
try:
    from myproject.settings.local import *
except ImportError:
    pass
