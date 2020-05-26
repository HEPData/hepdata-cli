# -*- coding: utf-8 -*-

from .hepdata_cli.version import __version__

from setuptools import setup, find_packages

setup(
    name='hepdata-cli',
    version=__version__,
    author='Giuseppe De Laurentis',
    author_email='g.dl@hotmail.it',
    description='HEPData command-line interface',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'hepdata-cli = hepdata_cli.cli:cli',
        ],
    },
)
