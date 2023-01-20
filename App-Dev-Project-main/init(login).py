from flask import run, get, view, post, request, redirect, response
import uuid

# REDIS, MYSQL/MARIADB, SQLITE, MONGODB
users = [
  {
    "id":"1",
    "name":"a",
    "last_name":"aa",
    "email":"a@a.com",
    "password":"pass1"
  },
  {
    "id":"2",
    "name":"b",
    "last_name":"bb",
    "email":"b@b.com",
    "password":"pass2"
  },
]

sessions = {}


##############################
@get("/login")
@view("login")
def _():
  return

##############################
@get("/admin")
@view("admin")
def _():
  response.set_header("Cache-Control", "no-cache, no-store, must-revalidate")
  response.add_header("Pragma", "no-cache")
  user_session_id = request.get_cookie("user_session_id")
  print("#"*30)
  print("admin")
  print(user_session_id)
  if not user_session_id:
    return redirect("/login")
  if user_session_id not in sessions:
    return redirect("/login")
  user = sessions[user_session_id]
  return dict(user=user)

##############################
@get("/logout")
def _():
  user_session_id = request.get_cookie("user_session_id")
  sessions.pop(user_session_id)
  # Delete the cookies from the browser
  response.set_cookie("user_session_id", "", expires=0)
  print("#"*30)
  print("logout")
  print(user_session_id)
  print(sessions)
  return redirect("/login")

##############################
@post("/login")
def _():
  user_email = request.forms.get("user_email")
  user_password = request.forms.get("user_password")
  for user in users:
    if user_email == user["email"] and user_password == user["password"]:
      user_session_id = str(uuid.uuid4())
      sessions[user_session_id] = user
      print("#"*30)
      print(sessions)
      response.set_cookie("user_session_id", user_session_id)
      return redirect("/admin")

  return redirect("/login")

##############################
run(host="127.0.0.1", port=3333, debug=True, reloader=True)
