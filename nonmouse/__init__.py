#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from nonmouse import *
import os, glob

__copyright__    = 'Copyright (C) 2026 CeatursHarmginton'
__version__      = '3.0.0'
__license__      = 'Apache-2.0'
__author__       = 'CeatursHarmginton'
__author_email__ = ''
__url__          = 'https://github.com/CeatursHarmginton/camera-mouse-controller'

__all__ = [
    os.path.split(os.path.splitext(file)[0])[1]
    for file in glob.glob(os.path.join(os.path.dirname(__file__), '[a-zA-Z0-9]*.py'))
]