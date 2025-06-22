from django.core.serializers import serialize
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from users.serializers import UserListSerializer

from .models import School, SubSchool
from .permissions import IsSchoolAdminOrReadOnly
from .serializers import (SchoolCreateSerializer, SchoolListSerializer,
                          SchoolSerializer, SubSchoolCreateSerializer,
                          SubSchoolSerializer)


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
            raise permissions.PermissionDenied("Only super admins can create schools")
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
            raise permissions.PermissionDenied("Only super admins can toggle school status")

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
            return SubSchool.objects.all()
        elif getattr(self.request.user, 'school',None):
            return SubSchool.objects.filter(school=self.request.user.school,is_active=True)
        else:
            return SubSchool.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return SubSchoolCreateSerializer
        return SubSchoolSerializer

    def perform_create(self, serializer):
        if self.request.user.is_superuser:
            if 'school' not in self.request.data:
                raise serializers.ValidationError({'school':'School is required'})
        else :
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

    @action(detail=False, methods=['get'])
    def by_domain(self,request):
        domain = request.query_params.get('domain')
        if not domain:
            return Response ({'error':'Domain parameter is required'},
                             status=status.HTTP_400_BAD_REQUEST)
        domain = domain.lstrip('@')

        try :
            school = School.objects.get(email_domain=domain,is_active=True)
            serializer = SchoolListSerializer(school)
            return Response(serializer.data)
        except School.DoesNotExist:
            return Response({'error':f'No school found for domain: {domain}'},status=status.HTTP_400_BAD_REQUEST)








