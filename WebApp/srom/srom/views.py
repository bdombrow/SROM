from srom import app
from flask import Flask, render_template, request, flash
from plotting import getPlot
from forms import ContactForm
from contact import sendMessage

@app.route('/')
def index():
  plot, time = getPlot()
  return render_template('index.html', figure=plot, updated=time)
  
@app.route('/faq')
def faq():
  return render_template('faq.html')
  
@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()
  if request.method == 'POST':
    if form.validate() == False:
      flash("All fields are required!")
      return render_template('contact.html', form=form)
    else:
      sendMessage(form)
      return 'Thank You.'
  elif request.method == 'GET':
    return render_template('contact.html', form=form)