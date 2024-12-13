import firebase_admin
from firebase_admin import credentials, auth
from django.conf import settings
from django.http import JsonResponse
from .firebase_user_mapping import get_or_create_user_from_firebase

# Initialisation de Firebase avec les bonnes informations d'identification
if not firebase_admin._apps:  # Vérifie si Firebase n'a pas déjà été initialisé
    cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT_KEY)
    firebase_admin.initialize_app(cred)


class FirebaseAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            token = auth_header.split("Bearer ")[-1]
            try:

                decoded_token = auth.verify_id_token(token)

                request.user = get_or_create_user_from_firebase(decoded_token)
            except Exception as e:
                print("exception", e)  # Tu peux garder cela pour le débogage
                return JsonResponse({"error": "Invalid token"}, status=401)

        response = self.get_response(request)
        return response
