import os

import logging

from pycompilation.util import run_sub_setup

from symvarsub.numtransform._setup_numtransform import main as numtransform_main


def main():
    """
    Precompile some sources to object files
    and store in `prebuilt/` directories for
    speeding up meta-programming compilations.
    """
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)


    # numtransform
    cwd = os.path.join(os.path.abspath(
        os.path.dirname(__file__)),
                       './symvarsub/numtransform/')
    run_sub_setup(cwd, numtransform_main, logger)


if __name__ == '__main__':
    main()
