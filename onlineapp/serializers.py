from rest_framework import serializers
from onlineapp.models import *

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ('id','name','location','acronym','contact')

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id','name','dob','email','db_folder','dropped_out','college')

class MockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MockTest1
        fields = ('problem1','problem2','problem3','problem4','total')

class StudentDetailSerializer(serializers.ModelSerializer):
    mocktest1 = MockSerializer()
    class Meta:
        model = Student
        fields = ('name','dob','email','db_folder','dropped_out','mocktest1')
    def create(self, validated_data):
        m1 = validated_data.pop('mocktest1')
        student = Student(**validated_data)
        student.college_id = self.context["id"]
        student.save()
        MockTest1.objects.create(student = student,**m1)
        return student

    def update(self, instance, validated_data):
        mocktest1_data = validated_data.pop('mocktest1')
        mocktest1 = instance.mocktest1
        instance.name = validated_data.get('name',instance.name)
        instance.dob = validated_data.get('dob',instance.dob)
        instance.email = validated_data.get('email',instance.email)
        instance.db_folder = validated_data.get('db_folder',instance.db_folder)
        instance.save()
        mocktest1.problem1 = mocktest1_data.get('problem1',mocktest1.problem1)
        mocktest1.problem2 = mocktest1_data.get('problem2', mocktest1.problem2)
        mocktest1.problem3 = mocktest1_data.get('problem3', mocktest1.problem3)
        mocktest1.problem4 = mocktest1_data.get('problem4', mocktest1.problem4)
        mocktest1.total = mocktest1_data.get('total',mocktest1.total)
        mocktest1.save()
        return instance