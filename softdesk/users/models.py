from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Modèle personnalisé d'utilisateur étendant AbstractUser.
    Attributs supplémentaires :
    - can_be_contacted : Booléen indiquant si l'utilisateur accepte d'être contacté.
    - can_data_be_shared : Booléen indiquant si les données de l'utilisateur peuvent être partagées.
    - date_of_birth : Date de naissance de l'utilisateur (champ obligatoire).
    Méthodes :
    - is_minor() : indique si l'utilisateur est mineur (moins de 15 ans).
    """

    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=False, blank=False)

    def is_minor(self):
        """
        Calcule si l'utilisateur est mineur (moins de 15 ans).
        Retourne True si l'âge calculé à partir de la date de naissance est inférieur à 15 ans,
        sinon False.
        """

        from datetime import date
        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age < 15