from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomEmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        User = get_user_model()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None  # Email not found, authentication fails

        if user.check_password(password):
            return user  # Authentication succeeds
        else:
            return None  # Incorrect password, authentication fails
