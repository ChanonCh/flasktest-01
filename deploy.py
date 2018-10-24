##########################################################
#!/usr/bin/env python

# Write your code below
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Deployed</hi>'

##########################################################