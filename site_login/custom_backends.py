# from django.contrib.auth.backends import BaseBackend
# from blog.models import Usuario

# class EmailBackend(BaseBackend):
#     def authenticate(self, username=None, password=None, **kwargs):
#         UserModel = Usuario
#         try:
#             user = UserModel.objects.get(email=username)
#         except UserModel.DoesNotExist:
#             return None
#         else:
#             if user.check_password(password):
#                 return user
#         return None

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from blog.models import Usuario

class EmailBackend(ModelBackend):
    def authenticate(self, request,username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.is_superuser and user.check_password(password):
                return user
        except:
            pass

        try:
            usuario = Usuario.objects.get(email=username)
        except Usuario.DoesNotExist:
            return None
        else:
            if usuario.user.check_password(password):
                return usuario.user
        return None