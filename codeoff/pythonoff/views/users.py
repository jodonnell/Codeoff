from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import models
from django import forms
from django.contrib.auth import login, authenticate, logout
from django import http

class CodeoffUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

def create_user(request):
    if request.method == 'POST':
        form = CodeoffUserForm(request.POST)
        if form.is_valid():
            user = models.User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password1'])
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                return http.HttpResponseRedirect('/')
    else:
        form = CodeoffUserForm()
    return render_to_response('generic_form.html', {'form':form, 'form_name':'create_user', 'form_action':'/accounts/create/', 'form_method':'POST'})


def codeoff_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return http.HttpResponseRedirect('/')
    else:
        form = AuthenticationForm()

    return render_to_response('generic_form.html', {'form':form, 'form_name':'login', 'form_action':'/accounts/login/', 'form_method':'POST'})

def codeoff_logout(request):
    logout(request)
    return http.HttpResponseRedirect('/')
