from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model
from datetime import date

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', "password", 'date_of_birth', 'email', 'can_be_contacted', 'can_data_be_shared']
        extra_kwargs = {
            'password': {'write_only': True}  # Cache le password lors des réponses
        }

    def validate_date_of_birth(self, value):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 15:
            raise serializers.ValidationError("Vous ne pouvez pas vous inscrire si vous avez moins de 15 ans.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)  # Utilise le model du serializer
        if password:
            user.set_password(password)  # Hash le password
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user