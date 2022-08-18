#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 16:18:30 2022

@author: apschram
"""
from setuptools import setup

setup(name='PyPFF',
      version='0.1',
      description='PFF FC Software Development Kit for Python',
      author='Alexander Schram',
      author_email='alexander.schram@pff.com',
      url='https://github.com/pro-football-focus/pypff/',
      packages=['get'],
      py_modules=['functions'],
      install_requires=['pandas','requests']
     )