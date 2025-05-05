# SoftDesk Support - API RESTful
## Conception de la mise en œuvre ##

Ce document fournit tous les détails nécessaires pour vous aider dans la réalisation de l’API RESTful pour SoftDesk Support. Il décrit la logique métier, les ressources, les fonctionnalités et les recommandations pour tester l'API.

## Objectif ## 
Développer une API RESTful permettant la gestion de projets, d'issues (problèmes) et de commentaires dans un environnement de collaboration.

Respecter les bonnes pratiques de sécurité et d'optimisation.

Assurer la conformité au RGPD pour la gestion des données utilisateurs.

1. Diagramme des Relations du Système de Suivi des Problèmes

Diagramme des ressources principales :

 - User → Utilisateur de l'application.

 - Contributor → Lien entre l'utilisateur et un projet.

 - Project → Un projet contenant plusieurs issues (problèmes).

 - Issue → Problème ou tâche à résoudre dans un projet.

 - Comment → Commentaire attaché à un problème.

2. Définition des Ressources

**User**

 - Attributs :

     - username: Identifiant unique de l'utilisateur.

     - age: Âge de l'utilisateur (vérifié pour le consentement).

     - can_be_contacted: Autorisation de contact (booléen).

     - can_data_be_shared: Autorisation de partage des données (booléen).

 - Sécurité : Authentification avec un JSON Web Token (JWT).

**Contributor**

 - Attributs :

     - Lien entre un utilisateur et un projet.

     - Un utilisateur peut être contributeur sur plusieurs projets, et un projet peut avoir plusieurs contributeurs.

**Project**

 - Attributs :

    - name: Nom du projet.

    - description: Description du projet.

    - type: Type de projet (back-end, front-end, iOS, Android).

- Un utilisateur peut créer un projet et en devenir l'auteur.

**Issue**

- Attributs :

    - title: Titre de l'issue.

    - description: Détail du problème.

    - assigned_to: Contributeur assigné à l'issue.

    - priority: Priorité de l'issue (LOW, MEDIUM, HIGH).

    - tag: Nature de l'issue (BUG, FEATURE, TASK).

    - status: Statut de l'issue (To Do, In Progress, Finished).

**Comment**

- Attributs :

     - text: Contenu du commentaire.

     - linked_to: Lien vers l'issue.

     - uuid: Identifiant unique du commentaire généré automatiquement.

3. Fonctionnalités Requises

**Gestion des Utilisateurs**

  - Authentification via username et password.

  - Retour d'un JSON Web Token (JWT) pour chaque utilisateur authentifié.

  - Vérification de l'âge pour les utilisateurs (doit avoir plus de 15 ans pour donner un consentement valide).

  - Gestion des préférences de confidentialité (can_be_contacted, can_data_be_shared).

**Gestion des Projets**

  - Un utilisateur peut créer un projet (l'initialisation du projet en tant qu'auteur et contributeur).

  - Le projet inclut un nom, une description et un type.

  - Seuls les contributeurs peuvent accéder à un projet et à ses ressources associées (issues et commentaires).

**Création des Tâches et Problèmes (Issues)**

  - Les contributeurs peuvent créer des issues liées à un projet.

  - Les issues comprennent un titre, une description, une priorité, un tag (bug, fonctionnalité, tâche), et un statut (To Do, In Progress, Finished).

  - Les issues peuvent être assignées à des contributeurs spécifiques.

**Création des Commentaires**

  - Les contributeurs peuvent ajouter des commentaires aux issues.

  - Les commentaires doivent être liés à une issue spécifique et peuvent être modifiés ou supprimés uniquement par leur auteur.

4. Exigences de Sécurité et Optimisation

**OWASP Top 10**

L'application doit respecter les recommandations de sécurité OWASP Top 10. Cela inclut :

  - Authentification avec JWT pour garantir l'identité de l'utilisateur.

  - Autorisation : Seuls les utilisateurs authentifiés et autorisés peuvent accéder ou modifier certaines ressources (projets, issues, commentaires).

  - Contrôles d'accès : Un utilisateur peut seulement modifier ou supprimer des ressources qu'il a créées.

**RGPD (Règlement Général sur la Protection des Données)**

  - Accès, rectification et suppression des données personnelles.

  - Droit à l'oubli : Les utilisateurs peuvent supprimer définitivement leurs données personnelles.

  - Consentement : Collecte du consentement explicite de l'utilisateur pour être contacté ou pour partager ses données.

  - Vérification de l'âge : Validation de l'âge de l'utilisateur (au moins 15 ans).

**Green Code**

L'application doit réduire son impact environnemental en optimisant les ressources du serveur :

  - Pagination des ressources pour éviter la surcharge du serveur.

  - Gestion optimisée des requêtes et des données en cache.

**5. Tester les Points de Terminaison de l'API**

Tous les points de terminaison doivent être testés avec des outils comme Postman, curl ou directement via le serveur localhost du Django REST Framework.

**Points à Tester**

  - Authentification des utilisateurs avec JWT.

  - Création, modification et suppression des projets, issues et commentaires.

  - Vérification des permissions d'accès pour les utilisateurs et les contributeurs.

6. Exigences de Sécurité

**Authentification et Autorisation**

  - JWT (JSON Web Token) pour authentifier les utilisateurs.

  - Utilisation de Django REST Framework avec les permissions appropriées pour garantir l'accès sécurisé aux ressources.

**Sécurisation des Dépendances**

  - Utilisation de Pipenv ou Poetry pour la gestion des dépendances Python, et mise à jour régulière des bibliothèques pour éviter les vulnérabilités.

7. Exemple d'Utilisation de l'API

**Authentification**
  - POST /auth/login : Authentifie un utilisateur et retourne un JWT.

 Exemple :

    json

    {
    "username": "user1",
    "password": "password123"
    }

**Création d'un Projet**

  - POST /projects : Crée un projet pour un utilisateur authentifié.

 Exemple :

    json

    {
      "name": "New Project",
      "description": "A detailed project description",
      "type": "back-end"
    }

**Création d'une Issue**

  - POST /projects/{project_id}/issues : Crée une issue dans un projet existant.

 Exemple :

    json

    {
      "title": "Bug in the login page",
      "description": "Details about the bug",
      "priority": "HIGH",
      "tag": "BUG",
      "status": "To Do"
    }

**Création d'un Commentaire**

  - POST /issues/{issue_id}/comments : Crée un commentaire pour une issue existante.

 Exemple :

    json

    {
      "text": "This issue needs immediate attention.",
      "linked_to": "12345"
    }

**Conclusion**

Ce **README** vous guide dans la conception et l'implémentation de l'API RESTful pour **SoftDesk Support**. Il couvre les ressources essentielles, les fonctionnalités, la gestion de la sécurité, et la conformité avec les normes comme le **RGPD** et **OWASP**. Assurez-vous de tester chaque point de terminaison pour garantir la sécurité et la performance de l'application.


