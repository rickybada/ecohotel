from django.urls import path
from . import views

urlpatterns = [
    path('insert_energy/', views.insert_energy, name='insert_energy'),  # URL path for the insert_energy view
    path('energy_table/', views.energy_table, name='energy_table'),  # URL path for the energy_table view
    path('energy_totals/', views.energy_totals, name='energy_totals'),  # URL path for the energy_totals view
    path('login/', views.login_view, name='login'),  # URL path for the login view
    path('logout/', views.logout_view, name='logout'),  # URL path for the logout view
    path('access_control/', views.access_control, name='access_control')  # URL path for the access_control view
]
