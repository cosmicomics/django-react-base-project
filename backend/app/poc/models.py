from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class CustomUser(AbstractUser):
    is_superadmin = models.BooleanField(default=False)


class Account(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_accounts",
    )

    def __str__(self):
        return self.name


class AccountUserRole(models.Model):
    USER_ROLES = (
        ("superadmin", "Super Admin"),
        ("admin", "Admin"),
        ("user", "User"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES)

    class Meta:
        unique_together = ("user", "account")


"""
Modèles spécifiques
"""


class Website(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    url = models.CharField(max_length=512)
    is_whitelisted = models.BooleanField(default=False)
    is_blacklisted = models.BooleanField(default=False)
    is_sensitive = models.BooleanField(default=False)


class Input(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=512)
    value = models.CharField(max_length=512)
    strength = models.IntegerField()
    first_use = models.DateTimeField(auto_now_add=True)
    number_of_uses = models.IntegerField()
    associated_websites = models.ManyToManyField(Website)


class Log(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    input = models.ForeignKey(Input, on_delete=models.CASCADE)
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    is_suspicious = models.BooleanField(default=False)


class Alert(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    data = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
