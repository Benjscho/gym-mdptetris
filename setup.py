from setuptools import setup
from distutils.core import setup
from Cython.Build import cythonize


setup(name='gym_mdptetris',
      version='0.0.2',
      install_requires=['gym'],
      author="Ben Schofield",
      license='MIT',
      ext_modules=cythonize('gym_mdptetris/envs/*.pyx'))
