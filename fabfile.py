import os

from fabric.context_managers import cd
from fabric.contrib.files import upload_template
from fabric.decorators import task
from fabric.operations import put, run
from fabric.state import env

env.update({
    'home': '/Users/franhp',
    'containers': '/Users/franhp/containers',
    'uid': '501',  # franhp
    'gid': '20',  # staff
    'mysql_root_pwd': 'empty'
})


@task
def deploy():
    apps()
    setup_nginx()
    docker_compose_yml()
    restart()


@task
def apps():
    mkdir(inside_containers('manager'))
    mkdir(inside_containers('transmission'))
    mkdir(inside_containers('headphones'))
    mkdir(inside_containers('jackett'))
    #mkdir(inside_containers('jackett-new'))
    #mkdir(inside_containers('mylar'))
    #mkdir(inside_containers('plex'))
    mkdir(inside_containers('plexpy'))
    mkdir(inside_containers('couchpotato'))
    mkdir(inside_containers('sonarr'))


@task
def setup_nginx():
    mkdir(inside_containers('frontend'))
    put('nginx/manager.conf', inside_containers('frontend/manager.conf'))

@task
def docker_compose_yml():
    upload_template(
        'docker-compose.yml',
        inside_containers('docker-compose.yml'),
        context=env
    )


@task
def restart():
    with cd(inside_containers()):
        run('docker-compose stop && docker-compose up -d')


def inside_containers(*path):
    return os.path.join(env.containers, *path)


def mkdir(full_path):
    run('mkdir -p ' + full_path)
    #run('chown -h ' + env.uid + ' ' + full_path)
    #run('chgrp -h ' + env.gid + ' ' + full_path)
