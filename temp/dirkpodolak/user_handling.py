######################################################################################################
# user handling
######################################################################################################

import jinja_worker
import re
import random
import string
import hashlib
import secret
import hmac
from google.appengine.ext import db

###########################
# statics
###########################
USER_RE     = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE    = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

###########################
# helper functions
###########################
def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PASSWORD_RE.match(password)

def valid_email(email):
    return EMAIL_RE.match(email)

def hash_str(s):
    return hmac.new(secret.SECRET, s).hexdigest()

def make_secure_val(s):
    return s + "|" + hash_str(s)

def check_secure_val(h):
    parts = h.split("|")
    s = parts[0]
    hash = parts[1]
    s_hash = hash_str(s)
    
    if s_hash == hash:
        return s
    else:
        return None

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)

def valid_pw(name, pw, h):
    return make_pw_hash(name, pw, h.split(',')[1]) == h

def get_user(username):
    if not username:
        return None
    
    key = db.Key.from_path('User', username)
    
    return db.get(key)

def get_username_from_cookie(self):
    username = None
    username_cookie_str = self.request.cookies.get('username')
    
    if username_cookie_str:
        cookie_val = check_secure_val(username_cookie_str)
        if cookie_val:
            return cookie_val
    
    return None

###########################
# user class
###########################
class User(db.Model):
    password = db.StringProperty(required = True)

###########################
# page flow handler
###########################
class Handler_blog_signup(jinja_worker.Handler_jinja_worker):
    def get(self):
        username = ""
        email = ""
        error_username = ""
        error_password = ""
        error_verify = ""
        error_email = ""
        self.render(
            "signup.html",
            link = "blog",
            title = "Blog",
            username = username,
            email = email,
            error_username = error_username,
            error_password = error_password,
            error_verify = error_verify,
            error_email = error_email)
    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        
        username_valid = valid_username(username)
        user = get_user(username)
        password_valid = valid_password(password)
        verify_valid = (password == verify)
        
        if email == "":
            email_valid = True
        else:
            email_valid = valid_email(email)
        
        if username_valid:
            if user:
                error_username = "That user already exists."
            else:
                error_username = ""
        else:
            error_username = "That's not a valid username."
        
        if password_valid:
            error_password = ""
        else:
            error_password = "That wasn't a valid password."
        
        if verify_valid:
            error_verify = ""
        else:
            error_verify = "Your passwords didn't match."
        
        if email_valid:
            error_email = ""
        else:
            error_email = "That's not a valid email."
        
        if not (username_valid and not user and password_valid and verify_valid and email_valid):
            self.render(
                        "signup.html",
                        link = "blog",
                        title = "Blog",
                        username = username,
                        email = email,
                        error_username = error_username,
                        error_password = error_password,
                        error_verify = error_verify,
                        error_email = error_email)
        else:
            User(key_name = username, password = make_pw_hash(username, password)).put()
            self.response.headers.add_header('Set-Cookie', 'username=%s; Path=/' % str(make_secure_val(username)))
            self.redirect('/blog')

class Handler_blog_login(jinja_worker.Handler_jinja_worker):
    def get(self):
        username = ""
        error = ""
        self.render("login.html", link = "blog", title = "Blog", username = username, error = error)
    def post(self):
        error = "Login invalid"
        username = self.request.get("username")
        password = self.request.get("password")
        username_valid = valid_username(username)

        if username_valid:
            user = get_user(username)
            
            if user:
                passwordhash_and_salt = user.password.split(",")
                passwordhash = passwordhash_and_salt[0]
                salt = passwordhash_and_salt[1]
                
                if user.password == make_pw_hash(username, password, salt):
                    self.response.headers.add_header('Set-Cookie', 'username=%s; Path=/' % str(make_secure_val(username)))
                    self.redirect('/blog/welcome')
        
        self.render("login.html", link = "blog", title = "Blog", username = username, error = error)

class Handler_blog_logout(jinja_worker.Handler_jinja_worker):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'username=; Path=/')
        self.redirect('/blog')

class Handler_blog_welcome(jinja_worker.Handler_jinja_worker):
    def get(self):
        username = None
        username_cookie_str = self.request.cookies.get('username')
        
        if username_cookie_str:
            cookie_val = check_secure_val(username_cookie_str)
            
            if cookie_val:
                username = cookie_val
                self.render("welcome.html", username = username)
            else:
                self.redirect('/signup')
        else:
            self.redirect('/signup')

    def post(self):
        if self.request.get("blog"):
            self.redirect("/blog")
        elif self.request.get("logout"):
            self.redirect("/blog/logout")
        elif self.request.get("newpost"):
            self.redirect("/blog/newpost")

###########################
# wiki page flow handler
###########################
class Handler_wiki_signup(jinja_worker.Handler_jinja_worker):
    def get(self):
        username = ""
        email = ""
        error_username = ""
        error_password = ""
        error_verify = ""
        error_email = ""
        self.render(
            "signup.html",
            link = "wiki",
            title = "Wiki",
            username = username,
            email = email,
            error_username = error_username,
            error_password = error_password,
            error_verify = error_verify,
            error_email = error_email)
    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        
        username_valid = valid_username(username)
        user = get_user(username)
        password_valid = valid_password(password)
        verify_valid = (password == verify)
        
        if email == "":
            email_valid = True
        else:
            email_valid = valid_email(email)
        
        if username_valid:
            if user:
                error_username = "That user already exists."
            else:
                error_username = ""
        else:
            error_username = "That's not a valid username."
        
        if password_valid:
            error_password = ""
        else:
            error_password = "That wasn't a valid password."
        
        if verify_valid:
            error_verify = ""
        else:
            error_verify = "Your passwords didn't match."
        
        if email_valid:
            error_email = ""
        else:
            error_email = "That's not a valid email."
        
        if not (username_valid and not user and password_valid and verify_valid and email_valid):
            self.render(
                        "signup.html",
                        link = "wiki",
                        title = "Wiki",
                        username = username,
                        email = email,
                        error_username = error_username,
                        error_password = error_password,
                        error_verify = error_verify,
                        error_email = error_email)
        else:
            User(key_name = username, password = make_pw_hash(username, password)).put()
            self.response.headers.add_header('Set-Cookie', 'username=%s; Path=/' % str(make_secure_val(username)))
            self.redirect('/wiki')

class Handler_wiki_login(jinja_worker.Handler_jinja_worker):
    def get(self):
        username = ""
        error = ""
        self.render("login.html", link = "wiki", title = "Wiki", username = username, error = error)
    def post(self):
        error = "Login invalid"
        username = self.request.get("username")
        password = self.request.get("password")
        username_valid = valid_username(username)

        if username_valid:
            user = get_user(username)
            
            if user:
                passwordhash_and_salt = user.password.split(",")
                passwordhash = passwordhash_and_salt[0]
                salt = passwordhash_and_salt[1]
                
                if user.password == make_pw_hash(username, password, salt):
                    self.response.headers.add_header('Set-Cookie', 'username=%s; Path=/' % str(make_secure_val(username)))
                    self.redirect('/wiki')
        
        self.render("login.html", link = "wiki", title = "Wiki", username = username, error = error)

class Handler_wiki_logout(jinja_worker.Handler_jinja_worker):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'username=; Path=/')
        self.redirect('/wiki')
