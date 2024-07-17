from django.urls import path, include
from . import views

urlpatterns = [
    path("shift", views.shift_page, name ="shiftpage-view"),
    path("endshift/<int:id>", views.end_shift, name ="endshift-view"),
    path("updateshift/<int:id>", views.update_shift, name="updateshift-view"),
    #path("editshift/<int:id>", views.edit_shift_page, name="editshift-view"),
    #path("shiftinfo", views.shiftinfo_page, name="shiftinfo-view"),
    path("deleteshift", views.delete_shift, name="deleteshift-view"),
]
