# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "dmss_api"
VERSION = ""

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion>=2.0.2",
    "swagger-ui-bundle>=0.0.2",
    "python_dateutil>=2.6.0"
]

setup(
    name=NAME,
    version=VERSION,
    description="Data Modelling Storage Service API",
    author_email="",
    url="",
    keywords=["OpenAPI", "Data Modelling Storage Service API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['dmss_api=dmss_api.__main__:main']},
    long_description="""\
    Data storage service for DMT
    """
)

