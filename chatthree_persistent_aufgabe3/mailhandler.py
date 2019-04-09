import email
from google.appengine.ext import webapp 
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler 
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import mail
from google.appengine.ext import db
import logging


# Klasse für DataSTore
class ChatMessage(db.Model):
    user = db.StringProperty(required=True)
    timestamp = db.DateTimeProperty(auto_now_add=True)
    message = db.TextProperty(required=True)

    def __str__(self):
        return "%s (%s): %s" % (self.user, self.timestamp, self.message)


class ChatMailHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("Received a message from: " + mail_message.sender)
        user = mail_message.sender
        message = ""

        # nur den PlainText aus der Nachricht holen
        for content_type, body in mail_message.bodies('text/plain'):
            message += body.decode()

        # Nachricht zum Chat hinzufügen
        chatmsg = ChatMessage(user=user, message=message)
        chatmsg.put()

        # Email zur bestätigung an Absender zurück
        mail.send_mail(sender="noreply@nils-schlicher-chatroom-003.appspotmail.com",
                       to=mail_message.sender,
                       subject="Weiterleitung an Chat: %s" % mail_message.subject,
                       body="Nachricht in Chat eingefuegt:\n" + message
                       )

chatmail = webapp.WSGIApplication([ChatMailHandler.mapping()])

def main():
    run_wsgi_app(chatmail)


if __name__ == "__main__":
    main()

