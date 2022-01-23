from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import index, admin, login_api, avatar

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin, name='dashboard'),
    path('avatar/', avatar, name="avatar"),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login_api/', login_api, name='login_api')
]
