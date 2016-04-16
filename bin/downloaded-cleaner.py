#!/usr/bin/env python
'''
Scan specified dir for downloading files and process the downloaded ones.
'''

import argparse
import os
import shutil
import sys
import urllib

from contextlib import closing

def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--library-dir', required=True, help='directory of media library path')
    parser.add_argument(
        '--download-dir', required=True, help='directory to scan')
    parser.add_argument(
        '--flag', required=True,
        help='extension of flag file indicates the downloading in process')
    parser.add_argument(
        '--plex-server', default='http://127.0.0.1:32400',
        help='Plex server URL (default: %(default)s)')
    parser.add_argument(
        '--plex-section', type=int, default=1,
        help='Plex library section number (default: %(default)s)')
    parser.add_argument(
        '-n', '--dry-run', action='store_true',
        help='Do nothing but print the actions')
    return parser.parse_args(argv)


def download_in_process(root_dir, subdir, flag):
    ''' check any donwloading flag file is in the sub directory '''
    return any([f.endswith(flag) for f in
                os.listdir(os.path.join(root_dir, subdir))])


def process_top_level_files(root_dir, files, flag, next_step):
    ''' Some downloaded media has no folder with '''
    rc = False

    flag_files = [f for f in files if f.endswith(flag)]
    for f, f_flag in [(f_, f_[:-len(flag)]) for f_ in flag_files]:
        files.remove(f)
        files.remove(f_flag)

    for f in files:
        next_step(os.path.join(root_dir, f))
        rc = True

    return rc


def scan_dir(directory, flag, next_step):
    ignored_dirs = ['ThunderDB']
    rc = False
    for root_dir, dirs, files in os.walk(directory):
        rc |= process_top_level_files(root_dir, files, flag, next_step)

        # process sub dirs
        for d in ignored_dirs:
            if d in dirs:
                dirs.remove(d)

        for d in dirs[:]:
            if not download_in_process(root_dir, d, flag):
                next_step(os.path.join(root_dir, d))
                rc = True
            dirs.remove(d)

    return rc


def how_to_process(library_dir, dry_run=False):
    def func(file_or_dir):
        print 'Moving %s' % file_or_dir
        if not dry_run:
            shutil.move(file_or_dir, library_dir)
    return func


def refresh_plex(server, section, dry_run=False):
    url = '%s/library/sections/%s/refresh' % (server, section)
    if dry_run:
        print 'refresh by GET %s' % url
        return

    with closing(urllib.urlopen(url)):
        pass


def main(argv):
    opts = parse_args(argv)
    something_new = scan_dir(opts.download_dir, opts.flag,
                             how_to_process(opts.library_dir, opts.dry_run))
    if something_new:
        refresh_plex(opts.plex_server, opts.plex_section, opts.dry_run)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
