from wsgiref import util
from image import draw
import urlparse

description = { # partial list of status codes
100: 'Continue',
101: 'Switching Protocols',
102: 'Processing',
200: 'OK',
201: 'Created',
202: 'Accepted',
203: 'Non-Authoritative Information',
204: 'No Content',
205: 'Reset Content',
206: 'Partial Content',
207: 'Multi-Status',
300: 'Multiple Choices',
301: 'Moved Permanently',
302: 'Found',
303: 'See Other',
304: 'Not Modified',
305: 'Use Proxy',
306: 'Switch Proxy',
307: 'Temporary Redirect',
400: 'Bad Request',
401: 'Unauthorized',
402: 'Payment Required',
403: 'Forbidden',
404: 'Not Found',
405: 'Method Not Allowed',
406: 'Not Acceptable',
407: 'Proxy Authentication Required',
408: 'Request Timeout',
409: 'Conflict',
410: 'Gone',
411: 'Length Required',
412: 'Precondition Failed',
413: 'Request Entity Too Large',
414: 'Request-URI Too Long',
415: 'Unsupported Media Type',
416: 'Requested Range Not Satisfiable',
417: 'Expectation Failed',
418: "I'm a teapot",
422: 'Unprocessable Entity',
423: 'Locked',
424: 'Failed Dependency',
425: 'Unordered Collection',
426: 'Upgrade Required',
429: 'Too Many Requests',
431: 'Request Header Fields Too Large',
444: 'No Response',
449: 'Retry With',
450: 'Blocked by Windows Parental Controls',
500: 'Internal Server Error',
501: 'Not Implemented',
502: 'Bad Gateway',
503: 'Service Unavailable',
504: 'Gateway Timeout',
505: 'HTTP Version Not Supported',
506: 'Variant Also Negotiates',
507: 'Insufficient Storage',
508: 'Loop Detected',
509: 'Bandwidth Limit Exceeded',
510: 'Not Extended',
599: 'Network Connect Timeout Error',
}

def error(environment, start_response, code):
    HTML = """
    <html><body>
      <h1>%(error)s</h1>
      <img src = http://httpcats.herokuapp.com/%(error)s.jpg /><br>
      The requested URL <i>%(url)s</i> returned a %(error)s %(description)s.
    </body></html>"""
    start_response('%s %s' % (error, description[code]), [('content-type', 'text/html')])
    return [HTML % {'url': util.request_uri(environment), 'error': code, 'description': description[code]}]

def image(environment, start_response, code):
    query = dict(urlparse.parse_qsl(environment['QUERY_STRING']))
    try:
        result = draw(**query)
    except: # this whole error thing should be dealt with upstream in image.py
        raise    
    start_response('%s %s' % (error, description[code]), [('content-type', 'image/png')])
    return result.getvalue()

responses = {
'error': error,
'index': ,
'image': image,
}



def handle_request(environment, start_response):
    try:
        fn = util.shift_path_info(environment)
        if not fn:
            fn = 'index'
        response = responses[fn]
    except KeyError:
        response = responses['error'](environment, start_response, 404)
    return response

if __name__ == '__main__':
    from wsgiref import simple_server

    print("Starting server on port 8080...")
    try:
        simple_server.make_server('', 8080, handle_request).serve_forever()
    except KeyboardInterrupt:
        print("trl-C caught, Server exiting...")
        
        
