Installation
============
Make sure you have **pip** installed and then run::

    pip install -e git+https://github.com/LucianU/django-startproject#egg=django-startproject

Quickstart
==========
Make sure you have installed **PostgreSQL** (including the **pg_config** binary), **nginx**
and **virtualenv**.

#. Create your project (you will be prompted for some data)::

        django-startproject.py project

#. Run git init in the project directory and make your first commit
#. Create a database for the project::
    
        createdb project

#. Put in your database credentials in settings/local.py
#. Activate your environment and run ``django-admin.py syncdb`` 
#. Symlink project/confs/development/nginx.conf into the 'sites-enabled' directory of your **nginx** installation and restart the server
#. Go to your repo root and run ``supervisord``. Go to http://localhost:8000/ and you should see the greeting from Django

Overview
========

**django-startproject** does 3 things:

#. It creates a Django project that already has the appropriate structure
   and the necessary files::

    project/
             setup.py
	     fabfile.py
             README.rst
             requirements/
                     common.pip
                     development.pip
                     production.pip
	     bin/
	             bootstrap.py
             confs/
                     development/
		             nginx.conf
			     supervisord.conf
			     uwsgi.ini
		     staging/
			     same
		     production/
			     same
     	     maint/
	             lock/
                     run/
                             project.sock
                             uwsgi.pid
                     log/
                             nginx/
			             access.log
				     error.log
	     project/
                     __init__.py
		     urls.py
		     wsgi.py
		     settings/
		             __init__.py
			     local.py (not version tracked)
			     common.py
			     development.py
			     staging.py
			     production.py
                     apps/
                     static/
		     templates/

#. The created project provides a way to easily deploy the project in any kind of
   environment (development, staging, production): the ``bin/bootstrap.py`` script. This
   script:

   - creates a virtualenv called ``env`` and installs the packages specified in 
     ``requirements/common.pip`` and those specific to the deployment environment.
   - writes at the end of the bin/activate file the declaration 
     ``export DJANGO_SETTINGS_MODULE=myproject.settings.deployment_env_settings``,
     where ``deployment_env_settings`` can be one of ``development``, ``staging``, 
     ``production``.
   - it makes an ``etc`` directory in the virtual env, and symlinks to the supervisord.conf
     file specific to the deployment environment

#. The created project uses the same stack (**nginx**, **uwsgi**, **supervisord**) for all environments,
   including development, and doesn't even have a manage.py file. The reason for this is 
   that it adheres to the principle that the  development and the production environments 
   should be as similar as possible, to avoid issues when switching from one to the other. 
   This is also why **PostgreSQL** is used in development, instead of **SQLite**. 