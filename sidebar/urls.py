from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('inventory/', views.inventory, name='inventory'),
    path('notifications/', views.notifications, name='notifications'),
<<<<<<< HEAD
=======
    path('notifications/', views.notifications_list, name='notifications'),
    path('notifications/clear/', views.clear_notifications, name='clear_notifications'),
    path('notifications/clear_all/', views.clear_all_notifications, name='clear_all_notifications'),
>>>>>>> 80c6c77791f8829d3528efd83f1827c0b1f090b1
    path('log_history/', views.log_history, name='log_history'),
    path('about/', views.about, name='about'),
    path('logout/', views.logout_view, name='logout'),
]
