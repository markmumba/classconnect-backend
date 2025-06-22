from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import CustomUser, SubSchool


class SubSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model= SubSchool
        fields =('id','name')

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, validators=[validate_password])

    sub_school = serializers.PrimaryKeyRelatedField(queryset=SubSchool.objects.all())

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name',
                  'quote', 'school', 'career_path')

    def validate(self, attrs):
        email = attrs['email']
        if not email.endswith(f'@riarauniveristy.ac.ke'):
            raise serializers.ValidationError(
                "Email is not Associated with school")
        return attrs


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
    sub_school = SubSchoolSerializer(read_only=True)
    full_name = serializers.CharField(source='full_name',read_only=True)
    school_name = serializers.CharField(source='school.name')
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name','school_name', 'quote','full_name', 'picture', 'date_joined', 'career_path',)
        read_only_fields = ('id', 'email', 'date_joined')


class UserListSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name')
    class Meta:
        model = CustomUser
        fields = ('id','email','first_name','last_name','school_name')