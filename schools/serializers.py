from rest_framework import serializers

from .models import School, SubSchool



class SubSchoolSerializer(serializers.ModelSerializer):

    school_name=serializers.CharField(source='school.name',read_only=True)

    class Meta:
        model =SubSchool
        fields =['id','name','description','school','school_name','is_active']


class SubSchoolCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model=SubSchool
        fields =['name','description']

    def validate(self, attrs):

        request = self.context.get('request')
        if not request or not request.user:
            return attrs

        if request.user.is_superuser:
            school_id = request.data.get('school')
            if not school_id:
                raise serializers.ValidationError({'school': 'School is required'})
            try:
                school = School.objects.get(id=school_id)
            except School.DoesNotExist:
                raise serializers.ValidationError({'school': 'Invalid school'})
        else:
            school = request.user.school
            if not school:
                raise serializers.ValidationError({'error': 'User must belong to a school'})

        name = attrs.get('name')
        if name:
            existing = SubSchool.objects.filter(school=school, name=name)
            if existing.exists():
                raise serializers.ValidationError({
                    'name': f'Department "{name}" already exists in {school.name}'
                })

        return attrs


class SubSchoolListSerializer(serializers.ModelSerializer):
    class Meta:
        model= SubSchool
        fields =['id','name']


class SchoolSerializer(serializers.ModelSerializer):

    full_email_domain = serializers.ReadOnlyField()
    user_count = serializers.SerializerMethodField()
    department_count = serializers.SerializerMethodField()
    departments=SubSchoolListSerializer(many=True,read_only=True)

    class Meta:
        model = School
        fields = [
            'id','name','email_domain','full_email_domain',
            'location','phone','logo','is_active','user_count','departments',
            'department_count','created_at','updated_at'
        ]
        read_only_fields=['created_at','updated_at']

    def get_user_count(self,obj):
        return obj.users.filter(is_active=True).count()

    def get_department_count(self,obj):
        return obj.departments.filter(is_active=True).count()

    def validate_email_domain(self, value):
        value = value.lstrip('@')  
        if not '.' in value:
            raise serializers.ValidationError("Enter a valid domain (e.g., university.edu)")
        return value


class SchoolCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ['name','email_domain','location','phone','logo']

class SchoolListSerializer(serializers.ModelSerializer):

    full_email_domain = serializers.ReadOnlyField()
    
    class Meta:
        model = School
        fields = ['id', 'name', 'full_email_domain']










