from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions
from .serializers import UserSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les utilisateurs.
    Fournit les actions CRUD sur le modèle User personnalisé.
    Restreint l'accès aux utilisateurs authentifiés.
    """
    queryset = get_user_model().objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Crée un nouvel utilisateur avec gestion personnalisée des erreurs de validation.
        Si la validation échoue, retourne un message d'erreur spécifique lié à la date de naissance
        dans la réponse JSON, avec le même contenu que les données envoyées.
        En cas de succès, retourne les données de l'utilisateur avec un message de confirmation.
        """
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            # Construit une réponse avec les mêmes champs, mais un message d’erreur
            data = request.data.copy()
            data["message"] = e.detail.get("date_of_birth", ["Erreur inconnue"])[0]
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        data["message"] = "Votre compte a été créé avec succès ! 🎉"
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)



    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if user != request.user:
            return Response({"Message": "Vous n'avez pas le droit de modifier ce compte."}, status=403)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user != request.user:
            return Response({"Message": "Vous n'avez pas le droit de supprimer ce compte."}, status=403)
        return super().destroy(request, *args, **kwargs)






