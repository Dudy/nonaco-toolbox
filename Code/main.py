import os, sys
import webapp2, cgi

sys.path.append(os.path.join(os.path.dirname(__file__), 'handler'))

import homepage

app = webapp2.WSGIApplication([
    ('/', homepage.Handler_homepage)
], debug=True)
