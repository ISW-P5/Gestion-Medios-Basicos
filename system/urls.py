from django.urls import path, include
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework import routers

from .views import (index, admin, avatar, login_api, user_data_api, csrf_api, basic_medium_metadata,
                    responsible_ticket_metadata, responsible_metadata, basic_medium_without_certificate_metadata,
                    roles_metadata, generate_fixtures)
from .api import (UserViewSet, BasicMediumExpedientViewSet, RequestTicketViewSet,
                  MovementTicketViewSet, ResponsibilityCertificateViewSet)


# Incluyo el enrutador de los ViewSet declarados para el API
router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'basic_medium', BasicMediumExpedientViewSet)
router.register(r'request_ticket', RequestTicketViewSet)
router.register(r'movement_ticket', MovementTicketViewSet)
router.register(r'responsibility_certificate', ResponsibilityCertificateViewSet)

urlpatterns = [
    # Default System urls
    path('', index, name='index'),
    path('admin/', admin, name='dashboard'),

    # Authentication urls
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # API urls
    path('api/login/', login_api, name='api_login'),
    path('api/avatar/', avatar, name="avatar"),
    path('api/csrf/', csrf_api, name="csrf_api"),
    path('api/user/', user_data_api, name="user_data"),
    path('api/responsible/', responsible_metadata, name='responsible_list'),
    path('api/responsible_ticket/', responsible_ticket_metadata, name='responsible_ticket_list'),
    path('api/roles/', roles_metadata, name='roles_list'),
    path('api/mediums/', basic_medium_metadata, name='basic_medium_list'),
    path('api/mediums_certificate/', basic_medium_without_certificate_metadata, name='basic_medium_certificate_list'),
    path('api/', include(router.urls)),
]

# This is required for static files while in development mode. (DEBUG=TRUE)
if settings.DEBUG:
    urlpatterns += [path('fixtures/', generate_fixtures)]
