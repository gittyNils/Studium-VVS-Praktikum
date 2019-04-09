from google.appengine.ext import webapp #<callout id="co.import"/>
from google.appengine.ext.webapp.util import run_wsgi_app
import datetime

class WelcomePage(webapp.RequestHandler):#<callout id="co.class"/>
    def get(self):#<callout id="co.get"/>
        self.response.headers["Content-Type"] = "text/html"#<callout id="co.header"/>
        self.response.out.write(#<callout id="co.output"/>
          """<html>
               <head>
                 <title>Welcome to Nils Schlicher's chat service</title>
               </head>
               <body>
                 <h1>Welcome to Nils Schlicher's chat service</h1>
                 <p> The current time is: %s</p>
               </body>
             </html>
          """ % (datetime.datetime.now()))
        

chatapp = webapp.WSGIApplication([('/', WelcomePage)]) #<callout id="co.app"/>

def main(): #<callout id="co.main"/>
    run_wsgi_app(chatapp)

if __name__ == "__main__":
    main()


