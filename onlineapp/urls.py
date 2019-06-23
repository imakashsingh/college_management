from django.urls import *
from onlineapp import views
from onlineapp.viewss.college import *
from onlineapp.forms.college import AddCollege
from onlineapp.serializers import *
from rest_framework.authtoken import views

urlpatterns = [
    #path('testapp/',views.hello_world),
    #path('hello/',viewss.hello_world),
    #path('get_clg_name/',viewss.get_my_college),
    #path('get_all_clgs/',viewss.get_all_colleges),
    #path('get_all_clgst/',viewss.get_all_colleges_temp),
    path('colleges/',CollegeView.as_view(),name = "colleges_html"),
    path('colleges/<int:pk>/',StudentView.as_view(),name = "colleges_details"),
    path('colleges/add/',AddCollegeView.as_view(),name = "add_college_details"),
    path('colleges/<int:pk>/edit',AddCollegeView.as_view(),name = "edit_college"),
    path('colleges/<int:pk>/delete',AddCollegeView.as_view(),name = "delete_college"),
    path('colleges/<str:acronym>/',StudentView.as_view(),name = "colleges_details"),
    path('colleges/<int:pk>/add',AddStudentView.as_view(),name = "add_student_details"),
    path('colleges/<int:pk>/sedit',AddStudentView.as_view(),name = "edit_student_details"),
    path('colleges/<int:pk>/sdelete',AddStudentView.as_view(),name = "delete_student_details"),
    path('login/',LoginView.as_view(),name = "login"),
    path('logout/',logout_func,name = "logout"),
    path('signup/',SignupView.as_view(),name = "signup"),

    path('api/v1/colleges/',add_college_api,name = "add_college_api"),
    path('api/v1/colleges/<int:pk>/',add_college_api,name = "add_college_api"),
    path('api/v1/colleges/<int:id>/students/',add_student_api,name = "add_student_api"),
    path('api/v1/colleges/<int:id>/students/<int:stuid>/',add_student_api,name = "add_student_api"),

        path('api-token-auth/',views.obtain_auth_token),
]