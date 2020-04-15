from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from . import forms
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

def signup(request):
    context = {}
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            try:
              user = User.objects.create_user(
                form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'])
              user.is_active = False
              user.save()
              current_site = get_current_site(request)
              email_subject = 'Activate Your Account'
              message = render_to_string('account_activation/activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),})
              to_email = form.cleaned_data.get('email')
              email = EmailMessage(email_subject, message, to=[to_email])
              email.send()
              return render(request, 'account_activation/activation_sent.html', context)
            except IntegrityError:
                form.add_error('username', 'Username is taken')
        context['form'] = form
    return render(request, 'accounts/signup.html', context)

def activate_account(request, uidb64, token):
    context = {}
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'account_activation/activated_successfully.html', context)
    else:
        return render(request, 'account_activation/activation_invalid.html', context)

def do_login(request):
    context = {}
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request,
              username=form.cleaned_data['username'],
              password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if 'next' in request.GET:
                    return HttpResponseRedirect(request.GET['next'])
                return HttpResponseRedirect('/')
            else:
                form.add_error(None, 'Unable to log in')
        context['form'] = form
    return render(request, 'accounts/login.html', context)

def do_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
