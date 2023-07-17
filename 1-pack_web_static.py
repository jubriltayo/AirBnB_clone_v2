#!/usr/bin/python3
# Fabric script to generate a `.tgz` archive from contents of web_static
import os
from datetime import datetime
from fabric.api import local


def do_pack():
    """ Creates a tar-generated `gzip` archive of web_static folder """
    dt = datetime.now()
    a_file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                           dt.month,
                                                           dt.day,
                                                           dt.hour,
                                                           dt.minute,
                                                           dt.second)
    # create directory `versions` if it doesnt exist
    if os.path.isdir("versions") is False:
        # create directory on local machine without error if failed
        if local("mkdir -p versions").failed is True:
            return None
    # create gzip file using `tar` command
    if local("tar -czvf {} web_static".format(a_file)).failed is True:
        return None
    return a_file
