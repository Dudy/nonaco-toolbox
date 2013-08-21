import jinja_worker
import os, sys

from google.appengine.api import users

sys.path.append(os.path.join(os.path.dirname(__file__), '../model'))

import model.project

class Handler_base(jinja_worker.Handler_jinja_worker):
    def get(self):
        user = users.get_current_user()
        projects = model.project.get_projects()
        
        if user:
            self.render("base.html", username = user.nickname(), url = users.create_logout_url('/'), projects = projects)
        else:
            self.render("base.html", username = None, url = users.create_login_url('/'), projects = None)

class Handler_demo(jinja_worker.Handler_jinja_worker):
    def get(self):
        self.render("demo.html")