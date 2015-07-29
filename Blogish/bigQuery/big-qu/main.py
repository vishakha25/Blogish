#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import sys
import webapp2
import jinja2
import os
import httplib2
import json

from apiclient import discovery
from oauth2client import appengine
from oauth2client import client
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.api import users
from apiclient.discovery import build
from oauth2client.appengine import OAuth2DecoratorFromClientSecrets

template_dir= os.path.join(os.path.dirname(__file__),'templates')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
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
class Handler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)
    def render_str(self,template,**params):
        t=jinja_env.get_template(template)
        return t.render(params)
    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))
        
class MainHandler(Handler):
    def get(self):
        self.render('homepage.html')   


http = httplib2.Http(memcache)
service = discovery.build("bigquery", "v2", http=http)
decorator = appengine.oauth2decorator_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/bigquery',message=MISSING_CLIENT_SECRETS_MESSAGE)
PROJECTID="publicdata"

       
class OauthHandler(Handler):  
     @decorator.oauth_aware
     def get(self):
        variables = {
                     'url': decorator.authorize_url(),
                     'has_credentials': decorator.has_credentials()
                     }
        template = jinja_env.get_template('login.html')
        self.write(template.render(variables))


class AboutHandler(webapp2.RequestHandler):
    @decorator.oauth_required
    def get(self):
        try:
            http = decorator.http()
            user = service.people().get(userId='me').execute(http=http)
            text = 'Hello, %s!' % user['displayName']

            template = jinja_env.get_template('testpage.html')
            self.response.write(template.render({'text': text }))
        except client.AccessTokenRefreshError:
            self.redirect('/')

class HomeHandler(Handler):
    def get(self):
        self.render("testpage.html")
        
class ListDatasets(Handler):
  @decorator.oauth_required
  def get(self):
    """Lists the datasets in PROJECTID"""
    http = decorator.http()
    datasets = service.datasets()

    response = datasets.list(projectId=PROJECTID).execute(http)

    self.response.out.write('<h3>Datasets.list raw response:</h3>')
    self.response.out.write('<pre>%s</pre>' %
                            json.dumps(response, sort_keys=True, indent=4,
                                       separators=(',', ': ')))
    
    #query_data = {'query':'SELECT TOP(title, 10) as title, COUNT(*) as revision_count FROM [publicdata:samples.wikipedia] WHERE wp_namespace = 0;'}
    #query_request = bigquery_service.jobs()
    #query_response = query_request.query(projectId=PROJECT_NUMBER,
                                #         body=query_data).execute()
   # query_response = query_request.query(projectId=PROJECT_NUMBER,
                               #      body=query_data).execute()
    #print 'Query Results:'
       # for row in query_response['rows']:
        #    result_row = []
         #   for field in row['f']:
           #     result_row.append(field['v'])
             #   print ('\t').join(result_row)
            
                                    
                                       
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/permission',OauthHandler),
    ('/home',ListDatasets),
    #('/about',AboutHandler),
    (decorator.callback_path, decorator.callback_handler()),
], debug=True)
