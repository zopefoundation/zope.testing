##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Functional test server to interactively inspect the state of the system.

You can run it in a functional test by adding a line like this:

  startServer(http, url, "username", "password")

http is an instance of HTTPCaller, url is the url that will be opened
in the browser, the username and password are optional. When you're
done with inspecting the application press Ctrl+C to continue with the
functional test.
"""
from __future__ import print_function

import sys
import warnings
import webbrowser


# XXX: I don't think this module works on Python 3!

try:  # pragma: PY3
    from http.server import BaseHTTPRequestHandler
    from http.server import HTTPServer
    from urllib import parse as urlparse
except ImportError:  # pragma: PY2
    import urlparse
    from BaseHTTPServer import BaseHTTPRequestHandler
    from BaseHTTPServer import HTTPServer


def makeRequestHandler(http, user=None, password=None):  # pragma: PY2
    warnings.warn(
        'zope.testing.server.makeRequestHandler is deprecated. It probably'
        ' does not work on Python 3.', DeprecationWarning, stacklevel=2)

    class FunctionalTestRequestHandler(BaseHTTPRequestHandler):

        def do_GET(self):
            request = self.raw_requestline
            if user and password:
                # Authentication is built in, as there is no fluent
                # way of transferring session from functional test to
                # the real browser
                request += "Authorization: Basic %s:%s\r\n" % (user, password)

            # Write headers to the request
            for header in self.headers.headers:
                request += header
            request += '\r\n'

            if self.headers.get('Content-Length'):
                data = self.rfile.read(int(self.headers.get('Content-Length')))
                request += data
            else:
                # if no content-length was set - read until the last
                # char, then finish
                self.request.setblocking(0)
                while True:
                    try:
                        char = self.rfile.read()
                    except Exception:  # XXX: should probably be IOError?
                        break
                    request += char

            response = http(request)
            self.wfile.write(response)

        do_POST = do_GET

    return FunctionalTestRequestHandler


def addPortToURL(url, port):
    """Add a port number to the url.

        >>> from zope.testing.server import addPortToURL
        >>> addPortToURL('http://localhost/foo/bar/baz.html', 3000)
        'http://localhost:3000/foo/bar/baz.html'
        >>> addPortToURL('http://foo.bar.com/index.html?param=some-value', 555)
        'http://foo.bar.com:555/index.html?param=some-value'

        >>> addPortToURL('http://localhost:666/index.html', 555)
        'http://localhost:555/index.html'

    """
    (scheme, netloc, url, query, fragment) = urlparse.urlsplit(url)
    netloc = netloc.split(':')[0]
    netloc = "%s:%s" % (netloc, port)
    url = urlparse.urlunsplit((scheme, netloc, url, query, fragment))
    return url


def startServer(http, url, user=None, password=None, port=8000):  # pragma: PY2
    warnings.warn(
        'zope.testing.server.startServer is deprecated. It probably'
        ' does not work on Python 3.', DeprecationWarning, stacklevel=2)
    try:
        server_address = ('', port)
        requestHandler = makeRequestHandler(http, user, password)
        url = addPortToURL(url, port)
        httpd = HTTPServer(server_address, requestHandler)
        # XXX we rely on browser being slower than our server
        webbrowser.open(url)
        print('Starting HTTP server...', file=sys.stderr)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Stopped HTTP server.', file=sys.stderr)
