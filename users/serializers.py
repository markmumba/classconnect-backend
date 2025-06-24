from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from schools.serializers import SubSchoolSerializer

from .models import CustomUser
from schools.models import School,SubSchool




class UserRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, validators=[validate_password])
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.filter(is_active=True))
    sub_school = serializers.PrimaryKeyRelatedField(queryset=SubSchool.objects.all(),required=False,allow_null=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name','password','sub_school','major','school_id',
                  'quote', 'school', 'career_path','picture')

    def validate_email(self,value):
        domain = value.split('@')[1] if '@' in value else None
        if not domain:
            raise serializers.ValidationError("Invalid email format")
        return value

    def validate(self, attrs):
        email=attrs['email']
        school=attrs['school']

        email_domain = email.split('@')[1] if '@' in email else None
        if email_domain != school.email_domain:
            raise serializers.ValidationError({
                "email":f"Email domain must be {school.email_domain} for {school.name}"
            })

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            **validated_data,
            role='student',
            is_active=True
        )
        return user



class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get(
                'request'), username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(
                'Must include email and password')


class UserProfileSerializer(serializers.ModelSerializer):
    sub_school = serializers.CharField(source='sub_school.name',read_only=True)
    full_name = serializers.CharField(read_only=True)
    school_id = serializers.PrimaryKeyRelatedField(queryset=School.objects.all(),required=False,allow_null=True)
    school_name = serializers.CharField(source='school.name',read_only=True)
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name','school_id','school_name','graduation_year', 'quote','full_name', 'picture', 'date_joined', 'career_path','sub_school')
        read_only_fields = ('id', 'email', 'date_joined')


class UserListSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name')
    class Meta:
        model = CustomUser
        fields = ('id','email','first_name','last_name','school_name')