from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = User.objects.get(email=email)
        if not user:
            raise serializers.ValidationError("User does not exist")
        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password")

        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(
            email=validated_data['email'],
        )
        if password is not None:
            user.set_password(password)
        user.save()

        return user

    def update(self, instance, validated_data):
        email = validated_data.get('email', instance.email)
        username = validated_data.get('username', instance.username)
        password = validated_data.get('password', None)

        if password:
            instance.set_password(password)

        instance.email = email
        instance.username = username
        instance.save()
        return instance


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, data):
        refresh_token_str = data.get('refresh_token')
        try:
            refresh = RefreshToken(refresh_token_str)
            refresh.verify()
        except Exception as e:
            raise serializers.ValidationError("Invalid refresh token")

        payload = refresh.payload
        user_id = payload.get('user_id')
        if not user_id:
            raise serializers.ValidationError("В токене отсутствует user_id")
        try:
            user = User.objects.get(id=user_id)
            user.refresh_token = ""
            user.save()
            refresh.blacklist()
            data['logout'] = True
            return data
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")


class TokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, data):
        refresh_token_str = data.get('refresh_token')
        try:
            refresh = RefreshToken(refresh_token_str)
            refresh.verify()
        except Exception as e:
            raise serializers.ValidationError("Invalid refresh token")

        payload = refresh.payload
        user_id = payload.get('user_id')
        if not user_id:
            raise serializers.ValidationError("В токене отсутствует user_id")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")

        access_token = str(refresh.access_token)
        data['access_token'] = access_token
        return data
