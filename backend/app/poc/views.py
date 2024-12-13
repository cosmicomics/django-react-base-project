from django.contrib.auth import get_user_model
from django.db.models import Count, Max, Avg, F, ExpressionWrapper, FloatField, Q
from django.db.models.functions import Now, Round
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Account, AccountUserRole, Log, Website, Input
from .serializers import (
    UserSerializer,
    AccountSerializer,
    UserRoleSerializer,
    WebsiteSerializer,
    ExtendedWebsiteSerializer,
    InputSerializer,
    ExtendedInputSerializer,
    LogSerializer,
)
from .permissions import IsSuperAdmin, IsAdmin
from datetime import datetime, timedelta


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperAdmin]


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAdmin]

    # Action personnalisée pour retourner les utilisateurs d'un compte
    @action(detail=True, methods=["get"], url_path="users")
    def get_account_users(self, request, pk=None):
        account = self.get_object()  # Récupérer l'instance du compte via l'ID
        # Obtenir tous les utilisateurs associés à ce compte via AccountUserRole
        users = get_user_model().objects.filter(accountuserrole__account=account)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    # Action personnalisée pour retourner les inputs d'un compte
    @action(detail=True, methods=["get"], url_path="inputs")
    def get_account_inputs(self, request, pk=None):
        account = self.get_object()  # Récupérer l'instance du compte via l'ID
        # Obtenir tous les inputs associés à ce compte
        inputs = Input.objects.filter(account=account).annotate(
            age_in_days=ExpressionWrapper(
                Round(
                    (Now() - F("first_use")) / (86400 * 1000000)
                ),  # Diviser par 86400 pour obtenir l'âge en jours
                output_field=FloatField(),
            ),
            total_sites=Count("associated_websites", distinct=True),
            has_suspicious_log=Count(
                "log__is_suspicious", filter=Q(log__is_suspicious=True)
            ),
            last_used_date=Max("log__timestamp"),
            usage_frequency=ExpressionWrapper(
                F("number_of_uses")
                / (
                    Round((Now() - F("first_use")) / (86400 * 1000000)) + 1
                ),  # Diviser par 86400 pour obtenir la fréquence en jours
                output_field=FloatField(),
            ),
        )
        serializer = ExtendedInputSerializer(inputs, many=True)
        return Response(serializer.data)

    # Action personnalisée pour retourner les websites d'un compte
    @action(detail=True, methods=["get"], url_path="websites")
    def get_account_websites_metrics(self, request, pk=None):
        account = self.get_object()
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        # Convertir les dates en format datetime
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        else:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")

        if not end_date:
            end_date = datetime.now()
        else:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

        # Calcul de la durée de la période en jours
        period_in_days = (end_date - start_date).days or 1

        # Liste des valeurs de mots de passe réutilisés
        reused_passwords = (
            Input.objects.filter(account=account)
            .values("value")
            .annotate(count=Count("id"))
            .filter(count__gt=1)
            .values_list("value", flat=True)
        )

        # Calculs des annotations pour chaque site associé à l'account
        websites = Website.objects.filter(account=account).annotate(
            # Nombre total de saisies pendant la période
            total_entries=Count(
                "log", filter=Q(log__timestamp__range=(start_date, end_date))
            ),
            # Nombre moyen de saisies par jour pendant la période
            avg_entries_per_day=ExpressionWrapper(
                Count("log", filter=Q(log__timestamp__range=(start_date, end_date)))
                / period_in_days,
                output_field=FloatField(),
            ),
            user_count=Count("input__user", distinct=True),
            id_password_count=Count("input__value", distinct=True),
            # Moyenne de `number_of_uses` pour chaque input lié au site
            avg_entry_frequency=Avg("input__number_of_uses"),
            # Nombre de mots de passe réutilisés
            reused_password_count=Count(
                "input", filter=Q(input__value__in=reused_passwords), distinct=True
            ),
            # Nombre de logs suspects pour chaque site
            suspicious_alerts=Count("log", filter=Q(log__is_suspicious=True)),
        )

        serializer = ExtendedWebsiteSerializer(websites, many=True)
        return Response(serializer.data)


class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = AccountUserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsSuperAdmin]


"""
Vues spécifiques
"""


class WebsiteViewSet(viewsets.ModelViewSet):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer


class InputViewSet(viewsets.ModelViewSet):
    queryset = Input.objects.all()
    serializer_class = InputSerializer

    def get_queryset(self):
        account_id = self.kwargs.get(
            "account_id"
        )  # Récupère l'ID du compte depuis l'URL
        current_date = datetime.now()
        queryset = Input.objects.filter(account_id=account_id).annotate(
            age_in_days=ExpressionWrapper(
                (Now() - F("first_use"))
                / 86400,  # Diviser par 86400 pour obtenir l'âge en jours
                output_field=FloatField(),
            ),
            total_sites=Count("associated_websites", distinct=True),
            has_suspicious_log=Count(
                "log__is_suspicious", filter=Q(log__is_suspicious=True)
            ),
            last_used_date=Max("log__timestamp"),
            usage_frequency=ExpressionWrapper(
                F("number_of_uses")
                / (Now() - F("first_use"))
                / 86400,  # Diviser par 86400 pour obtenir la fréquence en jours
                output_field=FloatField(),
            ),
        )
        return queryset


class LogViewSet(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
