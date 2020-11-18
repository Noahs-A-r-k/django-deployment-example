from django.shortcuts import render
from AuthApp.forms import UserForm,UserProfileInfoForm
# Create your views here.
# check if there is a POST call and manipulate data from there

#
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
# decorate view with login_required to require user is logged in
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request,'AuthApp/index.html')

def register(request):

    # assume they are not registered at first
    registered = False

    if request.method == 'POST':
        # get information from both forms
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # check if both forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # if valid grab everything from the base user_form
            user = user_form.save()
            # goes into settings.py file and sets it as a hash
            user.set_password(user.password)
            user.save()

            # deal with extra info: website link etc
            # do not commit as to not override previous user
            profile = profile_form.save(commit=False)
            # relates extra attributes to OneToOne relationship?
            profile.user = user

            # check if there is a picture in the profile_pic form
            if 'profile_pic' in request.FILES:
                # if so, save it
                profile.profile_pic = request.FILES['profile_pic']

            # if all forms are is_valid
            profile.save()
            registered = True

        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'AuthApp/registration.html',
                                    {'user_form':user_form,
                                     'profile_form':profile_form,
                                     'registered':registered,})

# login view
def user_login(request):

    if request.method == 'POST':
        # uses the name from the html and gets the values
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username,password=password)

        # if authenticated and user is active
        if user:
            if user.is_active:
                # function we imported passing in user object returned by authenticate
                login(request,user)
                # redirects users to homepage
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("Account not active")
        else:
            print("Someone tried to login and failed")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request,'AuthApp/login.html',{})

@login_required
def special(request):
    return(HttpResponse("You are currently logged in :D"))

# view that requires login, with decorator
@login_required
def user_logout(request):
     # auto logout user
    logout(request)
    # reverse looks through all urls and returns the actual url of the named parameter
    return HttpResponseRedirect(reverse('index'))
