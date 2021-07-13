#
# mgz2lut_report ds ChRIS plugin app
#
# (c) 2021 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#
import os
from importlib.resources import files
import sys
import nibabel as nib
import numpy as np
import collections
import re
import pandas as pd
from yattag import Doc
import pdfkit
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


    NAME

       mgz2lut_report 

    SYNOPSIS

        mgz2lut_report                                                  \\
            [--file_name <fileName>]                                    \\
            [--report_name <reportName>]                                \\
            [--report_types <reportTypes>]                              \\
            [--LUT <lookUpFile>]                                        \\
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

            docker run --rm -u $(id -u)                             \\
                -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \\
                fnndsc/pl-mgz2LUT_report mgz2lut_report             \\
                --file_name nameOfFile                              \\
                /incoming /outgoing

    DESCRIPTION

        `mgz2lut_report` is  a simple script to generate a report 
         (text,pdf, html, json) based on user's choice when an input 
         .mgz file is provided. The default look up table used is 
         FreeSurferColorLUT.txt but the user can specify their own 
         look up file using the arg <lookUpFile>

    ARGS
    
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
    An app to generate a report on volumes of various brain segments listed in a Look-up Table (Default = FreeSurferColorLUT.txt).
    """
    PACKAGE                 = __package__
    TITLE                   = 'A ChRIS plugin app'
    CATEGORY                = ''
    TYPE                    = 'ds'
    ICON                    = '' # url of an icon image
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
        self.add_argument('--file_name',
                             dest='file_name',
                             type = str,
                             optional = True, 
                             help="Segmented mgz file name",
                             default="aparc.a2009s+aseg.mgz")
                             
        self.add_argument('--report_name', 
                             dest='report_name',
                             type = str,
                             optional = True, 
                             help="Output report name", 
                             default="mgz2LUT_report")
                             
        self.add_argument('--report_types', 
                             dest='report_types',
                             type = str,
                             optional = True,
                             help="comma separated output report file types", 
                             default="txt")
                             
        self.add_argument('--LUT',
                             dest='LUT',
                             type = str,
                             optional = True, 
                             help="Look Up File Name", 
                             default="FreeSurferColorLUT.txt")
                             
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
            report_columns = ['Index','Label Name', 'Volume (in cc)']
            rep = pd.DataFrame(columns = report_columns)
            line_count = 1
            ## Create an HTML report
            if report_type == 'html' or report_type == 'pdf':
                doc, tag, text = Doc().tagtext()
                with tag('html'):
                    with tag('head'):
                        with tag('link',rel='stylesheet' ,href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css"):
                            with tag('style'):
                                text('body{margin:0 100; background:whitesmoke;}')
                    with tag('body'):
                        with tag('h1'):
                            text('Brain Segmentation Report')
                        with tag('table', id = 'main', klass='table table-striped table-hover',text='report'):
                            with tag('thead',klass='thead-dark'):
                                with tag('tr'):
                                    with tag('th',scope='col'):
                                        text('Index')
                                    with tag('th',scope='col'):
                                        text('Label Name')    
                                    with tag('th',scope='col'):
                                        text('Volume (in cc)')
                            for k in sorted(counter.keys()):
                                res_df=df_FSColorLUT.loc[df_FSColorLUT['#No'] == str(k),['LabelName']]

                                with tag('tr'):
                                    with tag('td'):
                                        text(line_count)
                                    with tag('td'):
                                        text(res_df['LabelName'].to_string(index=False))
                                    with tag('td'):
                                        text(round(counter[k]/1000,1))
                                line_count = line_count + 1
                result = doc.getvalue()
                f.write(result)
                if report_type == 'pdf':
                    f = open("/tmp/report.html",'a')
                    f.write(result)
                    opt = {
                        'quiet':''
                        }
                    pdfkit.from_file("/tmp/report.html",report_path,options=opt)
                continue;
            for k in sorted(counter.keys()):
                res_df=df_FSColorLUT.loc[df_FSColorLUT['#No'] == str(k),['LabelName']]

                rep.loc[len(rep)]= [line_count, res_df['LabelName'].to_string(index=False),round(counter[k]/1000,1)]
                line_count = line_count + 1
            if report_type == 'json':
                rep = rep.to_json(orient='index')
                f.write(rep)
            elif report_type == 'csv':
                f.write(rep.to_csv(index=False))
            else:
                f.write(rep.to_string(index=False))
            f.close()
        
        f = open(report_path,'r')
        #print(f.read())
        print("Report saved as %s/%s in %s format(s)" %(options.outputdir,options.report_name, options.report_types))
        
    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)
