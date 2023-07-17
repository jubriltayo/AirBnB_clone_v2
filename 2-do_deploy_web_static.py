#!/usr/bin/python3
import os
from fabric.api import run, put, env

env.hosts = ["34.207.121.58", "54.237.103.145"]

def do_deploy(archive_path):
    try:
        if not os.path.isfile(archive_path):
            return False

        # upload archive to `/tmp/`on web server
        put(archive_path, "/tmp/")

        # extract filename without extension
        archive_name = os.path.basename(archive_path)
        arc_name_no_ext = archive_name.split(".")[0]
        print(arc_name_no_ext)

        # create new directory on server
        server_dir = "/data/web_static/releases/{}".format(arc_name_no_ext)
        run("mkdir -p {}".format(server_dir))

        # uncompress archive to a new directory on the same server
        run("tar -xzf /tmp/{} -C {}".format(archive_name, server_dir))

        # delete archive from old dir ('/tmp/')
        run("rm -rf /tmp/{}".format(archive_name))

        # delete symbolic link
        run("rm /data/web_static/current")

        # create a new symbolic link to link to the new file in server_dir
        run("ln -s {} /data/web_static/current".format(server_dir))

        return True

    except:
        return False
