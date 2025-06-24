
from rest_framework import  permissions,serializers, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import PermissionDenied
from users.serializers import UserListSerializer

from .models import School, SubSchool
from .permissions import IsSchoolAdminOrReadOnly
from .serializers import (SchoolCreateSerializer, SchoolListSerializer,
                          SchoolSerializer, SubSchoolCreateSerializer,
                          SubSchoolSerializer, SubSchoolListSerializer)


class SchoolViewSet(viewsets.ModelViewSet): 
    queryset = School.objects.all()
    permission_classes =[IsSchoolAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return SchoolCreateSerializer
        elif self.action == 'list':
            return SchoolListSerializer
        return SchoolSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return School.objects.all()
        elif getattr(self.request.user,'school',None):
            return School.objects.filter(id=self.request.user.school.id)
        else:
            return School.objects.none()

    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            raise PermissionDenied("Only super admins can create schools")
        serializer.save()

    @action(detail=True,methods=['get'])
    def users(self,request,pk=None):
        school= self.get_object()
        users= school.users.filter(is_active=True)
        serializer = UserListSerializer(users,many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def departments(self,request,pk=None):
        school = self.get_object()
        departments = school.departments.filter(is_active=True)
        serializer = SubSchoolSerializer(departments, many=True)
        return Response(serializer.data)

    @action(detail=True,methods=['post'])
    def toggle_status(self,request,pk=None):
        if not request.user.is_superuser:
            raise PermissionDenied("Only super admins can toggle school status")

        school = self.get_object()
        school.is_active = not school.is_active
        school.save()

        return Response({
            'message': f'School {school.name} is now {"active" if school.is_active else "inactive"}',
            "is_active": school.is_active
        })





class SubSchoolViewSet(viewsets.ModelViewSet):
    serializer_class = SubSchoolSerializer
    permission_classes = [IsSchoolAdminOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return SubSchool.objects.all().select_related('school')
        elif getattr(self.request.user, 'school',None):
            return SubSchool.objects.filter(school=self.request.user.school,is_active=True).select_related('school')
        else:
            return SubSchool.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return SubSchoolCreateSerializer
        return SubSchoolSerializer

    def perform_create(self, serializer):
        if self.request.user.is_superuser:
            school_id = self.request.data.get('school')
            if not school_id:
                raise ValidationError({'school': 'School is required'})
            school = get_object_or_404(School, id=school_id)
            serializer.save(school=school)
        else:
            serializer.save(school=self.request.user.school)


    @action(detail=True,methods=['get'])
    def users(self,request,pk=None):
        department =self.get_object()
        users = department.users.filter(is_active=True)
        serializer = UserListSerializer(users,many=True)
        return Response(serializer.data)



class PublicSchoolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = School.objects.filter(is_active=True)
    serializer_class = SchoolListSerializer
    permission_classes = [permissions.AllowAny]

class PublicSubSchoolViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubSchoolListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        school_id = self.request.query_params.get('school_id')
        queryset = SubSchool.objects.filter(school_id=school_id, is_active=True).select_related('school')
        if not school_id:
            queryset=SubSchool.objects.none()

        return queryset









