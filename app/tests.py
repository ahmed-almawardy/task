"""General Testing modual provides Unit, Integration and end-to-end tests
in order to, maintan the code with no errors
"""
from django.test import TestCase
from django.urls import reverse
from app.models import Files
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch

class TaskTestAPI(TestCase):
    """Tests for checking the ability to upload a file"""

    @classmethod
    def setUpClass(cls):
        super(TaskTestAPI, cls).setUpClass()
        cls.client = APIClient()
        
    def test_upload_file_json_format(self):
        data = {'data': "SOME DATA",'name': 'filenamed.txt'}
        url = reverse('app:upload-file')
        with patch('app.services.upload_to_drive', return_value=None) as patched_func:
            response = self.client.post(url,data=data, content_type='application/json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertIsNotNone(Files.objects.last())
            patched_func.assert_called_once_with(name=data['name'], data=data['data'])
