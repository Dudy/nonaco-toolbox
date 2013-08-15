######################################################################################################
# wiki main handler
######################################################################################################
import jinja_worker
import user_handling
import wikientry
import json
import time
import logging

from google.appengine.ext import db
from google.appengine.api import memcache

dirty = { "frontpage":True }

def get_page(url):
    global dirty
    page = memcache.get(url)
    if page is None or dirty.get(url):
        query = db.Query(wikientry.Wikientry)
        query.filter('url =', url)
        query.order('-created')
        page = query.get()
        if page:
            memcache.set(url, page)
            dirty[url] = False
    return page

class Handler_wiki_edit(jinja_worker.Handler_jinja_worker):
    def get(self, url):
        self.set_autoescape(False)
        
        url = url[1:] # strip off leading slash
        username = user_handling.get_username_from_cookie(self)
        
        if username:
            page = get_page(url)
            if not page:
                page = wikientry.Wikientry(url = url, content = "")
            
            self.render("edit_wiki_page.html", wikientry = page, username = username)
            self.set_autoescape(False)
        else:
            page = get_page(url)
            if page:
                self.redirect("/wiki/" + url)
            else:
                self.redirect("/wiki/frontpage")

    def post(self, url):
        url = url[1:] # strip off leading slash
        global dirty
        page = wikientry.Wikientry(url = url, content = self.request.get("content"))
        memcache.set(url, page)
        dirty[url] = False
        page.put()
        self.redirect("/wiki/" + url)

class Handler_wiki_history(jinja_worker.Handler_jinja_worker):
    def get(self, url = None):
        self.set_autoescape(True)
        
        if url is None:
            self.redirect("/wiki/_history/frontpage")
            return
        
        url = url[1:] # strip off leading slash
        username = user_handling.get_username_from_cookie(self)
        
        page = get_page(url)
        if page:
            # history is not cached at all
            query = db.Query(wikientry.Wikientry)
            query.filter('url =', url)
            query.order('-created')
            history_page_list = query.run()
            self.render("history_wiki_page.html", wikientry = page, entries = history_page_list, username = username)
        else:
            self.redirect("/wiki/_edit/" + url)

class Handler_wiki_showpage(jinja_worker.Handler_jinja_worker):
    def get(self, url = None):
        self.set_autoescape(False)
        
        if url is None or url == "/wiki":
            self.redirect("/wiki/frontpage")
            return
        
        url = url[1:] # strip off leading slash
        username = user_handling.get_username_from_cookie(self)
        
        version_number = self.request.get('v')
        if version_number:
            query = db.Query(wikientry.Wikientry)
            query.filter('url =', url)
            query.order('created')
            history_page = query.get(offset = int(version_number))
            if history_page:
                self.render("view_wiki_page.html", wikientry = history_page, username = username)
            else:
                self.redirect("/wiki")
        else:
            page = get_page(url)
            if page:
                self.render("view_wiki_page.html", wikientry = page, username = username)
            else:
                if url == "frontpage":
                    global dirty
                    new_frontpage = wikientry.Wikientry(url = "frontpage", content = "Welcome!")
                    memcache.set(url, new_frontpage)
                    dirty[url] = False
                    new_frontpage.put()
                    self.redirect("/wiki/frontpage")
                    pass
                else:
                    self.redirect("/wiki/_edit/" + url)
        
        self.set_autoescape(True)

class Handler_blog_newpost(jinja_worker.Handler_jinja_worker):
    def get(self):
        username = user_handling.get_username_from_cookie(self)
        self.render("newpost.html", username = username)
    
    def post(self):
        global dirties
        
        username = user_handling.get_username_from_cookie(self)
        subject = self.request.get("subject")
        content = self.request.get("content")
        
        if subject and content:
            a = blogentry.Blogentry(subject = subject, content = content)
            a.put()
            dirties[0] = True
            
            self.redirect("/blog/" + str(a.key().id()))
        else:
            error = "we need both a subject and some content!"
            self.render("newpost.html", subject = subject, content = content, error = error, username = username)

class Handler_blog_permalink(jinja_worker.Handler_jinja_worker):
    def get(self, id):
        global dirties
        global last_query_times
        
        username = user_handling.get_username_from_cookie(self)
        
        int_id = int(id)
        be = memcache.get('permalink_' + id)
        
        if be is None or dirties.get(int_id) is None or dirties.get(int_id) == True:
            logging.error("load")
            be = blogentry.Blogentry.get_by_id(int_id)
            memcache.set('permalink_' + id, be)
            last_query_times[int_id] = time.time()
            age = 0
            dirties[int_id] = False
            logging.error("dirties[int_id] = " + str(dirties[int_id]))
        else:
            logging.error("don't load")
            if not last_query_times.get(int_id):
                last_query_times[int_id] = time.time()
            age = int(time.time() - last_query_times.get(int_id))
        
        self.render("permalink.html", blogentry = be, username = username, age = age)

    def post(self, id):
        if self.request.get("logout"):
            self.redirect("/blog/logout")
        elif self.request.get("newpost"):
            self.redirect("/blog/newpost")

class Handler_blog_json(jinja_worker.Handler_jinja_worker):
    def get(self, id = None):
        json_output = ""
        
        if id:
            be = blogentry.Blogentry.get_by_id(int(id))
            json_output = "[" + be.get_json() + "]"
        else:
            json_output = "["
            blogentries = db.GqlQuery("select * from Blogentry order by created desc limit 10")
            blogentries = list(blogentries)
 
# auch eine Moeglichkeit, im Forum gefunden: http://forums.udacity.com/cs253-april2012/questions/21869/lost-in-hw-5
#            json_output = [{'subject': blogentry.title,
#                            'content': blogentry.post,
#                            'created': str(blogentry.created.strftime('%a %b %d %H:%M:%S %Y')),
#                            'last_modified': str(blogentry.last_modified.strftime('%a %b %d %H:%M:%S %Y'))
#                           } for blogentry in blogentries]
            
            for be in blogentries:
                json_output += be.get_json() + ','
            json_output = json_output[0:-1] + "]"
            
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.response.out.write(json.dumps(json_output))

class Handler_blog_flush(jinja_worker.Handler_jinja_worker):
    def get(self):
        global dirties
        for d in dirties:
            dirties[d] = True
        memcache.flush_all()
        self.redirect('/blog')