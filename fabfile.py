#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.api import task, prefix, run, sudo, env, require, cd, quiet
from fabric.colors import green, yellow
from fabric.contrib import django
from functools import wraps
import sys
import os.path


# put project directory in path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_root)

django.project('pbw')
from django.conf import settings

REPOSITORY = 'github.com/kingsdigitallab/pbw-django.git'

env.user = settings.FABRIC_USER
env.hosts = ['pbw2.kdl.kcl.ac.uk']
env.gateway = 'ssh.cch.kcl.ac.uk'
env.root_path = '/vol/pbw2/webroot/'
env.envs_path = os.path.join(env.root_path, 'envs')
env.solr='solr-4.10.4'


def server(func):
    """Wraps functions that set environment variables for servers"""
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            env.servers.append(func)
        except AttributeError:
            env.servers = [func]

        return func(*args, **kwargs)
    return decorated


@task
@server
def dev():
    env.srvr = 'dev'
    env.solr = '/vol/pbw2/webroot/stg/solr/solr-4.10.4/'
    set_srvr_vars()


@task
@server
def stg():
    env.srvr = 'stg'
    env.solr = '/vol/pbw2/webroot/stg/solr/solr-4.10.4/'
    set_srvr_vars()


@task
@server
def liv():
    env.srvr = 'liv'
    set_srvr_vars()


def set_srvr_vars():
    env.path = os.path.join(env.root_path, env.srvr, 'django',
                            'pbw')
    env.within_virtualenv = 'source {}'.format(
        os.path.join(env.envs_path, env.srvr, 'bin', 'activate'))


@task
def setup_environment(version=None):
    require('srvr', 'path', 'within_virtualenv', provided_by=env.servers)
    create_virtualenv()
    clone_repo()
    update(version)
    install_requirements()


@task
def create_virtualenv():
    require('srvr', 'path', 'within_virtualenv', provided_by=env.servers)
    with quiet():
        env_vpath = os.path.join(env.envs_path, env.srvr)
        if run('ls {}'.format(env_vpath)).succeeded:
            print((
                green('virtual environment at [{}] exists'.format(env_vpath))))
            return

    print((yellow('setting up virtual environment in [{}]'.format(env_vpath))))
    run('virtualenv {}'.format(env_vpath))


@task
def clone_repo():
    require('srvr', 'path', 'within_virtualenv', provided_by=env.servers)
    with quiet():
        if run('ls {}'.format(os.path.join(env.path, '.git'))).succeeded:
            print((green(('repository at'
                         ' [{}] exists').format(env.path))))
            return

    print((yellow('cloneing repository to [{}]'.format(env.path))))
    run('git clone {} {}'.format(REPOSITORY, env.path))


@task
def install_requirements():
    require('srvr', 'path', 'within_virtualenv', provided_by=env.servers)

    reqs = 'requirements-{}.txt'.format(env.srvr)

    try:
        assert os.path.exists(reqs)
    except AssertionError:
        reqs = 'requirements.txt'

    with cd(env.path), prefix(env.within_virtualenv):
        run('pip install --no-cache -U -r {}'.format(reqs))


@task
def reinstall_requirement(which):
    require('srvr', 'path', 'within_virtualenv', provided_by=env.servers)

    with cd(env.path), prefix(env.within_virtualenv):
        run('pip uninstall {0} && pip install --no-deps {0}'.format(which))


@task
def deploy(version=None, index='yes'):
    update(version)
    install_requirements()
    migrate()
    collect_static()
    if index.lower() == 'yes':
        update_index()
    # clear_cache()
    own_django_log()
    touch_wsgi()


@task
def update(version=None):
    require('srvr', 'path', 'within_virtualenv', provided_by=env.servers)

    if version:
        # try specified version first
        to_version = version
    elif not version and env.srvr in ['local', 'vagrant', 'dev']:
        # if local, vagrant or dev deploy to develop branch
        to_version = 'develop'
    else:
        # else deploy to master branch
        to_version = 'master'

    with cd(env.path), prefix(env.within_virtualenv):
        run('git pull')
        run('git checkout {}'.format(to_version))


@task
def own_django_log():
    """ make sure logs/django.log is owned by www-data"""
    require('srvr', 'path', 'within_virtualenv', provided_by=env.servers)

    with quiet():
        log_path = os.path.join(env.path, 'logs', 'django.log')
        if run('ls {}'.format(log_path)).succeeded:
            sudo('chown www-data {}'.format(log_path))


@task
def migrate(app=None):
    require('srvr', 'path', 'within_virtualenv', provided_by=env.servers)

    with cd(env.path), prefix(env.within_virtualenv):
        run('./manage.py migrate {}'.format(app if app else ''))


@task
def collect_static(process=False):
    require('srvr', 'path', 'within_virtualenv', provided_by=env.servers)

    if env.srvr in ['local', 'vagrant']:
        print((yellow('Do not run collect_static on local servers')))
        return

    with cd(env.path), prefix(env.within_virtualenv):
        run('./manage.py collectstatic {process} --noinput'.format(
            process=('--no-post-process' if not process else '')))


@task
def update_index():
    require('srvr', 'path', 'within_virtualenv', provided_by=env.servers)

    with cd(env.path), prefix(env.within_virtualenv):
        run('./manage.py build_solr_schema > schema.xml')
        run('mv schema.xml {}/collection1/conf/'.format(env.solr))
        sudo('service tomcat7-{} restart'.format(env.srvr))
        run('./manage.py update_index')


@task
def clear_cache():
    require('srvr', 'path', 'within_virtualenv', provided_by=env.servers)

    with cd(env.path), prefix(env.within_virtualenv):
        run('./manage.py clear_cache')


@task
def touch_wsgi():
    require('srvr', 'path', 'within_virtualenv', provided_by=env.servers)

    with cd(os.path.join(env.path, 'pbw')), \
            prefix(env.within_virtualenv):
        run('touch wsgi.py')
