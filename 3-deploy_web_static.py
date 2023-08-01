#!/usr/bin/python3
# Fabric script to creates and distributes an archive to your web servers, using the function deploy()
import os
from datetime import datetime
from fabric.api import local, run, env, put

env.hosts = ["34.207.121.58", "54.237.103.145"]


def do_pack():
    """ Creates a tar-generated `gzip` archive of web_static folder """
    dt = datetime.now()
    a_file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                           dt.month,
                                                           dt.day,
                                                           dt.hour,
                                                           dt.minute,
                                                           dt.second)
    """ create directory `versions` if it doesnt exist """
    if os.path.isdir("versions") is False:
        # create directory on local machine without error if failed
        if local("mkdir -p versions").failed is True: 
            return None 
    # create gzip file using `tar` command 
    if local("tar -czvf {} web_static".format(a_file)).failed is True:
        return None 
    return a_file

def do_deploy(archive_path):
    try:
        if not os.path.isfile(archive_path):
            return False

        # Upload archive to `/tmp/` on the web server
        put(archive_path, "/tmp/")

        # Extract filename without extension
        archive_name = os.path.basename(archive_path)
        fname = archive_name.split(".")[0]

        # Create a new directory on the server
        server_dir = "/data/web_static/releases/{}".format(fname)
        run("mkdir -p {}".format(server_dir))

        # Uncompress archive to a new directory on the same server
        run("tar -xzf /tmp/{} -C {}".format(archive_name, server_dir))

        # Delete archive from the old directory ('/tmp/')
        run("rm -rf /tmp/{}".format(archive_name))

        # Move content out of the sub-folder
        run("sudo mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(fname, fname))

        # Remove the now empty web_static dir
        run("sudo rm -rf /data/web_static/releases/{}/web_static/"
            .format(fname))

        # Delete existing symbolic link
        run("rm /data/web_static/current")

        # Create a new symbolic link to link to the new file in server_dir
        run("ln -s {} /data/web_static/current".format(server_dir))

        return True

    except Exception:
        return False


def deploy():
    """ creates and distributes an archive to the web servers """
    path = do_pack()
    if not path:
        return False
    return do_deploy(path)
