#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from distutils.core import setup

name_ = 'symvarsub'

version_ = '0.0.2'

if '--help'in sys.argv[1:] or sys.argv[1] in (
        '--help-commands', 'egg_info', 'clean', '--version'):
    cmdclass_ = {}
    ext_modules_ = []
else:
    from pycompilation.dist import clever_build_ext
    from pycompilation.dist import CleverExtension
    import symvarsub.numtransform._setup_numtransform

    cmdclass_ = {'build_ext': clever_build_ext}
    ext_modules_ = [
        CleverExtension(
            name_+'.numtransform.transform_wrapper',
            [],
            copy_files = ['symvarsub/numtransform/transform_wrapper.pyx'],
            dist_files = [('symvarsub/numtransform/transform_template.f90', None)],
            build_callbacks = [
                (
                    symvarsub.numtransform._setup_numtransform.prebuild,
                    ('symvarsub/numtransform/transform_wrapper.pyx',), {}
                )
            ],
            link_ext=False,
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
