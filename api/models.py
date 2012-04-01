from google.appengine.ext import db
from google.appengine.api import mail
import simplejson as json

def emailProspectAwaitingVet(p):
    email = p.email
    name = p.name
    mail.send_mail(sender="Example.com Support <support@example.com>",
              to="Albert Johnson <Albert.Johnson@example.com>",
              subject="Your booking is awaiting confirmation",
              body="""BITCHES""")

def emailProspectConfirmingVet(p):
    email = p.email
    name = p.name
    mail.send_mail(sender="Example.com Support <support@example.com>",
              to="Albert Johnson <Albert.Johnson@example.com>",
              subject="Congratulations, booking successful!",
              body="""BITCHES""")

def emailExchangingDetails(p, e):
    prospectEmail = p.email
    prospectName = p.name

    employerEmail = e.email
    employerName = e.name
    employerCompany  = e.company
    
    mail.send_mail(sender="Example.com Support <support@example.com>",
              to="Albert Johnson <Albert.Johnson@example.com>",
              subject="Congratulations, booking successful!",
              body="""BITCHES""")

class Prospect(db.Model):
    skype = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    email = db.EmailProperty(required=True)
    education = db.StringProperty(required=True)
    linkedin = db.LinkProperty(required=False)
    github = db.LinkProperty(required=False)
    applicationDate = db.DateTimeProperty(auto_now_add=True)
    vetted = db.BooleanProperty(default=False)

    @staticmethod
    def addProspect(s, n, em, ed, ln, gh):
        p = Prospect(skype=s, name=n, email=em, education=ed, linkedin=ln, github=gh)
        p.put()
        emailProspectAwaitingVet(p)
        
class Employer(db.Model):
    skype = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    company = db.StringProperty(required=True)
    email = db.EmailProperty(required=True)

class Interest(db.Model):
    employer = db.ReferenceProperty(Employer, required=True)
    prospect = db.ReferenceProperty(Prospect)

class Booking(db.Model):
    employer = db.ReferenceProperty(Employer, required=True)
    prospect = db.ReferenceProperty(Prospect, required=True)
    when = db.DateTimeProperty(auto_now_add=True)

    happened = db.BooleanProperty(default=False)
    accepted = db.BooleanProperty(default=False)

    @staticmethod
    def renderBookings(employerSkype):
        bookingList = []
        for booking in Booking.all():
            if booking.employer.skype == employerSkype:
                bd = dict()
                p = booking.prospect
                bd["skype"] = p.skype
                bd["name"] = p.name
                bd["education"] = p.education
                bd["linkedin"] = p.linkedin
                bd["github"]= p.github
                bd["when"] = str(booking.when.isoformat())
                bookingList += [bd]

        bookingList.sort(lambda x, y: x["when"] > y["when"])
        return json.dumps(bookingList)

    @staticmethod
    def acceptBooking(prospectSkype, employerSkype):
        bookings = db.GqlQuery("SELECT * "
                            "FROM Booking "
                            "WHERE employer.skype IS :1 AND prospect.skype= :2",
                            employerSkype, prospectSkype)

        for booking in bookings:
            booking.accepted = True
            emailExchangingDetails(booking.prospect, booking.employee)
