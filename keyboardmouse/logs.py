#!/usr/bin/env python3
#coding=utf-8
# date 2019-07-22 23:15:49
# author calllivecn <calllivecn@outlook.com>


__all__ = ["logger", "setLevel"]


import sys
import logging
from os import path

logger = logging.getLogger(sys.argv[0])

stream = logging.StreamHandler(sys.stderr)

fmt = logging.Formatter("%(asctime)s %(filename)s:%(lineno)d %(levelname)s %(message)s", datefmt="%Y-%m-%d-%H:%M:%S")

stream.setFormatter(fmt)

logger.addHandler(stream)

logfilename, ext = path.splitext(sys.argv[0])

logfilename = logfilename + ".logs"

logsname = logging.FileHandler(logfilename, "a")
logsname.setFormatter(fmt)

logger.addHandler(logsname)


logger.setLevel(logging.WARN)



def setLevel(level):

    if level == 0:
        logger.setLevel(logging.WARN)
    elif level == 1:
        logger.setLevel(logging.INFO)
    elif level == 2 or level > 2:
        logger.setLevel(logging.DEBUG)

