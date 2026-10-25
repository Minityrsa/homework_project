from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from catalog import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Товары (CBV)
    path('', views.ProductListView.as_view(), name='product_list'),
    path('products/add/', views.ProductCreateView.as_view(), name='product_add'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    # Товары по тегу
    path('tags/<slug:slug>/', views.ProductByTagView.as_view(), name='products_by_tag'),

    # Аутентификация
    path('users/login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('users/logout/', auth_views.LogoutView.as_view(next_page='product_list'), name='logout'),
    path('users/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
