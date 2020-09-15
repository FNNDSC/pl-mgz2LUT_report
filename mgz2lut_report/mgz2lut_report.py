#!/usr/bin/env python                                            
#
# mgz2lut_report ds ChRIS plugin app
#
# (c) 2016-2019 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#


import os
import sys
import nibabel as nib
import numpy as np
import collections
import re
import pandas as pd
sys.path.append(os.path.dirname(__file__))

# import the Chris app superclass
from chrisapp.base import ChrisApp


Gstr_title = """
                      _____  _       _                               _   
                     / __  \| |     | |                             | |  
 _ __ ___   __ _ ____`' / /'| |_   _| |_   _ __ ___ _ __   ___  _ __| |_ 
| '_ ` _ \ / _` |_  /  / /  | | | | | __| | '__/ _ \ '_ \ / _ \| '__| __|
| | | | | | (_| |/ / ./ /___| | |_| | |_  | | |  __/ |_) | (_) | |  | |_ 
|_| |_| |_|\__, /___|\_____/|_|\__,_|\__| |_|  \___| .__/ \___/|_|   \__|
            __/ |                     ______       | |                   
           |___/                     |______|      |_|                   

"""

Gstr_synopsis = """

(Edit this in-line help for app specifics. At a minimum, the 
flags below are supported -- in the case of DS apps, both
positional arguments <inputDir> and <outputDir>; for FS apps
only <outputDir> -- and similarly for <in> <out> directories
where necessary.)

    NAME

       mgz2lut_report.py 

    SYNOPSIS

        python mgz2lut_report.py                                         \\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            <inputDir>                                                  \\
            <outputDir> 

    BRIEF EXAMPLE

        * Bare bones execution

            mkdir in out && chmod 777 out
            python mgz2lut_report.py   \\
                                in    out

    DESCRIPTION

        `mgz2lut_report.py` ...

    ARGS

        [-h] [--help]
        If specified, show help message and exit.
        
        [--json]
        If specified, show json representation of app and exit.
        
        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.
        
        [--savejson <DIR>] 
        If specified, save json representation file to DIR and exit. 
        
        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.
        
        [--version]
        If specified, print version number and exit. 

"""


class Mgz2lut_report(ChrisApp):
    """
    An app to generate a report on volumes of various brain segments listed in a Look-up Table (Default = FreeSurferLUT.txt).
    """
    AUTHORS                 = 'Sandip Samal (sandip.samal@childrens.harvard.edu)'
    SELFPATH                = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC                = os.path.basename(__file__)
    EXECSHELL               = 'python3'
    TITLE                   = 'A segmented mgz reporting app'
    CATEGORY                = ''
    TYPE                    = 'ds'
    DESCRIPTION             = 'An app to generate a report on volumes of various brain segments listed in a Look-up Table (Default = FreeSurferLUT.txt)'
    DOCUMENTATION           = 'http://wiki'
    VERSION                 = '0.1'
    ICON                    = '' # url of an icon image
    LICENSE                 = 'Opensource (MIT)'
    MAX_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MAX_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """
        self.add_argument('--file_name', dest='file_name',type = str,optional = True, help="Segmented mgz file name", default="aparc.a2009s+aseg.mgz")
        self.add_argument('--report_name', dest='report_name',type = str,optional = True, help="Output report name", default="mgz2LUT_report")
        self.add_argument('--report_types', dest='report_types',type = str,optional = True, help="comma separated output report file types", default="pdf")
        self.add_argument('--LUT', dest='LUT',type = str,optional = True, help="Look Up File Name", default="FreeSurferColorLUT.txt")
    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print('Version: %s' % self.get_version())
        file_path = os.path.join(options.inputdir,options.file_name)
        # Load the file
        print("Loading file from %s" %file_path)
        mgz_file = nib.load(file_path)

        npy_file = mgz_file.get_fdata()
        npy_file = npy_file.astype(np.uint32)

        data_list=npy_file.flatten()
        counter=collections.Counter(data_list)

        # Load Look Up file
        print("Loading look up file from %s" %options.LUT)
        l_column_names = ["#No", "LabelName","R","G","B"]
        df_FSColorLUT = pd.DataFrame(columns=l_column_names)
        with open(options.LUT) as f:
            for line in f:
                if line and line[0].isdigit():
                    line = re.sub(' +', ' ', line)
                    l_line = line.split(' ')
                    l_labels = l_line[:5]
                    df_FSColorLUT.loc[len(df_FSColorLUT)] = l_labels
                    
        # split the report types
        report_types = options.report_types.split(',')
        for report_type in report_types:
            
            report_path = ("%s/%s.%s" %(options.outputdir,options.report_name,report_type))
            # Write and Save report
            print("Writing report as %s" %report_path)
            f = open(report_path,'a')
            f.truncate(0)
            f.write("Index \t Label Name \t Volume \n")
            line_count = 1
            for k in sorted(counter.keys()):
                res_df=df_FSColorLUT.loc[df_FSColorLUT['#No'] == str(k),['LabelName']]

                f.write ("%s\t%s\t%s%s" %(line_count, res_df['LabelName'].to_string(index=False),counter[k] ,"cc"))
                f.write('\n')
                line_count = line_count + 1
            f.close()
        
        f = open(report_path,'r')
        print(f.read())
        print("Report saved as %s in %s format(s)" %(options.report_name, options.report_types))
    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)


# ENTRYPOINT
if __name__ == "__main__":
    chris_app = Mgz2lut_report()
    chris_app.launch()
