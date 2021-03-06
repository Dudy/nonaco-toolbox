﻿import logging

from google.appengine.api import users
from google.appengine.ext import ndb

class Task(ndb.Model):
    author = ndb.UserProperty(required = True)
    id = ndb.TextProperty(indexed = True, required = True)
    title = ndb.TextProperty(indexed = False, required = True)
    content = ndb.TextProperty(indexed = False, required = True)

    @classmethod
    def all(self, userstory_key):
        user = users.get_current_user()
        
        if user:
            query = self.query(ancestor = userstory_key).order(Task.id)
            tasks = query.fetch()
            userstory = userstory_key.get()
            project = userstory_key.parent().parent().get()
            
            if len(tasks) == 0:
                if project.title == "Toolbox":
                    if userstory.title == "Liste der Teammitglieder":
                        task = Task(parent = userstory_key, author = user, id = "2.1.1", title = 'Daten', content = 'Liste aller Benutzer; eigenes User-Objekt mit user_id, vollem Namen als DB Eintrag')
                        task.put()
                        task = Task(parent = userstory_key, author = user, id = "2.1.2", title = 'Darstellung Widget', content = 'span2, well, sidebar-nav, Navigationsliste (ul-li-li-...)')
                        task.put()
                        task = Task(parent = userstory_key, author = user, id = "2.1.3", title = 'Darstellung Eintrag', content = 'Farben blau (online) und grau (offline), nav-list und nav-header mit Anpassung für inactive und active')
                        task.put()
                    elif userstory.title == "Links in Teamliste":
                        task = Task(parent = userstory_key, author = user, id = "2.2.1", title = 'Logik 1', content = 'jQuery Funktion für class: $(\'.user_link\'), url: /json/chat/user_id')
                        task.put()
                        task = Task(parent = userstory_key, author = user, id = "2.2.2", title = 'Logik 2', content = 'jQuery Funktion setzt Sichtbarkeit des Chatfensters (display: none => display: block), füllt Inhalt mit Daten aus Ajax-Call aus Task \'Logik 1\'')
                        task.put()
                        task = Task(parent = userstory_key, author = user, id = "2.2.3", title = 'Darstellung', content = '<a> Tags ohne href, mit class = user_link, data-url = user_id')
                        task.put()
                    elif userstory.title == "neues Lesezeichen":
                        task = Task(parent = userstory_key, author = user, id = "1.3.1", title = 'Darstellung', content = 'oberster Eintrag der Liste ist leerer Eintrag mit placeholder "neue URL" und "neue Notiz", anstatt eines Löschen-Icons rechts oben gibt es ein Speichern-Icon')
                        task.put()
                        task = Task(parent = userstory_key, author = user, id = "1.3.2", title = 'Logik', content = 'wenn URL und Notiz gefüllt und Speichern geklickt wird, verschieben sich alle Listeneinträge eins nach unten, der neue Eintrag wird zweitoberster Eintrag und der oberste wird wieder leer, so wie an Anfang')
                        task.put()
                
                    tasks = query.fetch()
            
            return tasks
        else:
            return None

    @classmethod
    def max_id(self, userstory_key):
        task = self.query(ancestor = userstory_key).order(-Task.id).fetch(1)
        if task:
            id = task[0].id
        else:
            id = userstory_key.get().id + '.0' # this mimics "no entries"
        return id












