#!/bin/env python2

'''
Shell pipe logs rotation. Reads stdin and writes data into rotated log files.
Python2 usage recomended because the script can't support byte strings
with python2 support
'''

import logging
import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from logging.handlers import RotatingFileHandler


def argument_parser():
    ''' Arguments parser
    '''

    parser = ArgumentParser(
        description=sys.modules[__name__].__doc__,
        conflict_handler='resolve',
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser_add = parser.add_argument

    parser_add(
        '-l',
        '--log',
        help='Log file path',
        required=True,
    )
    parser_add(
        '-b',
        '--bytes',
        help='Bytes per one file',
        type=int,
        default=10485760
    )
    parser_add(
        '-n',
        '--number',
        help='Number of rotated files',
        type=int,
        default=9
    )
    parser_add(
        '-t',
        '--timestamp',
        help='Enable timestamps',
        action='store_true'
    )
    parser_add(
        '-s',
        '--show',
        help='Print all logs for stdout',
        action='store_true'
    )
    parser_add(
        '-d',
        '--datefmt',
        help='Date format. It works only with enabled timestamps flag',
        default='%Y-%m-%d %H:%M:%S %z',
    )
    parser_add(
        '-f',
        '--format',
        help='Message format',
        default='[%(asctime)s]: %(message)s',
    )
    return parser.parse_args()


def logging_init(args):
    ''' Init logging subsystem
    '''
    handler = RotatingFileHandler(
        args.log,
        maxBytes=args.bytes,
        backupCount=args.number
        )

    if args.timestamp:
        formatter = logging.Formatter(
            args.format,
            datefmt=args.datefmt
            )
    else:
        formatter = logging.Formatter('%(message)s')

    handler.setFormatter(formatter)
    logging.root.handlers = [handler]


def main():
    args = argument_parser()
    logging_init(args)
    try:
        readline = sys.stdin.readline
        write = sys.stdout.write
        warning = logging.warning
        show = args.show
        while 1:
            line = readline()
            if not line:
                break
            warning(line[:-1])
            if show:
                write(line)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()
