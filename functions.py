import requests
from flask import redirect, render_template, request, session
from functools import wraps
from model import db, User, Clients,Features
from operator import itemgetter, attrgetter



def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
    
    
def reorder_priorities(client):
    features = Features.query.filter_by(client_id=client)
    if features == None:
        return None
    sort = False
    previous = False

    sorted_features = sorted(features, key = attrgetter("priority"))
        
    for feature in sorted_features:
        if sort:
            feature.priority = feature.priority + 1
        else:
            if previous != False:
                if feature.priority == previous.priority:
                    previous.priority = previous.priority + 1
                    sort = True
        previous = feature
    db.session.commit()
