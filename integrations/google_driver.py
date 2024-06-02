"""Modual for providing logic for working with Google Drive API"""

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

from rest_framework.exceptions import APIException

class FileUploadError(APIException):
    status_code = 400
    default_detail = 'File not uploaded try later.' 


def _gauth() -> GoogleDrive:
    """Authenticating with google drive"""
    gauth = GoogleAuth()
    return GoogleDrive(gauth)


def upload_to_drive(name: str, data: str):
    """Trying to upload file"""
    try:
        drive = _gauth()
        parents = [{'id':"19BpNCXjvL_Abt8_j14Ot4KIvPBbLzlE9"}]
        file_drive = drive.CreateFile({'title': name,'parents': parents})
        file_drive.SetContentString(data)
        file_drive.Upload()
    except Exception as e:
        raise FileUploadError()