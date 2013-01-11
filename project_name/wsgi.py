import os
import sys
import site
import subprocess

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
REPO_PATH = os.path.dirname(PROJECT_PATH)

# Add the virtualenv packages to the site directory. This uses the technique
# described at http://code.google.com/p/modwsgi/wiki/VirtualEnvironments

# Remember original sys.path.
prev_sys_path = list(sys.path)

# Get the path to the env's site-packages directory
site_packages = subprocess.check_output([
    os.path.join(REPO_PATH, 'env/bin/python'),
    '-c',
    'from distutils.sysconfig import get_python_lib;'
    'print get_python_lib(),'
]).strip()

# Add the virtualenv site-packages to the site packages
site.addsitedir(site_packages)

# Reorder sys.path so the new directories are at the front.
new_sys_path = []
for item in list(sys.path):
    if item not in prev_sys_path:
        new_sys_path.append(item)
        sys.path.remove(item)
sys.path[:0] = new_sys_path

# Add the app code to the path
sys.path.append(REPO_PATH)
sys.path.append(os.path.join(PROJECT_PATH, 'apps'))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
