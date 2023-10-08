#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers,
using the function do_deploy
"""

from fabric.api import local, put, run, env
from os.path import exists
from datetime import datetime

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'
env.key_filename = 'my_ssh_private_key'


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers and deploys it
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract the archive to the folder
        archive_filename = archive_path.split('/')[-1]
        archive_name_no_extension = archive_filename.split('.')[0]
        release_folder = "/data/web_static/releases/{}".format(
            archive_name_no_extension)
        run("mkdir -p {}".format(release_folder))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, release_folder))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(archive_filename))

        # Move the contents of the release folder to the parent directory
        run("mv {}/web_static/* {}".format(release_folder, release_folder))

        # Remove the now empty web_static folder
        run("rm -rf {}/web_static".format(release_folder))

        # Delete the old symbolic link /data/web_static/current
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the new version of your code
        run("ln -s {} /data/web_static/current".format(release_folder))

        print("New version deployed!")
        return True
    except Exception:
        return False
