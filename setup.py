#!/usr/bin/env python
from distutils.core import setup

setup(
    name='proteinutils',
    version='1.0',
    #package_dir = {'':'lib'},
    packages = ['rosettautil','rosettautil.graphics','rosettautil.protein','rosettautil.rosetta']
    )
