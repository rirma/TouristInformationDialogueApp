from setuptools import setup, find_packages,Command
from codecs import open
from os import path
import os
import subprocess
from distutils.command.build import build as _build


INSTALL_COMMAND = os.path.join(os.path.dirname(__file__),'pyjtalk/build.sh')


class build(_build):
    sub_commands=_build.sub_commands + [('CustomCommands',None)]

class CustomCommands(Command):
  def initialize_options(self):
    pass

  def finalize_options(self):
    pass

  def run(self):
    subprocess.run(INSTALL_COMMAND,shell=True,check=True)

setup(
    name='pyjtalk',

    version='1.1.3',

    description='Open-Jtalk Python wrapper',

    url='https://github.com/garicchi/pyjtalk',

    author='garicchi',
    author_email='xgaricchi@gmail.com',

    license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],

    python_requires='>=3',

    keywords='pyjtalk open-jtalk',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    
    install_requires=[],
    
    extras_require={},

    package_data={},

    entry_points={},

    cmdclass={
        #'build':build,
        #'CustomCommands':CustomCommands
    }
)
