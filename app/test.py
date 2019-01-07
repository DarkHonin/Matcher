from app.auth import create_jwt
print(create_jwt({"Some information" : "NakNakNak"}))