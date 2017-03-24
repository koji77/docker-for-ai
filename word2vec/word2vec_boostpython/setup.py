#!/usr/bin/env python
# setup.py
from distutils.core import setup, Extension
import numpy

module = Extension(
    'word2vec_boostpython',
    sources = ['word2vec.cpp'],
    include_dirs = ['/usr/include/boost', numpy.get_include()],
    library_dirs = ['/usr/lib'],
    libraries = ['boost_python'],
)

setup(
    name = 'word2vec_boostpython',
    version = '0.01',
    ext_modules = [module],
)
