from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.urls import reverse

import pyrebase

config = {
    "apiKey": "AIzaSyBPDBNI4BoXYX2l_m0Ak7s3vn4B3AbKsPo",
    "authDomain": "cfg42-fe337.firebaseapp.com",
    "databaseURL": "https://cfg42-fe337.firebaseio.com",
    "projectId": "cfg42-fe337",
    "storageBucket": "cfg42-fe337.appspot.com",
    "messagingSenderId": "500919872728",
    "appId": "1:500919872728:web:6c411b714dd01c2b187bad",
    "measurementId": "G-331ZH26DLW"
}

firebase = pyrebase.initialize_app(config)
firebase_auth = firebase.auth()
database = firebase.database()

# Log the user in
#user = auth.sign_in_with_email_and_password(email, password)

# Log the user in anonymously
#user = auth.sign_in_anonymous()

# Get a reference to the database service
def index(request):
    return render(request,'authorization/index.html',{})

def user_register(request):
    
    email = request.POST.get('email')
    email = str(email).rstrip(' \t\r\n\0') #new line added here --------
    password = request.POST.get('password')
    print('email',email)
    print('password',password)
    try:
        user = firebase_auth.create_user_with_email_and_password(email, password)
        print(user)
    except :
        message = "Invalid Login Credentials"
        return render(request,'authorization/register.html', {'message':message})

    return redirect('index')

def user_login(request):

    email = request.POST.get('email')
    email = str(email).rstrip(' \t\r\n\0') #new line added here --------
    password = request.POST.get('password')
    print('email',email)
    print('password',password)
    try:
        user = firebase_auth.sign_in_with_email_and_password(email, password)
        print(user)
        uid = user['localId']
        email = user['email']
        request.session['uid'] = str(uid)
        request.session['email'] = str(email)
        print(request)
    except :
        message = "Invalid Login Credentials"
        return render(request,'authorization/login.html', {'message':message})

    return render(request,'authorization/index.html',{'email':request.session.get('email')})


def user_logout(request):
    del request.session['uid']
    del request.session['email']    
    firebase_auth.current_user = None
    print(request.session)
    return render(request, "authorization/index.html",{})