import os
import re
import io

from setuptools import setup


def get_version(filename):

    here = os.path.dirname(os.path.abspath(__file__))
    f = open(os.path.join(here, filename))
    version_match = f.read()
    f.close()

    if version_match:
        return version_match
    raise RuntimeError("Unable to find version string.")



setup(name='pytest-excel',
      version=get_version('version.txt'),
      description='pytest plugin for generating excel reports',
      long_description=io.open('README.rst', encoding='utf-8', errors='ignore').read(),
      author='santosh',
      author_email=u'santosh.srikanta@gmail.com',
      url=u'https://github.com/ssrikanta/pytest-excel',
      packages=['pytest_excel'],
      entry_points={'pytest11': ['excel = pytest_excel.pytest_excel']},
      install_requires=['pytest>=2.7', 'openpyxl'],
      keywords='py.test pytest excel report',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Framework :: Pytest',
          'Intended Audience :: Developers',
          'Operating System :: POSIX',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: MacOS :: MacOS X',
          'Topic :: Software Development :: Testing',
          'Topic :: Software Development :: Quality Assurance',
          'Topic :: Software Development :: Libraries',
          'Topic :: Utilities',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ]
      )

