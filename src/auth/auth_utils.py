import jwt

def creat_access_token(user_id:int):
    payload = {'user_id': user_id}
    access_token = jwt.encode(payload, 'secret', algorithm='HS256')
    return access_token

def decode_access_token(access_token: str | bytes):
    data = jwt.decode(access_token, algorithms=['HS256'])
    return data