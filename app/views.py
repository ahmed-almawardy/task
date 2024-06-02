from rest_framework.generics import ListCreateAPIView, RetrieveAPIView ,GenericAPIView

from .serializers import UploadFileSerailizer
from .services import send_to_drive
from .models import Files


class FileUploadView(ListCreateAPIView, RetrieveAPIView ,GenericAPIView):
    """API VIEW for creating a files to google driver
    and save data in the database
    """
    serializer_class = UploadFileSerailizer
    queryset = Files.objects.all()

    def perform_create(self, serializer: UploadFileSerailizer):
        """Sending a file to GOOGLE DRIVE API, After Validation"""
        send_to_drive(serializer.validated_data)
        super().perform_create(serializer)
