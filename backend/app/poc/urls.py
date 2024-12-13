from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import (
    UserViewSet,
    AccountViewSet,
    UserRoleViewSet,
    WebsiteViewSet,
    InputViewSet,
    LogViewSet,
)


router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"accounts", AccountViewSet)
router.register(r"user-roles", UserRoleViewSet)

"""
Routes spécifiques
"""

router.register(r"websites", WebsiteViewSet)
router.register(r"inputs", InputViewSet)
router.register(r"logs", LogViewSet)

# Routeur imbriqué pour les inputs associés à un account spécifique
accounts_router = NestedDefaultRouter(router, r"accounts", lookup="account")
accounts_router.register(r"inputs", InputViewSet, basename="account-inputs")

urlpatterns = [
    path("", include(router.urls)),
    # path("", include(accounts_router.urls)),  # Inclure les routes imbriquées
]
