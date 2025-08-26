# -*- coding: utf-8 -*-

"""CLI and API to allow users to search, download from and upload to HEPData"""

import os

from setuptools import setup, find_packages


g = {}
with open(os.path.join('hepdata_cli', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']


install_requirements = [
    'click',
    'requests',
]

test_requirements = [
    'pytest',
    'pytest-cov',
    'requests_mock',
]

extras_require = {
    'tests': test_requirements,
}


setup(
    name='hepdata-cli',
    version=version,
    author='Giuseppe De Laurentis',
    author_email='g.dl@hotmail.it',
    description=__doc__,
    keywords='hepdata cli api',
    url='https://github.com/HEPData/hepdata-cli',
    packages=find_packages(),
    zip_safe=False,
    platforms='any',
    license='GPLv3',
    install_requires=install_requirements,
    extras_require=extras_require,
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'hepdata-cli = hepdata_cli.cli:cli',
        ],
    },
)
