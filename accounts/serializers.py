from rest_framework import serializers, exceptions, status
from django.contrib.auth import get_user_model, authenticate

from util.messages.response_SMS import send_sms_notification

User = get_user_model()


class AuthSerializer(serializers.ModelSerializer):
    confirm_pass = serializers.CharField(style={input: 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'phone', 'password', 'confirm_pass',
                  'is_active', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['id', 'is_active', 'date_joined']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        confirm_pass = validated_data.pop('confirm_pass', None)

        if password is not None and confirm_pass is not None:
            if password != confirm_pass:
                raise exceptions.AuthenticationFailed('Passwords must match.', "password_mismatch", )

            try:
                check_user = User.objects.get(email=validated_data['email'])
                if check_user:
                    raise serializers.ValidationError({'success': 0, "code": status.HTTP_400_BAD_REQUEST,
                                                       'message': 'Customer with the details exists.'})
            except User.DoesNotExist:
                user = self.Meta.model.objects.create_user(**validated_data)
                user.set_password(password)
                user.save()
                message = f'Dear {user.get_full_name()} , Thank you for joining us.'
                send_sms_notification(message, user.phone)
                return user

    def update(self, instance, validated_data):
        """Update the Customer profile """
        updated_field = [k for k in validated_data]
        for key, value in validated_data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        instance.save(update_fields=updated_field)


class ClientSerializer(serializers.Serializer):
    client_id = serializers.CharField(required=True, write_only=True)
    client_secret = serializers.CharField(required=True, write_only=True)


class ObtainTokenSerializer(ClientSerializer):
    callback_url = serializers.CharField(required=True, write_only=True)
    verification_code = serializers.CharField(required=True, write_only=True)


class RefreshTokenSerializer(ClientSerializer):
    refresh_token = serializers.CharField(write_only=True, required=True)
