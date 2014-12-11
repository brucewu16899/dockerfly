#!/bin/env python
# -*- coding: utf-8 -*-

import os
import grp
import logging
import signal
import daemon
import lockfile

import include
from dockerfly.settings import dockerfly_version
from dockerfly.http.server import run_server

working_directory = '/var/run/dockerfly'

if not os.path.exists(working_directory):
    os.mkdir(working_directory)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(os.path.join(working_directory, 'dockerflyd.log'))
logger.addHandler(fh)

def dockerflyd_setup():
    pass

def dockerflyd_cleanup():
    pass

def dockerflyd_reload_config():
    pass

context = daemon.DaemonContext(
    working_directory=working_directory,
    umask=0o002,
    pidfile=lockfile.FileLock(os.path.join(working_directory, 'dockerflyd.pid')),
    files_preserve = [fh.stream,],
)

context.signal_map = {
    signal.SIGTERM: dockerflyd_cleanup,
    signal.SIGHUP: 'terminate',
    signal.SIGUSR1: dockerflyd_reload_config,
    }

mail_gid = grp.getgrnam('mail').gr_gid
context.gid = mail_gid

if __name__ == '__main__':
    dockerflyd_setup()

    with context:
        run_server(debug=True)

