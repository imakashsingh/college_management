from django.views import View
from django.views.generic.edit import FormView
from onlineapp.models import *
from django.shortcuts import render,redirect,get_object_or_404
from onlineapp.forms.college import *
from django.urls import resolve
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from onlineapp.serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

class StudentView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request,*args,**kwargs):
        if kwargs:
            college = College.objects.get(**kwargs)
            #students = Student.objects.values('name','email','mocktest1__total').filter(college_id = college.id)
            students = list(college.student_set.order_by('-mocktest1__total'))
            return render(
                request,
                template_name="onlineapp/colleges_detail.html",
                context={
                    'college' : college,
                    'students' : students,
                    'title' : 'Students from {}'.format(college.name)
                }
            )

class CollegeView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self,request,*args,**kwargs):
        colleges = College.objects.all()
        return render(
            request,
            template_name="onlineapp/colleges.html",
            context={
                'jails': colleges,
                'title': 'All colleges'
            }
        )

class AddCollegeView(LoginRequiredMixin,FormView):
    login_url = '/login/'
    def get(self,request,*args,**kwargs):
        if resolve(request.path_info).url_name == 'delete_college':
            College.objects.get(pk=kwargs.get('pk')).delete()
            return redirect('colleges_html')
        form = AddCollege()
        if kwargs:
            college = College.objects.get(**kwargs)
            form = AddCollege(instance=college)
            return render(request,template_name="onlineapp/add_clg_formm.html",context={'form': form})
        else:
            return render(
                request,
                template_name= "onlineapp/add_clg_formm.html",context={'form': form})

    def post(self, request, *args, **kwargs):
        if resolve(request.path_info).url_name == 'edit_college':
            college = College.objects.get(pk = kwargs.get('pk'))
            form = AddCollege(request.POST,instance=college)
            if form.is_valid():
                form.save()
                return redirect('colleges_html')

        else:
            form = AddCollege(request.POST)
            if form.is_valid():
                form.save()
                return redirect('colleges_html')
            return render(
                request,
                template_name="onlineapp/add_clg_formm.html", context={'form': form})

class AddStudentView(LoginRequiredMixin,FormView):
    login_url = '/login/'
    def get(self,request,*args,**kwargs):
        if resolve(request.path_info).url_name == 'delete_student_details':
            get_object_or_404(Student, **kwargs).delete()
            return redirect('colleges_html')
        student_form = AddStudent()
        marks_form = Mockdetails()
        if resolve(request.path_info).url_name == 'edit_student_details':
            student = Student.objects.get(**kwargs)
            mock = MockTest1.objects.get(student = student)
            student_form = AddStudent(instance=student)
            marks_form = Mockdetails(instance=mock)
        return render(request,template_name="onlineapp/add_stu_form.html",
                      context={'student_form' : student_form,'marks_form' : marks_form})

    def post(self, request, *args, **kwargs):
        """if resolve(request.path_info).url_name == 'delete_student_details':
            s = get_object_or_404(Student,**kwargs).delete()
            return redirect('colleges_html')"""

        if resolve(request.path_info).url_name == 'edit_student_details':
            s = get_object_or_404(Student, **kwargs)
        else:
            c = College.objects.get(**kwargs)
            s = Student(college = c)

        student_form = AddStudent(request.POST,instance=s)

        if student_form.is_valid():
            student_form.save()
            total = sum([int(request.POST['problem' + str(i)]) for i in range(1,5)])

            if resolve(request.path_info).url_name == 'edit_student_details':
                mock = MockTest1.objects.get(student = s)
                mock.total = total
            else:
                mock = MockTest1(student = s,total = total)

            marks_form = Mockdetails(request.POST,instance=mock)
            if marks_form.is_valid():
                marks_form.save()
            return redirect('colleges_html')

class  LoginView(FormView):
    def get(self, request, *args, **kwargs):
        form = Login_form()
        return render(request,
                      template_name="onlineapp/logintemp.html",context={'form' : form})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = AuthenticationForm(request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username = username,password = password)
            if user is not None:
                login(request,user)
                return redirect('colleges_html')
            else:
                messages.error(request, 'username or password not correct')
                return redirect('login')
        else:
            form = AuthenticationForm()
            return render(request, 'onlineapp/logintemp.html', {'form': form})

class SignupView(FormView):
    def get(self, request, *args, **kwargs):
        form = SignUp_form()
        return render(request,
                      template_name='onlineapp/signup.html',context={'form':form})

    def post(self, request, *args, **kwargs):
        form = SignUp_form(request.POST)
        if form.is_valid():
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.create_user(username,password = password)
            user.save()
            if user is not None:
                login(request,user)
                return redirect('colleges_html')
            else:
                return redirect('signup')


@login_required
def logout_func(request):
    logout(request)
    return redirect('login')

@api_view(['GET', 'POST','PUT','DELETE'])
@authentication_classes((SessionAuthentication, BasicAuthentication,TokenAuthentication))
@permission_classes((IsAuthenticated,))
def add_college_api(request,*args,**kwargs):
    if request.method == 'GET':
        if kwargs:
            college = College.objects.get(**kwargs)
            serializer = ClassSerializer(college, many=False)
        else:
            college = College.objects.all()
            serializer = ClassSerializer(college,many=True)
        return Response(serializer.data,status = status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        college = College.objects.get(**kwargs)
        serializer = ClassSerializer(college, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        college = College.objects.get(**kwargs)
        college.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST','PUT','DELETE'])
@authentication_classes((SessionAuthentication, BasicAuthentication,TokenAuthentication))
@permission_classes((IsAuthenticated,))
def add_student_api(request,*args,**kwargs):
    if request.method == 'GET':
        if kwargs.get('stuid'):
            serializer = StudentDetailSerializer(Student.objects.get(id=kwargs['stuid']))
        else:
            serializer = StudentSerializer(Student.objects.filter(college=kwargs['id']),many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StudentDetailSerializer(data = request.data,context={**kwargs})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

    elif request.method == 'PUT':
        std = Student.objects.get(id=kwargs['stuid'])
        serializer = StudentDetailSerializer(instance=std,data=request.data,context={**kwargs})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

    elif request.method == 'DELETE':
        Student.objects.get(id = kwargs['stuid']).delete()
        return Response(status=204)
