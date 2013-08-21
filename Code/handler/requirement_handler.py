import logging
import json
import jinja_worker
import os, sys
import datetime as dt

from google.appengine.api import users
from google.appengine.ext import ndb

sys.path.append(os.path.join(os.path.dirname(__file__), '../model'))

from requirement import Requirement
from project import Project

''' handle a single requirement '''
class Handler_requirement(jinja_worker.Handler_jinja_worker):
    def get(self, id):
        user = users.get_current_user()
        
        if user:
            project_key = ndb.Key(urlsafe = project_urlString)
            project = project_key.get()
            requirements = Requirement.all(project.key)
            html_text = self.render_str("dynamic/requirements.body.html", project = project, requirements = requirements)
            requirement_dict = { 'content': html_text }
            self.response.write(json.dumps(requirement_dict))
        else:
            self.response.write('{ "message": "please log in" }')

''' handle a list of requirements '''
class Handler_requirements(jinja_worker.Handler_jinja_worker):
    def get(self, project_urlString):
        #self.response.write(project_urlString)
        user = users.get_current_user()
        
        if user:
            project_key = ndb.Key(urlsafe = project_urlString)
            project = project_key.get()
            requirements = Requirement.all(project.key)
            html_text = self.render_str("dynamic/requirements.body.html", project = project, requirements = requirements)
            requirement_dict = { 'content': html_text }
            self.response.write(json.dumps(requirement_dict))
        else:
            self.response.write('{ "message": "please log in" }')