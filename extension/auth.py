from abc import ABC
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from Torch.settings import SECRET_KEY

class JwtQueryParamsAuthentication(BaseAuthentication, ABC):
    def authenticate(self, request):
        token = request.environ['HTTP_TOKEN']   # 请求头中获取token
        # token = request.query_params.get('token')   # params中获取字段
        # token = request.data.get('token')   # body—data中获取字段

        salt = SECRET_KEY  # 盐值 加密字符串
        payload = None
        try:
            payload = jwt.decode(token, salt, algorithms=['HS256'])
        except jwt.exceptions.ExpiredSignatureError:
            raise AuthenticationFailed({"code": 1003, "error": 'token已失效'})
        except jwt.DecodeError:
            raise AuthenticationFailed({"code": 1004, "error": 'token认证失败'})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({"code": 1005, "error": '非法的token'})
        return payload, token

