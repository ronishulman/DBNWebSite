from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from employee.models import Employee
from shift.models import Shift
from datetime import datetime
from django.forms.models import model_to_dict
from site_base.models import WorkSchedule
from register.models import EmployeesWaitingForApproval
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.conf import settings
from django.shortcuts import get_object_or_404
import json
from clients.models import Client
from .forms import WorkScheduleForm
from django.utils import formats
from datetime import date

# GLOBAL VARIABLES
counter = 0

# this function returns the homepage
@login_required
def homepage(request):
    work_schedule_list = WorkSchedule.objects.all().order_by('date')
    return render(request,"site_base/homepage.html",{'work_schedule_list': work_schedule_list, 'user': request.user})

@login_required
def profile_page(request):
    connected_user = Employee.objects.get(id = request.user.id)
    connected_user_shifts = Shift.objects.filter(employee_id = request.user.id)
    calculate_employees_details(connected_user)

    return render(request,"site_base/profile.html", {'connected_user': connected_user})

#this function return the sign in page
def sign_in_page(request):
    return render(request,"register/signin.html")
#this function returns a page that displays for the logged in user his shifts

@login_required
def my_shifts(request):
    user = request.user
    user_id = request.user.id
    if request.method == "POST":
        _month = request.POST['month']
        _year = request.POST['year']
 
        user_shifts = Shift.objects.filter(employee_id = user_id, shift_start_date_time__month =_month).order_by("-shift_id")
        context = {"data": user_shifts , 'user': user}
        return render(request, "site_base/myshifts.html",context)

    user_shifts = Shift.objects.filter(employee_id = user_id).order_by("-shift_id")
    context = {"data": user_shifts , 'user': user}
    return render(request, "site_base/myshifts.html",context)
@login_required
def land_page(request):
    return render(request,"register/signin.html")
@login_required
def add_shift(request):
    sumbbited = False
    if request.method == "POST":
        form = WorkScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/homepage')
        else:
            print(form.errors)
            return render(request, "site_base/addshift.html", {'form': form})
    form = WorkScheduleForm() 
    return render(request,"site_base/addshift.html", {'form':form})
@login_required
def update_WorkSchedule_shift(request , id):
    shift = WorkSchedule.objects.get(pk=id)
    form = WorkScheduleForm(request.POST or None, instance=shift)
    if form.is_valid():
        form.save()
        return redirect('homepage')
    return render(request, 'site_base/updateshift.html', {'shift':shift, 'form':form})
@login_required
def delete_WorkSchedule_shift(request , id):
    shift = get_object_or_404(WorkSchedule, pk=id)
    shift.delete()
    return redirect('homepage')
@login_required
def employees_shifts(request):
    user = request.user
    employees = Employee.objects.all()
    context = {'employees': employees, 'user': user}

    if request.method == "POST":
        employee_name = request.POST['employee_full_name']
        requested_month = request.POST['month']
        requsted_year = request.POST['year']

        if(requested_month):
            requested_month = int(request.POST['month'])
        if(requsted_year):
            requsted_year = int(request.POST['year'])

        if(' ' in employee_name):
            first_name , last_name = employee_name.strip().split()
            if(requested_month and requsted_year):
                employee_requested_shifts = Shift.objects.filter(first_name = first_name, last_name = last_name, event_date__month= requested_month, event_date__year= requsted_year).order_by("-shift_id")
            elif (requested_month):
                employee_requested_shifts = Shift.objects.filter(first_name = first_name, last_name = last_name, event_date__month= requested_month).order_by("-shift_id")
            elif(requsted_year):
                employee_requested_shifts = Shift.objects.filter(first_name = first_name, last_name = last_name, event_date__year= requsted_year).order_by("-shift_id")
            else:
                employee_requested_shifts = Shift.objects.filter(first_name = first_name, last_name = last_name).order_by("-shift_id")

            if( employee_requested_shifts):                
                return render(request,"site_base/employeesinfo.html", {'employee_requested_shifts': employee_requested_shifts, 'employee_name': employee_name, 'user': user})
            else:
                message = "there is no shifts for these employee" 
                return render(request,"site_base/employeesinfo.html", {'message': message, 'user': user})
        else:
           message = "the name in invalid, please try again" 
           return render(request,"site_base/employeesinfo.html", {'message': message, 'user': user})

    return render(request, "site_base/employeesinfo.html", context)
@login_required
def clients_info(request):
    user = request.user
    clients = Client.objects.all()
    context = {'clients': clients, 'user': user}         
    return render(request,"site_base/clientsinfo.html", context)
@login_required
def employee_details(request, id):
    user = request.user
    required_employee = Employee.objects.get(id = id)
    connected_user_shifts = Shift.objects.filter(employee_id = request.user.id)
    calculate_employees_details(required_employee)

    if request.method == "POST":
        _month = request.POST.get('month')
        _year = request.POST.get('year')
        
        if not _month or not _year:
            user_shifts = Shift.objects.filter(employee_id = id).order_by("-shift_id")
            salary = calulate_salary(request)
            context = {'required_employee': required_employee, 'data':user_shifts,'salary': salary}
            return render(request,"site_base/employeedetails.html",context)   
        else:
            user_shifts = Shift.objects.filter(employee_id = id, shift_start_date_time__month =_month, shift_start_date_time__year =_year ).order_by("-shift_id")
            context = {'required_employee': required_employee, 'data':user_shifts, 'user': user}
            return render(request,"site_base/employeedetails.html",context) 
@login_required
def client_details(request):
     user = request.user
     if request.method == "POST":
        client_name = request.POST['client_name']
        _month = request.POST.get('month')
        _year = request.POST.get('year')

        if not _month or not _year:
            client_shifts = Shift.objects.filter(client = client_name).order_by("-shift_id")
            context = {'data':client_shifts, 'clinet_name': client_name, 'user': user}
            return render(request,"site_base/clientdetails.html",context)   
        else:
            client_shifts = Shift.objects.filter(client = client_name, shift_start_date_time__month =_month, shift_start_date_time__year =_year ).order_by("-shift_id")
            context = {'data':client_shifts, 'clinet_name': client_name, 'user': user}
            return render(request,"site_base/clientdetails.html",context)
@login_required
def employees_permits(request):
    user = request.user
    if request.method == "POST":
        id = request.POST['employee_id']
        wage = request.POST['wage']
        employee_to_aprove = EmployeesWaitingForApproval.objects.get(id = id)

        employee_info= Employee(employee_to_aprove.first_name, last_name= employee_to_aprove.last_name, id=employee_to_aprove.id,  email= employee_to_aprove.email, cell_phone = employee_to_aprove.cell_phone, hourly_wage= wage )
        employee_info.save()
        
        myuser= User.objects.create_user(username= employee_to_aprove.user_name, first_name = employee_to_aprove.first_name, last_name= employee_to_aprove.last_name, email=employee_to_aprove.email, password= employee_to_aprove.pass1, id= employee_to_aprove.id)
        myuser.save()

        employee_to_aprove.delete()

        subject = '.רישומך אושר'
        message = 'החשבון שלך אושר. בהצלחה!'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [employee_to_aprove.email]
        send_mail(subject, message, from_email, recipient_list)

        employees_waiting_for_permits = EmployeesWaitingForApproval.objects.all()
        context = {'employees': employees_waiting_for_permits, 'user': user}
        return render(request,"site_base/employeespermits.html", context)    

    employees_waiting_for_permits = EmployeesWaitingForApproval.objects.all()
    context = {'employees': employees_waiting_for_permits, 'user': user}
    return render(request,"site_base/employeespermits.html", context)          
@csrf_exempt
def update_hourly_wage(request):
    if request.method == "POST":
        employee_id = request.POST['employee_id']
        new_hourly_wage = request.POST['new_hourly_wage']
        employee = Employee.objects.get(id=employee_id)
        employee.hourly_wage = new_hourly_wage
        employee.save()

        response_data = {'success': True}
        return JsonResponse(json.dumps(response_data), safe=False)
    
    return JsonResponse({'success': False})
@login_required
def calulate_salary(request):
    all_shifts = Shift.objects.all()
    salary = 0

    for shift in all_shifts:
        if shift.employee_id == request.user.id:
            salary += shift.shift_pay

    return salary
@login_required
def edit_profile(request):
    logged_in_user = Employee.objects.get(id = request.user.id)
    salary = 0
    payment_for_fuel_refunds = 0
    payment_for_food_refunds = 0
    payment_for_public_transport_refunds = 0
    payment_for_parking_refunds = 0
    connected_user_shifts = Shift.objects.filter(employee_id = request.user.id)
    for shift in connected_user_shifts:
        salary += shift.shift_pay
        payment_for_fuel_refunds += shift.amount_of_km
        payment_for_parking_refunds += shift.parking_refund
        payment_for_public_transport_refunds += shift.public_transport
        payment_for_food_refunds += shift.food

    context = {'salary': salary , 'payment_for_fuel_refunds': payment_for_fuel_refunds, 'payment_for_public_transport_refunds': payment_for_public_transport_refunds, 'payment_for_food_refunds': payment_for_food_refunds, 'payment_for_parking_refunds': payment_for_parking_refunds, 'user': logged_in_user}

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        cell_phone = request.POST.get('cell_phone')

        if first_name:
            updated_first_name = first_name
        else:
            updated_first_name = logged_in_user.first_name
    
        if last_name:
            updated_last_name = last_name
        else:
            updated_last_name = logged_in_user.last_name
               
        if email:
            updated_email = email
        else:
            updated_email = logged_in_user.email
        
        if cell_phone:
            updated_cell_phone = cell_phone
        else:
            updated_cell_phone = logged_in_user.cell_phone
        
        logged_in_user = Employee(id = logged_in_user.id, first_name = updated_first_name , last_name = updated_last_name, email = updated_email, cell_phone = updated_cell_phone)
        logged_in_user.save()

        logged_in_user = Employee.objects.get(id = request.user.id)
        updated_context = {'salary': salary , 'payment_for_fuel_refunds': payment_for_fuel_refunds, 'payment_for_public_transport_refunds': payment_for_public_transport_refunds, 'payment_for_food_refunds': payment_for_food_refunds, 'payment_for_parking_refunds': payment_for_parking_refunds, 'user': logged_in_user}
        return render(request, 'site_base/profile.html', updated_context)

    return render(request, 'site_base/editprofile.html', context)
@login_required
def log_out(request):
    logout(request)
    return render(request, 'register/signin.html')
@login_required  
def add_client(request):
    if request.method == 'POST':
        new_client = request.POST.get('client_name')
        new_client = Client(name=new_client)
        new_client.save()  

        return redirect('clientsinfo')
    return render(request, "site_base/homepage.html")
@login_required
def delete_client(request):
    if request.method == "POST":
        client_name = request.POST['client_name']
        client = Client.objects.get(name=client_name)
        client.delete()
    return redirect('clientsinfo')

def delete_employee(request):
    if request.method == "POST":
        employee_id = request.POST['employee_id']
        employee = Employee.objects.get(id=employee_id)
        employee.delete()
        user = User.objects.get(id=employee_id)
        user.delete()
    return redirect('employeesinfo')

def calculate_employees_details(employee):
    employees_shifts = Shift.objects.filter(employee_id=employee.id)

    employee.total_km = 0
    employee.total_food = 0
    employee.total_transport = 0
    employee.total_parking = 0
    employee.salary = 0

    for shift in employees_shifts:
        employee.total_km += shift.amount_of_km
        employee.total_food += shift.food
        employee.total_transport += shift.public_transport
        employee.total_parking += shift.parking_refund
        employee.salary += shift.shift_pay
    
    employee.save()
    return



