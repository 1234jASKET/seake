import hashlib
import os

from django.core.cache import cache
from django.http import HttpResponse


class RequestThrottleMiddleware:
    """Small abuse barrier for admin login and public form submissions."""

    public_post_prefixes = (
        "/abonnement/",
        "/articles/",
        "/publicite/demande/",
        "/question-du-jour/",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        key = None
        if request.method == "POST" and request.path == "/admin/login/":
            key = self._key(request, "admin-login")
            if self._blocked(key, limit=8, timeout=60 * 15):
                return HttpResponse(
                    "Trop de tentatives. Attendez 15 minutes avant de reessayer.",
                    status=429,
                    content_type="text/plain; charset=utf-8",
                )
        elif request.method == "POST" and request.path.startswith(
            self.public_post_prefixes
        ):
            key = self._key(request, f"public-form:{request.path}")
            if self._blocked(key, limit=30, timeout=60 * 60):
                return HttpResponse(
                    "Trop d'envois. Attendez avant de reessayer.",
                    status=429,
                    content_type="text/plain; charset=utf-8",
                )

        response = self.get_response(request)
        if key and request.path == "/admin/login/" and response.status_code in (301, 302):
            cache.delete(key)
        return response

    def _key(self, request, scope):
        remote_addr = request.META.get("REMOTE_ADDR", "unknown")
        if os.environ.get("RENDER") and request.META.get("HTTP_X_FORWARDED_FOR"):
            remote_addr = request.META["HTTP_X_FORWARDED_FOR"].split(",", 1)[0].strip()
        username = request.POST.get("username", "") if scope == "admin-login" else ""
        identity = f"{scope}|{remote_addr}|{username.casefold()}"
        digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()
        return f"seake-throttle:{digest}"

    @staticmethod
    def _blocked(key, limit, timeout):
        if cache.add(key, 1, timeout=timeout):
            return False
        try:
            return cache.incr(key) > limit
        except ValueError:
            cache.set(key, 1, timeout=timeout)
            return False
