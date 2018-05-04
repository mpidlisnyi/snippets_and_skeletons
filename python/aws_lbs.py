from boto3 import client as boto3_client

SERVICES_FIELD = {
        'elbv2': 'LoadBalancers',
        'elb': 'LoadBalancerDescriptions',
        }

SERVICES_FIELD_KEYS = SERVICES_FIELD.keys()

def get_all_elb(PageSize=100, service='elb'):
    '''Get list of ELB or ALB

    PageSize - number of items per request(default=100)
    service - the service name. elbv2 for ALB, elb for ELB
    '''
    if service not in SERVICES_FIELD_KEYS:
        raise ValueError('service must be one of %s' % SERVICES_FIELD_KEYS)
    elb_client = boto3_client(service)
    run = True
    state = {'PageSize': PageSize}
    describe = elb_client.describe_load_balancers
    while run:
        res = describe(**state)
        try:
            state['Marker'] = res['NextMarker']
        except KeyError:
            run = False
        elbs = res[SERVICES_FIELD[service]]
        while elbs:
            elb = elbs.pop(0)
            if elb['Scheme'] == 'internet-facing':
                yield elb

def get_https_ports(elb, service='elb'):
    '''Get list of https ports for ELB and ALB

    elb - the dict from boto describe_load_balancers
    service - the service name. elbv2 for ALB, elb for ELB
    '''
    if service not in SERVICES_FIELD_KEYS:
        raise ValueError('service must be one of %s' % SERVICES_FIELD_KEYS)
    ports = []
    if service == 'elb':
        for listener in elb['ListenerDescriptions']:
            ls = listener['Listener']
            if ls['Protocol'] == 'HTTPS':
                ports.append(ls['LoadBalancerPort'])
    else:
        elb_client = boto3_client(service)
        listeners = elb_client.describe_listeners(LoadBalancerArn=elb['LoadBalancerArn'])
        for ls in listeners['Listeners']:
            if ls['Protocol'] == 'HTTPS':
                ports.append(ls['Port'])

    return ports



SERVICES = [
    'elb',
    'elbv2',
    ]

for service in SERVICES:
    for i in get_all_elb(service=service):
        print i['LoadBalancerName']
