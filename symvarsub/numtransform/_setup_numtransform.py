from pycompilation import pyx2obj

def main(dst, **kwargs):
    # Cythonize pyx file
    return [pyx2obj('transform_wrapper.pyx', dst, only_update=True,
                    metadir=dst, **kwargs)]
