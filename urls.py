from django.urls import path, include
from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    #path('accounts/', include('django.contrib.auth.urls')),  # Login, logout, password reset
    path('', views.home, name='home'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('register/', views.register, name='register'),
    #path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
    #   views.activate, name='activate'),
    path('additem/', views.add_item, name='add_item')
]

