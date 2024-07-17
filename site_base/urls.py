from django.urls import path, include
from . import views

urlpatterns = [
    #path('', views.land_page),
    path('myshifts', views.my_shifts, name='myshifts'),
    path('employeesinfo', views.employees_shifts, name='employeesinfo'),
    path('homepage/', views.homepage, name='homepage'),
    path('clientsinfo', views.clients_info, name='clientsinfo'),
    path('clientdetails', views.client_details),
    path('profile', views.profile_page),
    path('employeespermits', views.employees_permits),
    path('employee_details/<int:id>', views.employee_details, name="employee_details-view"),
    path('update_hourly_wage', views.update_hourly_wage, name='update_hourly_wage'),
    path('editprofile', views.edit_profile, name="edit_profile"),
    path('logout', views.log_out),
    path('addclient', views.add_client, name="add_client"),
    path('deleteclient', views.delete_client, name="delete_client"),
    path('deleteemployee', views.delete_employee, name="delete_employee"),
    path('addshift', views.add_shift, name= 'add_shift'),
    path('update_WorkSchedule_shift/<int:id>', views.update_WorkSchedule_shift, name="update-shift"),
    path('delete_WorkSchedule_shift/<int:id>', views.delete_WorkSchedule_shift, name="delete-shift"),
    path('', include('shift.urls')), 
]
