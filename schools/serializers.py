from rest_framework import serializers

from .models import School, SubSchool


class SchoolSerializer(serializers.ModelSerializer):

    full_email_domain = serializers.ReadOnlyField()
    user_count = serializers.SerializerMethodField()
    department_Count = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = [
            'id','name','email_domain','full_email_domain',
            'location','phone','logo','is_active',
            'subscription_type','max_users','user_count',
            'department_count','created_at','update_at'
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
        fields = ['id', 'name', 'full_email_domain', 'location', 'is_active']

class SubSchoolSerializer(serializers.ModelSerializer):

    school_name=serializers.CharField(source='school.name',read_only=True)

    class Meta:
        model =SubSchool
        fields =['id','name','description','school','school_name','is_active']

    def validate(self,attrs):
        school= attrs['school']
        name =attrs.get('name')

        if school and name:
            existing = SubSchool.objects.filter(school=school,name=name)
            if self.instance :
                existing = existing.exclude(pk=self.instance.pk)

        if existing.exists():
            raise serializers.ValidationError({
                'name':f'Department "{name}" already exists in {school.name}'
            })
        return attrs

class SubSchoolCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model=SubSchool 
        fields =['name','description']










