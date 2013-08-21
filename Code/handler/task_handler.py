import logging
import json
import jinja_worker
import os, sys
import datetime as dt

from google.appengine.api import users
from google.appengine.ext import ndb

sys.path.append(os.path.join(os.path.dirname(__file__), '../model'))

from task import Task
from userstory import UserStory
from requirement import Requirement
from project import Project

class Handler_tasks(jinja_worker.Handler_jinja_worker):
    def get(self, project_urlString):
        user = users.get_current_user()
        
        if user:
            project_key = ndb.Key(urlsafe = project_urlString)
            project = project_key.get()
            requirements = Requirement.all(project.key)
            
            userstory_titles = {}
            tasks = []
            for requirement in requirements:
                userstories = UserStory.all(requirement.key)
                for userstory in userstories:
                    some_tasks = Task.all(userstory.key)
                    for task in some_tasks:
                        userstory_titles[task.key.id()] = userstory.title
                    tasks += some_tasks

            html_text = self.render_str("dynamic/tasks.body.html", project = project, userstory_titles = userstory_titles, tasks = tasks)
            requirement_dict = { 'content': html_text }
            self.response.write(json.dumps(requirement_dict))
        else:
            self.response.write('{ "message": "please log in" }')