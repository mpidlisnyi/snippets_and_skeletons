import boto3
import logging
from urllib.request import urlopen, Request
from json import dumps as jdumps
from os import environ


ssm = boto3.client('ssm')
levels = [
    'CRITICAL',
    'ERROR',
    'WARNING',
    'INFO',
    'DEBUG',
    ]

loglevel = environ.get('LOGLEVEL')
if loglevel and loglevel in levels:
    level = getattr(logging, loglevel)
else:
    level = getattr(logging, 'CRITICAL')
logging.basicConfig(level=level)
logger = logging.getLogger()


def ssm_get(path):
    ''' Get SSM parameter
    '''
    return ssm.get_parameter(
        Name=path,
        WithDecryption=True
    )['Parameter']['Value']


def send_into_slack(channel, message, color='#439FE0'):
    ''' Send notifitcation into Slack channel
    '''
    params = {
        'channel': channel,
        'attachments': [
            {
                'color': color,
                'text': message,
                'mrkdwn_in': [
                    'text',
                    ],
                },
            ],
        }

    logger.debug(f'sending message "{message}" into channel {channel}')
    request = Request(slack_webhook_url, data=jdumps(params).encode('gbk'))
    response = urlopen(request)
    code = response.getcode()
    if code == 200:
        logger.debug('slack api said: %s', response.read())
    else:
        Exception(f'slack api returns code {code}: {response.read()}')


def handler(event, context):
    ''' Main entrypoint
    '''
    global slack_webhook_url
    slack_webhook_url = ssm_get(environ['SLACK_WEBHOOK_URL'])
    print(event)
