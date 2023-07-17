#!/usr/bin/python3

"""This module contains a script that generates a .tgz archive from the
contents of the web_static folder of AirBnB Clone v2, using the
function do_pack.
"""
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """This function generates a .tgz archive from the contents of the
    web_static folder of AirBnB Clone v2, using the function do_pack.
    """
    try:
        if not os.path.isdir('versions'):
            local('mkdir versions')
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} ./web_static".format(file_name))
        return file_name
    except Exception:
        return None
