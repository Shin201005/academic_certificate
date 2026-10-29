
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from accounts.permissions import IsAdmin, IsSchool, IsStudent


ACCESS_AGE = 15 * 60
REFRESH_AGE = 24 * 60 * 60
ALLOWED_ROLES = ("ADMIN", "SCHOOL", "STUDENT")


def set_auth_cookies(response, access, refresh):
    response.set_cookie(
        key=settings.JWT_AUTH_COOKIE,
        value=str(access),
        max_age=ACCESS_AGE,
        httponly=True,
        secure=settings.JWT_COOKIE_SECURE,
        samesite=settings.JWT_COOKIE_SAMESITE,
        path="/",
    )

    response.set_cookie(
        key=settings.JWT_REFRESH_COOKIE,
        value=str(refresh),
        max_age=REFRESH_AGE,
        httponly=True,
        secure=settings.JWT_COOKIE_SECURE,
        samesite=settings.JWT_COOKIE_SAMESITE,
        path="/api/auth/",
    )


def clear_auth_cookies(response):
    response.delete_cookie(
        settings.JWT_AUTH_COOKIE,
        path="/",
        samesite=settings.JWT_COOKIE_SAMESITE,
    )
    response.delete_cookie(
        settings.JWT_REFRESH_COOKIE,
        path="/api/auth/",
        samesite=settings.JWT_COOKIE_SAMESITE,
    )


@ensure_csrf_cookie
def csrf_view(request):
    return JsonResponse({
        "detail": "CSRF cookie da duoc thiet lap."
    })


@method_decorator(csrf_protect, name="dispatch")
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if (
            not isinstance(username, str)
            or not isinstance(password, str)
            or not username.strip()
            or not password
        ):
            return Response(
                {"detail": "Vui long nhap tai khoan va mat khau."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is None:
            return Response(
                {"detail": "Tai khoan hoac mat khau khong dung."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if user.role not in ALLOWED_ROLES:
            return Response(
                {"detail": "Tai khoan khong duoc phep truy cap."},
                status=status.HTTP_403_FORBIDDEN,
            )

        refresh = RefreshToken.for_user(user)

        response = Response({
            "detail": "Dang nhap thanh cong.",
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role,
                "school_id": user.school_id,
            },
        })

        set_auth_cookies(response, refresh.access_token, refresh)
        return response


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "school_id": user.school_id,
        })


@method_decorator(csrf_protect, name="dispatch")
class RefreshView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        raw_token = request.COOKIES.get(
            settings.JWT_REFRESH_COOKIE
        )

        if not raw_token:
            return Response(
                {"detail": "Khong tim thay Refresh Token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        User = get_user_model()
        try:
            old_refresh = RefreshToken(raw_token)

            user_id = old_refresh.get("user_id")
            user = User.objects.get(pk=user_id)

            if not user.is_active or user.role not in ALLOWED_ROLES:
                return Response(
                    {"detail": "Tai khoan khong hop le."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Tao cap token moi
            new_refresh = RefreshToken.for_user(user)
            new_access = new_refresh.access_token

            # Thu hoi Refresh Token cu
            old_refresh.blacklist()

        except (TokenError, User.DoesNotExist, ValueError, TypeError):
            return Response(
                {"detail": "Refresh Token khong hop le."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response = Response({
            "detail": "Lam moi token thanh cong."
        })

        set_auth_cookies(response, new_access, new_refresh)
        return response


@method_decorator(csrf_protect, name="dispatch")
class LogoutView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        raw_token = request.COOKIES.get(
            settings.JWT_REFRESH_COOKIE
        )

        if raw_token:
            try:
                refresh = RefreshToken(raw_token)
                refresh.blacklist()
            except TokenError:
                pass

        response = Response({
            "detail": "Dang xuat thanh cong."
        })

        clear_auth_cookies(response)
        return response

class AdminOnlyView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({
            "detail": "ADMIN truy cap thanh cong."
        })


class SchoolOnlyView(APIView):
    permission_classes = [IsSchool]

    def get(self, request):
        return Response({
            "detail": "SCHOOL truy cap thanh cong.",
            "school_id": request.user.school_id,
        })


class StudentOnlyView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        return Response({
            "detail": "STUDENT truy cap thanh cong."
        })

