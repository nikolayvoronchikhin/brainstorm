#!/usr/bin/env python
import os
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://brainstorm.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='brainstorm',
    version='0.1.0',
    description='A fresh start for the pylstm RNN library',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Klaus Greff',
    author_email='qwlouse@gmail.com',
    url='https://github.com/Qwlouse/brainstorm',
    packages=['brainstorm'],
    install_requires=['six', 'numpy'],
    tests_requires=['pytest', 'mock'],
    cmdclass={'test': PyTest},
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
    ],
)
