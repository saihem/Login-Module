from login.models import UserProfile
from django.contrib.auth.models import User

class UserProfileInstanceResource(object):
    def _post(self, kwargs):
        name = kwargs.get("name", None)
        username = kwargs.get("username", None)
        password = kwargs.get("password", None)
        user = User.objects.create_user(username=username, password=password)
        user.save()
        user_profile = UserProfile(user=user, name=name, username=username)
        user_profile.save()
        return user

class UserProfileListResource(object):
    def _get(self, *args,  **kwargs):
        users = UserProfile.objects.all()
        all_users = []
        for user in users:
            all_users.append({"name": user.name,
                                "username": user.username})
        return all_users
