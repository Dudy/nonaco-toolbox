from google.appengine.ext import ndb

PROJECT_LIST_DB_KEY_NAME = 'project_list_db_key'

class Project(ndb.Model):
    title = ndb.TextProperty(indexed = True, required = True)

    @classmethod
    def project_db_key(self):
        return ndb.Key('Project', PROJECT_LIST_DB_KEY_NAME)

    @classmethod
    def all(self):
        query = self.query(ancestor = self.project_db_key()).order(Project.title)
        projects = query.fetch()
        
        if len(projects) == 0:
            project = Project(parent = self.project_db_key(), title = 'Toolbox')
            project.put()
            project = Project(parent = self.project_db_key(), title = 'Notify.me')
            project.put()
            project = Project(parent = self.project_db_key(), title = 'SourcecodeBroker')
            project.put()
            projects = query.fetch()
        
        return projects