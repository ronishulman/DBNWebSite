from django.shortcuts import render

# this function returns the homepage
#@login_required
def homepage(request):
    #work_schedule_list = WorkSchedule.objects.all().order_by('date')
    return render(request,"site_base/homepage.html")
