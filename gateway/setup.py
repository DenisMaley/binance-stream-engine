#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='binance-stream-gateway',
    version='0.0.1',
    description='Gateway to the service',
    packages=find_packages(exclude=['test', 'test.*']),
    install_requires=[
        'nameko==2.14.0',
        'marshmallow==2.19.2',
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
