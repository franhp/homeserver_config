import os
from fabric.operations import run
from fabric.state import env


def inside_containers(*path):
    print(env.host)
    print(env.containers)
    shit = os.path.join(env.containers, path)
    print(shit)
    return shit


def mkdir(path):
    full_path = inside_containers(path)
    run('mkdir -p -m 0755 ' + full_path)
    run('chown -h ' + env.uid + ' ' + full_path)
    run('chgrp -h ' + env.gid + ' ' + full_path)
