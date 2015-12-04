from bottle import route, template, run, static_file, request, response, view
from bottle import install, abort, redirect

from PIL import Image
import cassandra
import time
import random
import hashlib
import mimetypes
import uuid
import StringIO
import functools
import os
import re
import threading

def setup_db(cassandra):
	session = cassandra.getsession()
	session.execute("create keyspace if not exists PetBay with replication = {'class':'SimpleStrategy', 'replication_factor': 1};")
	session.execute("create table if not exists PetBay.User(email text primary key, password text, picids set<uuid>, walloffame_picids set<uuid>, profile_data blob, profile_mime text, description text, nickname text)")
	session.execute("create table if not exists PetBay.Pic(picid uuid primary key, user_email text, data blob, data_thumb blob, mime text, time_added bigint)")
	session.execute("create table if not exists PetBay.WallOfFame(picid uuid primary key, user_email text, data blob, data_thumb blob, mime text, time_added bigint)")
	session.execute("create table if not exists PetBay.Votes(picid uuid primary key, votes_up counter, votes_down counter)")
	session.execute("create table if not exists PetBay.Voters(picid uuid, email text, up_vote boolean, primary key(picid, email))")
	
	session.execute("create table if not exists PetBay.Session(sessionid uuid primary key, email text)")
	return session

# taken from: http://stackoverflow.com/a/16368571/783711 (credit J.F. Sebastian)
def set_interval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop(): # executed in another thread
                while not stopped.wait(interval): # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True # stop if the program exits
            t.start()
            return stopped
        return wrapper
    return decorator

def is_valid_uuid(uuid, no_dashes=False):
	" returns whether or not passed in str is uuid "
	if no_dashes and re.match("^[0-9a-f]{32}$", uuid, re.I):
		return True
	elif not no_dashes and re.match("^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", uuid, re.I):
		return True
	return False

def get_str_from_uuid(uuid):
	" returns uuid with dashes as string "
	return uuid.urn.split(":")[-1]
	
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
		if session_id is not None and is_valid_uuid(session_id, no_dashes=True):
			prepared = db.prepare("select * from PetBay.Session where sessionid=?")
			rows = db.execute(prepared, (uuid.UUID(session_id),))
			if len(rows) > 0:
				row, = rows
				kwargs["email"] = row["email"]

		return callback(*args, **kwargs)
	return wrapper

def get_pics(db, table, picids=None, last_time=0):
	where = ""
	if picids is not None:
		where = "where picid in (%s)" % ','.join(map(get_str_from_uuid, picids))

	pics = db.execute("select picid, user_email, time_added, ttl(data) from PetBay.%s %s" % (table, where))
	picids = []
	pic_dict = {}
	for pic in pics:
		if pic["time_added"] > last_time:
			picid = pic["picid"]
			pic["votes"] = 0
			pic_dict[picid] = pic
			picids.append(picid)
	
	prepared = db.prepare("select * from PetBay.Votes where picid in (" + (','.join(["?"] * len(picids))) + ")")
	votes = db.execute(prepared, picids)
	for vote in votes:
		pic_dict[vote["picid"]]["votes"] = (vote["votes_up"] or 0) - (vote["votes_down"] or 0)
	
	return pic_dict
	
@route("/static/<filename:path>")
def get_static(filename):
	response.content_type = mimetypes.guess_type(filename)
	return static_file(filename, root="./static")
	
@route("/ajax/getnew")
@view("new")
def get_new(db):
	last_time = request.query.get("last_time")
	if last_time is None or not last_time.isdigit():
		abort(500)
	
	return {"pics": get_pics(db, "Pic", int(last_time))}

@route("/")
@view("index")
@get_user
def get_index(db, email):
	#row, = db.execute("select count(*) from PetBay.Pic")

	#return {"pics": get_pics(db, "Pic"), "email": email, "total_pics": row["count"]}
	return {"pics": get_pics(db, "Pic"), "email": email}

@route("/halloffame")
@view("halloffame")
@get_user
def get_halloffame(db, email):
	#row, = db.execute("select count(*) from PetBay.WallOfFame")

	#return {"pics": get_pics(db, "WallOfFame"), "email": email, "total_pics": row["count"]}
	return {"pics": get_pics(db, "WallOfFame"), "email": email}

@route("/profile")
@route("/profile/<user>")
@view("profile")
@get_user
def get_profile(db, email, user=None):
	if user is None:
		if email is None:
			return redirect("/")
		return redirect("/profile/%s" % email)
	
	prepared = db.prepare("select * from PetBay.User where email=?")
	rows = db.execute(prepared, (user,))
	if len(rows) <= 0:
		return abort(404)
	
	row, = rows
	pics = get_pics(db, "WallOfFame", picids=row["walloffame_picids"])
	
	return {"email": email, "user": user, "nickname": row["nickname"], "description": row["description"], "walloffame_picids": row["walloffame_picids"], "pics": pics}

@route("/ajax/login", method="POST")
def perform_login(db):
	email = request.forms.get("email", "")
	password = request.forms.get("password", "")
	
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

			response.set_cookie("pbsession", uuid.hex, path="/", max_age=604800)
			
			return {"status": "OK"}
	
	return {"status": "ERROR", "message": "Invalid username and password"}

@route("/ajax/logout", method="POST")
@route("/ajax/logout")
def perform_logout(db):	
	session_id = request.get_cookie("pbsession")
	if session_id is None or not is_valid_uuid(session_id, no_dashes=True):
		return
	
	# this will logout user from all browsers.. (what we want?)
	prepared = db.prepare("delete from PetBay.Session where sessionid=?")
	db.execute(prepared, (uuid.UUID(session_id),))
	
	response.delete_cookie("pbsession")

@route("/ajax/register", method="POST")
def perform_register(db):
	email = request.forms.get("email", "")
	password = request.forms.get("password", "")
	# nickname?

	salt = hashlib.new("sha256", email).hexdigest()
	password_hash = hashlib.new("sha256", salt + password).hexdigest()
	
	thumb_data = None
	thumb_mime = None
	upload = request.files.get("upload")
	if upload is not None:
		name, ext = os.path.splitext(upload.filename)
		if ext.lower() not in (".png", ".jpg", ".jpeg"):
			return {"status": "ERROR", "message": "Invalid file format"}

		try:
			im = Image.open(upload.file)
		except:
			return {"status": "ERROR", "message": "Bad file"}
		
		thumb_mime = "image/jpeg"
		thumb_data = StringIO.StringIO()
		im.thumbnail((300, 300), Image.ANTIALIAS)
		im.save(thumb_data, format="JPEG")
		thumb_data = thumb_data.getvalue()
	
	prepared = db.prepare("insert into PetBay.User(email, password, profile_data, profile_mime) values (?, ?, ?, ?) if not exists")
	row, = db.execute(prepared, (email, password_hash, thumb_data, thumb_mime))

	if row["[applied]"]:
		return {"status": "OK"}

	return {"status": "ERROR", "message": "Email already registered"}

@route("/ajax/upload", method="POST")
@get_user
def perform_upload(db, email):
	if email is None:
		abort(401)
	
	upload = request.files.get("upload")
	if upload is None:
		abort(500)
	
	name, ext = os.path.splitext(upload.filename)
	if ext.lower() not in (".png", ".jpg", ".jpeg"):
		return {"status": "ERROR", "message": "Invalid file format"}

	try:
		im = Image.open(upload.file)
	except:
		return {"status": "ERROR", "message": "Bad file"}

	orig_data = StringIO.StringIO()
	im.save(orig_data, format="JPEG")
		
	# thumb-nify..
	# calculate so image covers thumbnail area (target)
	target_w, target_h = (243, 200)
	aspect_ratio = float(im.width) / float(im.height)
	if im.width > im.height:
		thumb_h = min(im.height, target_h)
		thumb_w = aspect_ratio * thumb_h
	else:
		thumb_w = min(im.width, target_w)
		thumb_h = thumb_w / aspect_ratio
	
	# resize
	im.thumbnail((thumb_w, thumb_h), Image.ANTIALIAS)
	# crop
	thumb = Image.new("RGB", (target_w, target_h))
	thumb.paste(im, ((target_w - im.width) / 2, (target_h - im.height) / 2))
	
	thumb_data = StringIO.StringIO()
	thumb.save(thumb_data, format="JPEG")
	
	picid = cassandra.util.uuid_from_time(time.time())
	prepared = db.prepare("insert into PetBay.Pic(picid, user_email, data, data_thumb, mime, time_added) values (?, ?, ?, ?, ?, ?) if not exists using ttl 240")
	db.execute(prepared, (picid, email, orig_data.getvalue(), thumb_data.getvalue(), "image/jpeg", int(time.time())))
	
	prepared = db.prepare("update PetBay.User set picids = picids + {" + get_str_from_uuid(picid) + "} where email=?")
	db.execute(prepared, (email,))
	
	return {"status": "OK"}

@route("/ajax/update_profile", method="POST")
@get_user
def perform_update_profile(db, email):
	if email is None:
		abort(401)
	
	#prepared = db.prepare("select * from PetBay.User where email=?")
	#row, = db.execute(prepared, (email,))
	
	nickname = request.forms.get("nickname")
	if nickname is not None:
		prepared = db.prepare("update PetBay.User set nickname=? where email=?")
		db.execute(prepared, (nickname, email))
	
	description = request.forms.get("description")
	if description is not None:
		prepared = db.prepare("update PetBay.User set description=? where email=?")
		db.execute(prepared, (description, email))

	profile = request.files.get("upload")
	if profile is not None:
		name, ext = os.path.splitext(profile.filename)
		if ext.lower() not in (".png", ".jpg", ".jpeg"):
			return {"status": "ERROR", "message": "Invalid file format"}

		try:
			im = Image.open(profile.file)
		except:
			return {"status": "ERROR", "message": "Bad file"}
		
		thumb_mime = "image/jpeg"
		thumb_data = StringIO.StringIO()
		im.thumbnail((300, 300), Image.ANTIALIAS)
		im.save(thumb_data, format="JPEG")
		thumb_data = thumb_data.getvalue()
		
		prepared = db.prepare("update PetBay.User set profile_data=?, profile_mime='image/jpeg' where email=?")
		db.execute(prepared, (thumb_data, email))
	
	return {"status": "OK"}
	
@route("/pic/orig/<picid>")
def get_pic_original(picid, db):
	if not is_valid_uuid(picid):
		abort(500)

	prepared = db.prepare("select * from PetBay.Pic where picid=?")
	rows = db.execute(prepared, (uuid.UUID(picid),))

	if len(rows) <= 0:
		abort(404)

	row, = rows
	response.content_type = row["mime"]
	return row["data"]

@route("/pic/thumb/<picid>")
def get_pic_thumb(picid, db):
	if not is_valid_uuid(picid):
		abort(500)

	prepared = db.prepare("select * from PetBay.Pic where picid=?")
	rows = db.execute(prepared, (uuid.UUID(picid),))

	if len(rows) <= 0:
		abort(404)

	row, = rows
	response.content_type = row["mime"]
	return row["data_thumb"]

@route("/pic/profile/<email>")
def get_pic_profile(email, db):
	prepared = db.prepare("select * from PetBay.User where email=?")
	rows = db.execute(prepared, (email,))

	if len(rows) <= 0:
		abort(404)

	row, = rows
	if row["profile_data"] is not None:
		response.content_type = row["profile_mime"]
		return row["profile_data"]
	
	response.content_type = "image/jpeg"
	return static_file("css/profile_empty.jpg", root="./static")

@route("/pic/halloffame/thumb/<picid>")
def get_pic_halloffame_thumb(picid, db):
	if not is_valid_uuid(picid):
		abort(500)

	prepared = db.prepare("select * from PetBay.WallOfFame where picid=?")
	rows = db.execute(prepared, (uuid.UUID(picid),))

	if len(rows) <= 0:
		abort(404)

	row, = rows
	response.content_type = row["mime"]
	return row["data_thumb"]
	
@route("/pic/halloffame/orig/<picid>")
def get_pic_original(picid, db):
	if not is_valid_uuid(picid):
		abort(500)

	prepared = db.prepare("select * from PetBay.WallOfFame where picid=?")
	rows = db.execute(prepared, (uuid.UUID(picid),))

	if len(rows) <= 0:
		abort(404)

	row, = rows
	response.content_type = row["mime"]
	return row["data"]
	
@route("/ajax/vote/<vote>", method="POST")
@get_user
def perform_vote(vote, db, email):
	if email is None:
		return None
	
	if vote not in ("up", "down"):
		return None
	else:
		up_vote = (vote == "up")
	
	picid = request.forms.get("picid")
	if not is_valid_uuid(picid):
		abort(500)
	
	picid = uuid.UUID(picid)
	
	prepared = db.prepare("select * from PetBay.Pic where picid=?")
	rows = db.execute(prepared, (picid,))
	if len(rows) <= 0:
		# no such pic
		abort(404)
	
	prepared = db.prepare("select * from PetBay.Voters where email=? and picid=?")
	rows = db.execute(prepared, (email, picid))
	
	if len(rows) <= 0:
		# no past vote
		if up_vote:
			prepared = db.prepare("update PetBay.Votes set votes_up = votes_up + 1 where picid=?")
			db.execute(prepared, (picid,))
		else:
			prepared = db.prepare("update PetBay.Votes set votes_down = votes_down + 1 where picid=?")
			db.execute(prepared, (picid,))
		
		prepared = db.prepare("insert into PetBay.Voters(picid, email, up_vote) values (?, ?, ?)")
		db.execute(prepared, (picid, email, up_vote))
	elif len(rows) == 1:
		# 1 past vote
		
		row, = rows
		if up_vote != row["up_vote"]:
			# nullify last vote and add the new vote
			if up_vote:
				prepared = db.prepare("update PetBay.Votes set votes_up = votes_up + 1, votes_down = votes_down - 1 where picid=?")
				db.execute(prepared, (picid,))
			else:
				prepared = db.prepare("update PetBay.Votes set votes_up = votes_up - 1, votes_down = votes_down + 1 where picid=?")
				db.execute(prepared, (picid,))
		
			# change last vote to an up vote
			prepared = db.prepare("update PetBay.Voters set up_vote=? where email=? and picid=?")
			db.execute(prepared, (up_vote, email, picid))
		else:
			return {"status": "ERROR", "message": "Already voted"}
	else:
		return {"status": "ERROR", "message": "Multiple votes detected"}
	
	return {"status": "OK"}

@route("/ajax/welcome")
@view("welcome")
@get_user
def get_welcome(db, email):
	return {"email": email}

@set_interval(15)
def move_to_halloffame(db):
	""" cron job, moves about to expire sucessful new
		hall of fame entries to the hall of fame """
		
	# grab all the pics and their ttl
	rows = db.execute("select picid, user_email, ttl(data) from PetBay.Pic")
	
	# filter out those about to be destroyed
	rows = filter(lambda row: row["ttl(data)"] < 30, rows)
	
	for row in rows:
		prepared = db.prepare("select * from PetBay.Votes where picid=?")
		votes = db.execute(prepared, (row["picid"],))
		if len(votes) <= 0:
			# no votes
			continue
		vote, = votes
		score = (vote["votes_up"] or 0) - (vote["votes_down"] or 0)
		
		if score < 2:
			# not high enough
			continue
	
		prepared = db.prepare("update PetBay.User set walloffame_picids = walloffame_picids + {" + row["picid"].urn.split(":")[-1] + "} where email=?")
		db.execute(prepared, (row["user_email"],))
		
		# same picid used, so can be executed multiple times without duplication
		prepared = db.prepare("select * from PetBay.Pic where picid=?")
		pic_row, = db.execute(prepared, (row["picid"],))
		
		prepared = db.prepare("insert into PetBay.WallOfFame(picid, user_email, data, data_thumb, mime, time_added) values (?, ?, ?, ?, ?, ?)")
		db.execute(prepared, (pic_row["picid"], pic_row["user_email"], pic_row["data"], pic_row["data_thumb"], pic_row["mime"], pic_row["time_added"]))

if __name__ == "__main__":
	from cassandraplugin import CassandraPlugin
	cassandra_plugin = CassandraPlugin()
	install(cassandra_plugin)
	setup_db(cassandra_plugin)
	
	stop_mover = move_to_halloffame(cassandra_plugin.getsession())
	
	try:
		run(server="waitress", host='0.0.0.0', port=8080, debug=True)
	finally:
		stop_mover.set()
