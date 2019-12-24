from django.urls import path

from room.views.patient_edit_view import patient_edit

urlpatterns = [
    path('patient_edit/', patient_edit, name='patient_edit'),
]
