#!/usr/bin/env python
# -*- coding:utf-8 -*-

import io

from setuptools import setup


version = "2.0.3"


setup(
    name="python-lyric",
    version=version,
    description="Python API for talking to the Honeywell Lyric™ Thermostat",
    long_description=io.open("README.rst", encoding="UTF-8").read(),
    keywords="honeywell lyric thermostat",
    author="Bram Kragten",
    author_email="mail@bramkragten.nl",
    url="https://github.com/bramkragten/python-lyric/",
    packages=["lyric"],
    install_requires=["aiohttp>=3.6.2"],
)
