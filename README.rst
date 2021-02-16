
                      _____  _       _                               _   
                     / __  \| |     | |                             | |  
 _ __ ___   __ _ ____`' / /'| |_   _| |_   _ __ ___ _ __   ___  _ __| |_ 
| '_ ` _ \ / _` |_  /  / /  | | | | | __| | '__/ _ \ '_ \ / _ \| '__| __|
| | | | | | (_| |/ / ./ /___| | |_| | |_  | | |  __/ |_) | (_) | |  | |_ 
|_| |_| |_|\__, /___|\_____/|_|\__,_|\__| |_|  \___| .__/ \___/|_|   \__|
            __/ |                     ______       | |                   
           |___/                     |______|      |_|                   

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

Description
-----------

``mgz2lut_report`` is  a ChRIS DS plugin to generate a report 
(text,pdf, html, json) based on user's choice when an input 
.mgz file is provided. The default look up table used is 
FreeSurferColorLUT.txt but the user can specify their own 
look up file using the arg <lookUpFile>


Usage
--------

.. code::

    mgz2lut_report                                                  \
        [--file_name <fileName>]                                    \
        [--report_name <reportName>]                                \
        [--report_types <reportTypes>]                              \
        [--LUT <lookUpFile>]                                        \
        [-v <level>] [--verbosity <level>]                          \
        [--version]                                                 \
        [--man]                                                     \
        [--meta]                                                    \
        <inputDir>
        <outputDir> 

Arguments
---------

.. code::

    [--file_name <fileName>]
    Specify the path of the input mgz file here
                                            
    [--report_name <reportName>]
    If specified, creates an o/p in reportName
    Default report name is mgz2LUT_report
                                        
    [--report_types <reportTypes>]
    Specify comma separated file types to generate multiple reports
    You can specify txt, json, pdf, html
    Default is txt
                                      
    [--LUT <lookUpFile>]
    If specified, the lookUpFile is referred instead to default LUT
    Default LUT is FreeSurferColorLUT.txt            

    [-v <level>] [--verbosity <level>]
    Verbosity level for app. Not used currently.

    [--version]
    If specified, print version number. 
    
    [--man]
    If specified, print (this) man page.

    [--meta]
    If specified, print plugin meta data.
    
    
    Getting inline help is 
    
    .. code::
    
        docker run --rm fnndsc/pl-mgz2lut_report mgz2lut_report --man


Development
------------

Build the Docker container 

.. code:: bash

    docker build -t local/pl-mgz2lut_report .
    
Python dependencies can be added to ``setup.py``. After a successful build,
track which dependencies you have installed by generating the ``requirements.txt`` file

.. code:: bash

    docker run --rm local/pl-mgz2lut_report -m pip freeze > requirements.txt 
    
    
For the sake of reproducible builds, ensure that ``requirements.txt`` is up-to-date 
before you publish your code.

.. code:: bash
    
    git add requirements.txt && git commit -m "Bump requirements.txt" && git push
    


Run
---
Assuming that we have mgz files in the `in` directory named ``myFile.mgz``

.. code:: bash

    mkdir in out && chmod 777 out
    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
            fnndsc/pl-mgz2lut_report mgz2lut_report.py                  \
            --file_name myFile.mgz                                      \
            /incoming /outgoing







