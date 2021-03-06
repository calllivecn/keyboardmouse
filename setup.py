#!/usr/bin/env python3
# coding=utf-8
# date 2019-09-11 20:30:10
# author calllivecn <c-all@qq.com>

from setuptools import setup
#from distutils.core import setup

with open("LICENSE") as f:
    LICENSE = f.read()

setup(
        name="keyboardmouse",
        version="0.2.0",
        description="Virtaul Keyboard Mouse",
        author="calllivecn",
        author_email="c-all@qq.com",
        url="https://github.com/calllivecn/keyboardmouse",
        license=LICENSE,
        py_modules=["libkbm","libhotkey", "logs"],
        #packages=["libkbm"],
        install_requires=["libevdev>=0.7"],
        platforms=["linux"],
        scripts=["list-inputs.py", "checkkey.py"]
    )
