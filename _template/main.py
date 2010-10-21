#!/usr/bin/env python

# Always prefer a newer version of django, for at least the auto-escape ability of
# the template functions
from google.appengine.dist import use_library
use_library('django', '1.1')

from google.appengine.ext.webapp import WSGIApplication, RequestHandler
from google.appengine.ext.webapp.util import run_wsgi_app

# Local imports
import settings
import helpers
import models
import logging



class MainHandler(RequestHandler):
    def get(self):
        logging.info("Got request for /")
        helpers.render_template(self, 'index.html', {})

def main():
    application = WSGIApplication([
        ('/', MainHandler),
    ],
    debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
