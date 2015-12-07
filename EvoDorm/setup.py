from distutils.core import setup
from Cython.Build import cythonize

setup(
    name = 'Seed-bank evolution simulation',
    ext_modules = cythonize("EvoDorm.pyx")
)
