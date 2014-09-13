from srom import app
from flask import Flask, render_template, request, flash
from plotting import getPlot
from forms import ContactForm
from contact import sendMessage

@app.route('/', methods=['GET'])
def index():
  site = request.args.get('s', 'Bing')
  plot, time = getPlot(site)
  return render_template('index.html', figure=plot, updated=time, optionList=['Bing', 'Google Custom Search'], selected=site)
  
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
      return render_template('thankyou.html')
  elif request.method == 'GET':
    return render_template('contact.html', form=form)