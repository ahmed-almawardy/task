from django.urls import path

from .views import FileUploadView

app_name = 'app'

urlpatterns = [
    path('upload-file/', view=FileUploadView.as_view(), name='upload-file'),
]
