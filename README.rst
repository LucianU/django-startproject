Quickstart
##########
1. Create your virtualenv with the same name as the project, activate it and
   install Django.
2. Create your project by running::

    django-admin.py startproject --template=https://github.com/LucianU/django-startproject/zipball/master <project>


replacing ``<project>`` with the name of your project.

3. Look at the different files in the ``confs`` directory and its subdirectories
   and adjust the values as you wish. Replace the placeholders with your wanted
   values.

4. Go into the ``fabfile/targets.py`` file and adjust the env vars as you see fit.


Overview
########
This project template is based on a certain stack of applications. These are::

    - pip as package manager
    - virtualenv and virtualenvwrapper for dependency containment
    - postgresql as a database
    - nginx and uwsgi as a proxy and application server respectively
    - supervisor for process management
    - memcached for caching
    - fabric + git for deployment

The ``fabfile`` package contains several modules that provide tasks for
deployment, project setup and interaction with the applications used.

The most basic idea is that when you run a task you have to specify the
deployment enviroment on which you want the task to run. To do that you use a
task specific to that environment, one of ``here``, ``stag`` and ``prod``.
``here`` corresponds to your local machine, ``stag`` to the staging environment
and ``prod`` to the production environment. For example, to setup the project
on your machine, you run::

    fab here first_deploy

This task clones the project in the current directory, creates a virtualenv,
installs all the requirements, synchronizes the database and collects the
static files, so make sure you've installed the big dependencies, setup the
database and populated the ``local.py`` settings file with the credentials.

After that, every time you want to deploy changes to production, make sure
you've pushed them to the central repo and then run::

    fab prod deploy

This task updates the code and checks out the right branch, makes sure all
requirements are installed, runs ``syncdb`` and ``collectstatic`` and then
restarts ``supervisord``.


Contribute
##########
If you think this document could be improved in any way, please open an
issue on GitHub. The same is true for the project itself.
