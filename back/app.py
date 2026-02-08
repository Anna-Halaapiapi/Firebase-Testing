# basic flask server with protected endpoint for dashboard page

from flask import Flask, jsonify, request, render_template
# Import the Firebase service
import firebase_admin
from firebase_admin import auth
from flask_cors import CORS
from firebase_admin.exceptions import FirebaseError

# create web server
app = Flask(__name__)

# get rid of CORS related error in console
CORS(app)

# initialize admin SDK
firebase_admin.initialize_app()

# dashboard route
@app.route("/dashboard", methods=["GET"])
def get_dashboard():
    auth_header = request.headers.get('Authorization') # access the authorization header
    # extract JWT token from header
    token = None
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
    if not token:
        return jsonify({"Error: missin gtoken"}), 401

    # try calling admin SDK to verify and decode the token extracted from auth header
    try:
        decoded_token = auth.verify_id_token(token)
        firebase_uid = decoded_token['uid']
        print(f"firebase uid of user is: {firebase_uid}")
        return jsonify({"message": "Successfully logged in"}), 200
    except FirebaseError: # protects our endpoint by handling firebase specific errors (token expired, revoked etc)
        return jsonify({"Error: You are not authorised!!"}), 401

# run server
if __name__ == "__main__": 
    app.run()

