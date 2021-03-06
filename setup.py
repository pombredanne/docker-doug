#!/usr/bin/python
from setuptools import setup, find_packages
setup(
    name = 'libdoug',
    version = '0.4',
    packages = find_packages(),
    scripts = ['doug-cli'],
    install_requires = ['requests<2.5.0', 'docker-py', 'clint'],
    package_data = {
	'': ['LICENSE', 'README.md', 'VERSION']
    },
    author = 'Pavel Odvody',
    author_email = 'podvody@redhat.com',
    description = 'High level library around Docker Daemon, Registry and Hub',
    license = 'GNU/GPLv2',
    keywords = 'docker cli updates',
    url = 'https://github.com/shaded-enmity/docker-doug'
)
