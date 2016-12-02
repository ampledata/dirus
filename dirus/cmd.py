#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Dirus Commands"""

import argparse
import json
import time

import dirus

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016 Orion Labs, Inc.'


def cli():
    parser = argparse.ArgumentParser(description='Dirus')

    parser.add_argument(
        '-c', dest='config',
        default='dirus.json',
        help='Use this config file')
    args = parser.parse_args()

    with open(args.config) as config_file:
        config = json.load(config_file)

    print 'Starting Dirus...'

    dgate = dirus.Dirus(config)

    try:
        while dgate._running:
            time.sleep(0.01)
    except KeyboardInterrupt:
        dgate.exit()
    finally:
        dgate.exit()


if __name__ == '__main__':
    cli()
