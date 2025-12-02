from django.urls import path
from . import views 
from django.urls import path , include
urlpatterns =[
    path('', views.index, name='home'),
    path('accounts/', include('allauth.urls')),
    path('about/', views.about, name='about'),
    path('product/<str:cat>/<int:id>/', views.product_detail, name='product_detail'),
    path('auth/', views.login_register, name='auth'),
    path("profile/", views.profile, name="profile"),
    path("login-user/", views.login_user),
    path("register-user/", views.register_user),
    path("logout-user/", views.logout_user),

]