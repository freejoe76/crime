#!/usr/bin/env python
from setuptools import setup, Command
import subprocess


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        errno = subprocess.call(['py.test'])
        raise SystemExit(errno)

setup(
    name='CrimeParse',
    version='0.2',
    description='A crime parser for the City of Denver crime CSV.',
    license='Apache',
    url='https://github.com/freejoe76/crime',
    author='Joe Murphy',
    author_email='joe.murphy@gmail.com',
    packages=['crimeparse'],
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    )
