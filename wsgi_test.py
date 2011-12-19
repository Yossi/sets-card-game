# lifted off of here http://probablyprogramming.com/2008/06/26/building-a-python-web-application-part-1

from wsgiref import util
from image import draw
import urlparse


# Templates
wrapper = """
<html><head><title>%(title)s</title></head><body>
%(body)s
</body></html>
"""

error = """
<html><body>
  <h1>%(error)s</h1>
  <img src = http://httpcats.herokuapp.com/%(error)s.jpg /><br>
  The requested URL <i>%(url)s</i> was not found.
</body></html>"""

# Template Variables for each page
pages = {
    'index': wrapper % { 'title': "Hello There",
               'body':  
               """This is a test of the WSGI system.
                Perhaps you would also be interested in
                <a href="this_page">this page</a>?<br>
                <img border=1 src=http://127.1:8080/image/?number=two&color=green&shade=shaded&shape=squiggle><br>
                <img border=1 src=http://127.1:8080/image/?number=one&color=red&shade=empty&shape=diamond><br>
                <img border=1 src=http://127.1:8080/image/?number=three&color=purple&shade=filled&shape=oval><br>"""
              },
    'this_page': wrapper % { 'title': "You're at this page",
                   'body': 
                   """Hey, you're at this page.
                   <a href="/">Go back</a>?"""
                 },
    'image': {
             },
    }

def handle_request(environment, start_response):
    try:
        query = dict(urlparse.parse_qsl(environment['QUERY_STRING']))
        fn = util.shift_path_info(environment)
        if not fn:
            fn = 'index'
        if fn == 'image':
            response = draw(**query)
            #print response.size()
            start_response('200 OK', [('content-type', 'image/png', )])
            return response.getvalue()
        else:
            response = pages[fn]
            start_response('200 OK', [('content-type', 'text/html')])
    except KeyError:
        response = error % {'url':util.request_uri(environment), 'error': '404'}
        start_response('404 Not Found', [('content-type', 'text/html')])
    return [response]

if __name__ == '__main__':
    from wsgiref import simple_server

    print("Starting server on port 8080...")
    try:
        simple_server.make_server('', 8080, handle_request).serve_forever()
    except KeyboardInterrupt:
        print("trl-C caught, Server exiting...")
