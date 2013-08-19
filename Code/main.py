import os, sys
import webapp2, cgi

sys.path.append(os.path.join(os.path.dirname(__file__), 'handler'))

import homepage
import lazy_loader
import base
import projects
import postings

app = webapp2.WSGIApplication([
    # the web application urls
    ('/base.html', base.Handler_base),
    ('/postings.html', postings.Handler_postings),
    ('/new_post', postings.Handler_postings),
    ('/project/(.*)', projects.Handler_project),
    ('/', base.Handler_base),
    
    # the API
    (r'/json/next_posts/(.*)', lazy_loader.Handler_lazy_loader)
], debug=True)

