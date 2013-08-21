import os, sys
import webapp2, cgi

sys.path.append(os.path.join(os.path.dirname(__file__), 'handler'))

import homepage
import lazy_loader
import base
import projects
import postings
import requirement_handler
import userstory_handler
import task_handler
import overview_handler

app = webapp2.WSGIApplication([
    # the web application urls
    ('/base.html', base.Handler_base),
    ('/postings.html', postings.Handler_postings),
    ('/new_post', postings.Handler_postings),
    ('/project/(.*)', projects.Handler_project),
    ('/', base.Handler_base),
    
    ('/demo.html', base.Handler_demo),
    
    # the API
    (r'/json/next_posts/(.*)', lazy_loader.Handler_lazy_loader),
    
    (r'/json/overview/(.*)', overview_handler.Handler_overview),
    
    (r'/json/requirement/(.*)', requirement_handler.Handler_requirement),
    (r'/json/requirements/(.*)', requirement_handler.Handler_requirements),
    
    (r'/json/userstories/(.*)', userstory_handler.Handler_userstories),
    (r'/json/tasks/(.*)', task_handler.Handler_tasks)
], debug=True)

