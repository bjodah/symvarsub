#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import sys
from setuptools import setup
from symvarsub.numtransform import NumTransformer

pkg_name = 'symvarsub'

cmdclass = {}
ext_modules = []


def _path_under_setup(*args):
    return os.path.join(os.path.dirname(__file__), *args)


if len(sys.argv) > 1 and '--help' not in sys.argv[1:] and sys.argv[1] not in (
        '--help-commands', 'egg_info', 'clean', '--version'):
    from pycodeexport import pce_build_ext, PCEExtension
    from symvarsub.numtransform._setup_numtransform import prebuild

    cmdclass = {'build_ext': pce_build_ext}
    ext_modules = [
        PCEExtension(
            pkg_name + '.numtransform.transform_wrapper',
            sources=[],
            build_files=[_path_under_setup('symvarsub', 'numtransform',
                                           'transform_wrapper.pyx')],
            dist_files=[(_path_under_setup('symvarsub', 'numtransform', 'transform_template.f90'),
                         None)],
            build_callbacks=[
                (
                    prebuild,
                    (_path_under_setup('symvarsub', 'numtransform', 'transform_wrapper.pyx'),), {}
                )
            ],
            link_ext=False,
            logger=True,
        )
    ]

RELEASE_VERSION = os.environ.get('SYMVARSUB_RELEASE_VERSION', '')

# http://conda.pydata.org/docs/build.html#environment-variables-set-during-the-build-process
CONDA_BUILD = os.environ.get('CONDA_BUILD', '0') == '1'
if CONDA_BUILD:
    try:
        RELEASE_VERSION = 'v' + open(
            '__conda_version__.txt', 'rt').readline().rstrip()
    except IOError:
        pass

release_py_path = os.path.join(pkg_name, '_release.py')

if len(RELEASE_VERSION) > 1 and RELEASE_VERSION[0] == 'v':
    TAGGED_RELEASE = True
    __version__ = RELEASE_VERSION[1:]
else:
    TAGGED_RELEASE = False
    # read __version__ attribute from _release.py:
    exec(open(release_py_path).read())

classifiers = [
    "Development Status :: 3 - Alpha",
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Mathematics',
]

pkgs = [
    pkg_name,
    pkg_name + '.numtransform'
]

tests = [
    'symvarsub.tests',
]

descr = 'Convenience functions for use with sympy.'
deps = ['pycompilation', 'pycodeexport', 'numpy', 'sympy', 'mako',
        'cython', 'future']
setup_kwargs = dict(
    name=pkg_name,
    version=__version__,
    description=descr,
    classifiers=classifiers,
    author='Björn Dahlgren',
    author_email='bjodah@DELETEMEgmail.com',
    url='https://github.com/bjodah/' + pkg_name,
    license='BSD',
    packages=pkgs + tests,
    ext_modules=ext_modules,
    cmdclass=cmdclass,
    setup_requires=deps,
    install_requires=deps,
    eager_resources=[os.path.join('symvarsub', 'numtransform', path)
                     for path in NumTransformer.build_files],
)

if __name__ == '__main__':
    try:
        if TAGGED_RELEASE:
            # Same commit should generate different sdist
            # depending on tagged version (set SYMVARSUB_RELEASE_VERSION)
            # this will ensure source distributions contain the correct version
            shutil.move(release_py_path, release_py_path+'__temp__')
            open(release_py_path, 'wt').write(
                "__version__ = '{}'\n".format(__version__))
        setup(**setup_kwargs)
    finally:
        if TAGGED_RELEASE:
            shutil.move(release_py_path+'__temp__', release_py_path)
