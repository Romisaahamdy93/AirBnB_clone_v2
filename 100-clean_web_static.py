#!/usr/bin/python3
"""
Fabric script (based on the file 3-deploy_web_static.py) that deletes out-of-date archives
"""
from fabric.api import env, run, local
from datetime import datetime
import os

env.hosts = ['<IP web-01>', '<IP web-02>']


def do_clean(number=0):
    """
    Deletes out-of-date archives
    """
    number = int(number)
    if number <= 0:
        return

    with lcd('./versions'):
        local_archives = local('ls -t', capture=True).split('\n')
        archives_to_keep = local_archives[:number]
        for archive in local_archives[number:]:
            local('rm -rf {}'.format(archive))

    with cd('/data/web_static/releases'):
        remote_archives = run('ls -t').split('\n')
        archives_to_delete = remote_archives[number:]
        for archive in archives_to_delete:
            run('rm -rf {}'.format(archive))

]
