from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Account, AccountUserRole, Log, Input, Website


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "first_name", "last_name"]


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "name", "owner"]


class UserRoleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    account = AccountSerializer(read_only=True)
    role = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = AccountUserRole
        fields = ["id", "user", "account", "role"]


"""
Serializers spécifiques
"""


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = [
            "id",
            "account",
            "url",
            "is_whitelisted",
            "is_blacklisted",
            "is_sensitive",
        ]


class ExtendedWebsiteSerializer(serializers.ModelSerializer):
    total_entries = serializers.IntegerField(read_only=True)
    avg_entries_per_day = serializers.FloatField(read_only=True)
    user_count = serializers.IntegerField(read_only=True)
    id_password_count = serializers.IntegerField(read_only=True)
    avg_entry_frequency = serializers.FloatField(read_only=True)
    reused_password_count = serializers.IntegerField(read_only=True)
    suspicious_alerts = serializers.IntegerField(read_only=True)

    class Meta:
        model = Website
        fields = [
            "id",
            "account",
            "url",
            "is_whitelisted",
            "is_blacklisted",
            "is_sensitive",
            "total_entries",
            "avg_entries_per_day",
            "user_count",
            "id_password_count",
            "avg_entry_frequency",
            "reused_password_count",
            "suspicious_alerts",
        ]


class InputSerializer(serializers.ModelSerializer):
    associated_websites = WebsiteSerializer(many=True, read_only=True)

    class Meta:
        model = Input
        fields = [
            "id",
            "account",
            "user",
            "type",
            "value",
            "strength",
            "first_use",
            "number_of_uses",
            "associated_websites",
        ]
        read_only_fields = ["first_use"]


class LogSerializer(serializers.ModelSerializer):
    input = InputSerializer(read_only=True)
    website = WebsiteSerializer(read_only=True)

    class Meta:
        model = Log
        fields = [
            "id",
            "account",
            "timestamp",
            "user",
            "input",
            "website",
            "ip_address",
            "is_suspicious",
        ]
        read_only_fields = ["timestamp"]


class ExtendedInputSerializer(serializers.ModelSerializer):
    associated_websites = WebsiteSerializer(many=True, read_only=True)
    age_in_days = serializers.FloatField(read_only=True)
    total_sites = serializers.IntegerField(read_only=True)
    has_suspicious_log = serializers.IntegerField(read_only=True)
    last_used_date = serializers.DateTimeField(read_only=True)
    usage_frequency = serializers.FloatField(read_only=True)

    class Meta:
        model = Input
        fields = [
            "id",
            "value",
            "age_in_days",
            "strength",
            "total_sites",
            "has_suspicious_log",
            "number_of_uses",
            "usage_frequency",
            "last_used_date",
            "user",
            "associated_websites",
        ]
