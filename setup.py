
import sys
import os


# Make sure we are running python3.5+
if 10 * sys.version_info[0] + sys.version_info[1] < 35:
    sys.exit("Sorry, only Python 3.5+ is supported.")


from setuptools import setup


def readme():
    print("Current dir = %s" % os.getcwd())
    print(os.listdir())
    with open('README.rst') as f:
        return f.read()

setup(
      name             =   'mgz2lut_report',
      # for best practices make this version the same as the VERSION class variable
      # defined in your ChrisApp-derived Python class
      version          =   '0.1',
      description      =   'An app to generate a report on volumes of various brain segments listed in a Look-up Table (Default = FreeSurferLUT.txt)',
      long_description =   readme(),
      author           =   'Sandip Samal',
      author_email     =   'sandip.samal@childrens.harvard.edu',
      url              =   'http://wiki',
      packages         =   ['mgz2lut_report'],
      install_requires =   ['chrisapp', 'pudb'],
      test_suite       =   'nose.collector',
      tests_require    =   ['nose'],
      scripts          =   ['mgz2lut_report/mgz2lut_report.py'],
      license          =   'MIT',
      zip_safe         =   False
     )
