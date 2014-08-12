# #!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import re
import os
from setuptools import setup, find_packages


def parse_requirements():
    """
    Rudimentary parser for the `requirements.txt` file

    We just want to separate regular packages from links to pass them to the
    `install_requires` and `dependency_links` params of the `setup()`
    function properly.
    """
    try:
        requirements = \
            map(str.strip, local_file('requirements.txt'))
    except IOError:
        raise RuntimeError("Couldn't find the `requirements.txt' file :(")

    links = []
    pkgs = []
    for req in requirements:
        if not req:
            continue
        if 'http:' in req or 'https:' in req:
            links.append(req)
            name, version = re.findall("\#egg=([^\-]+)-(.+$)", req)[0]
            pkgs.append('{0}=={1}'.format(name, version))
        else:
            pkgs.append(req)

    return pkgs, links

local_file = lambda f: \
    open(os.path.join(os.path.dirname(__file__), f)).readlines()


if __name__ == '__main__':

    packages = find_packages(exclude=['*tests*'])
    pkgs, links = parse_requirements()

    setup(
        name="pyeqs",
        license="MIT",
        version='0.11.0',
        description=u'Django Querysets-esque implementation for Elasticsearch',
        author=u'Andrew Gross',
        author_email=u'andrew.w.gross@gmail.com',
        include_package_data=True,
        url='https://github.com/yipit/pyeqs',
        packages=packages,
        install_requires=pkgs,
        classifiers=(
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT',
            'Natural Language :: English',
            'Operating System :: Microsoft',
            'Operating System :: POSIX',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
        )
    )
