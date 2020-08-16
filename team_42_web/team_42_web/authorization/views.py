from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.urls import reverse, reverse_lazy

from django.urls import reverse
import os
import pyrebase

###### Firestore #######
from firebase import firebase
import firebase_admin
from firebase_admin import credentials, firestore, auth
########################
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


#############FIRESTORE##############

cred = credentials.Certificate(
    os.path.join(os.path.dirname(__file__), "ServiceAccountKey.json")
    
)
default_app = firebase_admin.initialize_app(cred)
print(    os.path.join(os.path.dirname(__file__), "ServiceAccountKey.json")
)
db = firestore.client()

current_user_uid = ""

######################################

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
    t = request.POST.get('type')
    print(t)
    try:
        user = firebase_auth.create_user_with_email_and_password(email, password)
        
        print(user)
        uid = user['localId']
        email = user['email']
        request.session['uid'] = str(uid)
        request.session['email'] = str(email)

        print(request.session.get('uid'))
        data = {"email":email, "password" : password,"type":t}
        db.collection(u"Users").document(email).set(data)
        
        user = firebase_auth.sign_in_with_email_and_password(email, password)
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
    user=None
    if email==None or password==None:
        pass

    try:
        user = firebase_auth.sign_in_with_email_and_password(email, password)
        print(user)
        uid = user['localId']
        email = user['email']
        request.session['uid'] = str(uid)
        request.session['email'] = str(email)
        
        print(request)
        return render(request,'authorization/index.html',{'email':request.session.get('email')})
    except :
        message = "Invalid Login Credentials"
        return render(request,'authorization/login.html', {'message':message})
    request.session['type'] = database.child("type").child("email").get()
    return render(request,'authorization/index.html',{'email':request.session.get('email')})
 
""" def user_register(request):
    
    email = request.POST.get('email')
    email = str(email).rstrip(' \t\r\n\0') #new line added here --------
    password = request.POST.get('password')
    print('email',email)
    print('password',password)
    try:
        
        user = firebase_auth.create_user_with_email_and_password(email, password)
        print("User created")
        e = user['localId']
        print("Check")
        data = {"email": email, "password":password}
        me = db.collection("Users").document(e).set(data)
        print(me)
        print("Success")
        return render(request,'authorization/index.html',{})
    except:
        message = "Invalid Login Credentials"
        return render(request,'authorization/register.html', {'message':message})

    return render(request,'authorization/index.html',{})"""

def user_logout(request):
    del request.session['uid']
    del request.session['email']  
    print(request.session.get('uid'))     
    firebase_auth.current_user = None
    print(request.session)
    return render(request, "authorization/index.html",{})

#def getClassNames(request):


def teacherRegistartion(request):
    data = { "fname" : request.POST.get('fname'),
            "lname" : request.POST.get('lname'),
            "addr" : request.POST.get('addr'),
            "city" : request.POST.get('city'),
            "state" : request.POST.get('state'),
            "zip" : request.POST.get('zip'),
            "title" : request.POST.get('title'),
            "school" :request.POST.get('school'),
            "phone" :request.POST.get('phone') }
    try:
        unid = request.session['uid']
        database.child("unid").set(data)
    
    except :
        message = "Can't Update Your Details"
        return render(request , 'authorization/teacherRegistration.html' , {'message' : message})
    return render(request,'authorization/teacherRegistration.html',{})
