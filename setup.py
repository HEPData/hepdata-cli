# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='hepdata-cli',
    version='0.1',
    author='Giuseppe De Laurentis',
    author_email='g.dl@hotmail.it',
    description='HEPData command-line interface',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'requests',
        're',
    ],
    entry_points={
        'console_scripts': [
            'hepdata = hepdata_cli.cli:cli',
        ],
    },
)
