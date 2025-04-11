from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.timezone import now
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'groups': {'required': False},  # Handle groups manually
            'user_permissions': {'required': False}  # Handle user_permissions manually
        }

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', None)  # Pop groups
        user_permissions_data = validated_data.pop('user_permissions', None)  # Pop user_permissions
        validated_data['is_active'] = False
        # Create user without groups and permissions for now
        user = User(**validated_data)
        password = validated_data.pop('password', None)
        
        if password:
            user.set_password(password)  # Set hashed password
        user.save()

        # Set groups if present
        if groups_data:
            user.groups.set(groups_data)

        # Set user_permissions if present
        if user_permissions_data:
            user.user_permissions.set(user_permissions_data)

        return user

    def update(self, instance, validated_data):
        groups_data = validated_data.pop('groups', None)  # Pop groups
        user_permissions_data = validated_data.pop('user_permissions', None)  # Pop user_permissions
        password = validated_data.pop('password', None)
        
        # Update other fields
        instance = super().update(instance, validated_data)
        
        if password:
            instance.set_password(password)  # Update hashed password
            instance.save()

        # Update groups if present
        if groups_data is not None:
            instance.groups.set(groups_data)

        # Update user_permissions if present
        if user_permissions_data is not None:
            instance.user_permissions.set(user_permissions_data)

        return instance
    
class SendOTPSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate_username(self, value):
        """Ensure the user exists before sending OTP."""
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError("User not found.")
        return value


class VerifyOTPSerializer(serializers.Serializer):
    username = serializers.CharField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        """Check if OTP is valid before verification."""
        try:
            user = User.objects.get(username=data["username"])
            if not user.otp or not user.otp_expiry or now() > user.otp_expiry:
                raise serializers.ValidationError("OTP expired or not generated.")
            if user.otp != data["otp"]:
                raise serializers.ValidationError("Invalid OTP.")
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")
        return data