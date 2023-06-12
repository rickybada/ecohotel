from django.urls import path
from . import views

urlpatterns = [
    path('insert_energy/', views.insert_energy, name='insert_energy'),
    path('energy_table/', views.energy_table, name='energy_table'),
    path('energy_totals/', views.energy_totals, name='energy_totals'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('access_control/', views.access_control, name='access_control')
]