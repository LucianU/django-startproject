Developer documentation is available in Sphinx format in the docs directory.

Initial installation instructions (including how to build the documentation as
HTML) can be found in docs/install.rst.

Deployment
==============================================================================

To deploy this application, you need to follow these steps:

#. Clone the repository with git.
#. Run the bootstrap.py script located in PROJECT_DIR/bin passing it 'dev',
   'prod' or 'stag'.

   This will create a virtual environment called 'env', in which it will
   install the packages listed in requirements/common.pip and in the file
   corresponding to the platform.

   Finally, it will append to the bin/activate file a declaration that will
   set DJANGO_SETTINGS_MODULE to the settings module corresponding to the
   platform when the virtual env is activated.
