#!/usr/bin/python3
# Fabfile to delete out-of-date archives.
import os
from fabric.api import *

env.hosts = ["104.196.168.90", "35.196.46.172"]


def do_clean(number=0):
    """Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.

    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    number = max(1, int(number))  # Ensure number is at least 1

    with lcd("versions"):
        local_archives = sorted(os.listdir("."))
        archives_to_delete = local_archives[:-number] if number > 1 else []  # Get archives to delete
        [local("rm -f {}".format(a)) for a in archives_to_delete]

    with cd("/data/web_static/releases"):
        remote_archives = run("ls -tr").split()
        remote_archives = [a for a in remote_archives if "web_static_" in a]
        archives_to_delete = remote_archives[:-number] if number > 1 else []  # Get archives to delete
        [run("rm -rf {}".format(a)) for a in archives_to_delete]
