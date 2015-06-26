#someone always prefers setuptools over distutils.core
import os, json
#from distutils.core import setup #must import find_package

from setuptools import setup, find_packages
from os.path import join, dirname

#######################################################
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
	    name = 'mppt',
	    author= 'Kevron Rees, Ryan Kapur',
	    author_email = 'kevron.rees@intel.com',
	    version = '1.0',
	    date_created = '6/19/2015',
	    long_description=read('README.txt'),
	    packages = {'python'},
	    url = 'https://github.com/tripzero/mppt',
	    py_modules = ['python.pwm_funcs',
	    			 'python.tracker_funcs',
	    			 'python.ina219',
	    			 'python.mppt'],
	    #'python.config.json',
	    license = 'Intel',

		install_requires = ['autobahn'], 

		classifiers = [
			'Development Status :: 3 - Alpha',
	    	'Intended Audience :: Developers',
			'Programming Language :: Python :: 3',
	        'Programming Language :: Python :: 3.2',
	        'Programming Language :: Python :: 3.3',
			'Programming Language :: Python :: 3.4',
		]
	)
