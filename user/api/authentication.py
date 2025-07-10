from rest_framework_simplejwt.authentication import JWTAuthentication
class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        print("CookieJWTAuthentication aufgerufen")
        header = self.get_header(request)
        if header is None:
            raw_token = request.COOKIES.get('access_token')
            print("Token im Cookie:", raw_token)
            if raw_token is None:
                return None
            validated_token = self.get_validated_token(raw_token)
            return self.get_user(validated_token), validated_token
        return super().authenticate(request)

