from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt, get_jwt_identity, unset_jwt_cookies
from flask_cors import CORS, cross_origin
from datetime import datetime, timedelta, timezone
import json
import utils
import populate_db

# Initializing flask app
app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'main'

connection = utils.establish_db_connection(app)

app.config['JWT_SECRET_KEY'] = "some-secret key" # remember to change the key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)

@app.route('/token', methods=['POST'])
def create_token():
    username = request.json["username"]
    password = request.json["password"]

    error_msg = "Invalid username or password"

    user_id = utils.try_get_user(connection, username)
    if user_id is None:
        print("invalid username")
        return jsonify({"msg": error_msg}), 401

    user_data = utils.verify_user(connection, user_id, password)
    if(user_data is None):
        print("not authorized")
        return jsonify({"msg": error_msg}), 401

    data = user_data["username"]
    utils.create_cache(data,"cache.txt")


    access_token = create_access_token(identity=user_id)

    print("aaa")

    return jsonify({"token":access_token})

@app.route('/signup', methods=['POST'])
def sign_up():
    username = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]
    full_name = request.json["full_name"]

    if(utils.try_get_user(connection, username) is not None):
        return jsonify({"msg": "Username already exists"}), 401
    if(utils.try_get_user_by_email(connection, email) is not None):
        return jsonify({"msg": "Email already exists"}), 401

    utils.create_user(connection, username, password,email,full_name)

    return jsonify({"msg": "Success"}), 200

@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        return response

@app.route('/logout', methods=['POST'])
def log_out():
    utils.delete_cache("cache.txt")
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

# populating data to the db
@app.route('/populate')
def populate():
    populate_db.run(connection)
    return("Populated succesfully")

# Route for seeing a data
@app.route('/api')
@jwt_required()
def data():
    data = utils.get_all_songs(connection)

    username = utils.read_cache("cache.txt")
    print(username)
    user_id = utils.try_get_user(connection, username)
    if user_id is None:
        print("invalid username")
        return jsonify({"msg": "Server error: user was not found."}), 401
    user_data = utils.get_user(connection,user_id)
    artists = utils.get_all_artists(connection)
    albums = utils.get_all_albums(connection)
    print(user_data) 

    res = {
        "songs":data,
        "playlists":["Playlist 1", "Playlist 2", "Playlist 3"],
        "user_data":user_data,
        "artists":artists,
        "albums":albums
    }

    # Returning an api for showing in  reactjs
    return jsonify(res)


@app.route('/api/song/<id>')
@jwt_required()
def song(id):
    file = utils.get_song_file(connection, id)
    return file


@app.route("/api/artist/<id>/cover/")
@cross_origin()
@jwt_required()
def song_image(id):
    file = utils.get_image_file(connection, id)
    return file

@app.route("/api/like_song",methods=["POST"])
@cross_origin()
@jwt_required()
def update_liked_songs():
    username = request.json["username"]
    liked_songs = request.json["liked_songs"]

    print(username,liked_songs)

    user_id = utils.try_get_user(connection, username)
    if user_id is None:
        print("invalid username")
        return jsonify({"msg": "Server error, try again"}), 401

    utils.like_song(connection, liked_songs,user_id)

    return jsonify({"msg": "Success"}), 200

@app.route("/api/fav_artist",methods=["POST"])
@cross_origin()
@jwt_required()
def update_favorite_artists():
    username = request.json["username"]
    fav_artists = request.json["fav_artists"]

    print(username,fav_artists)

    user_id = utils.try_get_user(connection, username)
    if user_id is None:
        print("invalid username")
        return jsonify({"msg": "Server error, try again"}), 401

    utils.add_favorite_artist(connection, fav_artists,user_id)

    return jsonify({"msg": "Success"}), 200

@app.route("/api/change_data",methods=["POST"])
@cross_origin()
@jwt_required()
def change_data():
    username = request.json["username"]
    email = request.json["email"]
    fullName = request.json["full_name"]
    input = request.json["input"]

    user_id = utils.try_get_user(connection, username)
    if user_id is None:
        print("invalid username")
        return jsonify({"msg": "Server error, try again"}), 401

    isTaken = utils.try_get_user(connection,input["username"])
    if isTaken is None:
        utils.change_username(connection,user_id,input["username"])
        utils.create_cache(input["username"],"cache.txt")
    elif username != input["username"]:
        return jsonify({"msg": "Mate. User with such username already exists"}), 401

    isTaken = utils.try_get_user_by_email(connection,input["email"])
    if isTaken is None:
        utils.change_email(connection,user_id,input["email"])
    elif email != input["email"]:
        return jsonify({"msg": "Buddy. This email is already taken"}), 401

    if input["password"] != "":
        utils.change_password(connection,user_id,input["password"])


    if fullName != input["fullName"]:
        utils.change_full_name(connection,user_id,input["fullName"])

    return jsonify({"msg": "Success"}), 200

@app.route("/api/add_streams",methods=["POST"])
@cross_origin()
@jwt_required()
def update_streams():
    id = request.json["id"]

    try:
        utils.add_streams(connection,id)
    except:
        return jsonify({"msg": "Server Error"}), 401
    return jsonify({"msg": "Success"}), 200

# Running app
if __name__ == '__main__':
    app.run(debug=True)