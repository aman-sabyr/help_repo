from datetime import date

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=2, max_length=20, required=True)
    password = serializers.CharField(min_length=6, max_length=20, required=True)
    password_confirm = serializers.CharField(min_length=6, max_length=20, required=True)

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('User with this is already exists')
        return username

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords are not similar')
        return data


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate_username(self, username):
        # checks if there is any user with this username
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError('User wasn\'t found')
        print(User.objects.get(username=username).password)
        return username

    def validate(self, data):
        # authentications
        request = self.context.get('request')
        username = data.get('username') # test_name
        password = data.get('password') # newpassword11
        if username and password:
            user = authenticate(username=username, password=password, request=request)
            print(user)
            if not user:
                raise serializers.ValidationError('Invalid password')
        else:
            raise serializers.ValidationError('You have to type you\'re mail and password')
        data['user'] = user
        return data


class UserInfoUpdateSerializer(serializers.Serializer):
    education = serializers.CharField(max_length=100, required=False)
    date_of_birth = serializers.DateField(default=None, format="%d-%m-%Y", input_formats=['%d-%m-%Y', 'iso-8601'], required=False)
    name = serializers.CharField(max_length=25, required=False)
    last_name = serializers.CharField(max_length=25, required=False)

    def calculate_age(self, date_of_birth):
        # calculate age by date of birth
        today = date.today()
        age_in_years = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        if age_in_years >= 100:
            return None
        if age_in_years >= 16:
            return age_in_years
        if age_in_years < 16:
            return age_in_years

    def to_internal_value(self, data):
        # checks if value is void
        if data.get('name', None) == '':
            data.pop('name')
        if data.get('last_name', None) == '':
            data.pop('last_name')
        if data.get('education', None) == '':
            data.pop('education')
        if data.get('date_of_birth', None) == '':
            data.pop('date_of_birth')
        return super().to_internal_value(data)

    def update(self, user, validated_data):
        # updates info of user
        for key, value in validated_data.items():
            setattr(user, key, value)
        user.save()
        return validated_data

    def validate_date_of_birth(self, date_of_birth):
        # validate age
        if self.calculate_age(date_of_birth) < 16:
            # if users age is lower than 16, makes his account nonactive
            request = self.context.get('request')
            user = request.user
            user.is_active = False
            user.save()
            raise serializers.ValidationError('You are too young!')
        elif self.calculate_age(date_of_birth) is None:
            raise serializers.ValidationError('Please enter correct date of birth')
        return date_of_birth

    def validate_name(self, name):
        # validate name and last name
        for char in name:
            if not (("A" <= char <= "Z") or ("a" <= char <= "z") or (char == " ")):
                return serializers.ValidationError('Name have to consist only with letters and first letter must be big')
        return name

    def validate_last_name(self, last_name):
        # validate last name
        return self.validate_name(last_name)

    def valiadte(self, data):
        # final validate and update
        request = self.context.get('request')
        user = request.user()
        return self.update(user, data)




