import uuid
from flask import Flask, session, redirect, url_for, request, render_template
from flask_session import Session
import json
from datetime import datetime, timedelta
import requests
import msal
import app_config
import threading

app = Flask(__name__)
app.config.from_object(app_config)
Session(app)

from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.route('/hw')
def hello_world():
    return 'Hello, World!'

@app.route("/")
def index():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template('index.html', user=session["user"], version=msal.__version__)

@app.route("/login")
def login():
    session["state"] = str(uuid.uuid4())
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    auth_url = _build_auth_url(scopes=app_config.SCOPE, state=session["state"])
    return render_template("login.html", auth_url=auth_url, version=msal.__version__)

@app.route(app_config.REDIRECT_PATH)  # Its absolute URL must match your app's redirect_uri set in AAD
def authorized():
    if request.args.get('state') != session.get("state"):
        return redirect(url_for("index"))  # No-OP. Goes back to Index page
    if "error" in request.args:  # Authentication/Authorization failure
        return render_template("auth_error.html", result=request.args)
    if request.args.get('code'):
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_authorization_code(
            request.args['code'],
            scopes=app_config.SCOPE,  # Misspelled scope would cause an HTTP 400 error here
            redirect_uri=url_for("authorized", _external=True))
        if "error" in result:
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims")
        _save_cache(cache)
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()  # Wipe out user and its token cache from session
    return redirect(  # Also logout from your tenant's web session
        app_config.AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("index", _external=True))

@app.route('/onlinemeeting')
def onlinemeeting():
    teams_url = _teams_start()
    return teams_url
    
@app.route('/onlinemeeting2')
def onlinemeeting2():
    teams_url = _teams_event()
    return teams_url

@app.route('/startonlinemeeting', methods=['POST']) #allow both GET and POST requests
def startonlinemeeting():
    req_json = request.get_json()
    if req_json['agent']:
        agent = req_json['agent']
        email = agent['email']
        name = agent['name']
        
        room_id = req_json['room_id']
        
        threading1 = threading.Thread(target=_send_button_qiscus, args=(email, name, room_id, ))
        threading1.start()
    return req_json

#----------------------------------------------------------------------------------------------------------------------------------
def _convert_dt_string(datetime):
    return datetime.strftime("%Y-%m-%dT%H:%M:%S-07:00")

def _get_token_from_pw():
    #cache = _load_cache()
    temp1 = msal.PublicClientApplication(app_config.CLIENT_ID, authority=app_config.AUTHORITYORG)
    result = temp1.acquire_token_by_username_password(
        username=app_config.username, password=app_config.pw, data={'client_secret':app_config.CLIENT_SECRET}, scopes=app_config.SCOPE)
    #session["user"] = result.get("id_token_claims")
    #_save_cache(cache)
    return result

def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()
        
        
def _send_button_qiscus(email, name, room_id):
    teams_url = _teams_start()

    json = {
        	"sender_email": "gume-br1lmyldfzyvrw2j_admin@qismo.com", 
        	"message": "Hi good morning",
        	"type": "buttons",
        	"room_id": str(room_id),
        	"payload": {
        		"text": "Teams Online Meeting".format(email),
        	    "buttons": [
            	        {
        	            "label": "Join",
        	            "type": "link",
        	            "payload": {
        	                "url": "{}".format(teams_url)
        	            }
        	        }
        		]
        	} 
        }
    base_url = "https://multichannel.qiscus.com/"
    app_code = 'gume-br1lmyldfzyvrw2j'
    url = base_url + app_code + "/bot"
    headers = {'Content-Type': 'application/json'}
    result = requests.post(url, headers=headers, json=json)
    
    
def _teams_start():
    #token = _get_token_from_pw()
    token = _get_token_from_cache(app_config.SCOPE)
    #print(token)
    if not token:
        return redirect(url_for("login"))
    
    duration = 10 # in minutes
    startDT = datetime.utcnow() - timedelta(hours=7)
    endDT = startDT + timedelta(minutes=duration)

    graph_data = requests.post(  
        "https://graph.microsoft.com/v1.0/me/onlineMeetings",
        headers={'Authorization': 'Bearer ' + token['access_token'],
                 'Content-type':'application/json'},
        
        json ={
            #"autoAdmittedUsers":"everyone",
            "startDateTime":_convert_dt_string(startDT),
            "endDateTime":_convert_dt_string(endDT),
            "participants": {
                "organizer": {
                    "identity": {
                        "user": {
                            "id": "30374d5c-c7df-4a1e-83f1-7d2e5e135b16"
                            }
                        }
                    }
                }
            }
        ).json()
    return graph_data

def _teams_event():
    #token = _get_token_from_pw()
    token = _get_token_from_cache(app_config.SCOPE)
    if not token:
        return redirect(url_for("login"))
    graph_data = requests.post(  
        "https://graph.microsoft.com/v1.0/users/c1141e56-e9e9-4fa7-94d5-7f84c2141bc7/events",
        headers={'Authorization': 'Bearer ' + token['access_token'],
                 'Content-type':'application/json'},
        
        json= {
              "subject": "Let's go for lunch",
              "body": {
                "contentType": "HTML",
                "content": "Does next month work for you?"
              },
              "isOnlineMeeting": True,
              "onlineMeetingProvider": "teamsForBusiness"
            }
        ).json()
    return graph_data
    
#----------------------------------------------------------------------------------------------
def _get_token_from_cache(scope=None):
    cache = _load_cache()  # This web app maintains one cache per session
    cca = _build_msal_app(cache=cache)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(cache)
        return result
    
def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID, authority=authority or app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET, token_cache=cache)


def _build_auth_url(authority=None, scopes=None, state=None):
    return _build_msal_app(authority=authority).get_authorization_request_url(
        scopes or [],
        state=state or str(uuid.uuid4()),
        redirect_uri=url_for("authorized", _external=True))

app.jinja_env.globals.update(_build_auth_url=_build_auth_url)  # Used in template

                  
if __name__ == "__main__":
    app.run()

#9dad4a29-78bf-4ad5-8e65-7be53fb88933