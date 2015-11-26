from bottle import route, template, run, static_file, request, response, view
from bottle import install, abort

from PIL import Image
import cassandra, time, random, hashlib, mimetypes, uuid, StringIO, functools, os

def setup_db(cassandra):
    session = cassandra.getsession()
    session.execute("create keyspace if not exists PetBay with replication = {'class':'SimpleStrategy', 'replication_factor': 1};")
    session.execute("create table if not exists PetBay.User(email text primary key, password text, picids set<uuid>, profile_data blob, profile_mime text)")
    session.execute("create table if not exists PetBay.Pic(picid uuid primary key, user_email text, data blob, data_thumb blob, mime text, time_added bigint)")
    session.execute("create table if not exists PetBay.WallOfFame(picid uuid primary key, user_email text, data blob, mime text, time_added bigint)")
    session.execute("create table if not exists PetBay.Votes(picid uuid primary key, votes_up counter, votes_down counter)")
    
    session.execute("create table if not exists PetBay.Session(sessionid uuid, email text, primary key (sessionid, email))")
    return session

def get_user(callback):
    " decorator that passes in logged in user to route handler "
    " requires: db and email parameters in route handler "

    @functools.wraps(callback)
    def wrapper(*args, **kwargs):
        db = kwargs.get("db")
        if db is None:
            raise Exception("needs 'db' argument in route handler")

        kwargs["email"] = None

        session_id = request.get_cookie("pbsession")
        if session_id is not None:
            prepared = db.prepare("select * from PetBay.Session where sessionid=?")
            rows = db.execute(prepared, (uuid.UUID(session_id),))
            if len(rows) > 0:
                row, = rows
                kwargs["email"] = row["email"]

        return callback(*args, **kwargs)
    return wrapper

@route("/static/<filename:path>")
def get_static(filename):
    response.content_type = mimetypes.guess_type(filename)
    return static_file(filename, root="./static")

@route("/")
@view("index")
def get_index(db):
    pics = db.execute("select * from PetBay.Pic")
    picids = map(lambda pic: pic["picid"], pics)
    prepared = db.prepare("select * from PetBay.Votes where picid in (" + (','.join(["?"] * len(picids))) + ")")
    votes = db.execute(prepared, picids)
    for vote in votes:
        
        
    return {"pics": rows}

@route("/ajax/login", method="POST")
def perform_login(db):
    email = request.forms.get("email")
    password = request.forms.get("password")
    
    prepared = db.prepare("select * from PetBay.User where email=?")
    rows = db.execute(prepared, (email,))

    if len(rows) > 0:
        row, = rows
        
        salt = hashlib.new("sha256", email).hexdigest()
        password_hash = hashlib.new("sha256", salt + password).hexdigest()
        if password_hash == row["password"]:

            uuid = cassandra.util.uuid_from_time(time.time())
            prepared = db.prepare("insert into PetBay.Session(sessionid, email) values (?, ?) using ttl 604800")
            db.execute(prepared, (uuid, email))

            response.set_cookie("pbsession", uuid.hex, max_age=604800)
            
            return {"status": "OK"}
    
    return {"status": "ERROR", "message": "Invalid username and password"}

@route("/ajax/logout", method="POST")
@get_user
def perform_logout(db, email):
    if email is None:
        return

    # this will logout user from all browsers.. (what we want?)
    prepared = db.prepare("delete from PetBay.Session where email=?")
    db.execute(prepared, (email,))
    
    response.delete_cookie("pbsession")

@route("/ajax/register", method="POST")
def perform_register(db):
    email = request.forms.get("email")
    password = request.forms.get("password")
    # nickname?

    salt = hashlib.new("sha256", email).hexdigest()
    password_hash = hashlib.new("sha256", salt + password).hexdigest()

    prepared = db.prepare("insert into PetBay.User(email, password) values (?, ?) if not exists")
    row, = db.execute(prepared, (email, password_hash))

    if row["[applied]"]:
        return {"status": "OK"}
    return {"status": "ERROR", "message": "Email already registered"}

@route("/ajax/upload", method="POST")
@get_user
def perform_upload(db, email):
    if email is None:
        abort(401)

    upload = request.files.get("upload")
    name, ext = os.path.splitext(upload.filename)
    if ext not in (".png", ".jpg", ".jpeg"):
        return {"status": "ERROR", "message": "Invalid file format"}

    try:
        im = Image.open(upload.file)
    except:
        return {"status": "ERROR", "message": "Bad file"}
        
    orig_data = StringIO.StringIO()
    im.save(orig_data, format="JPEG")
    im.thumbnail((400, 300), Image.ANTIALIAS)
    thumb_data = StringIO.StringIO()
    im.save(thumb_data, format="JPEG")
    
    prepared = db.prepare("insert into PetBay.Pic(picid, user_email, data, data_thumb, mime, time_added) values (?, ?, ?, ?, ?, ?) if not exists")
    db.execute(prepared, (cassandra.util.uuid_from_time(time.time()), email, orig_data.getvalue(), thumb_data.getvalue(), "image/jpeg", int(time.time())))
    return {"status": "OK"}

@route("/pic/orig/<picid>")
def get_pic_original(db):
    prepared = db.prepare("select * from PetBay.Pic where picid=?")
    rows = db.execute(prepared, (picid,))

    if len(rows) <= 0:
        abort(404)

    row, = rows
    response.content_type = row["mime"]
    return row["data"]

@route("/pic/thumb/<picid>")
def get_pic_thumb(db):
    prepared = db.prepare("select * from PetBay.Pic where picid=?")
    rows = db.execute(prepared, (picid,))

    if len(rows) <= 0:
        abort(404)

    row, = rows
    response.content_type = row["mime"]
    return row["data_thumb"]

if __name__ == "__main__":
    from cassandraplugin import CassandraPlugin
    cassandra_plugin = CassandraPlugin()
    install(cassandra_plugin)
    setup_db(cassandra_plugin)
    
    run(server="waitress", host='0.0.0.0', reloader=True, port=8080, debug=True)
