from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

sourcefiles = ['allsat.pyx', 'main.c', 'solver.c','bdd_reduce.c', 'list.c','my_hash.c', 'obdd.c','trie.c']

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("allsat", sourcefiles,extra_compile_args=['-w'])]
)
