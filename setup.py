import os
import sys
import subprocess
import numpy 

from setuptools import setup
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

args = sys.argv[1:]

if "cleanall" in args:
    print("Removing Cython build files...")
    subprocess.Popen("rm -rf build && rm -rf ./gym_mdptetris/envs/*.c && rm -rf ./gym_mdptetris/envs/*.so", shell=True, executable="/bin/bash")

    sys.argv[1] = "clean"

if args.count("build_ext") > 0 and args.count("--inplace") == 0:
    sys.argv.insert(sys.argv.index("build_ext")+1, "--inplace")

setup(name='gym_mdptetris',
    version='0.0.2',
    install_requires=['gym'],
    author="Ben Schofield",
    license='MIT',
    ext_modules=cythonize([Extension("*.pyx", ['gym_mdptetris/envs/*.pyx'], include_dirs=[numpy.get_include()])]))
