from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string


def envoyer_email_bienvenue(user):
    subject = "Bienvenue sur notre plateforme"
    message = f"Bonjour {user.first_name}, merci de rejoindre notre plateforme !"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)


def envoyer_email_mise_a_jour_email(user):
    subject = "Votre adresse e-mail a été mise à jour"
    message = f"Bonjour {user.first_name},\n\nVotre adresse e-mail a été modifiée dans notre système."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)


def envoyer_email_html(user):
    subject = "Votre adresse e-mail a été mise à jour"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    # Créer le message texte brut
    text_content = f"Bonjour {user.first_name},\n\nVotre adresse e-mail a été modifiée dans notre système."

    # Créer le message HTML
    html_content = render_to_string("emails/email_update.html", {"user": user})

    # Envoyer l'email avec texte brut et HTML
    email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    email.attach_alternative(html_content, "text/html")
    email.send()
