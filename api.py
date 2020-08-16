from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from functools import wraps
import jwt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/tpb'
app.config['SECRET_KEY'] = 'thisissecret'
DB = SQLAlchemy(app)

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'status':401,'response':'Unauthorized'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            currentProfile = Profile.query.filter_by(loginId = data['token']).first()
            if not currentProfile.isActive:
                return jsonify({'status':401,'response':'Disabled'}), 401
        except Exception as e:
            print(e)
            return jsonify({'status':401,'response':'Invalid Token'}), 401
        return f(currentProfile,*args,**kwargs)
    return decorated

class Login(DB.Model):
    id = DB.Column(DB.Integer, primary_key = True)
    uuid = DB.Column(DB.String(120), nullable = False)
    userId = DB.Column(DB.String(120), nullable = False)
    password = DB.Column(DB.String(120), nullable = False)

class Profile(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    loginId = DB.Column(DB.String(120), nullable=False)
    userType = DB.Column(DB.String(200), nullable=False)
    userEmail = DB.Column(DB.String(200), nullable=False)
    userName = DB.Column(DB.String(120), nullable=False)
    userImg = DB.Column(DB.String(120), nullable=False)
    country = DB.Column(DB.String(120), nullable=False)
    state = DB.Column(DB.String(120), nullable=False)
    city = DB.Column(DB.String(120), nullable=False)
    isActive = DB.Column(DB.Integer, nullable=False)

@app.route('/tpb/api/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate':'Basic-realm="Login Required"'})

    login = Login.query.filter_by(userId = auth.username).first()
    if not login:
        return make_response('Invalid Username', 401, {'WWW-Authenticate':'Basic-realm="Login Failed"'})
    if login.password == auth.password:
        token = jwt.encode({'token':login.uuid,'exp':datetime.utcnow() + timedelta(hours=12)}, app.config['SECRET_KEY'])
        return jsonify({'status':200,'token':token.decode('UTF-8')})
    else:
        return make_response('Invalid Password', 401, {'WWW-Authenticate': 'Basic-realm="Login Failed"'})

@app.route('/tpb/api/profiles', methods=['GET'])
@token_required
def getAllProfiles(token):
    profiles = Profile.query.all()
    result = []
    for profile in profiles:
        row = {'id':profile.id, 'loginId':profile.loginId, 'userType':profile.userType, 'userEmail':profile.userEmail,
               'userName':profile.userName, 'userImg':profile.userImg, 'country':profile.country, 'state':profile.state,
               'city':profile.city, 'isActive':profile.isActive}
        result.append(row)
    return jsonify({'status':200,'profiles':result}), 200

if __name__ == '__main__':
    app.run(debug=True)