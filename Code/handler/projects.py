import json, logging
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
        
        urlsafe = self.request.get('urlsafe', default_value = None)
        id = self.request.get('id', default_value = None)
        
        # project data handling
        if action == "overview":
            self.overview(urlsafe)
        elif action == "requirements":
            self.requirements(urlsafe)
        elif action == "userstories":
            self.userstories(urlsafe)
        elif action == "tasks":
            self.tasks(urlsafe)
            
        # create or edit operations
        elif action == "requirement":
            self.requirement()
        elif action == "userstory":
            self.userstory()
        elif action == "task":
            self.task()
        
        # other handling
        elif action == "navigation":
            self.navigation(urlsafe)
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
    
    ''' deprecated '''
    def userstories_old(self, project_urlString):
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
    
    def userstories(self, project_urlString):
        user = users.get_current_user()
        
        if user:
            project_key = ndb.Key(urlsafe = project_urlString)
            project = project_key.get()
            requirement_container_list = []
            
            for requirement in Requirement.all(project.key):
                requirement_container_list.append(RequirementContainer(requirement = requirement, userstories = UserStory.all(requirement.key)))

            html = self.render_str("dynamic/userstories.body.html", project = project, requirement_container_list = requirement_container_list)
            dict = { 'content': html }
        else:
            dict = { "message": "please log in" }
        
        self.response.write(json.dumps(dict))
    
    ''' deprecated '''
    def tasks_old(self, project_urlString):
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

    def tasks(self, project_urlString):
        user = users.get_current_user()
        
        if user:
            project_key = ndb.Key(urlsafe = project_urlString)
            project = project_key.get()
            requirement_container_list = []
            
            for requirement in Requirement.all(project.key):
                requirement_container = RequirementContainer(requirement = requirement, userstories = [])
                for userstory in UserStory.all(requirement.key):
                    requirement_container.userstories.append(UserStoryContainer(userstory = userstory, tasks = Task.all(userstory.key)))
                requirement_container_list.append(requirement_container)

            html = self.render_str("dynamic/tasks.body.html", project = project, requirement_container_list = requirement_container_list)
            dict = { 'content': html }
        else:
            dict = { "message": "please log in" }
        
        self.response.write(json.dumps(dict))

    def requirement(self):
        user = users.get_current_user()
        
        if user:
            operation = self.request.get('operation', default_value = None)
            
            if operation == 'create':
                project_key = ndb.Key(urlsafe = self.request.get('project-key'))
                new_requirement_id = str(int(Requirement.max_id(project_key)) + 1)
                requirement = Requirement(parent = project_key, author = user, id = new_requirement_id, title = None, content = None)
            elif operation == 'edit':
                requirement_key = ndb.Key(urlsafe = self.request.get('requirement-key'))
                #project_key = requirement_key.parent()
                requirement = requirement_key.get()
            
            #html = self.render_str("dynamic/requirement.body.html", project = project_key.get(), requirement = requirement)
            html = self.render_str("dynamic/requirement.body.html", requirement = requirement)
            dict = {
                'id': requirement.id,
                'title': requirement.title,
                'content': requirement.content,
                'html': html
            }
        else:
            dict = { 'message': 'please log in' }
        
        self.response.write(json.dumps(dict))

    def userstory(self):
        user = users.get_current_user()
        
        if user:
            operation = self.request.get('operation', default_value = None)
            
            if operation == 'create':
                requirement_key = ndb.Key(urlsafe = self.request.get('requirement-key'))
                project_key = requirement_key.parent()
                max_id = UserStory.max_id(requirement_key)
                index = max_id.rindex('.')
                new_id = max_id[:index + 1] + str(int(max_id[index + 1:]) + 1)
                userstory = UserStory(parent = project_key, author = user, id = new_id, title = None, content = None)
            elif operation == 'edit':
                userstory_key = ndb.Key(urlsafe = self.request.get('userstory-key'))
                requirement_key = userstory_key.parent()
                #project_key = requirement_key.parent()
                userstory = userstory_key.get()
            
            #html = self.render_str("dynamic/userstory.body.html", project = project_key.get(),userstory = userstory)
            html = self.render_str("dynamic/userstory.body.html", requirement_key = requirement_key.urlsafe(), userstory = userstory)
            dict = {
                'id': userstory.id,
                'title': userstory.title,
                'content': userstory.content,
                'html': html
            }
        else:
            dict = { 'message': 'please log in' }
        
        self.response.write(json.dumps(dict))

    def task(self):
        user = users.get_current_user()
        
        if user:
            operation = self.request.get('operation', default_value = None)
            
            if operation == 'create':
                userstory_key = ndb.Key(urlsafe = self.request.get('userstory-key'))
                max_id = Task.max_id(userstory_key)
                index = max_id.rindex('.')
                new_id = max_id[:index + 1] + str(int(max_id[index + 1:]) + 1)
                task = Task(parent = userstory_key, author = user, id = new_id, title = None, content = None)
            elif operation == 'edit':
                task_key = ndb.Key(urlsafe = self.request.get('task-key'))
                userstory_key = task_key.parent()
                userstory = userstory_key.get()
                task = task_key.get()
            
            #requirement_key = userstory_key.parent()
            #project_key = requirement_key.parent()
            #html = self.render_str("dynamic/task.body.html", project = project_key.get(),task = task)
            html = self.render_str("dynamic/task.body.html", userstory_key = userstory_key.urlsafe(), task = task)
            dict = {
                'id': task.id,
                'title': task.title,
                'content': task.content,
                'html': html
            }
        else:
            dict = { 'message': 'please log in' }
        
        self.response.write(json.dumps(dict))
    
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





class RequirementContainer:
    requirement = None
    userstories = []

    def __init__(self, requirement, userstories):
        self.requirement = requirement
        self.userstories = userstories

class UserStoryContainer:
    userstory = None
    tasks = []

    def __init__(self, userstory, tasks):
        self.userstory = userstory
        self.tasks = tasks



