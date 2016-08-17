import os
import re
import codecs

from setuptools import setup


def get_version(filename):

    here = os.path.dirname(os.path.abspath(__file__))
    f = codecs.open(os.path.join(here, filename), encoding='utf-8')
    version_file = f.read()
    f.close()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")



setup(name='pytest-excel',
      version=get_version('pytest_excel.py'),
      description='pytest plugin for generating excel reports',
      long_description=open('README.rst').read(),
      author='santosh',
      author_email='santosh.srikanta@gmail.com',
      url='https://github.com/ssrikanta/pytest-excel',
      packages=['pytest_excel'],
      entry_points={'pytest11': ['excel = pytest_excel']},
      install_requires=['pytest>=2.3', 'openpyxl'],
      keywords='py.test pytest excel report',
      classifiers=[
          'Development Status :: 1 - Alpha',
          'Framework :: Pytest',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: POSIX',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: MacOS :: MacOS X',
          'Topic :: Software Development :: Testing',
          'Topic :: Software Development :: Libraries',
          'Topic :: Utilities',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: Implementation :: PyPy',
      ]
      )

