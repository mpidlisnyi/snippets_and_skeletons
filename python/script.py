#!/bin/env python3

'''
Simple commandline script with args, configuration file validation and logging
'''

import logging
import traceback
import sys
from yaml import load
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from os import getcwd
from logging.handlers import RotatingFileHandler


SCHEMA = {
    'log': {
        'file': str,
        'level': 'INFO',
        },
    'mysql': {
        'host': str,
        'port': int,
        'user': str,
        'passwd': str,
        'db': str,
        },
    }


def config_parser(configfile, schema):
    ''' Configuration parser
    '''
    def config_check(config_sub, schema_sub, path=''):
        ''' Validate configuration file with the schema
        '''
        for key, value in schema_sub.iteritems():
            full_key = '.'.join([path, key])
            typ = type(value)
            if typ is type:
                typ = value
                if key not in config_sub.keys():
                    raise KeyError('the key "%s" is absent' % full_key)
            else:
                if key not in config_sub.keys():
                    config_sub[key] = value

            if isinstance(config_sub[key], typ):
                if typ is dict:
                    config_sub[key] = config_check(
                        config_sub[key],
                        value,
                        '%s' % full_key
                        )
            else:
                raise TypeError('the key "%s" must be %s' % (full_key, typ))
        return config_sub

    with open(configfile) as conf_file:
        conf = load(conf_file.read())

    return config_check(conf, schema)


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
        '-c',
        '--config',
        help='path to configuration file. (from cwd by default)',
        default='%s/.config.yaml' % getcwd(),
    )
    parser_add(
        '-e',
        '--environment',
        help='environment',
        choices=[
            'prod',
            'stg',
            'qa',
            'dev',
            ],
        required=True,
    )
    return parser.parse_args()


def logging_init(logfile, loglevel, maxBytes=10485760, backupCount=10):
    ''' Init logging subsystem
    '''
    if loglevel and loglevel in ['DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL']:
        level = getattr(logging, loglevel)
    else:
        level = getattr(logging, 'CRITICAL')
    if logfile:
        handler = RotatingFileHandler(
            logfile,
            maxBytes=maxBytes,
            backupCount=backupCount
            )
        logging.basicConfig(
            level=level
            )
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S %Z'
            )
        handler.setFormatter(formatter)
        logging.root.handlers = [handler]
        logging.basicConfig(
            level=level
            )
    else:
        logging.basicConfig(
            format='%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S %Z',
            level=level
            )


def main():
    args = argument_parser()
    config = config_parser(args.config, SCHEMA)
    logging_init(
        config['log']['file'],
        config['log']['level'],
        args.environment
        )
    try:
        logging.info('starting')
        # do something here
    except Exception:
        logging.critical('script failed')
        logging.critical(traceback.format_exc())
    else:
        logging.info('successful done')


if __name__ == '__main__':
    main()
