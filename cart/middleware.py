from django.contrib.sessions.backends.db import SessionStore


class AnonymousSessionMIddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        """
        создание сессии для анонимного пользователя
        """
        if not request.user.is_authenticated and not request.session.session_key:
            anonymous_session = SessionStore()
            anonymous_session.create()
            request.session = anonymous_session
        return self.get_response(request)
