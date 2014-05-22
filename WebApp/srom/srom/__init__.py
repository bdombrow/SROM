from flask import Flask
app = Flask(__name__)
app.secret_key = 'replace this with a real secret key'

import srom.views

