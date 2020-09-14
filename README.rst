pl-mgz2LUT_report
================================

.. image:: https://badge.fury.io/py/mgz2lut_report.svg
    :target: https://badge.fury.io/py/mgz2lut_report

.. image:: https://travis-ci.org/FNNDSC/mgz2lut_report.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/mgz2lut_report

.. image:: https://img.shields.io/badge/python-3.5%2B-blue.svg
    :target: https://badge.fury.io/py/pl-mgz2lut_report

.. contents:: Table of Contents


Abstract
--------

An app to generate a report on volumes of various brain segments listed in a Look-up Table (Default = FreeSurferLUT.txt)


Synopsis
--------

.. code::

    python mgz2lut_report.py                                           \
        [-v <level>] [--verbosity <level>]                          \
        [--version]                                                 \
        [--man]                                                     \
        [--meta]                                                    \
        <inputDir>
        <outputDir> 

Description
-----------

``mgz2lut_report.py`` is a ChRIS-based application that...

Arguments
---------

.. code::

    [-v <level>] [--verbosity <level>]
    Verbosity level for app. Not used currently.

    [--version]
    If specified, print version number. 
    
    [--man]
    If specified, print (this) man page.

    [--meta]
    If specified, print plugin meta data.


Run
----

This ``plugin`` can be run in two modes: natively as a python package or as a containerized docker image.

Using PyPI
~~~~~~~~~~

To run from PyPI, simply do a 

.. code:: bash

    pip install mgz2lut_report

and run with

.. code:: bash

    mgz2lut_report.py --man /tmp /tmp

to get inline help. The app should also understand being called with only two positional arguments

.. code:: bash

    mgz2lut_report.py /some/input/directory /destination/directory


Using ``docker run``
~~~~~~~~~~~~~~~~~~~~

To run using ``docker``, be sure to assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``. *Make sure that the* ``$(pwd)/out`` *directory is world writable!*

Now, prefix all calls with 

.. code:: bash

    docker run --rm -v $(pwd)/out:/outgoing                             \
            fnndsc/pl-mgz2lut_report mgz2lut_report.py                        \

Thus, getting inline help is:

.. code:: bash

    mkdir in out && chmod 777 out
    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
            fnndsc/pl-mgz2lut_report mgz2lut_report.py                        \
            --man                                                       \
            /incoming /outgoing

Examples
--------





