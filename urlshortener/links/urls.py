from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LinkViewSet, RedirectLinkView, user_dashboard
from django.contrib.auth import views as auth_views
from . import views

router = DefaultRouter()
router.register(r'links', LinkViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('create/', views.create_link, name='create_link'),
    path('dashboard/<str:short_id>/', RedirectLinkView.as_view(), name='redirect_link'),


]
