from email.mime.text import MIMEText
from subprocess import Popen, PIPE
from forms import ContactForm

def sendMessage(form):
  msg = MIMEText(form.message.data)
  msg["From"] = form.email.data
  msg["To"] = "brent.dombrowski@gmail.com"
  msg["Subject"] = form.subject.data
  p = Popen(["/usr/sbin/sendmail", "-it"], stdin=PIPE)
  p.communicate(msg.as_string())