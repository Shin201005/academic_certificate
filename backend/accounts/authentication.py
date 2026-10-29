
from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware

from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        return reason


class CookieJWTAuthentication(JWTAuthentication):

    def enforce_csrf(self, request):
        check = CSRFCheck(lambda req: None)
        django_request = request._request

        check.process_request(django_request)
        reason = check.process_view(
            django_request,
            lambda req: None,
            (),
            {},
        )

        if reason:
            raise PermissionDenied(
                f"CSRF Failed: {reason}"
            )

    def authenticate(self, request):
        header = self.get_header(request)

        # JWT tu Authorization header
        if header is not None:
            result = super().authenticate(request)

        else:
            # JWT tu HttpOnly Cookie
            raw_token = request.COOKIES.get(
                settings.JWT_AUTH_COOKIE
            )

            if raw_token is None:
                return None

            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)

            # Bat buoc kiem tra CSRF khi dung cookie
            self.enforce_csrf(request)

            result = (user, validated_token)

        if result is None:
            return None

        user, validated_token = result

        if user.role not in ("ADMIN", "SCHOOL", "STUDENT"):
            raise PermissionDenied(
                "Tai khoan khong co quyen truy cap."
            )

        return user, validated_token
