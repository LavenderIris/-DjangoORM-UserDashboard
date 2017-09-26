from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime, localtime
from .models import *
from django.contrib import messages
import bcrypt



def index(request):
    return render(request,'landingPage.html')

def add_user(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
       
    else: 
        myrequest = request.POST

        all_users = User.objects.all()
        user_level = 5
    
        # first user gets admin level
        if len(all_users) == 0:
            user_level = 0
        # need to Bcrypt our password
        hash1 = bcrypt.hashpw( myrequest['pw'].encode('utf8') , bcrypt.gensalt())
        user = User.objects.create(first_name=myrequest['first_name'], last_name=myrequest['last_name'], email=myrequest['email'], pw=hash1, user_level = user_level  )
        user.save()
        return redirect('/success')

    return redirect('/register')

def success(request):
    return render(request, 'success.html')

def login(request):
    if request.method == 'POST':
        myrequest = request.POST
        user = User.objects.filter(email=myrequest['email'])
        # if record not found
        if len(user) == 0:
            errors = {}
            errors['email_not_found'] = 'Email not found in our records'
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/signin')
        else:
            # password on file
            hashed_pw = user[0].pw
            if bcrypt.checkpw( myrequest['pw'].encode('utf8'), hashed_pw.encode('utf8') )  :
                if user[0].user_level == 0:
                    request.session['login']= True
                    request.session['first_name']= user[0].first_name
                    request.session['last_name']= user[0].last_name    
                    request.session['email']= user[0].email  
                
                    return redirect('/dashboard/admin')
                else:
                    return redirect('/dashboard')
                                
                return redirect('/success')
            else:
                errors = {}
                errors['password_no_match'] = "Password doesn't match our records. Incorrect password."
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)

    return redirect('/signin')

def signin(request):
    return render(request, 'signin.html')

def register(request):
    return render(request,'register.html')

def admindashboard(request):
    return render(request,'admindashboard.html', {'users': User.objects.all()})

def normaldashboard(request):
    return render(request,'normaldashboard.html', {'users': User.objects.all()})

def admin_add_user(request):
    return render(request,'admin_add_user.html')

def edit_user_admin(request, id):
    
    return render(request,'edit_user_admin.html', {'user': User.objects.get(id=id) })

def process_admin_edit(request):
    

    print "REQUEST FROM EDIT", request.POST
  
    return redirect('/register')