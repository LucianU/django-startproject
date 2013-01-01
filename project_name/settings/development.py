from {{ project_name }}.settings.common import *
try:
    from {{ project_name }}.settings.local import *
except ImportError:
    pass
