#!/usr/bin/python3
import os
from fabric.api import run, put, env

env.hosts = ["34.207.121.58", "54.237.103.145"]


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

