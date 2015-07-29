import os
import json
import sys


from apiclient.discovery import build

from google.appengine.ext import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app

from oauth2client.appengine import OAuth2DecoratorFromClientSecrets

decorator = OAuth2DecoratorFromClientSecrets(
  os.path.join(os.path.dirname(__file__), 'client_secrets.json'),
  scope='https://www.googleapis.com/auth/bigquery')

PROJECTID = 'blogish-1'

service = build('bigquery', 'v2')


class ListDatasets(webapp.RequestHandler):
  @decorator.oauth_required
  def get(self):
    http = decorator.http()

    datasets = service.datasets()
    try:
      response = datasets.list(projectId=PROJECTID).execute(http)

      self.response.out.write('<h3>Datasets.list raw response:</h3>')
      self.response.out.write('<pre>%s</pre>' % json.dumps(response,
                                                  sort_keys=True,
                                                  indent=4,
                                                  separators=(',', ': ')))
    except:
      e = str(sys.exc_info()[0]).replace('&', '&amp;'
                               ).replace('"', '&quot;'
                               ).replace("'", '&#39;'
                               ).replace(">", '&gt;'
                               ).replace("<", '&lt;')
      self.response.out.write( "<p>Error: %s</p>" % e )

application = webapp2.WSGIApplication([
                ('/login', ListDatasets),
                (decorator.callback_path, decorator.callback_handler()),
                ], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()