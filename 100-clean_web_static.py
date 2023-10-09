#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives.
"""

from fabric.api import local, env, run, lcd
from datetime import datetime
import os

env.hosts = ['<IP web-01>', '<IP web-02>']

def do_clean(number=0):
    """
    Deletes out-of-date archives.
    """
    try:
        number = int(number)
    except ValueError:
        return
    if number < 0:
        return
    if number == 0 or number == 1:
        number = 1
    else:
        number += 1

    with lcd("versions"):
        local("ls -t | tail -n +{} | xargs -I {{}} rm {{}}".format(number))

    with cd("/data/web_static/releases"):
        run("ls -t | tail -n +{} | xargs -I {{}} rm -rf {{}}".format(number))
