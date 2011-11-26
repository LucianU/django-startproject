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

def write_pth_file():
    """
    Writes a .pth file that makes the project and apps
    packages discoverable by Python
    """
    env_python_path = os.path.join(REPO_ROOT, ENV_DIR, 'bin/python')
    site_packages = subprocess.check_output([
                        env_python_path,
                        '-c', 
                        'from distutils.sysconfig import get_python_lib;'
                        'print get_python_lib(),'
    ]).strip()

    project_dir = get_project_dir()
    project_rel_path = os.path.relpath(REPO_ROOT, site_packages)
    project_abs_path = os.path.abspath(project_dir)
    apps_rel_path = os.path.relpath(
                        os.path.join(project_abs_path, 'apps'),
                        site_packages
    )

    # writing the .pth file
    with open(os.path.join(site_packages, '%s.pth' % project_dir), 'w') as f:
        f.writelines(['%s\n' % project_rel_path, apps_rel_path])

def write_activate_file(platform):
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

    sys.stdout.write('Creating virtual env...\n')
    subprocess.call([
        'virtualenv',
        '--no-site-packages',
        os.path.join(REPO_ROOT, ENV_DIR)
    ])

    sys.stdout.write('Installing packages in the %s requirements file...\n'
                     % REQ_FILES['common'].split('/')[1])
    subprocess.call([
        os.path.join(REPO_ROOT, ENV_DIR, 'bin', 'pip'),
        'install', '-r',
        os.path.join(REPO_ROOT, REQ_FILES['common'])
    ])

    platform = sys.argv[1]
    sys.stdout.write('Installing packages in the %s requirements file...\n'
                        % REQ_FILES[platform].split('/')[1])
    subprocess.call([
        os.path.join(REPO_ROOT, ENV_DIR, 'bin', 'pip'),
        'install', '-r',
        os.path.join(REPO_ROOT, REQ_FILES[platform])
    ])
    write_pth_file()
    write_activate_file(platform)

if __name__ == '__main__':
    main()
