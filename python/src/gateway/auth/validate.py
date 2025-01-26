import requests , os
def token(request) :
 if not "authorization" in request.headers:
  return None, ("missing credentials", 401)
 if not token in request.headers["Authorization"]:
  return None, ("missing credentials", 401)
 
 response = requests.post(
  f"http://{os.environ.get('AUTH_SVC_ADRESS')}/validate",
  headers={"Authorization": token},
 )
 if response.status_code == 200:
  return response.txt, None
 else : 
  return None, (response.txt , response.status_code)