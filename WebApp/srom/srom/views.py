from srom import app
from flask import render_template
from plotting import getPlot

@app.route('/')
def index():
  plot, time = getPlot()
  return render_template('index.html', figure=plot, updated=time)