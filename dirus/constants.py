#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Dirus Constants."""

import logging
import re

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016 Orion Labs, Inc.'


LOG_LEVEL = logging.DEBUG
LOG_FORMAT = logging.Formatter(
    '%(asctime)s dirus %(levelname)s %(name)s.%(funcName)s:%(lineno)d'
    ' - %(message)s')

SAMPLE_RATE = 44100
