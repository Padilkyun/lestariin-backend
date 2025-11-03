from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Profile, Report

class UserSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'first_name', 'last_name', 'is_admin', 'points']

    def get_is_admin(self, obj):
        return obj.is_staff or obj.is_superuser

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    is_admin = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'first_name', 'last_name', 'is_admin', 'password']

    def create(self, validated_data):
        is_admin = validated_data.pop('is_admin', False)
        user = User.objects.create_user(
            username=validated_data['email'],  # Use email as username
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        if is_admin:
            user.is_staff = True
            user.is_superuser = True
            user.save()
        Profile.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError('User account is disabled.')
            else:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include email and password.')
        return data

class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                if user.is_active:
                    if user.is_staff or user.is_superuser:
                        data['user'] = user
                    else:
                        raise serializers.ValidationError('User is not an admin.')
                else:
                    raise serializers.ValidationError('User account is disabled.')
            else:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include email and password.')
        return data

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                if user.is_active:
                    if not user.is_staff and not user.is_superuser:
                        data['user'] = user
                    else:
                        raise serializers.ValidationError('Admin users cannot login via this endpoint.')
                else:
                    raise serializers.ValidationError('User account is disabled.')
            else:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include email and password.')
        return data

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    photo = serializers.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['user', 'bio', 'photo', 'created_at', 'updated_at']

class ChatbotSerializer(serializers.Serializer):
    message = serializers.CharField()

class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'points']

class ReportSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)
    description = serializers.CharField(required=True)
    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)

    def get_image_url(self, obj):
        if obj.image and obj.image.name:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    class Meta:
        model = Report
        fields = ['id', 'image', 'image_url', 'user', 'description', 'latitude', 'longitude', 'water_classification', 'forest_classification', 'public_fire_classification', 'trash_classification', 'illegal_logging_classification', 'verified', 'created_at', 'updated_at']
        read_only_fields = ['id', 'water_classification', 'forest_classification', 'public_fire_classification', 'trash_classification', 'illegal_logging_classification', 'verified', 'created_at', 'updated_at']
        extra_kwargs = {'image': {'write_only': True}}
