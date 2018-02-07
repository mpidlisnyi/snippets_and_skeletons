#!/bin/env python3
#
# Simple command line script with args parsing, configuration file validation
# and logging
#
import logging
import traceback
from yaml import load
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from os import getcwd


SCHEMA = {
        'log': {
            'file': str,
            'level': str,
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
        for key, value in schema_sub.iteritems():
            full_key = '.'.join([path, key])
            if key not in config_sub.keys():
                raise KeyError('the key "%s" is absent' % full_key)
            typ = type(value)
            if typ == type:
                typ = value
            if isinstance(config_sub[key], typ):
                if typ == dict:
                    config_check(config_sub[key], value, '%s' % full_key)
            else:
                raise TypeError('the key "%s" must be %s' % (full_key, typ))
        return True
    with open(configfile) as conf_file:
        conf = load(conf_file.read())

    if config_check(conf, schema):
        return conf


def argument_parser():
    ''' Arguments parser
    '''

    parser = ArgumentParser(
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


def logging_init(logfile, loglevel, prefix):
    if loglevel and loglevel in ['DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL']:
        level = getattr(logging, loglevel)
    else:
        level = getattr(logging, 'CRITICAL')
    if logfile:
        logging.basicConfig(
            filename=logfile,
            format='[%(asctime)s] ' + prefix + ' %(levelname)s: %(message)s',
            level=level
            )
    else:
        logging.basicConfig(
            filename=logfile,
            format='%(message)s',
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
