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
#    def get(self, project_urlString, id):
#        user = users.get_current_user()
#        
#        if user:
#            project_key = ndb.Key(urlsafe = project_urlString)
#            project = project_key.get()
#            requirements = Requirement.all(project.key)
#            html_text = self.render_str("dynamic/requirements.body.html", project = project, requirements = requirements)
#            requirement_dict = { 'content': html_text }
#            self.response.write(json.dumps(requirement_dict))
#        else:
#            self.response.write('{ "message": "please log in" }')

    def post(self):
        user = users.get_current_user()
        
        if user:
            ####################################################################################################################################################
            #
            #post = Post(parent = Post.post_db_key(), author = user, content = self.request.get("content"))
            #post.put()
            #requirement_dict = { 'success': True, 'content': post.content, 'created': post.created.strftime("%d.%m.%Y %H:%M:%S"), 'user': user.nickname() }
            #
            ####################################################################################################################################################
            #
            #requirement_dict = { 'success': True }
            #self.response.write(json.dumps(requirement_dict))
            #
            ####################################################################################################################################################
            #
            # TODO: hier könnte man das Requirement in der DB checken, ob jemand anderes es schon bearbeitet hat, mit einem Hash oder einem last modified date
            # oder wie im Wiki oder oder ... Für den Augenblick bleibt's ganz billig. Ich will die Daten eher bei Github im Bugtracker speichern.
            
            id = id = self.request.get('id')
            
            requirements = Requirement.query(Requirement.id == id).fetch()
            
            if len(requirements) > 0:
                # existing requirement
                requirement = requirements[0]
            else:
                # new requirement
                project_key = ndb.Key(urlsafe = self.request.get('urlsafe'))
                requirement = Requirement(parent = project_key, id = id)
            
            requirement.author = user
            requirement.title = self.request.get('title')
            requirement.content = self.request.get('content')
            
            requirement.put()
            requirement_dict = { 'success': True }
            self.write(json.dumps(requirement_dict))
            
            #
            ####################################################################################################################################################################################################
            
        else:
            requirement_dict = { 'success': False, 'message': 'not logged in' }
            self.response.write(json.dumps(requirement_dict))

    def delete(self):
        pass

''' handle a list of requirements '''
class Handler_requirements(jinja_worker.Handler_jinja_worker):
    def get(self, project_urlString):
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