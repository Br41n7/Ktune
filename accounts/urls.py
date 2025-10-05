from django.urls import path
from . import views

app_name = 'accounts'  # for namespaced URL reversing

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.registration_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    # settings
    path('settings/',views.settings_view,name='settings'),
    path('settings/migrate/',views.migrate_to_host,name='migrate_to_host'),
]
