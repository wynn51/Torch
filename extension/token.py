import datetime
import jwt
from Torch.settings import SECRET_KEY

def create_token(payload, timeout=1):
    salt = SECRET_KEY    # token加密字段，可自定义
    # headers不同于请求头，直接写死
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    # 构造payload
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)  # 超时时间
    token = jwt.encode(payload=payload, key=salt, algorithm="HS256", headers=headers)

    return token
