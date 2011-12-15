from setuptools import setup
import os


README_FILE = open('README.rst')
try:
    LONG_DESCRIPTION = README_FILE.read()
finally:
    README_FILE.close()

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'django_startproject', 'project_template')
STARTPROJECT_DATA = []
for path, dirs, filenames in os.walk(DATA_DIR):
    # Ignore directories that start with '.'
    for i, dir in enumerate(dirs):
        if dir.startswith('.'):
            del dirs[i]
    path = path[len(DATA_DIR) + 1:]
    STARTPROJECT_DATA.append(os.path.join('project_template', path, '*.*'))
    # Get files starting with '.' too (they are excluded from the *.* glob).
    STARTPROJECT_DATA.append(os.path.join('project_template', path, '.*'))


setup(name='django-startproject',
      version='1.0a',
      author='Lucian Ursu',
      author_email='lucian.ursu@gmail.com',
      description=('Create a Django project layout that comes with a virtual env and '
                     'server configuration files.'),
      long_description=LONG_DESCRIPTION,
      packages=['django_startproject'],
      package_data={'django_startproject': STARTPROJECT_DATA},
      scripts=['bin/django-startproject.py'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules'])
