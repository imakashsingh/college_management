import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'classproject.settings')
django.setup()
from onlineapp.models import *
from django.db.models import *


#Query to retrieve all records from College
def retrieve_all_records_from_Colleges():
    c = College.objects.all()
    for x in c:
        print(x.name,x.location,x.acronym,x.contact)

#Query to retrieve number of colleges
def count_no_colleges():
    c= College.objects.all()
    print(len(c))

#Query to retrieve college acronym and contact
def print_loc_acrnym():
    """Method1
    c = College.objects.all()
    for x in c:
        print(x.location,x.acronym)"""

    #Method2
    val = College.objects.values('acronym','contact')
    for i in val:
        print(i['acronym'],i['contact'])

#Query to retrieve count number of colleges in a particular location
def numb_of_colg_in_location(locationn):

    x = College.objects.filter(location = locationn).count()
    print(x)

#Query to retrieve in sorted order of acronym
def sort_acronym():
    c= College.objects.order_by('acronym')
    for i in c:
        print(i.name,i.location,i.acronym,i.contact)

#Query to retrieve in sorted order of acronym in descending
def sort_acronym_desc():
    c= College.objects.order_by('-acronym')
    for i in c:
        print(i.name,i.location,i.acronym,i.contact)

#Query to retrieve top 5 records
def top_5():
    c = College.objects.order_by('acronym')[:5]
    for i in c:
        print(i.name, i.location, i.acronym, i.contact)

#Query to retrieve bottom 5 records in descending order
def bott5_in_desc():
    c = College.objects.order_by('-acronym')[:5]
    for i in c:
        print(i.name, i.location, i.acronym, i.contact)

#Query to retrieve no of colleges in all locations.
def no_of_colgs_in_all_loc():
    #Method 1
    """val = College.objects.all()
    d = {}
    for i in val:
        if i.location in d.keys():
            d[i.location]  += 1
        else:
            d[i.location] = 1
    for k,v in d.items():
        print(k,v)"""


    #Method2
    c = College.objects.all()
    c = c.values('location').annotate(cn = Count('location'))
    for i in c:
        print(i['location'],i['cn'])


#Query to sort the location based on number of colleges in descending order
def sort_based_on_loc_count():
    c = College.objects.all()
    c = c.values('location').annotate(cn=Count('location')).order_by('-cn')
    for i in c:
        print(i['location'], i['cn'])

#Query to print the college names with dropped out students
def col_with_dropped_out_students():
    c = Student.objects.filter(dropped_out = True).values('college__name').distinct()
    for i in c:
        print(i['college__name'])


#Query to print the no of students in a college
def no_of_students_in_college():
    c = Student.objects.all()
    c = c.values('college__name').annotate(cn = Count('college__name')).distinct().order_by('-cn')
    for i in c:
        print(i['college__name'],i['cn'])

#Query to print the no of students in a college excluding the dropped out students
def no_of_students_in_college_excluding_dropout():
    c = Student.objects.filter(dropped_out = False)
    c = c.values('college__name').annotate(cn=Count('college__name')).distinct().order_by('-cn')
    for i in c:
        print(i['college__name'],i['cn'])

#Query to print the no of students in a location
def no_of_students_in_location():
    c = Student.objects.all()
    c = c.values('college__location').annotate(cn = Count('college__location')).distinct().order_by('-cn')
    for i in c:
        print(i['college__location'],i['cn'])


#Query to print the no of students in a location excluding the dropped out students
def no_of_students_in_location_excluding_dropout():
    c = Student.objects.filter(dropped_out=False)
    c = c.values('college__location').annotate(cn = Count('college__location')).distinct().order_by('-cn')
    for i in c:
        print(i['college__location'],i['cn'])

#Query to get the location with maximum number of students
def loc_with_max_students():
    c = Student.objects.all()
    c = c.values('college__location').annotate(cn=Count('college__location')).distinct().order_by('-cn')[0]
    print(c['college__location'])

#Query to retrieve student name,total in mock test and acronym of college
def student_tot_acr():
    c = MockTest1.objects.all().values('student__name','student__college__acronym','total')
    for i in c:
        print(i['student__name'],i['student__college__acronym'],i['total'])

    """c = Student.objects.all().values('name','mocktest1__total','college__acronym')
    for i in c:
        print(i['name'],i['mocktest1__total'],i['college__acronym'])"""

#Query to retrieve student name,total in mock test and acronym of college for total > 30
def student_tot_acr_gt30():
    c = MockTest1.objects.all().values('student__name','student__college__acronym','total').filter(total__gt=30)
    for i in c:
        print(i['student__name'],i['student__college__acronym'],i['total'])

#Query to find the count of students who got more than 30
def student_marks_gt30():
    c = MockTest1.objects.filter(total__gt=30)

if __name__ == "__main__":
    student_tot_acr_gt30()