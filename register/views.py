from datetime import datetime
from email import message
from multiprocessing import context
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
#from employee.models import Employee
from register.models import EmployeesWaitingForApproval
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from site_base.views import homepage
from django.core.mail import send_mail
from register.forms import SingUpForm


def signup(request):
    if request.method== "POST":
        username= request.POST['username']
        fname= request.POST['fname']
        lname= request.POST['lname']
        _id= request.POST['id']
        _email= request.POST['email']
        _cell_phone = request.POST['cell_phone']
        pass1= request.POST['pass1']
        pass2= request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, 'שם משתמש כבר קיים')
            return redirect('signup')
        
        if User.objects.filter(email=_email):
            messages.error(request,'כתובת האימייל כבר קיימת')
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request,'הסיסמא אינה תואמת')
            return redirect('signup')

        if not username.isalnum():
            messages.error(request,'שם המשתמש חייב לכלול גם ספרות וגם אותיות')
            return redirect('signup')
        
        #user = User.objects.create_user(username, _email, pass1)
        
        employee_info= EmployeesWaitingForApproval(user_name = username, first_name= fname, last_name= lname, id= _id,  email= _email, cell_phone= _cell_phone, pass1 = pass1, pass2 = pass2)
        employee_info.save()

        subject = 'רישום ממתין לאישור'
        message = 'החשבון שלך ממתין לאישור.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [_email]
        send_mail(subject, message, from_email, recipient_list)

        return render(request, "register/signin.html")

    return render(request, "register/signup.html")

def signin(request):
    print("This is a debug message.")
    if request.method== "POST":
        username= request.POST['username']
        pass1= request.POST['pass1']
        
        user=authenticate(username= username, password= pass1)

        if user is not None:
            login(request, user)
            fname= user.first_name
            my_var={'fname': fname}
            return homepage(request)
            

        else:
            messages.error(request, "טעות בשם המשתמש או בסיסמא, אנא נסה שנית.")
            return render(request, "register/signin.html")

    return render(request, "register/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Log out successfully")
    return redirect('signin')
