from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django import forms
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class RegisterForm(forms.Form):
    pass

# Create your views here.
def index(request):
    return render(request, "index.html", {})
def signin(request):
    if(request.method=="POST"):
        login_details = LoginForm(request.POST)
        if(login_details.is_valid() == False):
            return render(request, "502.html", {})
        uname = login_details.cleaned_data["username"]
        password = login_details.cleaned_data["password"]
        user = authenticate(request, username=uname, password=password)
        if(uname == '' or password == ''):
            return render(request, "login.html", {
                "form": LoginForm(),
                "message": "Neither username or password can be blank."
            })
        if(user == None):
            return render(request, "login.html", {
                "form": LoginForm(),
                "message": "Incorrect username or password"
            }) 
        login(request, user)
        return HttpResponseRedirect("index.html")
    return render(request, "login.html", {
        "form": LoginForm(),
        "message": ""
    })
#def register(request):
#    if(request.method=="POST"):
#