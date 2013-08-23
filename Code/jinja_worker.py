######################################################################################################
# jinja worker
######################################################################################################

import webapp2
import os
import jinja2
import codecs

# statics
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler_jinja_worker(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        bom = unicode(codecs.BOM_UTF8, "utf8")
        rendered_template = jinja_env.get_template(template)
        html = rendered_template.render(params)
        return html.replace(bom, '')
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
    
    def set_autoescape(self, autoescape = True):
        global jinja_env
        jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = autoescape)