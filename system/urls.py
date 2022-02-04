from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework import routers

from .views import index, admin, avatar, login_api
from .api import (UserViewSet, BasicMediumExpedientViewSet, RequestTicketViewSet,
                  MovementTicketViewSet, ResponsibilityCertificateViewSet)


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'basic_medium', BasicMediumExpedientViewSet)
router.register(r'request_ticket', RequestTicketViewSet)
router.register(r'movement_ticket', MovementTicketViewSet)
router.register(r'responsibility_certificate', ResponsibilityCertificateViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin, name='dashboard'),

    # Authentication
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # API
    path('api/login/', login_api, name='api_login'),
    path('api/avatar/', avatar, name="avatar"),
    # TODO: Create print documents and acceptation Tickets
    path('api/', include(router.urls)),
]
