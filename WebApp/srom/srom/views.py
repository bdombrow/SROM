from srom import app
from flask import Flask, render_template, request, flash
from plotting import getPlot
from forms import ContactForm
from contact import sendMessage
import psycopg2

@app.route('/', methods=['GET'])
def index():
  try:
    conn = psycopg2.connect(database='srom', user='srom_reader', host='10.9.73.10')
    curr = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    curr.execute("SELECT name FROM sites WHERE class != 'Disabled'")
    sites = [x.get('name') for x in curr.fetchall()]

    site = request.args.get('s', 'Bing')
    plot, time = getPlot(curr, site)
    curr.close()
    conn.close()
    return render_template('index.html', figure=plot, updated=time, optionList=sites, selected=site)
  except Exception as exc:
    return '<h2>Oops!</h2> <p>Looks like its broken.'

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