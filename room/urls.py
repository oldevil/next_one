from django.urls import path

from room.views.patient_edit_view import patient_detail, patient_create, patient_edit

urlpatterns = [
    path('patient/', patient_create, name='patient_create'),
    path('<int:patient_id>/patient/', patient_detail, name='patient_detail'),
    path('patient_edit/', patient_edit, name='patient_edit'),
]
