from google.appengine.ext import db
from google.appengine.api import mail
import simplejson as json

from api.models import *

p = Prospect(skype="robertwhitehead.07", name="Robert Whitehead", email="robertwhitehead.07@gmail.com", github=db.Link("http://www.github.com/robert00700"), education="University of Cambridge", linkedin=db.Link("http://www.linkedin.com/profile/view?id=9391391&locale=en_US&trk=tab_pro"))
p.put()

e = Employer(skype="robertwhitehead.07", name="Barry Smith", company="Twatter", email="rw401@cam.ac.uk")
e.put()

i = Interest(employer = e, prospect = p)
i.put()

b = Booking(employer=e, prospect=p, when="1333286123")
b.put()



