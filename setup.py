#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from distutils.core import setup

name_ = 'symvarsub'

version_ = '0.0.9'

if '--help'in sys.argv[1:] or sys.argv[1] in (
        '--help-commands', 'egg_info', 'clean', '--version'):
    cmdclass_ = {}
    ext_modules_ = []
else:
    import numpy
    from pycompilation.dist import clever_build_ext
    from pycompilation.dist import CleverExtension
    from symvarsub.numtransform._setup_numtransform import prebuild

    cmdclass_ = {'build_ext': clever_build_ext}
    ext_modules_ = [
        CleverExtension(
            name_+'.numtransform.transform_wrapper',
            sources=[],
            include_dirs=[numpy.get_include()],
            build_files = ['./symvarsub/numtransform/transform_wrapper.pyx'],
            dist_files = [('./symvarsub/numtransform/transform_template.f90', None)],
            build_callbacks = [
                (
                    prebuild,
                    ('./symvarsub/numtransform/transform_wrapper.pyx',), {}
                )
            ],
            link_ext=False,
            logger=True,
        )
    ]

setup(
    name=name_,
    version=version_,
    author='Björn Dahlgren',
    author_email='bjodah@DELETEMEgmail.com',
    description='Convenience functions for use with sympy.',
    license = "BSD",
    url='https://github.com/bjodah/'+name_,
    download_url='https://github.com/bjodah/'+name_+'/archive/v'+version_+'.tar.gz',
    packages=['symvarsub', 'symvarsub.numtransform'],
    ext_modules=ext_modules_,
    cmdclass = cmdclass_
)
