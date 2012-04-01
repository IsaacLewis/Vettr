import cgi
import datetime
import urllib
import wsgiref.handlers

from api.models import Employer, Prospect

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

LEFT = "[[["
RIGHT = "]]]"

def CSS(str):
    return '<link rel="stylesheet" type="text/css" href="'+str+'" />'

def JS(str):
    return '<script type="text/javascript" src="'+str+'"></script>'

def INCLUDE(str):
    f = file(str, "r")
    return f.read()

def RENDER(string, **ctx):
    t = INCLUDE(string)
    return process(t, ctx)

def RENDER_DICT(string, ctx):
    t = INCLUDE(string)
    return process(t, ctx)

def RENDER_JSON(string, f):
    t = INCLUDE(string)
    return process(t, json.loads(INCLUDE(f)))

generalContent = dict(CSS=CSS, INCLUDE=INCLUDE, RENDER=RENDER, RENDER_DICT=RENDER_DICT, RENDER_JSON=RENDER_JSON)

def process(string, ctx=None):
    p1 = string.partition(LEFT)
    start = p1[0]
    if p1[2] != "":
        p2 = p1[2].partition(RIGHT)
        if p2[1] == RIGHT:
            rest = p2[2]
            code = p2[0]

            if(not(ctx)):
              ctx = generalContent
            
            middle =  eval(code, ctx)
            final = process(rest, ctx)
            return start + str(middle) + final
        else:
            print "Malformed Expression"
            return ""
    else:
        return start

class MainPage(webapp.RequestHandler):
    def get(self):
      self.response.headers['Content-Type'] = 'text/html'
      self.response.out.write(RENDER("static/index.html"))

class EmployerPage(webapp.RequestHandler):
    def get(self):
      self.response.headers['Content-Type'] = 'text/html'
      self.response.out.write(RENDER("static/index.html"))

class ProspectPage(webapp.RequestHandler):
    def get(self):
      self.response.headers['Content-Type'] = 'text/html'
      self.response.out.write(RENDER("static/signup.html"))

    def post(self):
      skype = self.request.get("skype")
      name = self.request.get("name")
      email = self.request.get("email")
      education = self.request.get("education")
      
      linkedin = self.request.get("linkedin")
      github = self.request.get("github")

      if(github == ""):
        github = None
      else:
        if "http://" not in github:
          github = "http://"  + github

      if(linkedin == ""):
        linkedin = None
      else:
        if "http://" not in linkedin:
          github = "http://"  + linkedin
      
      Prospect.addProspect(skype, name, email, education, linkedin, github)
      self.response.redirect("/potential/complete", permanent=False)

class ProspectComplete(webapp.RequestHandler):
    def get(self):
      self.response.headers['Content-Type'] = 'text/html'
      self.response.out.write(RENDER("static/signup.html"))

application = webapp.WSGIApplication([
  ('/', MainPage),
  ('/potential', ProspectPage),
  ('/potential/complete', ProspectPage),
  ('/employer', EmployerPage),
], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
