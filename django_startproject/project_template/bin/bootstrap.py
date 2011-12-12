#!/usr/bin/env python
"""
This script is to be used when deploying a project for development
or production. The general use case is that, after the source is cloned
with git, this script is run to create the virtual env and install 
the packages specified in requirements/common.pip and those specific
to the platform (development or production).
"""

import os
import sys
import subprocess

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_NAME = os.path.basename(REPO_ROOT)
ENV_DIR = 'env'
SETTINGS_MODULES = {
    'dev': 'development',
    'stag': 'staging',
    'prod': 'production',
}
REQ_FILES = {
    'common': 'requirements/common.pip',
    'dev': 'requirements/development.pip',
    'stag': 'requirements/production.pip',
    'prod': 'requirements/production.pip',
}

def get_project_dir():
    """
    Returns the name of the project dir; it's hackish, but I don't
    see a better way to do this
    """
    for d in os.listdir(REPO_ROOT):
        if os.path.isdir(d) and 'settings' in os.listdir(d):
            return d

def create_env(path):
    """
    Creates a virtual env at the specified path
    """
    sys.stdout.write('Creating virtual env...\n')
    subprocess.call([
        'virtualenv',
        '--no-site-packages',
        path
    ])

def install_packages(platform):
    """
    Uses pip to install packages for the specified platform
    """
    sys.stdout.write('Installing packages in the %s requirements file...\n'
                     % REQ_FILES[platform].split('/')[1])
    subprocess.call([
        os.path.join(REPO_ROOT, ENV_DIR, 'bin', 'pip'),
        'install', '-r',
        os.path.join(REPO_ROOT, REQ_FILES[platform])
    ])

def write_activate_file(platform):
    """
    Writes the DJANGO_SETTINGS_MODULE env var export declaration
    to the 'activate' file of the virtual env
    """
    with open(os.path.join(REPO_ROOT, ENV_DIR, 'bin/activate'), 'a') as f:
        f.write('export DJANGO_SETTINGS_MODULE=%s.settings.%s' %
                (get_project_dir(), SETTINGS_MODULES[platform])
        )

def main():
    if (len(sys.argv) < 2 or (len(sys.argv) == 2
        and sys.argv[1] not in ['prod', 'dev', 'stag'])):
        sys.stdout.write("You need to pass 'stag', 'prod' or 'dev'"
                         " to specify the deployment environment.\n")
        return sys.exit(1)

    if ENV_DIR in os.listdir(REPO_ROOT):
        sys.stdout.write('Virtual env named %s already exists\n' % ENV_DIR)
        return sys.exit(1)

    create_env(os.path.join(REPO_ROOT, ENV_DIR))

    install_packages('common')
    platform = sys.argv[1]
    install_packages(platform)
    write_activate_file(platform)

if __name__ == '__main__':
    main()
