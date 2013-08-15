import jinja_worker

from google.appengine.api import users

class Handler_homepage(jinja_worker.Handler_jinja_worker):
    def get(self):
        user = users.get_current_user()
        if user:
            self.render("homepage.html", username = user.nickname(), url = users.create_logout_url('/'))
        else:
            self.render("homepage.html", username = None, url = users.create_login_url('/'))

        #self.response.out.write('<html><body>%s</body></html>' % greeting)
        #self.render("homepage.html", username = username)
        #self.redirect("/blog/signup")
