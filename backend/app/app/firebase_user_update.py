from django.contrib.auth import get_user_model


def update_user_from_firebase(decoded_token):
    """
    Met à jour les informations d'un utilisateur Django à partir des données Firebase si elles diffèrent.
    """
    email = decoded_token.get("email")
    firebase_first_name = (
        decoded_token.get("name", "").split()[0] if decoded_token.get("name") else ""
    )
    firebase_last_name = (
        decoded_token.get("name", "").split()[1] if decoded_token.get("name") else ""
    )

    # Récupère ou crée l'utilisateur Django correspondant à cet email
    user, created = get_user_model().objects.get_or_create(
        username=email,
        defaults={
            "email": email,
            "first_name": firebase_first_name,
            "last_name": firebase_last_name,
        },
    )

    # Vérifie si les données Firebase sont différentes des données Django
    update_needed = False

    if user.email != email:
        user.email = email
        update_needed = True

    if user.first_name != firebase_first_name:
        user.first_name = firebase_first_name
        update_needed = True

    if user.last_name != firebase_last_name:
        user.last_name = firebase_last_name
        update_needed = True

    # Met à jour l'utilisateur seulement si nécessaire
    if update_needed:
        user.save()

    return user
