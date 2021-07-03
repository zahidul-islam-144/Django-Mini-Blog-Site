from django.urls import path
from . import views

app_name = 'App_Login'

urlpatterns = [
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change_profile/', views.profile_change, name='change_profile'),
    path('password/', views.pass_change, name='change_pass'),
    path('add-picture/', views.add_pro_pic, name='add-picture'),
    path('change-picture/', views.change_pro_pic, name='change-picture'),
]