import jwt

token = jwt.encode({'user':'admin', "exec":"2024-11-13"}, "secret", algorithm="HS256")
print(token)