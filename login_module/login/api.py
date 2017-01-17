from login.models import UserProfile
from django.contrib.auth.models import User

class UserProfileInstanceResource(object):
    def _post(self, kwargs):
        # registered = False
        # #process form data.
        # if request.method == 'POST':
        #     # Attempt to grab information from the raw form information.
        #     user_form = UserForm(data=request.POST)
        #     if user_form.is_valid():
        #         # Save the user's form data to the database.
        #         user = user_form.save()
        #         user.set_password(user.password)
        #         user.save()
        name = kwargs.get("name", None)
        username = kwargs.get("username", None)
        password = kwargs.get("password", None)
        user = User()
        user.password = password
        user.username = username
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
        print all_users
        return all_users
