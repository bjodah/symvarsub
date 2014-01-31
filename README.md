symvarsub
=========
[![Build Status](https://travis-ci.org/bjodah/symvarsub.png?branch=master)](
https://travis-ci.org/bjodah/symvarsub)

symvarsub collects routines useful for performing variable
subsitutions in collections of SymPy expressions. 

It provides an alternative to sympy.utilities.lambdify, its main
benefit is much faster compile times thanks to caching of object file.

Installation
------------
E.g. do:

    pip install --user --upgrade -r http://raw.github.com/bjodah/symvarsub/master/requirements.txt
    pip install --user --upgrade http://github.com/bjodah/symvarsub/archive/v0.0.9.tar.gz

(modify to your needs)

Related projects
----------------
* [fastinverse](http://github.com/bjodah/fastinverse) generating C
  code for fast calculation of inverses (table lookup -> polynomial
  interpolation -> newton refinement) 

## License
Open Source. Released under the very permissive simplified (2-clause)
BSD license. See LICENCE.txt for further details. 
