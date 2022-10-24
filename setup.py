#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 16:18:30 2022

@author: apschram
"""
from setuptools import setup, find_packages

setup(name='PyPFF',
      version='0.2',
      description='PFF FC Software Development Kit for Python',
      author='PFF FC',
      author_email='fchelp@pff.com',
      url='https://github.com/pro-football-focus/pypff/',
      # packages=['pypff/'],
      packages=find_packages(),
      py_modules=['pff','normalize'],
      install_requires=['pandas','requests','pyhumps'],
      package_dir={'':'norm'},
      include_package_data=True
     )