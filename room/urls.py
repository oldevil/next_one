from django.urls import path

from room.views.patient_view import patient_detail, patient_create, patient_edit, patient_get_in, patient_delete
from room.views.room_view import room_index, room_detail, room_update_queue
from room.views.surgeon_view import surgeon_detail, surgeon_create, surgeon_edit, surgeon_index, surgeon_delete
from room.views.assistant_view import assistant_detail, assistant_create, assistant_edit, assistant_index, assistant_delete

app_name = 'room'

urlpatterns = [
    path('', room_index, name='room_index'),
    path('<int:room_id>/', room_detail, name='room_detail'),
    path('<int:room_id>/room_update_queue/', room_update_queue, name='room_update_queue'),
    path('patient/', patient_create, name='patient_create'),
    path('<int:patient_id>/patient/', patient_detail, name='patient_detail'),
    path('patient_edit/', patient_edit, name='patient_edit'),
    path('<int:patient_id>/patient_get_in/', patient_get_in, name='patient_get_in'),
    path('<int:patient_id>/patient_delete/', patient_delete, name='patient_delete'),
    path('surgeon_index/', surgeon_index, name='surgeon_index'),
    path('surgeon/', surgeon_create, name='surgeon_create'),
    path('<int:surgeon_id>/surgeon/', surgeon_detail, name='surgeon_detail'),
    path('surgeon_edit/', surgeon_edit, name='surgeon_edit'),
    path('<int:surgeon_id>/surgeon_delete/', surgeon_delete, name='surgeon_delete'),
    path('assistant_index/', assistant_index, name='assistant_index'),
    path('assistant/', assistant_create, name='assistant_create'),
    path('<int:assistant_id>/assistant/', assistant_detail, name='assistant_detail'),
    path('assistant_edit/', assistant_edit, name='assistant_edit'),
    path('<int:assistant_id>/assistant_delete/', assistant_delete, name='assistant_delete'),
]
