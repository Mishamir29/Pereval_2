from django.urls import path
from . import views

urlpatterns = [
    path('submitData/', views.submit_data, name='submit_data'),
    path('submitData/<int:id>/', views.get_pereval_by_id, name='get_pereval_by_id'),
    path('submitData/<int:id>/', views.edit_pereval, name='edit_pereval'),
    path('submitData/', views.get_perevals_by_user_email, name='get_perevals_by_user_email'),
]