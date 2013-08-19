import os, sys
import webapp2, cgi

sys.path.append(os.path.join(os.path.dirname(__file__), 'handler'))

import homepage
import lazy_loader

app = webapp2.WSGIApplication([
    ('/', homepage.Handler_homepage),
    ('/new_post', homepage.Handler_homepage),
    (r'/json/next_posts/(.*)', lazy_loader.Handler_lazy_loader)
], debug=True)

