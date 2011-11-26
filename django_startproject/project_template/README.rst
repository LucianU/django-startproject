Developer documentation is available in Sphinx format in the docs directory.

Initial installation instructions (including how to build the documentation as
HTML) can be found in docs/install.rst.

Deployment
==============================================================================

To deploy this application, you need to follow these steps:
1) Clone the repository with git.
2) Run the bootstrap.py script located in PROJECT_DIR/bin passing it 'dev',
   'prod' or 'stag'.

   This will create a virtual environment called 'env', in which it will
   install the packages listed in requirements/common.pip and in the file
   corresponding to the platform.

   Afterwards, it will put in site-packages a .pth file with the same name
   as the project which will contain relative paths to the project repository
   and the apps packages. This will make the project package and the apps
   available in python path.

   Finally, it will append to the bin/activate file a declaration that will
   set DJANGO_SETTINGS_MODULE to the settings module corresponding to the
   platform when the virtual env is activated.
