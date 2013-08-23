import jinja_worker
import os, sys

from google.appengine.api import users

sys.path.append(os.path.join(os.path.dirname(__file__), '../model'))

import model.project

from jinja2 import Template

class Handler_base(jinja_worker.Handler_jinja_worker):
    def get(self):
        user = users.get_current_user()
        projects = model.project.get_projects()
        
        if user:
            navigation_top = self.render_str("dynamic/navigation.top.html", username = user.nickname(), url = users.create_logout_url('/'))
            navigation_left = self.render_str("dynamic/navigation.left.html", username = user.nickname(), projects = projects)
            navigation_right = self.render_str("dynamic/navigation.right.html")
            footer = self.render_str("dynamic/footer.html")
            
            
            self.set_autoescape(False)
            site = self.render_str("base.html", username = user.nickname(), url = users.create_logout_url('/'), projects = projects, navigation_top = navigation_top, navigation_left = navigation_left, navigation_right = navigation_right, footer = footer)
            self.set_autoescape(True)
            
            self.response.write(site)
        else:
            self.set_autoescape(False)
            navigation_top = self.render_str("dynamic/navigation.top.html", username = None, project = None, url = users.create_login_url('/'), projects = None)
            
            site = self.render_str("base.html", username = None, url = users.create_login_url('/'), projects = None, navigation_top = navigation_top, navigation_left = None)
            self.response.write(site)
            
            self.set_autoescape(True)

class Handler_demo(jinja_worker.Handler_jinja_worker):
    def get(self):
        self.render("demo.html")

class Handler_demo2(jinja_worker.Handler_jinja_worker):
    def get(self):
        self.render("demo2.html")