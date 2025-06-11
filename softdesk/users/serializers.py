from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model
from datetime import date

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle User personnalisé.
    Gère la sérialisation/désérialisation des utilisateurs avec gestion sécurisée du mot de passe.
    Valide que l'utilisateur ait au moins 15 ans lors de la création ou mise à jour.
    """

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', "password", 'date_of_birth', 'email', 'can_be_contacted', 'can_data_be_shared']
        extra_kwargs = {
            'password': {'write_only': True}  # Cache le password lors des réponses
        }

    def validate_date_of_birth(self, value):

        """
        Valide la date de naissance pour s'assurer que l'utilisateur a au moins 15 ans.
        Lève une ValidationError si l'âge est inférieur à 15 ans.
        """



        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 15:
            raise serializers.ValidationError("Vous ne pouvez pas vous inscrire si vous avez moins de 15 ans.")
        return value

    def create(self, validated_data):

        """
        Crée un nouvel utilisateur à partir des données validées.
        - Extrait le mot de passe pour le hacher correctement.
        - Crée l'utilisateur avec le mot de passe sécurisé.
        """


        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)  # Utilise le model du serializer
        if password:
            user.set_password(password)  # Hash le password
        user.save()
        return user

    def update(self, instance, validated_data):

        """
        Met à jour un utilisateur existant.
        - Permet la mise à jour du mot de passe en le hachant correctement.
        """

        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user