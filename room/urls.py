from django.urls import path

from room.views.patient_edit_view import patient_detail, patient_create, patient_edit, patient_get_in
from room.views.room_view import room_index, room_detail

app_name = 'room'

urlpatterns = [
    path('', room_index, name='room_index'),
    path('<int:room_id>/', room_detail, name='room_detail'),
    path('patient/', patient_create, name='patient_create'),
    path('<int:patient_id>/patient/', patient_detail, name='patient_detail'),
    path('patient_edit/', patient_edit, name='patient_edit'),
    path('<int:patient_id>/patient_get_in/', patient_get_in, name='patient_get_in'),
]
