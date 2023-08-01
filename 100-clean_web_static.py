#!/usr/bin/python3
""" Fabric script to delete out-of-date archives """
import os
from fabric.api import *
from datetime import datetime

env.hosts = ["34.207.121.58", "54.237.103.145"]


def do_clean(number=0):
    """ Deletes out-of-date archives

    Args:
        number (int): number of archives to keep

    If number is 0 or 1, keep only the most recent version of your
    archive. if number is 2, keep the most recent, and second most
    recent versions of your archive, etc.
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
