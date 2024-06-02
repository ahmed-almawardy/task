from rest_framework import serializers

from .models import Files

class UploadFileSerailizer(serializers.ModelSerializer):
    created = serializers.DateTimeField(read_only=True)
    modified = serializers.DateTimeField(read_only=True)
    data = serializers.CharField()
    name = serializers.CharField(min_length=2,)

    class Meta:
        model = Files
        fields = [
            'name',
            'data',
            'created',
            'modified'
        ]
