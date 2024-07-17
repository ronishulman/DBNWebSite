import imp
import sys
import pytz
import re
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.timezone import datetime
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from datetime import date, datetime, timedelta, time
from django.utils import timezone
import datetime
from .models import Shift
from clients.models import Client
from employee.models import Employee
from site_base.models import WorkSchedule
from django.core.exceptions import ObjectDoesNotExist
from site_base.views import homepage
from .forms import ShiftFillingForm, ShiftUpdateForm
from site_base.views import my_shifts

tz = pytz.timezone('Israel')

# This function returns the shift page
@login_required
def shift_page(request):
    if request.method == "POST":
        form = ShiftFillingForm(request.POST)
        if form.is_valid():
            logged_in_user= Employee.objects.get(id = request.user.id)
    
            form.instance.shift_start_date_time = timezone.now()
            form.instance.employee_id = logged_in_user.id
            form.instance.first_name = logged_in_user.first_name
            form.instance.last_name = logged_in_user.last_name
            form.save()
            return HttpResponseRedirect('/homepage')
        else:
            return render(request, "shift/shift.html", {'form': form})
    form = ShiftFillingForm() 
    return render(request,"shift/shift.html", {'form':form})

@login_required
def update_shift(request , id):
    shift = Shift.objects.get(pk=id)
    form = ShiftUpdateForm(request.POST or None, instance=shift)

    if form.is_valid():
        logged_in_user= Employee.objects.get(id = request.user.id)
    
        _shift_start_date_time = form.cleaned_data['shift_start_date_time']
        _shift_end_date_time = form.cleaned_data['shift_end_date_time']
        _type_of_shift = form.cleaned_data['type_of_shift']
        _amount_of_km = form.cleaned_data['amount_of_km']
        _public_transport = form.cleaned_data['public_transport']
        _food = form.cleaned_data['food']
        _parking_refund = form.cleaned_data['parking_refund']

        # Correctness check for date and time of end and start of the shift
        if _shift_start_date_time.date() > _shift_end_date_time.date():
            print("התאריך של תחילת המשמרת גדול משל הסוף")
            messages.error(request, " תאריך תחילת המשמרת חייב להיות מוקדם יותר מתאריך סוף המשמרת, אנא נסה שנית.")
            return render(request, 'shift/updateshift.html', {'form': form, 'shift_id': shift.shift_id, 'shift': shift})
        
        if _shift_start_date_time.date() == _shift_end_date_time.date():
            start_time = _shift_start_date_time.time()
            end_time = _shift_end_date_time.time()
            if start_time >= end_time:
                messages.error(request, "זמן תחילת המשמרת חייב להיות מוקדם יותר מזמן סוף המשמרת, אנא נסה שנית.")
                return render(request, 'shift/updateshift.html', {'form': form, 'shift_id': shift.shift_id, 'shift': shift})

        form.save()

        _shift_length = calculate_shift_time(request, id)
        _shift_pay = calculate_shift_salary(id, logged_in_user, _type_of_shift, _shift_length, _amount_of_km, _public_transport, _food, _parking_refund)
        
        return redirect('homepage')
    return render(request, 'shift/updateshift.html', {'form':form, 'shift_id': shift.shift_id, 'shift':shift})

def end_shift(request , id):
    current_shift = Shift.objects.get(shift_id = id)
    current_shift.shift_end_date_time = timezone.now()
    current_shift.save()
    return redirect(reverse('updateshift-view', args=[id]))
    
# The function deletes a shift from the database
@login_required
def delete_shift(request):
    shift_id = request.POST.get('shift_id')
    shift = Shift.objects.get(pk=shift_id)
    shift.delete()
    return HttpResponseRedirect(reverse('homepage'))

# The function calculates the time of the shift
def calculate_shift_time(request, id):  
    shift = Shift.objects.get(shift_id = id)

    shift_start_date_time = shift.shift_start_date_time
    shift_end_date_time = shift.shift_end_date_time
    duration_hours = (shift_end_date_time - shift_start_date_time).total_seconds() / 3600

    integer_part = int(duration_hours)
    decimal_part = duration_hours - integer_part
    minutes = int(decimal_part * 60)

    combined_number = float(str(integer_part) + '.' + str(int(minutes)))

    shift.length_of_the_shift = combined_number
    
    shift.save()    

    return duration_hours

# The function calculates the payment for the shift
def calculate_shift_salary(shift_id, employee, selected_option, shift_length, amount_of_km, public_transport, food, parking_refund):
    shift_pay = 0
    shift = Shift.objects.get(shift_id = shift_id)

    if selected_option == 'הקמה' or selected_option == 'נציגות' or selected_option == 'ראש צוות':
        if shift_length<8:
            shift_pay += employee.hourly_wage*8
        else:
            shift_pay += (shift_length * employee.hourly_wage)

    elif selected_option == 'פירוק':
        if shift_length<6:
             shift_pay += 300
        else:
            shift_pay += (float(shift_length)*50)

    elif selected_option == 'פירוק + פריקה במחסן':
        if shift_length<6:
             shift_pay += 300
        else:
            shift_pay += (float(shift_length)*50)
        shift_pay += 100
        
    if bool(amount_of_km):
        converted_amount_of_km = float(amount_of_km)
        shift_pay += (converted_amount_of_km*0.75)
        
    if bool(public_transport):
        converted_public_transport = float(public_transport)
        shift_pay += converted_public_transport

    if bool(food):
        converted_food= float(food)
        shift_pay += converted_food
        
    if bool(parking_refund):
        converted_parking_refund= float(parking_refund)
        shift_pay += converted_parking_refund
    
    employee.save()
    shift.shift_pay = shift_pay
    shift.save()
    return shift_pay

