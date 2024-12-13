from django.contrib.auth import get_user_model


def get_or_create_user_from_firebase(decoded_token):
    email = decoded_token.get("email")
    user, created = get_user_model().objects.get_or_create(
        username=email,
        defaults={
            "email": email,
            "first_name": decoded_token.get("name", ""),
        },
    )
    return user
