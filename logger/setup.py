#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='binance-stream-logger',
    version='0.0.1',
    description='Store and serve orders',
    packages=find_packages(exclude=['test', 'test.*']),
    install_requires=[
        'nameko==2.14.0',
        'nameko-sqlalchemy==1.5.0',
        'alembic==1.0.10',
        'marshmallow==2.19.2',
        'psycopg2-binary==2.8.2',
    ],
    extras_require={
        'dev': [
            'pytest==4.5.0',
            'coverage==4.5.3',
            'flake8==4.0.1',
            'flake8-annotations==2.7.0',
        ],
    },
    zip_safe=True
)
