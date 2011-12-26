description = { # partial list of status codes. massive overkill
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

# yeah, they belong up there. bite me.
import urlparse, urllib
from wsgiref import util
from image import draw
from sets import Deck


def error(environment, start_response, code):
    html = '''
    <html><body>
      <h1>%(error)s</h1>
      The requested URL <i>%(url)s</i> returned a %(error)s %(description)s.<br>
      <img src = http://httpcats.herokuapp.com/%(error)s.jpg />
    </body></html>'''
    start_response('%s %s' % (code, description[code]), [('content-type', 'text/html')])
    return [html % {'url': util.request_uri(environment), 'error': code, 'description': description[code]}]

def image(environment, start_response, code):
    # qsl not qs because qs gives a dict of lists, and we need a dict of strings
    query = dict(urlparse.parse_qsl(environment['QUERY_STRING']))
    try:
        result = draw(**query)
    except: # errors should have been dealt with upstream in image.py. if not, KA-BOOM!
        raise
    start_response('%s %s' % (code, description[code]), [('content-type', 'image/png')])
    return result.getvalue()

def index(environment, start_response, code):
    deck = Deck()
    rows = []
    for card1, card2, card3 in deck:
        rows.append('''<tr>
                         <td><img src="image?%s" border=1 /></td>
                         <td><img src="image?%s" border=1 /></td>
                         <td><img src="image?%s" border=1 /></td>
                       </tr>''' % (urllib.urlencode(card1.attributes),
                                   urllib.urlencode(card2.attributes),
                                   urllib.urlencode(card3.attributes))
                    )
    html = '''
    <html><body>
      <table>
        %s
      </table>
    </body></html>'''
    start_response('%s %s' % (code, description[code]), [('content-type', 'text/html')])
    return html % ''.join(rows)

responses = {
'error': error,
'index': index,
'image': image,
}


def handle_request(environment, start_response):
    try:
        fn = util.shift_path_info(environment)
        if not fn:
            fn = 'index'
        response = responses[fn](environment, start_response, 200)
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
        
        
