# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages


g = {}
with open(os.path.join('hepdata_cli', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']


test_requirements = [
    'click',
    'requests',
]


install_requirements = [
    'click',
    'requests',
    'pytest',
    'pytest-cov',
]


setup(
    name='hepdata-cli',
    version=version,
    author='Giuseppe De Laurentis',
    author_email='g.dl@hotmail.it',
    description='HEPData command-line interface',
    packages=find_packages(),
    include_package_data=True,
    tests_require=test_requirements,
    install_requires=install_requirements,
    entry_points={
        'console_scripts': [
            'hepdata-cli = hepdata_cli.cli:cli',
        ],
    },
)
