from flask.ext.wtf import Form
from wtforms.fields import TextField, TextAreaField, SubmitField
from wtforms.validators import Required, ValidationError, Email

class ContactForm(Form):
  name = TextField("Name", [Required("Please enter your name.")])
  email = TextField("Email", [Required("Please enter your email address"), Email()])
  subject = TextField("Subject", [Required("Please enter a subject")])
  message = TextAreaField("Message", [Required("Please enter a message")])
  submit = SubmitField("Send")