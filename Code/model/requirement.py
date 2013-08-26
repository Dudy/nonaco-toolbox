import logging

from google.appengine.api import users
from google.appengine.ext import ndb

class Requirement(ndb.Model):
    author = ndb.UserProperty(required = True)
    id = ndb.TextProperty(indexed = True, required = True)
    title = ndb.TextProperty(indexed = False, required =  True)
    content = ndb.TextProperty(indexed = False, required =  True)
    
    @classmethod
    def all(self, project_key):
        user = users.get_current_user()
        
        if user:
            query = self.query(ancestor = project_key).order(Requirement.id)
            requirements = query.fetch()
            project = project_key.get()
            
            if len(requirements) == 0 and project.title == "Toolbox":
                requirement = Requirement(parent = project_key, author = user, id = "1", title = 'Lesezeichen', content = 'Jeder findet ab und zu mal einen nützlichen Link. Es soll eine Möglichkeit geben, eine URL zu speichern. Dazu soll man eine kleine Notiz speichern können, z.B. "Vorlage für Design" oder ähnliches. Die gesammelten Links kann man sich in einer Liste ansehen, zu der es im Navigationsbaum den Punkt "Links" gibt. Später soll es Kategorien geben.')
                requirement.put()
                requirement = Requirement(parent = project_key, author = user, id = "2", title = 'In-App Chat', content = 'Eine Liste soll alle Teammitglieder mit Online Status anzeigen. Bei Klick auf den Namen eines Teammitglieds, das online ist, soll ein Chatfenster aufgehen.')
                requirement.put()
                requirements = query.fetch()
            
            return requirements
        else:
            return None