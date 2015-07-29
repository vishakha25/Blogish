import os
import webapp2
import jinja2
import json
import sys

import httplib2
import logging

import pickle

from apiclient import discovery
from oauth2client import appengine
from oauth2client import client
from google.appengine.api import memcache
from google.appengine.ext import db
from oauth2client import client

template_dir= os.path.join(os.path.dirname(__file__),'templates')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    autoescape=True,
    extensions=['jinja2.ext.autoescape'])


## adding Oauth ##############

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

# Helpful message to display in the browser if the CLIENT_SECRETS file
# is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
<h1>Warning: Please configure OAuth 2.0</h1>
<p>
To make this sample run you will need to populate the client_secrets.json file
found at:
</p>
<p>
<code>%s</code>.
</p>
<p>with information found on the <a
href="https://code.google.com/apis/console">APIs Console</a>.
</p>
""" % CLIENT_SECRETS


########################




class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)
    def render_str(self,template,**params):
        t=jinja_env.get_template(template)
        return t.render(params)
    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))
    
class MainPage(Handler):
    def get(self):
        items= self.request.get_all("food")
        self.render("shopping_list.html", items=items)
        self.write(sys.modules)

        
class FizzBuzzHandler(Handler):        
    def get(self):
        n=self.request.get("n")
        n=int(n)
        self.render("fizzBuzz.html",n=n)
 

http = httplib2.Http(memcache)
service = discovery.build("plus", "v1", http=http)
decorator = appengine.oauth2decorator_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/plus.me',
    message=MISSING_CLIENT_SECRETS_MESSAGE)

class MainHandler(webapp2.RequestHandler):
    @decorator.oauth_aware
    def get(self):
        variables = {
                     'url': decorator.authorize_url(),
                     'has_credentials': decorator.has_credentials()
                     }
        template = JINJA_ENVIRONMENT.get_template('grant.html')
        self.response.write(template.render(variables))


class AboutHandler(webapp2.RequestHandler):
    @decorator.oauth_required
    def get(self):
        try:
            http = decorator.http()
            user = service.people().get(userId='me').execute(http=http)
            text = 'Hello, %s!' % user['displayName']

            template = JINJA_ENVIRONMENT.get_template('welcome.html')
            self.response.write(template.render({'text': text }))
        except client.AccessTokenRefreshError:
            self.redirect('/')
 
        
app = webapp2.WSGIApplication([
                               ('/', MainPage),
                               ('/fizzbuzz',FizzBuzzHandler),
                               ('/hello', MainHandler),
                               ('/about', AboutHandler),
     (decorator.callback_path, decorator.callback_handler()),
                               ], debug=True)