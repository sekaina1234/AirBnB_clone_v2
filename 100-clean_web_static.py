#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives using the function
"""

from fabric.api import local, env, run, lcd
from datetime import datetime
from os.path import exists

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'
env.key_filename = 'my_ssh_private_key'


def do_clean(number=0):
    """
    Delete out-of-date archives in both local and remote directories.
    The number parameter determines how many archives to keep.
    """
    if int(number) < 2:
        number = 1

    # Delete unnecessary archives in the versions folder locally
    local("ls -1t versions | tail -n +{} | xargs -I
           {{}} rm versions/{{}}".format(int(number) + 1))

    # Delete unnecessary archives in the folder on the web servers
    releases_folder = "/data/web_static/releases"
    with lcd("/tmp/"):
        archives = run("ls -1t {} | tail -n +{}"
                       .format(releases_folder, int(number) + 1)).split()
        for archive in archives:
            run("rm -f {}/{}".format(releases_folder, archive))
