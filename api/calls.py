import cgi
import datetime
import urllib
import wsgiref.handlers

from django.utils import simplejson

from api.models import Prospect, Booking

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import mail

class RegisterProspect(webapp.RequestHandler):
    def get(self):
        skype = self.request.get("skype")
        name = self.requst.get("name")
        email = self.request.get("email")
        education = self.request.get("education")
        linkedin = self.request.get("linkedin")
        github = self.request.get("github")

        Prospect.addProspect(skype, name, email, education, linkedin, github)

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write('Hello, webapp World!')
        self.response.redirect("/booking/success.html")

class Bookings(webapp.RequestHandler):
    def get(self):
        skype = self.request.get("skype")
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(Booking.renderBookings(skype))

class ContactProspect(webapp.RequestHandler):
    def get(self):
        prospectSkype = self.request.get("prospectSkype")
        employerSkype = self.request.get("employerSkype")
        for booking in Booking.all():
            if booking.prospect.skype == prospectSkype and booking.employer.skype == employerSkype:
                booking.accepted = True
                booking.put()

class ContactList(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        for booking in Booking.all():
            if booking.accepted:
                self.response.out.write("WRIING")
                self.response.out.write("Introduce " + str(booking.employer.name)  + "(" + str(booking.employer.email) +  ") at " + str(booking.employer.company) + "  to "  + str(booking.prospect.name) + " (" + str(booking.prospect.email) + ")")
            

application = webapp.WSGIApplication([
  ('/api/bookings', Bookings),
    ('/api/list', ContactList),
  ('/api/prospects/contact', ContactProspect)
], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
