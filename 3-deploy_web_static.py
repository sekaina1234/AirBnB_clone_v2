#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers,
using the function deploy
"""

from fabric.api import local, env, run, put
from datetime import datetime
from os.path import exists

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'
env.key_filename = 'my_ssh_private_key'


def do_pack():
    """
    Create a compressed archive of the web_static folder.
    Returns the path to the archive if successful, None otherwise.
    """
    try:
        # Create the 'versions' directory if it doesn't exist
        local("mkdir -p versions")

        # Generate the archive name using the current date and time
        now = datetime.now()
        archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
            now.year, now.month, now.day, now.hour, now.minute, now.second)

        # Compress the 'web_static' folder into the archive
        local("tar -czvf versions/{} web_static".format(archive_name))

        # Return the path to the archive
        return "versions/{}".format(archive_name)
    except Exception as e:
        return None


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
        run("tar -xzf /tmp/{} -C
             {}".format(archive_filename, release_folder))

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


def deploy():
    """
    Full deployment process including creating and distributing the archive
    """
    archive_path = do_pack()
    if archive_path is None:
        return False

    return do_deploy(archive_path)
