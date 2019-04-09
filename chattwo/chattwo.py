from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import datetime


class ChatMessage(object):
    def __init__(self, user, msg):
        self.user = user
        self.message = msg
        self.time = datetime.datetime.now()

    def __str__(self):
        return "%s (%s): %s" % (self.user, self.time, self.message)

# Globale Variablen:
Messages = []
appStartTimestamp = 0

class ChatRoomPage(webapp.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/html"
        self.response.out.write("""
           <html>
             <head>
               <title>Nils Schlicher's AppEngine Chat Room</title>
             </head>
             <body>
               <h1>Welcome to Nils Schlicher's AppEngine Chat Room</h1>
               <p>(Current time is %s)</p>
               <p>(This Service was started at %s)</p>
           """ % (datetime.datetime.now(), appStartTimestamp))
        # Nachrichten ausgeben
        global Messages
        for msg in Messages:
            self.response.out.write("<p>%s</p>" % msg)
        self.response.out.write("""
           <form action="" method="post">
           <div><b>Name:</b> 
           <textarea name="name" rows="1" cols="20"></textarea></div>
           <p><b>Message</b></p>
           <div><textarea name="message" rows="5" cols="60"></textarea></div>
           <div><input type="submit" value="Send ChatMessage"></input></div>
           </form>
         </body>
       </html>
       """)

    def post(self):
        chatter = self.request.get("name")
        msg = self.request.get("message")
        global Messages
        Messages.append(ChatMessage(chatter, msg))
        # Redirect zum Root, damit wir aktualisieren und alle Nachrichten sehen.
        self.redirect('/')


chatapp = webapp.WSGIApplication([('/', ChatRoomPage)])


def main():
    run_wsgi_app(chatapp)

if __name__ == "__main__":
    #dieses Programm wird selbst ausgeführt. Deshalb hier die Startzeit nehmen
    global appStartTimestamp
    appStartTimestamp = datetime.datetime.now()
    main()


