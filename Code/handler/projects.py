﻿import json
import jinja_worker
import os, sys

from google.appengine.api import users
from google.appengine.ext import ndb

sys.path.append(os.path.join(os.path.dirname(__file__), '../model'))

from task import Task
from userstory import UserStory
from requirement import Requirement
from project import Project

class Handler_project(jinja_worker.Handler_jinja_worker):

    def get(self, action = None):
        # TODO: besser machen, mit mehr if Abfragen und anderen else (nämlich dann nix machen)
        # außerdem könnte man doch wieder einzelne Controller machen, oder? Wobei ... jede Methode hat nur zehn Zeilen,
        # die Klasse nur zwei Bildschirme, eigentlich kann man's auch so lassen
        
        urlString = self.request.get('urlsafe', default_value = None)
        
        # project data handling
        if action == "overview":
            self.overview(urlString)
        elif action == "requirements":
            self.requirements(urlString)
        elif action == "userstories":
            self.userstories(urlString)
        elif action == "tasks":
            self.tasks(urlString)
            
        # other handling
        elif action == "requirement":
            self.requirement(urlString, self.request.get('id', default_value = None))
        elif action == "userstory":
            self.userstory(urlString, self.request.get('id', default_value = None))
        elif action == "task":
            self.task(urlString, self.request.get('id', default_value = None))
        elif action == "navigation":
            self.navigation(urlString)
        else:
            self.overview(action)

    ''' deprecated '''
    def alt(self, urlString = None):
        user = users.get_current_user()
        project = None
        projects = model.project.get_projects()
        
        if urlString:
            key = ndb.Key(urlsafe=urlString)
            project = key.get()
        
        if user:
            self.render("project.html", username = user.nickname(), url = users.create_logout_url('/'), project = project, projects = projects)
        else:
            self.render("project.html", url = users.create_login_url('/'), project = None, projects = None)
    
    def overview(self, project_urlString = None):
        user = users.get_current_user()
        
        if user:
            self.set_autoescape(False)
            project_key = ndb.Key(urlsafe = project_urlString)
            project = project_key.get()
            requirements = self._get_requirements(project)
            html = self.render_str("dynamic/overview.body.html", project = project, requirements = requirements)
            requirement_dict = { 'content': html }
            self.response.write(json.dumps(requirement_dict))
            self.set_autoescape(True)
        else:
            self.response.write('{ "message": "please log in" }')
    
    def requirements(self, project_urlString = None):
        user = users.get_current_user()
        
        if user:
            project_key = ndb.Key(urlsafe = project_urlString)
            project = project_key.get()
            requirements = Requirement.all(project.key)
            html = self.render_str("dynamic/requirements.body.html", project = project, requirements = requirements)
            requirement_dict = { 'content': html }
            self.response.write(json.dumps(requirement_dict))
        else:
            self.response.write('{ "message": "please log in" }')
    
    def userstories(self, project_urlString):
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

            html = self.render_str("dynamic/userstories.body.html", project = project, requirement_titles = requirement_titles, userstories = userstories)
            requirement_dict = { 'content': html }
            self.response.write(json.dumps(requirement_dict))
        else:
            self.response.write('{ "message": "please log in" }')
    
    def tasks(self, project_urlString):
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

            html = self.render_str("dynamic/tasks.body.html", project = project, userstory_titles = userstory_titles, tasks = tasks)
            requirement_dict = { 'content': html }
            self.response.write(json.dumps(requirement_dict))
        else:
            self.response.write('{ "message": "please log in" }')
    
    def requirement(self, project_urlString, id):
        user = users.get_current_user()
        
        if user:
            project_key = ndb.Key(urlsafe = project_urlString)
            project = project_key.get()
            requirement_query = Requirement.query(Requirement.id == id, ancestor = project_key)
            requirements = requirement_query.fetch(1)
            
            if len(requirements) > 0:
                requirement = requirements[0]
                html = self.render_str("dynamic/requirement.body.html", project = project, requirement = requirement)
                
                dict = {
                    'id': requirement.id,
                    'title': requirement.title,
                    'content': requirement.content,
                    'html': html
                }
                
                self.response.write(json.dumps(dict))
            else:
                self.response.write('{ "message": "no requirement found with id ' + id + '" }')
        else:
            self.response.write('{ "message": "please log in" }')

    def userstory(self, project_urlString, id):
        user = users.get_current_user()
        
        if user:
            project_key = ndb.Key(urlsafe = project_urlString)
            project = project_key.get()
            userstory_query = UserStory.query(UserStory.id == id, ancestor = project_key)
            userstories = userstory_query.fetch(1)
            
            if len(userstories) > 0:
                userstory = userstories[0]
                html = self.render_str("dynamic/userstory.body.html", project = project, userstory = userstory)
                
                dict = {
                    'id': userstory.id,
                    'title': userstory.title,
                    'content': userstory.content,
                    'html': html
                }
                
                self.response.write(json.dumps(dict))
            else:
                self.response.write('{ "message": "no userstory found with id ' + id + '" }')
        else:
            self.response.write('{ "message": "please log in" }')
    
    def task(self, project_urlString, id):
        user = users.get_current_user()
        
        if user:
            project_key = ndb.Key(urlsafe = project_urlString)
            project = project_key.get()
            task_query = Task.query(Task.id == id, ancestor = project_key)
            tasks = task_query.fetch(1)
            
            if len(tasks) > 0:
                task = tasks[0]
                html = self.render_str("dynamic/task.body.html", project = project, task = task)
                
                dict = {
                    'id': task.id,
                    'title': task.title,
                    'content': task.content,
                    'html': html
                }
                
                self.response.write(json.dumps(dict))
            else:
                self.response.write('{ "message": "no task found with id ' + id + '" }')
        else:
            self.response.write('{ "message": "please log in" }')
    
    def navigation(self, project_urlString):
        user = users.get_current_user()
        
        if user:
            project_key = ndb.Key(urlsafe = project_urlString)
            project = project_key.get()
            html = self.render_str("dynamic/project.data-navigation.html", project = project)
            requirement_dict = { 'content': html }
            self.response.write(json.dumps(requirement_dict))

####################################################################################################
    def _get_requirements(self, project):
        user = users.get_current_user()
        
        if user:
            html = ""
            requirements = Requirement.all(project.key)
            for requirement in requirements:
                userstories = self._get_userstories(requirement)
                html += self.render_str("dynamic/overview.requirement.html", requirement = requirement, userstories = userstories)
            return html
        else:
            return None

    def _get_userstories(self, requirement):
        user = users.get_current_user()
        
        if user:
            html = ""
            userstories = UserStory.all(requirement.key)
            for userstory in userstories:
                tasks = self._get_tasks(userstory)
                html += self.render_str("dynamic/overview.userstory.html", userstory = userstory, tasks = tasks)
            return html
        else:
            return None

    def _get_tasks(self, userstory):
        user = users.get_current_user()
        
        if user:
            html = ""
            tasks = Task.all(userstory.key)
            for task in tasks:
                html += self.render_str("dynamic/overview.task.html", task = task)
            return html
        else:
            return None












