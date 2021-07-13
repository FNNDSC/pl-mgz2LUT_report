from os import path
from setuptools import setup

with open(path.join(path.dirname(path.abspath(__file__)), 'README.rst')) as f:
    readme = f.read()

setup(
    name             = 'mgz2lut_report',
    version          = '1.2.5',
    description      = 'An app to generate a report on volumes of various brain segments listed in a Look-up Table (Default =     FreeSurferColorLUT.txt',
    long_description = readme,
    author           = 'Sandip Samal',
    author_email     = 'sandip.samal@childrens.harvard.edu',
    url              = 'https://github.com/FNNDSC/pl-mgz2LUT_report',
    packages         = ['mgz2lut_report'],
    install_requires = ['chrisapp'],
    test_suite       = 'nose.collector',
    tests_require    = ['nose'],
    license          = 'MIT',
    zip_safe         = False,
    python_requires  = '>=3.8',
    package_data     = {
        'mgz2lut_report': ['assets/*']
    },
    entry_points     = {
        'console_scripts': [
            'mgz2lut_report = mgz2lut_report.__main__:main'
            ]
        }
)

