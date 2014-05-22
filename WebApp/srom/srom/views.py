from srom import app
from flask import Flask, render_template, request
from plotting import getPlot
from forms import ContactForm

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
    return 'Form posted.'
  elif request.method == 'GET':
    return render_template('contact.html', form=form)