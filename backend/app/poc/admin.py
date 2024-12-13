from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, AccountUserRole, Input, Log, Website
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("is_superadmin",)}),)

    list_display = (
        "username",
        "email",
        "is_superadmin",
        "is_staff",
        "is_superuser",
        "is_active",
    )


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
    )  # Affiche le nom du compte et le propriétaire dans la liste
    search_fields = (
        "name",
        "owner__username",
    )  # Permet de rechercher par nom de compte ou propriétaire


@admin.register(AccountUserRole)
class AccountUserRoleAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "account",
        "role",
    )  # Affiche l'utilisateur, le compte et le rôle
    list_filter = ("role",)  # Ajoute un filtre par rôle
    search_fields = (
        "user__username",
        "account__name",
    )  # Permet de rechercher par utilisateur ou nom de compte


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "url",
        "account",
        "is_whitelisted",
        "is_blacklisted",
        "is_sensitive",
    )
    list_filter = ("is_whitelisted", "is_blacklisted", "is_sensitive")
    search_fields = ("url",)


@admin.register(Input)
class InputAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "account",
        "user",
        "type",
        "value",
        "strength",
        "first_use",
        "number_of_uses",
    )
    list_filter = ("type", "strength")
    search_fields = ("value", "user__username")
    filter_horizontal = (
        "associated_websites",
    )  # Ajoute une interface pour gérer les relations avec les websites


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "account",
        "user",
        "input",
        "website",
        "timestamp",
        "ip_address",
        "is_suspicious",
    )
    list_filter = ("is_suspicious",)
    search_fields = ("ip_address", "user__username", "website__url")
    readonly_fields = (
        "timestamp",
    )  # Empêche la modification du timestamp dans l'admin
