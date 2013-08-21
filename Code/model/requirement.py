from google.appengine.api import users
from google.appengine.ext import ndb

class Requirement(ndb.Model):
    author_id = ndb.TextProperty(indexed = False, required = True)
    id = ndb.TextProperty(indexed = True, required = True)
    title = ndb.TextProperty(indexed = False, required =  True)
    content = ndb.TextProperty(indexed = False, required =  True)
    
    @classmethod
    def all(self, project):
        query = self.query(ancestor = project)
        requirements = query.fetch()
        project_obj = project.get()
        
        if len(requirements) == 0 and project_obj.title == "Toolbox":
            requirement = Requirement(parent = project, author_id = '185804764220139124118', id = "1", title = 'Lesezeichen', content = 'Jeder findet ab und zu mal einen nützlichen Link. Es soll eine Möglichkeit geben, eine URL zu speichern. Dazu soll man eine kleine Notiz speichern können, z.B. "Vorlage für Design" oder ähnliches. Die gesammelten Links kann man sich in einer Liste ansehen, zu der es im Navigationsbaum den Punkt "Links" gibt. Später soll es Kategorien geben.')
            requirement.put()
            requirement = Requirement(parent = project, author_id = '185804764220139124118', id = "2", title = 'In-App Chat', content = 'Eine Liste soll alle Teammitglieder mit Online Status anzeigen. Bei Klick auf den Namen eines Teammitglieds, das online ist, soll ein Chatfenster aufgehen.')
            requirement.put()
            requirements = query.fetch()
        
        return requirements