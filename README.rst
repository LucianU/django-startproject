Usage
#####
Create your virtualenv, activate it and install Django and then you can
run::

    django-admin.py startproject --template=https://github.com/LucianU/django-startproject/zipball/master <project>

replacing `<project>` with the name of your project.

Symlink all the configuration files that you use in their required locations.

Overview
########
This project template is based on a certain stack of applications. These are::

    - postgresql as a database
    - nginx and uwsgi as a proxy and application server respectively
    - supervisor for process management
    - memcached for caching
