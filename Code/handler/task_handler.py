import logging
import json
import jinja_worker
import os, sys
import datetime as dt

from google.appengine.api import users
from google.appengine.ext import ndb

sys.path.append(os.path.join(os.path.dirname(__file__), '../model'))

from task import Task
from task import Task
from requirement import Requirement
from project import Project

class Handler_tasks(jinja_worker.Handler_jinja_worker):

    def post(self, id):
        user = users.get_current_user()
        
        if user:
            ####################################################################################################################################################
            #
            # TODO: hier könnte man den Task in der DB checken, ob jemand anderes es schon bearbeitet hat, mit einem Hash oder einem last modified date
            # oder wie im Wiki oder oder ... Für den Augenblick bleibt's ganz billig. Ich will die Daten eher bei Github im Bugtracker speichern.
            
            tasks = Task.query(Task.id == id).fetch()
            
            if len(tasks) > 0:
                # existing task
                task = tasks[0]
            else:
                # new task
                project_key = ndb.Key(urlsafe = self.request.get('urlsafe'))
                task = Task(parent = project_key, id = id)
            
            task.author = user
            task.title = self.request.get('title')
            task.content = self.request.get('content')
            
            task.put()
            dict = { 'success': True }
            self.write(json.dumps(dict))
            
            #
            ####################################################################################################################################################
            
        else:
            dict = { 'success': False, 'message': 'not logged in' }
            self.response.write(json.dumps(dict))

    def delete(self):
        pass











