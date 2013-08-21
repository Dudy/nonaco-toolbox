from google.appengine.api import users
from google.appengine.ext import ndb

class UserStory(ndb.Model):
    author_id = ndb.TextProperty(indexed = False, required = True)
    id = ndb.TextProperty(indexed = False, required = True)
    title = ndb.TextProperty(indexed = False, required = True)
    content = ndb.TextProperty(indexed = False, required = True)

    @classmethod
    def all(self, requirement):
        query = self.query(ancestor = requirement)
        userstories = query.fetch()
        requirement_obj = requirement.get()
        project_obj = requirement.parent().get()
        
        if len(userstories) == 0:
            if project_obj.title == "Toolbox":
                if requirement_obj.title == "Lesezeichen":
                    userstory = UserStory(parent = requirement, author_id = '185804764220139124118', id = "1.1", title = 'Ansicht eines Lesezeichens', content = 'Als Benutzer möchte ich zu jedem Lesezeichen eine URL und einen kurzen Hinweistext eingeben können, damit beide Informationen später für alle verfügbar sind.')
                    userstory.put()
                    userstory = UserStory(parent = requirement, author_id = '185804764220139124118', id = "1.2", title = 'Eintrag im Navigationsbaum', content = 'Als Benutzer möchte ich im linken Navigationsbaum einen Eintrag zum Ansteuern der Lesezeichenliste, damit ich mir dort die bestehenden ansehen kann.')
                    userstory.put()
                    userstory = UserStory(parent = requirement, author_id = '185804764220139124118', id="1.3", title = 'neues Lesezeichen', content = 'Als Benutzer möchte ich in der Ansicht aller Lesezeichen einen Knopf haben, um ein neues Lesezeichen anlegen zu können.')
                    userstory.put()
                elif requirement_obj.title == "In-App Chat":
                    userstory = UserStory(parent = requirement, author_id = '185804764220139124118', id = "2.1", title = 'Liste der Teammitglieder', content = 'Als Benutzer möchte ich rechts eine Liste aller Teammitglieder, um mit einem Blick zu sehen, wer online ist und wer nicht.')
                    userstory.put()
                    userstory = UserStory(parent = requirement, author_id = '185804764220139124118', id = "2.2", title = 'Links in Teamliste', content = 'Als Benutzer möchte ich in der Liste aller Teammitglieder rechts die Namen als Link, um mit einem Mausklick ein Chatfenster zu diesem Benutzer öffnen zu können.')
                    userstory.put()
            
            userstories = query.fetch()
        
        return userstories