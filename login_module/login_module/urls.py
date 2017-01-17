from login.views import LoginView
from login.views import LogoutView
from login.views import UserView
from login.views import RegisterView

from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^register/', RegisterView.as_view(), name="register"),
    url(r'^logout/', LogoutView.as_view(), name="logout"),
    url(r'^users/', UserView.as_view(), name="users"),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
]
