from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from catalog import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Главная и товары
    path('', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    # Аутентификация
    path('users/login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('users/logout/', auth_views.LogoutView.as_view(next_page='product_list'), name='logout'),
    path('users/', include('users.urls')),
]
