"""ORM Django modals """
from django.db import models
from model_utils.models import TimeStampedModel


class Files(TimeStampedModel):
    """
        Represnting uploading file, saved with the the create-modified time
        from TimeStampedModel
    """
    name = models.CharField(max_length=250)
    data = models.TextField()
    
    def __str__(self):
        return f'{self.name}'
