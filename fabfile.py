import os
from contextlib import contextmanager as _contextmanager

from fabric.api import env, run, cd, prefix, settings

# The directory where you will deploy your project,
# for example /home/user/
env.proj_root = '<Path to project location>'

env.proj_dir = os.path.join(env.proj_root, '{{ project_name }}')
env.proj_repo = '<URL to central repo>'
env.virtualenv = '{{ project_name }}'
env.activate = 'workon %s' % env.virtualenv


def stag():
    """
    Staging connection information
    """
    env.user = ''
    env.hosts = []
    env.branch = ''


def prod():
    """
    Production connection information
    """
    env.user = ''
    env.hosts = []
    env.branch = ''


@_contextmanager
def _virtualenv():
    """
    Changes to the proj_dir and activates the virtualenv
    """
    with cd(env.proj_dir):
        with prefix(env.activate):
            yield


def clone():
    """
    Clones the project from the central repository
    """
    run('git clone %s %s' % (env.proj_repo, env.proj_dir))


def make_virtualenv():
    """
    Creates a virtualenv on the remote host
    """
    run('mkvirtualenv %s' % env.virtualenv)


def update_reqs():
    """
    Makes sure all packages listed in requirements are installed
    """
    with _virtualenv():
        run('pip install -r requirements/production.pip')


def update_code():
    """
    Pulls changes from the central repo and checks out the right branch
    """
    with cd(env.proj_dir):
        run('git pull && git checkout %s' % env.branch)


def restart_uwsgi():
    """
    Restarts uwsgi process
    """
    with _virtualenv():
        run('supervisorctl -c confs/production/supervisord.conf'
            ' restart uwsgi')


def start_supervisord():
    """
    Starts supervisord on the remote host
    """
    with _virtualenv():
        run('supervisord -c confs/production/supervisord.conf')


def syncdb():
    """
    Runs syncdb (along with any pending south migrations)
    """
    with _virtualenv():
        run('python manage.py syncdb --migrate')


def deploy():
    """
    Creates or updates the project, runs migrations, installs dependencies.
    """
    first_deploy = False
    with settings(warn_only=True):
        if run('test -d %s' % env.proj_dir).failed:
            first_deploy = True
            clone()
        if run('test -d $WORKON_HOME/%s' % env.virtualenv).failed:
            make_virtualenv()

    update_code()
    update_reqs()
    syncdb()
    if first_deploy:
        start_supervisord()
    else:
        restart_uwsgi()
