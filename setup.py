import sys
import os

from setuptools import setup
from distutils.sysconfig import get_python_lib

version = "1.0.0a1"

SITE_PACKAGES_PATH = os.path.relpath(get_python_lib(), sys.prefix)

setup(
    name="pwncollege_client",
    version=version,
    packages=["pwncollege_client"],
    url="https://github.com/pwn-college/client",
    description="Client for pwn.college CTFs",
    author="Connor Nelson",
    python_requires='>=3.6',
    install_requires=[
        'pwntools @ git+https://github.com/Gallopsled/pwntools@dev3',
        'requests'
    ]
)
