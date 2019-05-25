#!/usr/bin/env python
from datetime import datetime
from pprint import pprint as pp
from flask import make_response, Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, \
                            login_required, login_user, logout_user 
from data_handler import validateUserLogin, generateSessionEntity, query_data, updateSessionEntity
import uuid
import json
import os
import logging
import requests
from security import security

AUTH_LEVEL = os.environ.get('AUTH_LEVEL')
DEMO_APP_SIGNATURE_CERT_PRIVATE_KEY = os.environ.get('DEMO_APP_SIGNATURE_CERT_PRIVATE_KEY')
MYINFO_CONSENTPLATFORM_SIGNATURE_CERT_PUBLIC_CERT = os.environ.get('MYINFO_CONSENTPLATFORM_SIGNATURE_CERT_PUBLIC_CERT')
MYINFO_APP_CLIENT_ID = os.environ.get('MYINFO_APP_CLIENT_ID')
MYINFO_APP_CLIENT_SECRET = os.environ.get('MYINFO_APP_CLIENT_SECRET')
MYINFO_APP_REALM = os.environ.get('MYINFO_APP_REALM')
MYINFO_APP_REDIRECT_URL = os.environ.get('MYINFO_APP_REDIRECT_URL')
MYINFO_API_AUTHORISE= os.environ.get('MYINFO_API_AUTHORISE')
MYINFO_API_TOKEN= os.environ.get('MYINFO_API_TOKEN')
MYINFO_API_PERSON= os.environ.get('MYINFO_API_PERSON')
MYINFO_APP_ENGINE_PROJECT = os.environ.get('PROJECT_ID')

_attributes = "name,sex,race,nationality,dob,email,mobileno,regadd,housingtype,hdbtype,marital,edulevel,assessableincome,ownerprivate,assessyear,cpfcontributions,cpfbalances"

person_test =  {
                    "link" : "http://localhost:3001/myinfo/S9812381D",
                    "users":[
                                {
                                "name":"TAN XIAO HUI",
                                "sex": "F",
                                "race": "CN",
                                "nationality": "SG",
                                "dob":"1970-05-17",
                                "email": "myinfotesting@gmail.com",
                                "mobileno": "+97399245",
                                "regadd": "SG, 128 street BEDOK NORTH AVENUE 4 block 102 postal 460102 floor 09 building PEARL GARDEN", 
                                "hdbtype":"113",
                                "marital": "1",
                                "edulevel": "3",
                                "assessableincome": "1456789.00",
                                "uinfin":"S9812381D"
                                }
                            ]
                }


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# silly user model
class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"
        
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)
def refill_data(person):
    data = dict()
    data['name'] = person['name']['value']
    data['sex'] = person['sex']['value']
    data['race'] = person['race']['value']
    data['nationality'] = person['nationality']['value']
    data['dob'] = person['dob']['value']
    data['email'] = person['email']['value']
    data['mobileno'] = person['mobileno']['prefix'] + person['mobileno']['code'] + person['mobileno']['nbr']
    data['edulevel'] = person['edulevel']['value']
    data['assessableincome'] = person['assessableincome']['value']
    data['hdbtype'] = person['hdbtype']['value']
    data['marital'] = person['marital']['value']
    data['regadd'] = person['regadd']['block'] + " " + person['regadd']['building'] + " " + person['regadd']['floor'] 
    data['regadd'] += " " + person['regadd']['street'] + " " + person['regadd']['postal'] + " " + person['regadd']['country']
    return data

# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User(userid)

@app.route('/')
@login_required
def index():
    return redirect(url_for('login'))

@app.route('/dashboard/<userId>')
@login_required
def dashboard(userId):
    session = generateSessionEntity(userId)
    pp(MYINFO_APP_ENGINE_PROJECT)
    if MYINFO_APP_ENGINE_PROJECT != "":
        link = "https://{}.appspot.com/myinfo/{}".format(MYINFO_APP_ENGINE_PROJECT, str(session))
    else:
        link = "http://localhost:3001/myinfo/{}".format(str(session))
    payload = dict()
    payload['link'] = link
    data = query_data(userId)
    payload['users'] = data
    return render_template('dashboard.html', data=payload)

def format_response(res):
    res= json.dumps(res, indent = 4)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r

@app.route('/getEnv')
def getEnv():
    res = dict()
    res['authLevel'] = AUTH_LEVEL
    res['privateKey'] = DEMO_APP_SIGNATURE_CERT_PRIVATE_KEY
    res['publickKey'] = MYINFO_CONSENTPLATFORM_SIGNATURE_CERT_PUBLIC_CERT
    res['clientId'] = MYINFO_APP_CLIENT_ID
    res['secretKey'] = MYINFO_APP_CLIENT_SECRET
    res['realm'] = MYINFO_APP_REALM
    res['redirectUrl'] = MYINFO_APP_REDIRECT_URL
    return format_response(res)

@app.route('/myinfo/<sessionId>')
def myInfo(sessionId):
    return render_template('consent_given.html', data=sessionId)

def token_request(code):
    cacheCtl = "no-cache"
    contentType = "application/x-www-form-urlencoded"
    url = MYINFO_API_TOKEN
    params = {}
    params['grant_type'] = 'authorization_code'
    params['code'] = code
    params['redirect_uri'] = MYINFO_APP_REDIRECT_URL
    params['client_id'] = MYINFO_APP_CLIENT_ID
    params['client_secret'] = MYINFO_APP_CLIENT_SECRET
    headers = dict()
    headers['Content-Type'] = contentType
    headers['Cache-Control'] = cacheCtl
    authHeaders = None
    if AUTH_LEVEL == "L0":
        authHeaders = ""
    else:
        authHeaders = security.generateAuthorizationHeader(url,
                                                            params,
                                                            "POST",
                                                            contentType,
                                                            AUTH_LEVEL,
                                                            MYINFO_APP_CLIENT_ID,
                                                            DEMO_APP_SIGNATURE_CERT_PRIVATE_KEY,
                                                            MYINFO_APP_CLIENT_SECRET,
                                                            MYINFO_APP_REALM)
    if authHeaders != "":
        headers['Authorization'] = authHeaders
    pp(headers)
    res = requests.post(url, data=params, headers=headers)
    return res

def person_request(uinfin, validToken):
    pp(uinfin)
    pp(validToken)
    cacheCtl = "no-cache"
    params = {}
    headers = dict()
    authHeaders = None
    url = "{}/{}/".format(MYINFO_API_PERSON, uinfin)
    pp("URL for person request 1 " + url)

    # assemble params for Person API
    params = dict()
    params['client_id'] = MYINFO_APP_CLIENT_ID
    params['attributes'] = _attributes
    # assemble headers for Person API
    if AUTH_LEVEL == "L0":
        authHeaders = ""
    else:
        authHeaders = security.generateAuthorizationHeader(url,
                                                            params,
                                                            "GET",
                                                            "",
                                                            AUTH_LEVEL,
                                                            MYINFO_APP_CLIENT_ID,
                                                            DEMO_APP_SIGNATURE_CERT_PRIVATE_KEY,
                                                            MYINFO_APP_CLIENT_SECRET,
                                                            MYINFO_APP_REALM)
    headers['Cache-Control'] = cacheCtl
    if authHeaders == "":
        headers['Authorization'] =  "Bearer {}".format(validToken)
    else:
        authorization =  "{},Bearer {}".format(authHeaders, validToken)
        headers['Authorization'] = authorization
    pp(headers)
    res = requests.get(url, params=params, headers=headers)
    return res

@app.route('/callback')
def callback():
    code = request.args['code']
    state = request.args['state']
    if code is None or code == "":
        return format_response({"result" : "Bad Request"})
    if state is None or state == "":
        return format_response({"result" : "Bad Request"})
    res = token_request(code)
    body = res.json()
    pp(body)
    payload = security.verifyJWS(body.get('access_token'), MYINFO_CONSENTPLATFORM_SIGNATURE_CERT_PUBLIC_CERT)
    uinfin = payload['sub']
    pp(payload)
    res = person_request(payload['sub'], body.get('access_token'))
    body = res.text
    pp("body =" + body)
    person_data = security.decryptJWE(body, DEMO_APP_SIGNATURE_CERT_PRIVATE_KEY)
    data = refill_data(person_data)
    data['uinfin'] = uinfin
    pp(data)
    sess = updateSessionEntity(state, None, uinfin, data)
    pp(sess)
    return format_response({"result" : "OK"})

@app.route('/test')
def test():
        return render_template(
        'consent_given.html')

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] is not None 
                and request.form['username'] != "" 
                and request.form['password'] is not None 
                and request.form['password'] != "" 
                and validateUserLogin(request.form['username'], request.form['password']) == True):
            user = User(request.form['username'])
            login_user(user)
            return redirect(url_for('dashboard', userId = request.form['username']))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__=='__main__':
    app.run(port=3001, debug=True)