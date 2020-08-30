#!/usr/bin/env python
# -*- coding:utf-8 -*-
import io

from setuptools import setup, find_packages

version = "2.0.0"

setup(
    name="python-lyric",
    version=version,
    description="Python API for talking to the Honeywell Lyric™ Thermostat",
    long_description=io.open("README.rst", encoding="UTF-8").read(),
    keywords="honeywell lyric thermostat",
    author="Bram Kragten",
    author_email="mail@bramkragten.nl",
    url="https://github.com/bramkragten/python-lyric",
    packages=find_packages(exclude=["tests"]),
    install_requires=["aiohttp>=3.6.2"],
)
