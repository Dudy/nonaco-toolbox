######################################################################################################
# jinja worker
######################################################################################################

import webapp2
import os
import jinja2

# statics
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler_jinja_worker(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
    
    def set_autoescape(self, autoescape = True):
        global jinja_env
        jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = autoescape)