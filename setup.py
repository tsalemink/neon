import io
import os
import re

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'src', 'opencmiss', 'neon', '__init__.py')) as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')


def readfile(filename, split=False):
    with io.open(filename, encoding="utf-8") as stream:
        if split:
            return stream.read().split("\n")
        return stream.read()


readme = readfile("README.rst", split=True)
readme.append('License')
readme.append('=======')
readme.append('')
readme.append('')

software_licence = readfile("LICENSE")

classifiers = """\
Development Status :: 3 - Alpha
Intended Audience :: Developers
Intended Audience :: Education
Intended Audience :: Science/Research
License :: OSI Approved :: Apache Software License
Programming Language :: Python
Operating System :: Microsoft :: Windows
Operating System :: Unix
Operating System :: MacOS :: MacOS X
Topic :: Scientific/Engineering :: Medical Science Apps.
Topic :: Scientific/Engineering :: Visualization
Topic :: Software Development :: Libraries :: Python Modules
"""

requires = ['opencmiss.utils >= 0.3.0', 'PySide2', 'opencmiss.zinc', 'opencmiss.zincwidgets >= 2.1.0']

setup(
    name='opencmiss.neon',
    packages=find_packages("src"),
    package_dir={"": "src"},
    version=version,
    url='http://opencmiss.org/',
    license='Apache-2.0',
    author='Neon Developers',
    author_email='neon.developers@auckland.ac.nz',
    description='Visual editing environment for OpenCMISS.',
    long_description_content_type='text/x-rst',
    license_files=("LICENSE",),
    classifiers=filter(None, classifiers.split("\n")),
    install_requires=requires,
    entry_points={
        'console_scripts': ['neon=opencmiss.neon.neon:main'],
        'gui_scripts': ['neon-gui=opencmiss.neon.neon:main'],
    },
)
