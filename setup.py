from setuptools import setup, find_packages
import sys, os
from glob import glob

version = '0.1'

setup(name='atlastools',
      version=version,
      description="Tools for building math-atlas",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Matthew Brett',
      author_email='matthew.brett@gmail.com',
      url='',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      scripts=glob('scripts/*.py'),
      )
