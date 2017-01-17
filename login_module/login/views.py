# -*- coding: utf-8 -*-
# Django
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.base import View
from django.views.generic import TemplateView, FormView
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# Login
from login.forms import LoginForm, UserForm
from login.api import UserProfileInstanceResource
from login.api import UserProfileListResource
from login.models import UserProfile

# Python
import datetime

# Requests
import requests

print "ALL OBS", UserProfile.objects.all()
for user in UserProfile.objects.all():
    print user.user
    print user.username
    print user.name
    print user.user.password

class LoginView(TemplateResponseMixin,View):
    template_name = "login.html"
    form_class = LoginForm
    print "IN LOGIN View"

    def get(self, request):
        print "IN GET"
        if request.user.is_authenticated():
            return HttpResponseRedirect('users')
        else:
            template_values = {}
            template_values['form'] = self.form_class()
            return self.render_to_response(template_values)

    def post(self, request):
        data = request.POST.copy()
        print "IN POST"

        form = self.form_class(data)
        print form
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            print user, "USER"
            return HttpResponseRedirect('%s?success=1'% reverse('users'))
        else:

            return self.render_to_response({
                'form': form,
            })
@method_decorator(login_required, name='dispatch')
class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')

@method_decorator(login_required, name='dispatch')
class UserView(TemplateView):
    template_name = 'users.html'

    def get(self, *args, **kwargs):
        users = UserProfileListResource()._get()
        template_values = {"users":users}
        return self.render_to_response(template_values)


class RegisterView(FormView):
    '''
    Add Users
    '''
    template_name = "register.html"
    form_class = UserForm

    def get(self, *args, **kwargs):
        print "in register view"
        form = self.form_class(self.request.POST)
        return super(RegisterView, self).get(self, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        username = form.cleaned_data['username']
        if UserProfile.objects.filter(username=username).exists():
            return self.render_to_response({'username':username})
        else:
            user = UserProfileInstanceResource()._post(form.cleaned_data)
            return HttpResponseRedirect('%s?success=1'% reverse('login'))
