from urllib import urlencode

QUERY_PARAMS={'username': 'apiuser', 'password': 'secret password'}

def encode_params(data):
    """Encode parameters in a piece of data.
    Will successfully encode parameters when passed as a dict or a list of
    2-tuples. Order is retained if data is a list of 2-tuples but arbitrary
    if parameters are supplied as a dict.
    """
    result = []
    for k, vs in QUERY_PARAMS.items():
        if isinstance(vs, basestring) or not hasattr(vs, '__iter__'):
            vs = [vs]
        for v in vs:
            if v is not None:
                result.append(
                    (k.encode('utf-8') if isinstance(k, str) else k,
                     v.encode('utf-8') if isinstance(v, str) else v))
    return urlencode(result, doseq=True)


def process_request_options(options):
    url = options.get('url')
    if 'swscan.apple.com' not in url:
        #concat url and query string
        print 'URL Before: %s' % options.get('url')
        options['url'] = options['url'] + '?' + encode_params(QUERY_PARAMS)
        print 'URL After: %s' % options.get('url')
    return options