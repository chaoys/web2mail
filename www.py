import logging
import webapp2
from google.appengine.api.app_identity import app_identity
from google.appengine.api import urlfetch
from google.appengine.api import mail
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

appid = app_identity.get_application_id()
mail_sender='www@'+appid+'.appspotmail.com'

class RMailHandler(InboundMailHandler):
	def receive(self, msg):
		logging.info(msg.sender + " " + msg.subject)
		if msg.subject:
			UrlHandler(msg.subject, msg.sender)

def UrlHandler(url, receipt):
	try:
		logging.info("fetching "+url)
		result = urlfetch.Fetch(url, deadline=30) 
		if result.status_code == 200:
			logging.info("done "+url)
			TMailHandler(receipt, result.content, "Re: "+url)
		else:
			logging.error(url+":"+result.status)
	except Exception, e:
		print(e)
		return None

def TMailHandler(r, c, s):
	mail.send_mail(sender=mail_sender, to=r, subject=s, body=c)

app = webapp2.WSGIApplication([RMailHandler.mapping()], debug=True)
