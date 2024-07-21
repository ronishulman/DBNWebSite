
# from datetime import date
# from .models import Employee, EmployeeMonthlyData


# def aggregate_monthly_data():
#     today = date.today()
#     if today.day != 1:  # Ensure it only runs on the first day of the month
#         return

#     current_month = today.replace(day=1)
#     employees = Employee.objects.all()

#     for employee in employees:
#         salary = employee.salary
#         total_km = employee.total_km
#         total_transport = employee.total_transport
#         total_food = employee.total_food
#         total_parking = employee.total_parking

#         EmployeeMonthlyData.objects.update_or_create(
#             employee=employee,
#             month=current_month,
#             defaults={
#                 'salary': salary,
#                 'total_km': total_km,
#                 'total_transport': total_transport,
#                 'total_food': total_food,
#                 'total_parking': total_parking,
#             }
#         )

#         # Reset the employee's data for the new month
#         employee.total_km = 0
#         employee.total_transport = 0
#         employee.total_food = 0
#         employee.total_parking = 0
#         employee.save()