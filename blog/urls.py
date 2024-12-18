from django.urls import path
from . import views
from .views import UserProfileListView, UserProfileEditView

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.Register.as_view(), name='register'), # путь для регистрации
    path('login/', views.Login.as_view(), name='login'), # путь для входа
    path('logout/', views.logout_user, name='logout'), # путь для выхода
    path('profile/', UserProfileListView.as_view(), name='profile'), # путь для профиля
    path('profile/edit/', UserProfileEditView.as_view(), name='edit_profile'), # путь для редактирования профиля
    path('profile/delete/', views.delete_user, name='delete_profile'), # путь для удаления профиля

]