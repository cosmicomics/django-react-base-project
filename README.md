
# Base de projet Django & React

## Backend Django

Les dépendances pip sont :
- django
- djangorestframework
-  django-cors-headers
-  firebase-admin


Dans le dossier **backend** :

- activer l'environnement virtuel en exécutant
 `source venv/bin/activate`
 
- effectuer les migrations du model de données
 `python manage.py makemigrations`
`python manage.py migrate`

- lancer le serveur
`python manage.py runserver`

Pour ajouter un super user : 
`python manage.py createsuperuser`

Les dépendances python peuvent être freezées en exécutant :
`pip freeze > requirements.txt`

Les User Django et Firebase sont liés par leur email.
Une requête dont le jeton d'authentification est validé par Firebase engendre la création d'un nouveau User Djangon, si aucun User ne correspond à l'email de l'utilisateur retourné par Firebase.

Les modèles incluent :

- le modèle `User` par défaut de Django
- un modèle `Account`, qui correspond à un compte détenu par un User
- un modèle `AccountUserRole`, qui permet de lier un `User` à un `Account` en lui assignant un rôle

Les rôles proposés sont :

- Super Admin (accès à toutes les ressources - administrateur de l'app)
- Admin (accès aux ressources d'un compte - utilisateur de l'app, détenteur d'un compte, B2B)
- User (accès aux ressources qu'il détient - utilisateur de l'app, géré par un admin, B2C)

### Sécurité
En contexte de développement, les clés d'accès Firebase utilisées dans `app/app/firebase.py` sont `situées dans app/firebase-service-account.json`
**En production, ce fichier doit être stocké de manière sécurisée et son chemin doit être renseigné dans une variable d'environnement.**
La variable d'environnement `FIREBASE_SERVICE_ACCOUNT_KEY` est récupérée dans `app/settings.py`.
Si `FIREBASE_SERVICE_ACCOUNT_KEY` n'est pas définie, la variable est initialisée à `app/firebase-service-account.json`
