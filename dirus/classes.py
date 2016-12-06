#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Dirus Classes."""

import os
import logging
import logging.handlers
import subprocess
import tempfile
import threading
import time

import dirus

__author__ = 'Greg Albrecht W2GMD <oss@undef.net>'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2016 Orion Labs, Inc.'


class Dirus(threading.Thread):

    """Dirus Class."""

    _logger = logging.getLogger(__name__)
    if not _logger.handlers:
        _logger.setLevel(dirus.LOG_LEVEL)
        _console_handler = logging.StreamHandler()
        _console_handler.setLevel(dirus.LOG_LEVEL)
        _console_handler.setFormatter(dirus.LOG_FORMAT)
        _logger.addHandler(_console_handler)
        _logger.propagate = False

    def __init__(self, config):
        threading.Thread.__init__(self)
        self.config = config
        self.direwolf_conf = None
        self.processes = {}
        self.daemon = True
        self._stop = threading.Event()

    def __del__(self):
        self.stop()

    def _write_direwolf_conf(self):
        tmp_fd, self.direwolf_conf = tempfile.mkstemp(
            prefix='dirus_', suffix='.conf')
        os.write(tmp_fd, "ADEVICE null null\n")
        os.close(tmp_fd)

    def run(self):
        self._write_direwolf_conf()

        # Allow use of 'rx_fm' for Soapy/HackRF
        rtl_cmd = self.config['rtl'].get('command', 'rtl_fm')

        frequency = "%sM" % self.config['rtl']['frequency']
        sample_rate = self.config['rtl'].get('sample_rate', dirus.SAMPLE_RATE)
        ppm = self.config['rtl'].get('ppm')
        gain = self.config['rtl'].get('gain')
        device_index = self.config['rtl'].get('device_index', '0')

        if bool(self.config['rtl'].get('offset_tuning')):
            enable_option = 'offset'
        else:
            enable_option = 'none'

        src_cmd = [rtl_cmd]
        src_cmd.extend(('-f', frequency))
        src_cmd.extend(('-s', sample_rate))
        src_cmd.extend(('-E', enable_option))
        src_cmd.extend(('-d', device_index))

        if ppm is not None:
            src_cmd.extend(('-p', ppm))

        if gain is not None:
            src_cmd.extend(('-g', gain))

        src_cmd.append('-')

        src_cmd = map(str, src_cmd)

        self._logger.debug('src_cmd="%s"', ' '.join(src_cmd))

        src_proc = subprocess.Popen(
            src_cmd,
            stdout=subprocess.PIPE
        )

        self.processes['src'] = src_proc

        direwolf_cmd = ['direwolf']

        # Configuration file name.
        direwolf_cmd.extend(('-c', self.direwolf_conf))
        # Text colors.  1=normal, 0=disabled.
        direwolf_cmd.extend(('-t', 0))
        # Number of audio channels, 1 or 2.
        direwolf_cmd.extend(('-n', 1))
        # Bits per audio sample, 8 or 16.
        direwolf_cmd.extend(('-b', 16))
        # Read from STDIN.
        direwolf_cmd.append('-')

        direwolf_cmd = map(str, direwolf_cmd)

        self._logger.debug('direwolf_cmd="%s"', ' '.join(direwolf_cmd))

        direwolf_proc = subprocess.Popen(
            direwolf_cmd,
            stdin=self.processes['src'].stdout,
            stdout=subprocess.PIPE
        )

        self.processes['direwolf'] = direwolf_proc

        while not self.stopped():
            time.sleep(0.01)

    def stop(self):
        """
        Stop the thread at the next opportunity.
        """
        for name in ['direwolf', 'src']:
            try:
                proc = self.processes[name]
                proc.terminate()
            except Exception as ex:
                self._logger.exception(
                    'Raised Exception while trying to terminate %s: %s',
                    name, ex)
        self._stop.set()

    def stopped(self):
        """
        Checks if the thread is stopped.
        """
        return self._stop.isSet()
