#!/usr/bin/python3
# Fabric script to generate a `.tgz` archive from contents of web_static
import os
from datetime import datetime
from fabric.api import local


def do_pack():
    """ Creates a tar-generated `gzip` archive of web_static folder """
    dt = datetime.now()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                        dt.month,
                                                        dt.day,
                                                        dt.hour,
                                                        dt.minute,
                                                        dt.second)
    # create directory `versions` if it doesnt exist								
    if not os.path.isdir("versions"):
        # create directory on local machine without error if failed
        if local("mkdir versions").failed:
            return None
    # create gzip file using `tar` command
    if local("tar -czvf {} web_static".format(file)).failed:
        return None

    return file
