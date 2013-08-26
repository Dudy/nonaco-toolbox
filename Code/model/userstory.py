import logging

from google.appengine.api import users
from google.appengine.ext import ndb

class UserStory(ndb.Model):
    author = ndb.UserProperty(required = True)
    id = ndb.TextProperty(indexed = True, required = True)
    title = ndb.TextProperty(indexed = False, required = True)
    content = ndb.TextProperty(indexed = False, required = True)

    @classmethod
    def all(self, requirement_key):
        user = users.get_current_user()
        
        if user:
            query = self.query(ancestor = requirement_key).order(UserStory.id)
            userstories = query.fetch()
            requirement = requirement_key.get()
            project = requirement_key.parent().get()
            
            if len(userstories) == 0:
                if project.title == "Toolbox":
                    if requirement.title == "Lesezeichen":
                        userstory = UserStory(parent = requirement_key, author = user, id = "1.1", title = 'Ansicht eines Lesezeichens', content = 'Als Benutzer möchte ich zu jedem Lesezeichen eine URL und einen kurzen Hinweistext eingeben können, damit beide Informationen später für alle verfügbar sind.')
                        userstory.put()
                        userstory = UserStory(parent = requirement_key, author = user, id = "1.2", title = 'Eintrag im Navigationsbaum', content = 'Als Benutzer möchte ich im linken Navigationsbaum einen Eintrag zum Ansteuern der Lesezeichenliste, damit ich mir dort die bestehenden ansehen kann.')
                        userstory.put()
                        userstory = UserStory(parent = requirement_key, author = user, id="1.3", title = 'neues Lesezeichen', content = 'Als Benutzer möchte ich in der Ansicht aller Lesezeichen einen Knopf haben, um ein neues Lesezeichen anlegen zu können.')
                        userstory.put()
                    elif requirement.title == "In-App Chat":
                        userstory = UserStory(parent = requirement_key, author = user, id = "2.1", title = 'Liste der Teammitglieder', content = 'Als Benutzer möchte ich rechts eine Liste aller Teammitglieder, um mit einem Blick zu sehen, wer online ist und wer nicht.')
                        userstory.put()
                        userstory = UserStory(parent = requirement_key, author = user, id = "2.2", title = 'Links in Teamliste', content = 'Als Benutzer möchte ich in der Liste aller Teammitglieder rechts die Namen als Link, um mit einem Mausklick ein Chatfenster zu diesem Benutzer öffnen zu können.')
                        userstory.put()
                    
                    userstories = query.fetch()
            
            return userstories
        else:
            return None