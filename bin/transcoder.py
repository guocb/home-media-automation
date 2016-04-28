#!/usr/bin/env python
'''
Transcoder running in background
'''
import argparse
import os
import sys
import logging

from logging.handlers import RotatingFileHandler
from subprocess import check_output


def parse_args(argv):
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('-l', '--log-file', default='/var/log/transcoder.log',
                        help='log file name (default: %(default)s)')
    parser.add_argument('-p', '--pipe', default='/var/run/transcoder-q',
                        help='The named pipe name (default: %(default)s)')
    return parser.parse_args(argv)


def setup_logging(log_file):
    logger = logging.getLogger('Transcoder')
    logger.setLevel(logging.DEBUG)
    fh = RotatingFileHandler(log_file, maxBytes=20000000, backupCount=2)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        '%(asctime)s:%(levelname)-.1s:%(message)s'))
    logger.addHandler(fh)
    return logger


def main(argv):
    opts = parse_args(argv)
    logger = setup_logging(opts.log_file)
    logger.info('Transcoder started')
    while True:
        if not os.path.exists(opts.pipe):
            os.mkfifo(opts.pipe)

        with open(opts.pipe) as pipe_in:
            for cmd in pipe_in:
                cmd = 'nice -n 19 %s' % cmd
                logger.info('Processing: %s', cmd)
                output = check_output(cmd.split())
                logger.debug('===\n%s', output)
                logger.info('Done: %s', cmd)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
