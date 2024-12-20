import jwt , os, datetime
from flask import Flask, request
from flask_mysqldb import MySQL


# create an instance of the class application and sql connection 
server = Flask(__name__)
mysql = MySQL(server)

# configuration 
server.config["MYSQL_HOST"]  = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"]  = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"]  = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"]  = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"]  = os.environ.get("MYSQL_PORT")
print(server.config["MYSQL_HOST"])
@server.route("/login", methods=["POST"]) 
def login() : 
 auth = request.authorization
 if not auth : 
  return "missing credentials " , 401
 #check for the user name
 cur = mysql.connection.cursor()
 req = cur.execute(
  "SELECT email, password FROM user WHERE email=%s", (auth.username)
 )
 if req > 0 :
  user_row = cur.fetchone()
  email = user_row[0]
  password = user_row[1]

  if auth.email != email or auth.password != password :
   return "missing credentials",401 
  else :
   createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
 else :
  return "missing credentials" , 401
 
@server.route("/validate", methods=["POST"])
def validate():
 encoded_jwt = request.headers["Authorization"]
 if not encoded_jwt:
  return "messing credentials" , 401
 encoded_jwt = encoded_jwt.split(" ")[1]

 try :
  decoded = jwt.decode(encoded_jwt, os.environ.get['JWT_SECRET'], algorithms=["HS256"])
 except:
  return "not authorized ", 403
 return decoded , 200


def createJWT(username, secret, authz) :
 return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            "iat": datetime.datetime.now(datetime.timezone.utc),
            "admin": authz,
        },
        secret,
        algorithm="HS256",
    )


if __name__ == "__main__" :
 server.run(host="0.0.0.0", port=5000)