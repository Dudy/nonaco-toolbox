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

    def post(self):
        user = users.get_current_user()
        
        if user:
            ####################################################################################################################################################
            #
            # TODO: hier könnte man die User Story in der DB checken, ob jemand anderes es schon bearbeitet hat, mit einem Hash oder einem last modified date
            # oder wie im Wiki oder oder ... Für den Augenblick bleibt's ganz billig. Ich will die Daten eher bei Github im Bugtracker speichern.
            
            id = id = self.request.get('id')
            
            userstories = UserStory.query(UserStory.id == id).fetch()
            
            if len(userstories) > 0:
                # existing userstory
                userstory = userstories[0]
            else:
                # new userstory
                project_key = ndb.Key(urlsafe = self.request.get('urlsafe'))
                userstory = UserStory(parent = project_key, id = id)
            
            userstory.author = user
            userstory.title = self.request.get('title')
            userstory.content = self.request.get('content')
            
            userstory.put()
            dict = { 'success': True }
            self.write(json.dumps(dict))
            
            #
            ####################################################################################################################################################
            
        else:
            dict = { 'success': False, 'message': 'not logged in' }
            self.response.write(json.dumps(dict))

    def delete(self):
        pass











