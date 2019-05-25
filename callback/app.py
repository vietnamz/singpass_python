from flask import make_response, Flask, flash, redirect, render_template, request, url_for
import os
import requests
from pprint import pprint as pp

MYINFO_APP_ENGINE_PROJECT = os.environ.get('PROJECT_ID')

app = Flask(__name__)

@app.route('/callback')
def callback():
    url = request.url
    pp(url)
    url = url.replace("http://localhost:3001", "https://{}.appspot.com".format(MYINFO_APP_ENGINE_PROJECT))
    pp(url)
    res = requests.get(url)
    return res.text

if __name__=='__main__':
    app.run(port=3001, debug=True)