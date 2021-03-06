# -*- coding: utf-8 -*-

import os
from pycompilation.compilation import pyx2obj
from pycompilation.util import make_dirs


def prebuild(build_temp, ext_fullpath, ext, rel_src_path, **kwargs):
    # Cythonize pyx file
    src = os.path.join(build_temp, rel_src_path)
    dst = os.path.join(os.path.dirname(ext_fullpath), 'prebuilt/')
    make_dirs(dst)
    return [pyx2obj(src, dst, only_update=True, metadir=dst,
                    include_numpy=True, **kwargs)]
