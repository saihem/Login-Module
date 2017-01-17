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

# Requests
import requests

print "ALL OBS", UserProfile.objects.all()
for user in UserProfile.objects.all():
    print user.user, "username" , user.user.username,
    print "name", user.name
    print user.username
    print user.user.password

class LoginView(TemplateResponseMixin,View):
    template_name = "login.html"
    form_class = LoginForm
    '''
    Login authenticates user, if successful redirects to UserView
    '''
    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('users')
        else:
            template_values = {}
            template_values['form'] = self.form_class()
            return self.render_to_response(template_values)

    def post(self, request):
        data = request.POST.copy()
        form = self.form_class(data)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('%s?success=1'% reverse('users'))
            else:
                return HttpResponseRedirect('%s?error=1'% reverse('login'))
        else:
            # errors in form will get passed to template
            return self.render_to_response({
                'form': form,
            })

@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    '''
    Logs user out to login page
    '''
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')

@method_decorator(login_required, name='dispatch')
class UserView(TemplateView):
    '''
    Shows a list of Users
    '''
    template_name = 'users.html'

    def get(self, *args, **kwargs):
        users = UserProfileListResource()._get()
        template_values = {"users":users}
        return self.render_to_response(template_values)

class RegisterView(FormView):
    '''
    Renders template to add users
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
            return self.render_to_response({'username_exists':username})
        else:
            user = UserProfileInstanceResource()._post(form.cleaned_data)
            return HttpResponseRedirect('%s?success=1'% reverse('login'))
