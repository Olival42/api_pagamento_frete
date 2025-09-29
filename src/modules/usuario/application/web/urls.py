from django.urls import path
from modules.usuario.application.web.views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    """ path('test-protected/', TestProtectedView.as_view(), name='test-protected'), """
]