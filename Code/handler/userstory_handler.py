import logging
import json
import jinja_worker
import os, sys
import datetime as dt

from google.appengine.api import users
from google.appengine.ext import ndb

sys.path.append(os.path.join(os.path.dirname(__file__), '../model'))

from userstory import UserStory
from requirement import Requirement
from project import Project

class Handler_userstories(jinja_worker.Handler_jinja_worker):
    def get(self, project_urlString):
        user = users.get_current_user()
        
        if user:
            project_key = ndb.Key(urlsafe = project_urlString)
            project = project_key.get()
            requirements = Requirement.all(project.key)
            
            requirement_titles = {}
            userstories = []
            for requirement in requirements:
                some_userstories = UserStory.all(requirement.key)
                for userstory in some_userstories:
                    requirement_titles[userstory.key.id()] = requirement.title
                userstories += some_userstories

            html_text = self.render_str("dynamic/userstories.body.html", project = project, requirement_titles = requirement_titles, userstories = userstories)
            requirement_dict = { 'content': html_text }
            self.response.write(json.dumps(requirement_dict))
        else:
            self.response.write('{ "message": "please log in" }')