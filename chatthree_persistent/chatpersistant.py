from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import datetime
from google.appengine.ext import db


class ChatMessage(db.Model):
    user = db.StringProperty(required=True)
    timestamp = db.DateTimeProperty(auto_now_add=True)
    message = db.TextProperty(required=True)

    def __str__(self):
        return "%s (%s): %s" % (self.user, self.timestamp, self.message)

# Globale Variablen:
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
        messages = db.GqlQuery("SELECT * From ChatMessage ORDER BY timestamp")
        for msg in messages:
            self.response.out.write("<p>%s</p>" % msg)
        self.response.out.write("""
           <form action="/talk" method="post">
           <div><b>Name:</b> 
           <textarea name="name" rows="1" cols="20"></textarea></div>
           <p><b>Message</b></p>
           <div><textarea name="message" rows="5" cols="60"></textarea></div>
           <div><input type="submit" value="Send ChatMessage"></input></div>
           </form>
         </body>
       </html>
       """)




class ChatRoomCountViewPage(webapp.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/html"
        self.response.out.write("""
           <html>
             <head>
               <title>Nils Schlicher's AppEngine Chat Room (last 20)</title>
             </head>
             <body>
               <h1>Welcome to Nils Schlicher's AppEngine Chat Room</h1>
               <p>You are seeing the last 20 messages</p>
               <p>(Current time is %s)</p>
               <p>(This Service was started at %s)</p>
           """ % (datetime.datetime.now(), appStartTimestamp))
        # Nachrichten ausgeben
        messages = db.GqlQuery("SELECT * From ChatMessage ORDER BY " +
                               "timestamp DESC LIMIT 20").fetch(20)
        messages.reverse()
        for msg in messages:
            self.response.out.write("<p>%s</p>" % msg)
        self.response.out.write("""
           <form action="/talk" method="post">
           <div><b>Name:</b> 
           <textarea name="name" rows="1" cols="20"></textarea></div>
           <p><b>Message</b></p>
           <div><textarea name="message" rows="5" cols="60"></textarea></div>
           <div><input type="submit" value="Send ChatMessage"></input></div>
           </form>
         </body>
       </html>
       """)


class ChatRoomTimeViewPage(webapp.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/html"
        self.response.out.write("""
           <html>
             <head>
               <title>Nils Schlicher's AppEngine Chat Room (last 5 minutes)</title>
             </head>
             <body>
               <h1>Welcome to Nils Schlicher's AppEngine Chat Room</h1>
               <p>You are seeing the messages from the last 5 minutes</p>
               <p>(Current time is %s)</p>
               <p>(This Service was started at %s)</p>
           """ % (datetime.datetime.now(), appStartTimestamp))
        # Nachrichten ausgeben
        messages = ChatMessage.gql("WHERE timestamp > :fiveago ORDER BY timestamp", 
                                  fiveago=datetime.datetime.now() - datetime.timedelta(minutes=5))
        for msg in messages:
            self.response.out.write("<p>%s</p>" % msg)
        self.response.out.write("""
           <form action="/talk" method="post">
           <div><b>Name:</b> 
           <textarea name="name" rows="1" cols="20"></textarea></div>
           <p><b>Message</b></p>
           <div><textarea name="message" rows="5" cols="60"></textarea></div>
           <div><input type="submit" value="Send ChatMessage"></input></div>
           </form>
         </body>
       </html>
       """)

class ChatRoomPoster(webapp.RequestHandler):
    def post(self):
        chatter = self.request.get("name")
        msg = self.request.get("message")
        chatmsg = ChatMessage(user=chatter, message=msg)
        chatmsg.put()
        # Redirect zum Root, damit wir aktualisieren und alle Nachrichten sehen.
        self.redirect('/')


chatapp = webapp.WSGIApplication([('/', ChatRoomPage),
                                  ('/talk', ChatRoomPoster),
                                  ('/limited/count', ChatRoomCountViewPage),
                                  ('/limited/time', ChatRoomTimeViewPage)])


def main():
    run_wsgi_app(chatapp)

if __name__ == "__main__":
    #dieses Programm wird selbst ausgeführt. Deshalb hier die Startzeit nehmen
    global appStartTimestamp
    appStartTimestamp = datetime.datetime.now()
    main()


