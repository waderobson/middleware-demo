_How to use middleware_

### Introduction

This optional feature allows a Munki Admin to use their own code, or from a third party to manipulate Munki's HTTP requests. The primary use case for this feature is to provide interaction with APIs, although it is not limited to that. Middleware is activated by the presence of a Python file. If it's there it gets called, if it's not it won't, it's as simple as that.


### Details

Middleware gets imported at runtime as a Python module so the middleware file **must** be written in Python. Nothing is stopping you from then calling another executable from Python, so in that sense, you're not limited to Python.  
At the beginning of the Munki run, Munki searches for "middleware*.py". If Munki finds the middleware file it then looks for the function, "process_request_options". The options are then sent through, examined, changed, or not, before heading to the server. 

You may only use one middleware file. If you have more then one of middleware file you **will** have unpredictable results.

#### Requirements

For the middleware to work, you will need the following:

##### Filename
Munki is looking for files the start with "middleware" and end with ".py".  
Examples of good and bad middleware filenames:  
- middleware.py👍
- ~~middleware~~👎
- ~~my_middleware.py~~👎
- middleware_cloudfoo.py👍

##### Location
The middleware file must live in the root of the munkitools folder(/usr/local/munki). 

##### Permissions
Root must be the owner of the file and be able to read it. Since its imported by python, the executable part isn't necessary. It's important to note that if you plan on storing sensitive information inside you should restrict access.
```bash
sudo chown root /usr/local/munki/middleware*.py
sudo chmod 600 /usr/local/munki/middleware*.py
```

##### The "process_request_options" function
This is the fuction that Munki is looking for. Think of it as the "main" fuction for the middleware. If Munki doesn't find this function it will abandon the middleware, and continue on as if it wasn't there.   

_Example function_
 ```python
 def process_request_options(options):
    print '***Requesting: %s' % options.get('url')
    return options
```
This is a basic example. The options are inbound from Munki, we print the requested url and then return the options unchanged.


#### Middleware examples
##### Query Parameters
_Query Params Example_
```python
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
        print 'URL Before: %s' % options.get('url')
        #concat url and query string
        options['url'] = options['url'] + '?' + encode_params(QUERY_PARAMS)
        print 'URL After: %s' % options.get('url')
    return options
```
In the example above we are joining the URL from Munki and query string together.
######Before:   
`http://munki.example.com/catalogs/production`
######After:
`http://munki.example.com/catalogs/production?username=apiuser&password=secret+password`
  

##### Headers

_Headers Example_
```python
HEADERS = {'api_key': '123_IAM_A_KEY', 'api_secret': 'SECRETKEY'}


def process_request_options(options):
    url = options.get('url')
    if 'swscan.apple.com' not in url:
        print 'Headers before: %s' % options['additional_headers']
        # Merge headers with Munki
        options['additional_headers'].update(HEADERS)
        print 'Headers after: %s' % options['additional_headers']
    return options
```
Since the 'additional_headers' key is a dictionary it is easy for us to update retaining the `User-Agent` and `Authorization` headers.
###### Before: 
`{u'Authorization': u'Basic bXVua2k6WUhuUXhWWFFh==', 'User-Agent': u'managedsoftwareupdate/2.6.1 Darwin/15.4.0'}`  
###### After: 
`{'api_secret': 'SECRETKEY', 'api_key': '123_IAM_A_KEY', u'Authorization': u'Basic bXVua2k6WUhuUXhWWFFh==', 'User-Agent': u'managedsoftwareupdate/2.6.1 Darwin/15.4.0'}`




##### Available options
These are all the options that can be changed with the middleware. Note: 99% of the time you'll only be interested in the **url** and the **additional_headers**

| Key | Type | Description  | Default Value |
|-----|------|--------------|---------------|
| url    | String | The 'url' you are requesting. ||
| additional_headers | Dictionary | These are the HTTP headers that are going in the get request. [List of HTTP header fields](https://en.wikipedia.org/wiki/List_of_HTTP_header_fields) | `{'User-Agent': u'managedsoftwareupdate/%MUNKI_VER% Darwin/%OS_VER%'}` |
| follow_redirects | String | Explained [here](https://github.com/munki/munki/wiki/Preferences#followhttpredirects) | `None` |
| resume | Boolean | If `True`, Gurl will attempt to resume an interrupted download. _**You should probably leave this alone._ | `False` |
| download_only_if_changed| Boolean | If destinationpath already exists, you can set 'onlyifnewer' to true to indicate you only want to download the file only if it's newer on the server.  _**You should probably leave this alone._ | `False` |
| cache_data | NSObject | _**Don't touch this._ ||
| logging_function | Function | The logging function in use.  _**You should probably leave this alone._ ||

