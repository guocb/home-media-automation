#!/usr/bin/env python
'''
Scan specified dir for downloading files and process the downloaded ones.
'''

import argparse
import os
import shutil
import sys


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--library-dir', required=True, help='directory of media library path')
    parser.add_argument(
        '--download-dir', required=True, help='directory to scan')
    parser.add_argument(
        '--flag', required=True,
        help='extension of flag file indicates the downloading in process')
    return parser.parse_args(argv)


def download_in_process(root_dir, subdir, flag):
    ''' check any donwloading flag file is in the sub directory '''
    return any([f.endswith(flag) for f in
                os.listdir(os.path.join(root_dir, subdir))])


def process_top_level_files(root_dir, files, flag, next_step):
    ''' Some downloaded media has no folder with '''
    flag_files = [f for f in files if f.endswith(flag)]
    for f, f_flag in [(f_, f_[:-len(flag)]) for f_ in flag_files]:
        files.remove(f)
        files.remove(f_flag)

    for f in files:
        next_step(os.path.join(root_dir, f))


def scan_dir(directory, flag, next_step):
    for root_dir, dirs, files in os.walk(directory):
        process_top_level_files(root_dir, files, flag, next_step)

        # process sub dirs
        for d in dirs[:]:
            if not download_in_process(root_dir, d, flag):
                next_step(os.path.join(root_dir, d))
            dirs.remove(d)


def how_to_process(library_dir):
    def func(file_or_dir):
        print 'Moving %s' % file_or_dir
        shutil.move(file_or_dir, library_dir)
    return func


def main(argv):
    opts = parse_args(argv)
    scan_dir(opts.download_dir, opts.flag, how_to_process(opts.library_dir))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
