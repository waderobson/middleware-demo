"""Header example"""
HEADERS = {'api_key': '123_IAM_A_KEY', 'api_secret': 'SECRETKEY'}


def process_request_options(options):
    url = options.get('url')
    if 'swscan.apple.com' not in url:
        print 'Headers before: %s' % options['additional_headers']
        # Merge headers with Munki
        options['additional_headers'].update(HEADERS)
        print 'Headers after: %s' % options['additional_headers']
    return options
