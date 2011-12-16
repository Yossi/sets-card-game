# lifted off of here http://probablyprogramming.com/2008/06/26/building-a-python-web-application-part-1

from wsgiref import util

# Templates
wrapper = """
<html><head><title>%(title)s</title></head><body>
%(body)s
</body></html>
"""

four_oh_four = """
<html><body>
  <h1>404-ed!</h1>
  The requested URL <i>%(url)s</i> was not found.
</body></html>"""

# Template Variables for each page
pages = {
    'index': { 'title': "Hello There",
               'body':  
               """This is a test of the WSGI system.
                Perhaps you would also be interested in
                <a href="this_page">this page</a>?"""
              },
    'this_page': { 'title': "You're at this page",
                   'body': 
                   """Hey, you're at this page.
                   <a href="/">Go back</a>?"""
                   }
    }

def handle_request(environment, start_response):
    try:
        fn = util.shift_path_info(environment)
        if not fn:
            fn = 'index'
        response = wrapper % pages[fn]
        start_response('200 OK', [('content-type', 'text/html')])
    except:
        start_response('404 Not Found', [('content-type', 'text/html')])
        response = four_oh_four % {'url':util.request_uri(environment)}
    return [response]

if __name__ == '__main__':
    from wsgiref import simple_server

    print("Starting server on port 8080...")
    try:
        simple_server.make_server('', 8080, handle_request).serve_forever()
    except KeyboardInterrupt:
        print("Ctrl-C caught, Server exiting...")
